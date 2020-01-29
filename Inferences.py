"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""
import re
from z3 import BoolRef, BoolSort, StringSort, StringVal, Function, Const, Implies, And, simplify, substitute, Optimize

from Structure_ import *
from Solver import *
from utils import *



#################
# INFERENCES
#################

def metaJSON(idp):
    "response to meta request"
    symbols = []
    for i in idp.unknown_symbols().values():
        symbol_type = "function"
        if type(i.translated) == BoolRef:
            symbol_type = "proposition"
        typ = i.out.name
        symbols.append({
            "idpname": str(i.name),
            "type": symbol_type,
            "priority": "core",
            "showOptimize": True, # GUI is smart enough to show buttons appropriately
            "view": "expanded" if i.name == str(idp.goal) else idp.view.viewType
        })
    out = {"title": "Interactive Consultant", "symbols": symbols}
    return out


def propagation(case):
     
    out = Structure_(case)

    for key, l in case.literals.items():
        if l.truth.is_known() and key in case.GUILines:
            if case.GUILines[key].is_visible:
                out.addAtom(l.subtence, l.truth)

    return out.m

def expand(case):
    solver, reify, _ = mk_solver(case.translate(), case.GUILines)
    solver.check()
    return model_to_json(case, solver, reify)

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
        s = s.instances[args[0]].translated
    else:
        s = (s.instances[ f"{args[0]}({','.join(args[1:])})" ]).translated

    solver = Optimize()
    solver.add(case.translate())
    if minimize:
        solver.minimize(s)
    else:
        solver.maximize(s)

    (reify, _) = reifier(case.GUILines, solver)
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
    return model_to_json(case, solver, reify)

def explain(case, symbol, value):
    out = Structure_(case, case.given)  

    negated = value.startswith('~')
    value = value.replace("\\u2264", "≤").replace("\\u2265", "≥").replace("\\u2260", "≠") \
        .replace("\\u2200", "∀").replace("\\u2203", "∃") \
        .replace("\\u21d2", "⇒").replace("\\u21d4", "⇔").replace("\\u21d0", "⇐") \
        .replace("\\u2228", "∨").replace("\\u2227", "∧")
    value = value[1:] if negated else value
    if value in case.GUILines:
        to_explain = case.GUILines[value].translated #TODO value is an atom string

        # rules used in justification
        if not to_explain.sort()==BoolSort(): # calculate numeric value
            # TODO should be given by client
            s, _, _ = mk_solver(case.translate(), case.GUILines)
            s.check()
            val = s.model().eval(to_explain)
            to_explain = to_explain == val
        if negated:
            to_explain = Not(to_explain)

        s = Solver()
        (reify, unreify) = reifier(case.GUILines, s)
        def r1(a): return reify[a] if a in reify else a
        def r2(a): return Not(r1(a.children()[0])) if is_not(a) else r1(a)
        ps = {} # {reified: constraint}
        for i, ass in enumerate(case.given):
            p = Const("wsdraqsesdf"+str(i), BoolSort())
            ps[p] = ass
            s.add(Implies(p, ass.translate()))
        for i, constraint in enumerate(case.idp.translated):
            p = Const("wsdraqsesdf"+str(i+len(case.given)), BoolSort())
            ps[p] = constraint
            s.add(Implies(p, constraint))
        s.push()  

        s.add(Not(r2(to_explain)))
        s.check(list(ps.keys()))
        unsatcore = s.unsat_core()
        
        if unsatcore:
            for a1 in case.given:
                for a2 in s.unsat_core():
                    if type(ps[a2]) == LiteralQ and a1 == ps[a2]: #TODO we might miss some equality
                        out.addAtom(a1.subtence, a1.truth)
            out.m["*laws*"] = []
            for a1 in case.idp.theory.definitions + case.idp.theory.constraints: 
                #TODO find the rule
                for a2 in unsatcore:
                    if str(a1.translated) == str(ps[a2]):
                        out.m["*laws*"].append(a1.reading)

    return out.m

def abstract(case):
    out = {} # {category : [LiteralQ]}

    # extract fixed atoms from constraints
    out["universal"] = list(l for l in case.literals.values() if l.is_universal())
    out["given"    ] = list(l for l in case.literals.values() if l.is_given())
    out["fixed"    ] = list(l for l in case.literals.values() if l.is_consequence())
    out["irrelevant"]= list(LiteralQ(Truth.TRUE, l.subtence) for l in case.literals.values() if l.is_irrelevant())

    # create keys for models using first symbol of atoms
    models, count = {}, 0
    for GuiLine in case.GUILines.values():
        atomZ3 = GuiLine.translated #TODO
        for symb in GuiLine.unknown_symbols().keys():
            models[symb] = [] # models[symb][row] = [relevant atoms]
            break
    
    done = set(out["universal"] + out["given"] + out["fixed"])
    theory = And(case.idp.translated)
    solver, reify, unreify = mk_solver(theory, case.GUILines)
    solver.add(list(case.given.values()))
    while solver.check() == sat and count < 50: # for each parametric model

        # theory that forces irrelevant atoms to be irrelevant
        theory2 = And(theory, And(case.idp.vocabulary.translated)) # is this a way to copy theory ??

        atoms = [] # [LiteralQ]
        for atom_string, atom in case.GUILines.items():
            if atom_string in case.literals:
                literal = case.literals[atom_string]
                if literal.truth == Truth.UNKNOWN and atom.type == 'bool':
                    truth = solver.model().eval(reify[atom])
                    if truth == True:
                        atoms += [ LiteralQ(Truth.TRUE,  atom) ]
                    elif truth == False:
                        atoms += [ LiteralQ(Truth.FALSE, atom) ]
                    else: #unknown
                        theory2 = And(theory2,
                                        substitute(theory2, [(atomZ3, BoolVal(True))]),  # don't simplify !
                                        substitute(theory2, [(atomZ3, BoolVal(False))])) # it would break later substitutions
                    # models.setdefault(groupBy, [[]] * count) # create keys for models using first symbol of atoms

        # start with negations !
        atoms.sort(key=lambda l: (l.truth, str(l.subtence)))

        # remove atoms that are irrelevant in AMF
        solver2 = Solver()
        solver2.add(theory2)
        solver2.add([l.translate() for l in done]) # universal + given + fixed (ignore irrelevant)
        (reify2, _) = reifier({str(l.subtence) : l.subtence for l in atoms}, solver2)
        for i, literalQ in enumerate(atoms):
            if literalQ.truth.is_known():
                solver2.push()
                a = Not(reify2[literalQ.subtence]) if literalQ.truth.is_true() else \
                    reify2[literalQ.subtence]
                solver2.add(a)
                solver2.add(And([l.translate() for j, l in enumerate(atoms) if j != i]))
                result = solver2.check()
                solver2.pop()
                if result == sat:
                    theory2 = And(theory2, 
                                substitute(theory2, [(literalQ.subtence.translated, BoolVal(True))]),
                                substitute(theory2, [(literalQ.subtence.translated, BoolVal(False))]))
                    solver2.add(theory2)
                    atoms[i] = LiteralQ(Truth.IRRELEVANT, literalQ.subtence) # represents True

        # remove atoms that are consequences of others in the AMF
        solver2 = Solver()
        solver2.add(case.idp.vocabulary.translated) # without theory !
        (reify2, _) = reifier({str(l.subtence) : l.subtence for l in atoms}, solver2)
        for i, literalQ in enumerate(atoms):
            if literalQ.truth.is_known():
                solver2.push()
                solver2.add(And([l.translate() for j, l in enumerate(atoms) if j != i]))

                # evaluate not(literalQ)
                a = Not(reify2[literalQ.subtence]) if literalQ.truth.is_true() else \
                    reify2[literalQ.subtence]
                result, consq = solver2.consequences([], [a])
                if result!=sat or consq: # remove it if it's a consequence
                    atoms[i] = LiteralQ(Truth.IRRELEVANT, literalQ.subtence)
                    # ??? theory2 = substitute(theory2, [(literalQ.subtence, BoolVal(literalQ.truth & 1))])
                solver2.pop()

        # add constraint to eliminate this model
        modelZ3 = Not(And( [l.translate() for l in atoms] ))
        theory = And(theory, modelZ3)
        solver.add(modelZ3)

        # group atoms by symbols
        model = {}
        for l in atoms:
            for symb in l.subtence.unknown_symbols().keys():
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
    out["models"] = "" if count < 50 else "More than 50 models..."
    out["variable"] = [[ [symb] for symb in models.keys() if symb in active_symbol ]]
    for i in range(count):
        out["variable"] += [[ models[symb][i] for symb in models.keys() if symb in active_symbol ]]
    return out


    
