"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import re
import time
from z3 import Solver, BoolSort, Const, Implies, And, substitute, Optimize, \
    Not, BoolVal

from Idp.Expression import AComparison, AUnary
from Idp.utils import *
from .IO import *


"""
#################
# INFERENCES
#################
"""

# def get_relevant_subtences(self) -> Tuple[Dict[str, SymbolDeclaration], Dict[str, Expression]]:
#     """ causal interpretation of relevance """
#     #TODO performance.  This method is called many times !  use expr.contains(expr, symbols)
#     constraints = ( self.constraints )

#     # determine relevant symbols (including defined ones)
#     relevant_symbols = mergeDicts( e.unknown_symbols() for e in constraints )

#     # remove irrelevant domain conditions
#     self.constraints = list(filter(lambda e: e.is_type_constraint_for is None or e.is_type_constraint_for in relevant_symbols
#                                  , self.constraints))

#     # determine relevant subtences
#     relevant_subtences = mergeDicts( e.subtences() for e in constraints )
#     relevant_subtences.update(mergeDicts(s.instances for s in relevant_symbols.values()))

#     for k, l in self.assignments.items():
#         symbols = list(l.sentence.unknown_symbols().keys())
#         has_relevant_symbol = any(s in relevant_symbols for s in symbols)
#         if k in relevant_subtences and symbols and has_relevant_symbol:
#             l.relevant = True

def get_relevant_subtences(self):
    """         
    sets 'relevant in self.assignments
    sets rank of symbols in self.relevant_symbols
    removes irrelevant constraints in self.constraints
    """
    # self is a State
    for a in self.assignments.values():
        a.relevant = False

    # collect (co-)constraints
    constraints = OrderedSet()
    for constraint in self.constraints:
        constraints.append(constraint)
        constraint.co_constraints(constraints)


    # initialize reachable with relevant, if any
    reachable = OrderedSet()
    for constraint in constraints:
        if type(constraint)==AppliedSymbol and constraint.name=='__relevant':
            for e in constraint.sub_exprs:
                assert e.code in self.assignments, \
                    f"Invalid expression in relevant: {e.code}" 
                reachable.append(e)

    # analyse given information
    given, hasGiven = OrderedSet(), False
    for q in self.assignments.values():
        if q.status == Status.GIVEN:
            hasGiven = True
            if not q.sentence.has_decision():
                given.append(q.sentence)


    # constraints have set of questions in self.assignments
    # set constraint.relevant, constraint.questions
    for constraint in constraints:
        constraint.relevant = False
        constraint.questions = OrderedSet()
        constraint.collect(constraint.questions, 
            all_=True, co_constraints=False)

        # add goals in constraint.original to constraint.questions
        # only keep questions in self.assignments
        qs = OrderedSet()
        constraint.original.collect(qs, all_=True, co_constraints=False)
        for q in qs:
            if q in reachable: # a goal
                constraint.questions.append(q)
        constraint.questions = OrderedSet([q for q in constraint.questions
            if q.code in self.assignments])


    # nothing relevant --> make every question in a constraint relevant
    if len(reachable) == 0: 
        for constraint in constraints:
            if constraint.is_type_constraint_for is None:
                for q in constraint.questions:
                    reachable.append(q)

    # find relevant symbols by depth-first propagation
    # relevants, rank = {}, 1
    # def dfs(question):
    #     nonlocal relevants, rank
    #     for constraint in constraints:
    #         # consider constraint not yet considered
    #         if ( not constraint.relevant
    #         # containing the question
    #         and question in constraint.questions):
    #             constraint.relevant = True
    #             for q in constraint.questions:
    #                 self.assignments[q.code].relevant = True
    #                 for s in q.unknown_symbols(co_constraints=False):
    #                     if s not in relevants:
    #                         relevants[s] = rank
    #                         rank = rank+1
    #                 if q.code != question.code \
    #                 and q.type == 'bool'\
    #                 and not q in given:
    #                     print("==>", q)
    #                     reachable.add(q)
    #                     dfs(q)
    # for question in list(reachable.values()):
    #     dfs(question)

    # find relevant symbols by breadth-first propagation
    # input: reachable, given, constraints
    # output: self.assignments[].relevant, constraints[].relevant, relevants[].rank
    relevants = {}  # Dict[string: int]
    to_add, rank = reachable, 1
    while to_add:
        for q in to_add:
            self.assignments[q.code].relevant = True
            for s in q.unknown_symbols(co_constraints=False):
                if s not in relevants:
                    relevants[s] = rank
            if not q in given:
                reachable.append(q)

        to_add, rank = OrderedSet(), 2 # or rank+1
        for constraint in constraints:
            # consider constraint not yet considered
            if ( not constraint.relevant
            # and with a question that is reachable but not given
            and  any(q in reachable and not q in given 
                    for q in constraint.questions) ):
                constraint.relevant = True
                to_add.extend(constraint.questions)
    if not hasGiven or self.idp.display.moveSymbols:
        self.relevant_symbols = relevants

    # remove irrelevant domain conditions
    is_relevant = lambda constraint: constraint.relevant
    self.constraints = list(filter(is_relevant, self.constraints))


def explain(state, question):
    out = Output(state, state.given)  

    question = decode_UTF(question)
    negated = question.replace('~', '¬').startswith('¬')
    question = question[1:] if negated else question
    if question in state.assignments:
        to_explain = state.assignments[question].sentence

        # rules used in justification
        if to_explain.type != 'bool': # recalculate numeric value
            val = state.assignments[question].value
            if val is None: # can't explain an expanded value
                return out.m
            to_explain = AComparison.make("=", [to_explain, val])
        if negated:
            to_explain = AUnary.make('¬', to_explain)

        s = Solver()
        s.set(':core.minimize', True)
        ps = {} # {reified: constraint}

        for ass in state.given.values():
            p = ass.translate()
            ps[p] = ass
            s.add(Implies(p, ass.translate()))
        todo = (list(state.idp.theory.constraints) 
                + list(state.idp.theory.def_constraints.values()))
        for constraint in todo:
            p = constraint.reified()
            ps[p] = constraint.translate()
            s.add(Implies(p, constraint.translate()))

        s.add(Not(to_explain.translate()))
        s.check(list(ps.keys()))
        unsatcore = s.unsat_core()
        
        if unsatcore:
            for a1 in state.given.values():
                for a2 in unsatcore:
                    if type(ps[a2]) == Assignment \
                    and a1.sentence.code == ps[a2].sentence.code: #TODO we might miss some equality
                        out.addAtom(a1.sentence, a1.value, a1.status)

            # remove irrelevant atoms
            for symb, dictionary in out.m.items():
                out.m[symb] = { k:v for k,v in dictionary.items()
                    if type(v)==dict and v['status']=='GIVEN' 
                    and v.get('value', '') != ''}
            out.m = {k:v for k,v in out.m.items() if v}
                
            out.m["*laws*"] = []
            for a1 in (list(state.idp.theory.def_constraints.values()) 
                    + list(state.idp.theory.constraints)): 
                #TODO find the rule
                for a2 in unsatcore:
                    if str(a1.translate()) == str(ps[a2]):
                        out.m["*laws*"].append(a1.annotations['reading'])
    return out.m

def abstract(state, given_json):
    timeout = time.time()+20 # 20 seconds max
    out = {} # {category : [Assignment]}

    # extract fixed atoms from constraints
    out["universal"] = list(l for l in state.assignments.values() 
                        if l.status == Status.UNIVERSAL)
    out["given"    ] = list(l for l in state.assignments.values() 
                        if l.status == Status.GIVEN)
    out["fixed"    ] = list(l for l in state.assignments.values() 
                        if l.status in [Status.ENV_CONSQ, Status.CONSEQUENCE])
    out["irrelevant"]= list(l for l in state.assignments.values() 
        if not l.status in [Status.ENV_CONSQ, Status.CONSEQUENCE] 
        and not l.relevant)

    # create keys for models using first symbol of atoms
    models, count = {}, 0
    for q in state.assignments.values():
        models[q.symbol_decl.name] = []
    
    done = set(out["universal"] + out["given"] + out["fixed"])
    theory = And(state.idp.theory.translate())
    solver = Solver()
    solver.add(theory)
    solver.add([ass.translate() for ass in state.given.values()])
    while solver.check() == sat and count < 50 and time.time()<timeout: # for each parametric model

        # theory that forces irrelevant atoms to be irrelevant
        theory2 = And(theory) # is this a way to copy theory ??

        atoms = [] # [Assignment]
        for assignment in state.assignments.values():
            atom = assignment.sentence
            if assignment.value is None \
            and assignment.relevant and atom.type == 'bool':
                solver.push()
                solver.add(atom.reified() == atom.translate())
                solver.check()
                value = solver.model().eval(atom.reified())
                solver.pop()
                if value == True:
                    atoms += [ Assignment(atom, TRUE , Status.UNKNOWN) ]
                elif value == False:
                    atoms += [ Assignment(atom, FALSE, Status.UNKNOWN) ]
                else: #unknown
                    theory2 = And(theory2,
                        substitute(theory2, [(atom.translate(), BoolVal(True))]),  # don't simplify !
                        substitute(theory2, [(atom.translate(), BoolVal(False))])) # it would break later substitutions

        # start with negations !
        atoms.sort(key=lambda l: (l.value==TRUE, str(l.sentence)))

        # remove atoms that are irrelevant in AMF
        solver2 = Solver()
        solver2.add(theory2)
        solver2.add([l.translate() for l in done]) # universal + given + fixed (ignore irrelevant)
        for i, assignment in enumerate(atoms):
            if assignment.value is not None and time.time()<timeout:
                atom = assignment.sentence
                solver2.push()
                if atom.type == 'bool':
                    solver2.add(atom.reified() == atom.translate())
                a = Not(atom.reified()) if assignment.value else atom.reified()
                solver2.add(a)
                solver2.add(And([l.translate() 
                                for j, l in enumerate(atoms) if j != i]))
                result = solver2.check()
                solver2.pop()
                if result == sat:
                    theory2 = And(theory2, 
                        substitute(theory2, [(atom.translate(), BoolVal(True))]),
                        substitute(theory2, [(atom.translate(), BoolVal(False))]))
                    solver2.add(theory2)
                    atoms[i] = Assignment(TRUE, TRUE, Status.UNKNOWN)

        # remove atoms that are consequences of others in the AMF
        solver2 = Solver()
        for i, assignment in enumerate(atoms):
            if assignment.value is not None and time.time()<timeout:
                atom = assignment.sentence
                solver2.push()
                solver2.add(And([l.translate() 
                                for j, l in enumerate(atoms) if j != i]))

                # evaluate not(assignment)
                if atom.type == 'bool':
                    solver2.add(atom.reified() == atom.translate())
                a = Not(atom.reified()) if assignment.value else atom.reified()
                result, consq = solver2.consequences([], [a])
                if result!=sat or consq: # remove it if it's a consequence
                    atoms[i] = Assignment(TRUE, TRUE, Status.UNKNOWN)
                    # ??? theory2 = substitute(theory2, [(atom, BoolVal(assignment.value & 1))])
                solver2.pop()

        # add constraint to eliminate this model
        modelZ3 = Not(And( [l.translate() for l in atoms] ))
        theory = And(theory, modelZ3)
        solver.add(modelZ3)

        # group atoms by symbols
        model = {}
        for l in atoms:
            if l.sentence != TRUE:
                model.setdefault(l.symbol_decl.name, []).append([ l ])
        # add to models
        for k,v in models.items(): # add model
            models[k] = v + [ model[k] if k in model else [] ]
        count +=1

    # detect symbols with atoms
    active_symbol = {}
    for symb in models.keys():
        for i in range(count):
            if not models[symb][i] == []:
                active_symbol[symb] = True

    # build table of models
    out["models"] = ("" if count < 50 and time.time()<timeout else 
                "Time out or more than 50 models...Showing partial results")
    out["variable"] = [[ [symb] for symb in models.keys() 
                        if symb in active_symbol ]]
    for i in range(count):
        out["variable"] += [[ models[symb][i] for symb in models.keys() 
                            if symb in active_symbol ]]
    return out


    
