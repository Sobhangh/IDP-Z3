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
from debugWithYamlLog import NEWL
from itertools import chain
import re
import time
from z3 import Solver, BoolSort, Const, Implies, And, substitute, Optimize, \
    Not, BoolVal, unsat

from Idp.Expression import AComparison, AUnary, AConjunction, ADisjunction
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

        for ass in state.assignments.values():
            if ass.status in [Status.GIVEN, Status.STRUCTURE, Status.UNIVERSAL]:
                p = ass.translate()
                ps[p] = ass
                #TODO use assert_and_track ?
                s.add(Implies(p, ass.translate()))
        todo = chain(state.constraints, state.def_constraints.values())
        for constraint in todo:
            p = constraint.reified()
            constraint.original = constraint.original.interpret(state)
            ps[p] = constraint.original.translate()
            s.add(Implies(p, constraint.original.translate()))

        s.add(Not(to_explain.translate()))
        s.check(list(ps.keys()))
        unsatcore = s.unsat_core()
        
        if unsatcore:
            for a1 in state.assignments.values():
                if a1.status in [Status.GIVEN, Status.STRUCTURE, Status.UNIVERSAL]:
                    for a2 in unsatcore:
                        if type(ps[a2]) == Assignment \
                        and a1.sentence.same_as(ps[a2].sentence): #TODO we might miss some equality
                            out.addAtom(a1.sentence, a1.value, a1.status)

            # remove irrelevant atoms
            for symb, dictionary in out.m.items():
                out.m[symb] = { k:v for k,v in dictionary.items()
                    if type(v)==dict and v['status'] in ['GIVEN', 'STRUCTURE', 'UNIVERSAL'] 
                    and v.get('value', '') != ''}
            out.m = {k:v for k,v in out.m.items() if v}
                
            out.m["*laws*"] = []
            for a1 in chain(state.def_constraints.values(), state.constraints): 
                #TODO find the rule
                for a2 in unsatcore:
                    if str(a1.original.translate()) == str(ps[a2]):
                        out.m["*laws*"].append(a1.annotations['reading'])
    return out.m

def abstract(state, given_json):
    return DMN(state, "", False)

def DMN(state, goal_string, first_hit=True):
    if goal_string:
        # add (goal | ~goal) to state.constraints
        assert goal_string in state.assignments, (
            f"Unrecognized goal string: {goal_string}")
        temp = state.assignments[goal_string].sentence
        temp = ADisjunction.make('∨', [temp, AUnary.make('¬', temp)])
        temp = temp.interpret(state)
        state.constraints.append(temp)

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
    models, count = [], 0
    
    done = set(out["universal"] + out["given"] + out["fixed"]) 

    # ignore type constraints
    questions = OrderedSet()
    for c in state.constraints:
        if not c.is_type_constraint_for:
            c.collect(questions, all_=False)
    assert not goal_string or goal_string in [a.code for a in questions], \
        f"Internal error"

    known = And([ass.translate() for ass in state.assignments.values()
                    if ass.status != Status.UNKNOWN]
                + [q.reified()==q.translate()
                    for q in questions
                    if q.is_reified()])

    theory = state.formula().translate()
    goal = None
    solver = Solver()
    solver.add(theory)
    solver.add(known)
    while solver.check() == sat and count < 50 and time.time()<timeout: # for each parametric model
        # find the interpretation of all atoms in the model
        assignments = [] # [Assignment]
        model = solver.model()
        for atom in questions.values():
            assignment = state.assignments[atom.code]
            if assignment.value is None and atom.type == 'bool':
                if not atom.is_reified():
                    val1 = model.eval(atom.translate())
                else:
                    val1 = model.eval(atom.reified())
                if val1 == True:
                    ass = Assignment(atom, TRUE , Status.UNKNOWN)
                elif val1 == False:
                    ass = Assignment(atom, FALSE, Status.UNKNOWN)
                else:
                    ass = None
                if ass is not None:
                    if atom.code == goal_string:
                        goal = ass
                    else:
                        assignments.append(ass)
        # start with negations !
        assignments.sort(key=lambda l: (l.value==FALSE, str(l.sentence)))
        if goal is not None:
            assignments.append(goal)

        assignments = state._generalize(assignments, known, theory)
        models.append(assignments)

        # add constraint to eliminate this model
        modelZ3 = Not(And( [l.translate() for l in assignments 
            if l.value is not None] ))
        solver.add(modelZ3)

        count +=1
    
    models.sort(key=len)
    
    if first_hit:
        theory = state.formula().translate()
        models1 = []
        while models:
            model = models.pop(0).copy()
            possible = And(known, Not(And([l.translate() for l in model[:-1]
                                            if l.value is not None])))
            solver = Solver()
            solver.add(theory)
            solver.add(possible)
            if solver.check() == sat or len(models)==0:
                known = possible
                models1.append(model)
                models = [state._generalize(m, known, theory) for m in models]
                models.sort(key=len)
        models = models1

    # detect symbols with assignments
    active_symbol = {}
    for i, model in enumerate(models):
        for ass in model:
            if ass.sentence != TRUE:
                active_symbol[ass.symbol_decl.name] = True
    #create empty table
    table = {}
    for ass in state.assignments.values():
        if (ass.symbol_decl.name in active_symbol
        and ass.symbol_decl.name not in table):
            table[ass.symbol_decl.name] = [ [] for i in range(len(models))]
    # fill table
    for i, model in enumerate(models):
        print('[', f"{NEWL}  ".join(str(a) for a in model), ']')
        for ass in model:
            table[ass.symbol_decl.name][i].append(ass)

    # build table of models
    out["models"] = ("" if count < 50 and time.time()<timeout else 
                "Time out or more than 50 models...Showing partial results")
    out["variable"] = [[ [symb] for symb in table.keys() 
                        if symb in active_symbol ]]
    for i in range(len(models)):
        out["variable"] += [[ table[symb][i] for symb in table.keys() 
                            if symb in active_symbol ]]
    return out


    
