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
from z3.z3 import _py2expr

from Structure_ import *
from Theory import *
from utils import *

class ConfigCase:

    def __init__(self, idp):
        self.idp = idp
        self.structure = {} # {literalQ : atomZ3} from the GUI (needed for propagate)
        
        idp.translate(self)
        

    def theory(self, with_assumptions=False):
        return And(self.idp.theory.translated 
            + self.idp.vocabulary.typeConstraints
            + (list(self.structure.values()) if with_assumptions else []))


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


def propagation(case, expanded_symbols):
    expanded_symbols = [] if expanded_symbols is None else expanded_symbols
    
    out = Structure_(case.idp)
    
    todo = [ a for a in case.idp.atoms.values()
                # if it is shown to the user
                if any([s in expanded_symbols for s in a.unknown_symbols().keys()]) ]

    amf = consequences(case.theory(with_assumptions=True), todo, {})
    for literalQ in amf:
        out.addAtom(literalQ.subtence, literalQ.truth)

    # useful for non linear structure
    """
    amf = consequences(case.theory(with_assumptions=False), todo, amf)
    for literalQ in amf:
        out.addAtom(literalQ.subtence, literalQ.truth)
    """

    for literalQ in case.structure: # needed to keep some numeric assignments
        out.addAtom(literalQ.subtence, literalQ.truth)
    return out.m

def expand(case):
    theory = case.theory(with_assumptions=True)
    solver, reify, _ = mk_solver(theory, case.idp.atoms.values())
    solver.check()
    return model_to_json(case.idp, solver, reify)

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
                    p = re.compile(func_name + "\(" + func_current_param + "\)$")
                    return p.match(inp).groups()
                except:
                    func_current_param += ", " + func_params_adder
    
    args = parse_func_with_params(symbol)
    s = case.idp.unknown_symbols()[args[0]]
    if len(args) == 1:
        s = s.instances[args[0]].translated
    else:
        s = (s.instances[args[0]+ "(" + ",".join(args[1:]) + ")"]).translated

    solver = Optimize()
    solver.add(case.theory(with_assumptions=True))
    if minimize:
        solver.minimize(s)
    else:
        solver.maximize(s)

    (reify, _) = reifier(case.idp.atoms.values(), solver)
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
    return model_to_json(case.idp, solver, reify)

def explain(case, symbol, value):
    out = Structure_(case.idp, case.structure)  

    value = value.replace("\\u2264", "≤").replace("\\u2265", "≥").replace("\\u2260", "≠") \
        .replace("\\u2200", "∀").replace("\\u2203", "∃") \
        .replace("\\u21d2", "⇒").replace("\\u21d4", "⇔").replace("\\u21d0", "⇐") \
        .replace("\\u2228", "∨").replace("\\u2227", "∧")
    if value in case.idp.atoms:
        to_explain = case.idp.atoms[value].translated #TODO value is an atom string

        # rules used in justification
        if not to_explain.sort()==BoolSort(): # calculate numeric value
            # TODO should be given by client
            theory = case.theory(with_assumptions=True)
            s, _, _ = mk_solver(theory, case.idp.atoms.values())
            s.check()
            val = s.model().eval(to_explain)
            to_explain = to_explain == val

        s = Solver()
        (reify, unreify) = reifier(case.idp.atoms.values(), s)
        def r1(a): return reify[a] if a in reify else a
        def r2(a): return Not(r1(a.children()[0])) if is_not(a) else r1(a)
        ps = {} # {reified: constraint}
        for i, ass in enumerate(case.structure):
            p = Const("wsdraqsesdf"+str(i), BoolSort())
            ps[p] = ass
            s.add(Implies(p, ass.asZ3()))
        constraints = case.idp.theory.translated + case.idp.vocabulary.typeConstraints
        for i, constraint in enumerate(constraints):
            p = Const("wsdraqsesdf"+str(i+len(case.structure)), BoolSort())
            ps[p] = constraint
            s.add(Implies(p, constraint))
        s.push()  

        s.add(Not(r2(to_explain)))
        s.check(list(ps.keys()))
        unsatcore = s.unsat_core()
        if not unsatcore: # try to explain not(to_explain)
            #TODO refactor: client should send us the literal, not the atom
            s.pop()
            s.add(r2(to_explain))
            s.check(list(ps.keys()))
            unsatcore = s.unsat_core()
        
        if unsatcore:
            for a1 in case.structure:
                for a2 in s.unsat_core():
                    if type(ps[a2]) == LiteralQ and a1 == ps[a2]: #TODO we might miss some equality
                        out.addAtom(a1.subtence, a1.truth)
            out.m["*laws*"] = []
            for a1 in constraints:
                for a2 in unsatcore:
                    if str(a1) == str(ps[a2]):
                        out.m["*laws*"].append(a1.reading if hasattr(a1, "reading") else str(a1))

    return out.m

def abstract(case):
    out = {} # {category : [LiteralQ]}

    theory = case.theory(with_assumptions=False)
    solver, reify, unreify = mk_solver(theory, case.idp.atoms.values())

    # extract fixed atoms from constraints
    universal = consequences(theory, case.idp.atoms.values(), {}, solver, reify, unreify)
    out["universal"] = [k for k in universal.keys() if k.truth is not None]

    out["given"] = []
    for ass in case.structure:
        universal[ass] = True
        out["given"] += [ass]

    # find consequences of structure
    solver.add(list(case.structure.values()))
    theory2 = And([theory] + list(case.structure.values()))
    fixed = consequences(theory2, case.idp.atoms.values(), universal, solver, reify, unreify)
    out["fixed"] = [k for k in fixed.keys() if k.truth is not None]

    models, count = {}, 0
    done = set(out["universal"] + out["given"] + out["fixed"])

    # substitutions = [(quantifier/chained, reified)] + [(consequences, truthvalue)]
    substitutions = []
    reified = Function("qsdfvqe13435", StringSort(), BoolSort())
    for atom_string, atom in case.idp.atoms.items():
        atomZ3 = atom.translated #TODO
        if atom.type == 'bool' or (hasattr(atom.decl, 'sorts') and atom.decl.type.name == 'bool'):
            substitutions += [(atomZ3, reified(StringVal(atom_string.encode('utf8'))))]
    for literalQ in done:
        if is_bool(literalQ.subtence): #TODO
            substitutions += [(literalQ.subtence, BoolVal(literalQ.truth))]

    # relevants = getAtoms(simplify(substitute(case.constraints, substitutions)))
    simplified = simplify(substitute(And(case.idp.theory.translated), substitutions)) # it starts by the last substitution ??
    relevants = getAtoms(simplified, case.idp.unknown_symbols()) # includes reified !

    # --> irrelevant
    irrelevant = []
    for atom_string, atom in case.idp.atoms.items():
        atomZ3 = atom.translated #TODO
        if is_bool(atomZ3) \
        and not LiteralQ(True , atom) in done \
        and not LiteralQ(False, atom) in done:
            string2 = atom_as_string(reified(StringVal(atom_string.encode('utf8'))))
            if not string2 in relevants:
                irrelevant += [LiteralQ(True, atom)]
    out["irrelevant"] = irrelevant
    done2 = done.union(set(irrelevant))

    # create keys for models using first symbol of atoms
    for atom in case.idp.atoms.values():
        atomZ3 = atom.translated #TODO
        for symb in atom.unknown_symbols().keys():
            models[symb] = [] # models[symb][row] = [relevant atoms]
            break
    
    while solver.check() == sat and count < 50: # for each parametric model

        # theory that forces irrelevant atoms to be irrelevant
        theory2 = And(theory, And(case.idp.vocabulary.typeConstraints))

        atoms = [] # [LiteralQ]
        for atom_string, atom in case.idp.atoms.items():
            atomZ3 = atom.translated #TODO
            if is_bool(atomZ3) \
            and not LiteralQ(True , atom) in done2 \
            and not LiteralQ(False, atom) in done2 \
            and not atom_string in relevants :
                truth = solver.model().eval(reify[atom])
                if truth == True:
                    atoms += [ LiteralQ(True,  atom) ]
                elif truth == False:
                    atoms += [ LiteralQ(False, atom) ]
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
        solver2.add([l.asZ3() for l in done]) # universal + given + fixed (ignore irrelevant)
        (reify2, _) = reifier([l.subtence for l in atoms], solver2)
        for i, literalQ in enumerate(atoms):
            if literalQ.truth is not None:
                solver2.push()
                a = reify2[literalQ.subtence] if not literalQ.truth else Not(reify2[literalQ.subtence])
                solver2.add(a)
                solver2.add(And([l.asZ3() for j, l in enumerate(atoms) if j != i]))
                result = solver2.check()
                solver2.pop()
                if result == sat:
                    theory2 = And(theory2, 
                                substitute(theory2, [(literalQ.subtence.translated, BoolVal(True))]),
                                substitute(theory2, [(literalQ.subtence.translated, BoolVal(False))]))
                    solver2.add(theory2)
                    atoms[i] = LiteralQ("irrelevant", literalQ.subtence) # represents True

        # remove atoms that are consequences of others in the AMF
        solver2 = Solver()
        solver2.add(case.idp.vocabulary.typeConstraints) # without theory !
        (reify2, _) = reifier([l.subtence for l in atoms], solver2)
        for i, literalQ in enumerate(atoms):
            if literalQ.truth is not None:
                solver2.push()
                solver2.add(And([l.asZ3() for j, l in enumerate(atoms) if j != i]))

                # evaluate not(literalQ)
                a = reify2[literalQ.subtence] if not literalQ.truth else Not(reify2[literalQ.subtence])
                result, consq = solver2.consequences([], [a])
                if result!=sat or consq: # remove it if it's a consequence
                    atoms[i] = LiteralQ("irrelevant", literalQ.subtence)
                    # ??? theory2 = substitute(theory2, [(literalQ.subtence, BoolVal(literalQ.truth))])
                solver2.pop()

        # add constraint to eliminate this model
        modelZ3 = Not(And( [l.asZ3() for l in atoms] ))
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


    
