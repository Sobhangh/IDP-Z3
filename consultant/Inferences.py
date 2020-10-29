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




def propagation(case):
    out = Output(case)
    out.fill(case)

    return out.m

def expand(case):
    solver = Solver()
    solver.add(case.translate())
    solver.check()
    return model_to_json(case, solver)

def optimize(case, symbol, minimize):
    # symbol may be "angle(0)""
    def parse_func_with_params(inp):
        func_name = "([_a-zA-Z]+)"
        try:
            p = re.compile(func_name + "$")
            return p.match(inp).groups()
        except:
            func_current_param = func_params_adder = "([_a-zA-Z0-9.]+)"
            for count in range(10): # max 10 arguments
                try:
                    p = re.compile(f"{func_name}\({func_current_param}\)$")
                    return p.match(inp).groups()
                except:
                    func_current_param += ", " + func_params_adder
    
    args = parse_func_with_params(symbol)
    s = case.idp.unknown_symbols()[args[0]]
    if len(args) == 1:
        s = s.instances[args[0]].translate()
    else:
        s = (s.instances[ f"{args[0]}({','.join(args[1:])})" ]).translate()

    solver = Optimize()
    solver.add(case.translate())
    if minimize:
        solver.minimize(s)
    else:
        solver.maximize(s)

    solver.check()

    # deal with strict inequalities, e.g. min(0<x)
    solver.push()
    for i in range(0,10):
        val = solver.model().eval(s)
        if minimize:
            solver.add(s < val)
        else:
            solver.add(val < s)
        if solver.check()!=sat:
            solver.pop() # get the last good one
            solver.check()
            break    
    return model_to_json(case, solver)

def explain(case, symbol, value, given_json):
    out = Output(case, case.given)  

    negated = value.startswith('~')
    value = value.replace("\\u2200", "∀").replace("\\u2203", "∃") \
        .replace("\\u2264", "≤").replace("\\u2265", "≥").replace("\\u2260", "≠") \
        .replace("\\u21d2", "⇒").replace("\\u21d4", "⇔").replace("\\u21d0", "⇐") \
        .replace("\\u2228", "∨").replace("\\u2227", "∧")
    value = value[1:] if negated else value
    if value in case.assignments:
        to_explain = case.assignments[value].sentence

        # rules used in justification
        if to_explain.type != 'bool': # recalculate numeric value
            val = case.assignments[value].value
            to_explain = AComparison.make("=", [to_explain, val])
        if negated:
            to_explain = AUnary.make('~', to_explain)

        s = Solver()
        s.set(':core.minimize', True)
        ps = {} # {reified: constraint}
        
        given = json_to_literals(case.idp, given_json) # use non-simplified given data
        for i, ass in enumerate(given.values()):
            p = Const("wsdraqsesdf"+str(i), BoolSort())
            ps[p] = ass
            s.add(Implies(p, ass.translate()))
        for i, constraint in enumerate(case.idp.translate()):
            p = Const("wsdraqsesdf"+str(i+len(given)), BoolSort())
            ps[p] = constraint
            s.add(Implies(p, constraint))

        s.add(Not(to_explain.translate()))
        s.check(list(ps.keys()))
        unsatcore = s.unsat_core()
        
        if unsatcore:
            for a1 in case.given.values():
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
            for a1 in (list(case.idp.theory.def_constraints.values()) 
                    + list(case.idp.theory.constraints)): 
                #TODO find the rule
                for a2 in unsatcore:
                    if str(a1.translate()) == str(ps[a2]):
                        out.m["*laws*"].append(a1.annotations['reading'])
    return out.m

def abstract(case, given_json):
    timeout = time.time()+20 # 20 seconds max
    out = {} # {category : [Assignment]}

    # extract fixed atoms from constraints
    out["universal"] = list(l for l in case.assignments.values() 
                        if l.status == Status.UNIVERSAL)
    out["given"    ] = list(l for l in case.assignments.values() 
                        if l.status == Status.GIVEN)
    out["fixed"    ] = list(l for l in case.assignments.values() 
                        if l.status in [Status.ENV_CONSQ, Status.CONSEQUENCE])
    out["irrelevant"]= list(l for l in case.assignments.values() 
        if not l.status in [Status.ENV_CONSQ, Status.CONSEQUENCE] 
        and not l.relevant)

    questions = {a.sentence.code: a.sentence 
                for a in case.assignments.values()}

    # create keys for models using first symbol of atoms
    models, count = {}, 0
    for q in questions.values():
        for symb in q.unknown_symbols().keys():
            models[symb] = [] # models[symb][row] = [relevant atoms]
            break
    
    done = set(out["universal"] + out["given"] + out["fixed"])
    theory = And(case.idp.translate())
    solver = Solver()
    solver.add(theory)
    given = json_to_literals(case.idp, given_json) # use non-simplified given data
    solver.add([ass.translate() for ass in given.values()])
    while solver.check() == sat and count < 50 and time.time()<timeout: # for each parametric model

        # theory that forces irrelevant atoms to be irrelevant
        theory2 = And(theory) # is this a way to copy theory ??

        atoms = [] # [Assignment]
        for atom_string, atom in questions.items():
            assignment = case.assignments[atom_string]
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
                # models.setdefault(groupBy, [[]] * count) # create keys for models using first symbol of atoms

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
                for symb in l.sentence.unknown_symbols().keys():
                    model.setdefault(symb, []).append([ l ])
                    break
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


    
