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

from LiteralQ import *
from Theory import *
from utils import *

class ConfigCase:

    def __init__(self, idp):
        self.idp = idp
        self.enums = {} # {string: [string] } idp_type -> DSLobject
        self.valueMap = {"True": True}

        self.symbols = {} # {string: Z3Expr}, including starting with '_'
        self.symbol_types = {} # {string: string} symbol -> idp_type

        self.atoms = {} # {atom_string: Expression} atoms + numeric terms !

        self.structure = {} # {literalQ : atomZ3} (needed for propagate)
        self.constraints = {} # {Z3expr: string}
        self.typeConstraints = []
        
        idp.translate(self)

        for v in idp.vocabulary.symbol_decls.values():
            if v.is_var:
                self.atoms.update(v.instances)
        self.atoms.update( {k: v for k, v in idp.theory.subtences.items() if v.unknown_symbols()})

        ##TODO remove dead code
        #self.symbols = {k: v.translated for k, v in idp.vocabulary.symbol_decls.items() if v.is_var}
        #print("missing", {k:v for k,v in self.symbols.items() if k not in self.symbols2})
        #print("added", {k:v for k,v in self.symbols2.items() if k not in self.symbols})

    def print(self):
        out  = "\r\n\r\n".join(str(t) for t in self.typeConstraints) + "\r\n--\r\n"
        out += "\r\n\r\n".join(str(t) for t in self.constraints)     + "\r\n"
        return out
        


    #################
    # Helpers for translating idp code
    #################

    def Const(self, txt: str, sort,):
        const = self.symbols.setdefault(txt, Const(txt, sort))
        return const

    def EnumSort(self, name, objects):
        self.enums[name] = objects
        out = EnumSort(name, objects)
        for i in out[1]:
            self.valueMap[obj_to_string(i)] = i
        return out

    def Function(self, name, types, rel_vars, restrictive=True):
        out = Function(name, *types)
        rel_vars = list(map(lambda x: list(map(_py2expr, x)), rel_vars))
        args, vals = splitLast(rel_vars)
        args = list(itertools.product(*args))
        if not str(out).startswith('_'):
            self.symbols[str(out)] = out
        for arg in list(args):
            expr = out(*arg)
            if restrictive:
                exp = in_list(expr, vals)
                self.typeConstraints.append(exp)
        return out

    def Predicate(self, name, types, rel_vars, restrictive=True):
        p = self.Function(name, types + [BoolSort()], rel_vars + [[True]], False)
        if restrictive:
            argL = [Const('a' + str(ind), s) for s, ind in zip(types, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])]
            self.typeConstraints.append(
                ForAll(argL, Implies(p(*argL), And([in_list(a, t) for a, t in zip(argL, rel_vars)]))))
        return p

    def add(self, constraint, source_code):
        self.constraints[constraint] = source_code




    #################
    # INFERENCES
    #################

    def theory(self, with_assumptions=False):
        return And(list(self.constraints.keys()) 
            + self.typeConstraints
            + (list(self.structure.values()) if with_assumptions else []))

    def metaJSON(self):
        "response to meta request"
        symbols = []
        for i in self.symbols.values():
            symbol_type = "function"
            if type(i) == BoolRef:
                symbol_type = "proposition"
            typ = self.symbol_types[str(i)]
            symbols.append({
                "idpname": str(i),
                "type": symbol_type,
                "priority": "core",
                "showOptimize": True, # GUI is smart enough to show buttons appropriately
                "view": "expanded" if str(i) == str(self.goal) else self.view
            })
        out = {"title": "Interactive Consultant", "symbols": symbols}
        return out


    def propagation(self, expanded_symbols):
        expanded_symbols = [] if expanded_symbols is None else expanded_symbols
        
        out = self.initial_structure()
        
        todo = [ a for a in self.atoms.values() #TODO
                 if is_symbol(a.translated.decl().name(), self.symbols) 
                 or any([s in expanded_symbols for s in a.unknown_symbols().keys()]) ]

        amf = consequences(self.theory(with_assumptions=True), todo, {})
        for literalQ in amf:
            out.addAtom(self, literalQ.subtence, literalQ.truth)

        # useful for non linear structure
        """
        amf = consequences(self.theory(with_assumptions=False), todo, amf)
        for literalQ in amf:
            out.addAtom(self, literalQ.subtence, literalQ.truth)
        """

        for literalQ in self.structure: # needed to keep some numeric assignments
            out.addAtom(self, literalQ.subtence, literalQ.truth)
        return out.m

    def expand(self):
        theory = self.theory(with_assumptions=True)
        solver, reify, unreify = mk_solver(theory, self.atoms.values())
        solver.check()
        return self.model_to_json(solver, reify, unreify)

    def relevance(self): 
        out = self.initial_structure()
        return out.m

    def optimize(self, symbol, minimize):
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
        s = self.symbols[args[0]]
        if 1<len(args):
            s = s(args[1:])

        solver = Optimize()
        solver.add(self.theory(with_assumptions=True))
        if minimize:
            solver.minimize(s)
        else:
            solver.maximize(s)

        (reify, unreify) = reifier(self.atoms.values(), solver)
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
        return self.model_to_json(solver, reify, unreify)

    def explain(self, symbol, value):
        out = self.initial_structure()
        for ass in self.structure: # add numeric structure
            out.initialise(self, ass.subtence, False, False, "")    

        value = value.replace("\\u2264", "≤").replace("\\u2265", "≥").replace("\\u2260", "≠") \
            .replace("\\u2200", "∀").replace("\\u2203", "∃") \
            .replace("\\u21d2", "⇒").replace("\\u21d4", "⇔").replace("\\u21d0", "⇐") \
            .replace("\\u2228", "∨").replace("\\u2227", "∧")
        if value in self.atoms:
            to_explain = self.atoms[value].translated #TODO value is an atom string

            # rules used in justification
            if not to_explain.sort()==BoolSort(): # calculate numeric value
                # TODO should be given by client
                theory = self.theory(with_assumptions=True)
                s, _, _ = mk_solver(theory, self.atoms.values())
                s.check()
                val = s.model().eval(to_explain)
                to_explain = to_explain == val

            s = Solver()
            (reify, unreify) = reifier(self.atoms.values(), s)
            def r1(a): return reify[a] if a in reify else a
            def r2(a): return Not(r1(a.children()[0])) if is_not(a) else r1(a)
            ps = {} # {reified: constraint}
            for i, ass in enumerate(self.structure):
                p = Const("wsdraqsesdf"+str(i), BoolSort())
                ps[p] = ass
                s.add(Implies(p, ass.asZ3()))
            constraints = list(self.constraints.keys()) + self.typeConstraints
            for i, constraint in enumerate(constraints):
                p = Const("wsdraqsesdf"+str(i+len(self.structure)), BoolSort())
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
                for a1 in self.structure:
                    for a2 in s.unsat_core():
                        if type(ps[a2]) == LiteralQ and a1 == ps[a2]: #TODO we might miss some equality
                            out.addAtom(self, a1.subtence, a1.truth)
                out.m["*laws*"] = []
                for a1 in self.constraints.keys():
                    for a2 in s.unsat_core():
                        if str(a1) == str(ps[a2]):
                            out.m["*laws*"].append(a1.reading if hasattr(a1, "reading") else str(self.constraints[a1]))
                for a1 in self.typeConstraints:
                    for a2 in s.unsat_core():
                        if str(a1) == str(ps[a2]):
                            out.m["*laws*"].append(a1.reading if hasattr(a1, "reading") else str(a1))

        return out.m

    def abstract(self):
        out = {} # {category : [LiteralQ]}

        theory = self.theory(with_assumptions=False)
        solver, reify, unreify = mk_solver(theory, self.atoms.values())

        # extract fixed atoms from constraints
        universal = consequences(theory, self.atoms.values(), {}, solver, reify, unreify)
        out["universal"] = [k for k in universal.keys() if k.truth is not None]

        out["given"] = []
        for ass in self.structure:
            universal[ass] = True
            out["given"] += [ass]

        # find consequences of structure
        solver.add(list(self.structure.values()))
        theory2 = And([theory] + list(self.structure.values()))
        fixed = consequences(theory2, self.atoms.values(), universal, solver, reify, unreify)
        out["fixed"] = [k for k in fixed.keys() if k.truth is not None]

        models, count = {}, 0
        done = set(out["universal"] + out["given"] + out["fixed"])

        # substitutions = [(quantifier/chained, reified)] + [(consequences, truthvalue)]
        substitutions = []
        reified = Function("qsdfvqe13435", StringSort(), BoolSort())
        for atom_string, atom in self.atoms.items():
            atomZ3 = atom.translated #TODO
            if atom.type == 'bool' or (hasattr(atom.decl, 'sorts') and atom.decl.type.name == 'bool'):
                substitutions += [(atomZ3, reified(StringVal(atom_string.encode('utf8'))))]
        for literalQ in done:
            if is_bool(literalQ.subtence): #TODO
                substitutions += [(literalQ.subtence, BoolVal(literalQ.truth))]

        # relevants = getAtoms(simplify(substitute(self.constraints, substitutions)))
        simplified = simplify(substitute(And(list(self.constraints.keys())), substitutions)) # it starts by the last substitution ??
        relevants = getAtoms(simplified, self.valueMap, self.symbols) # includes reified !

        # --> irrelevant
        irrelevant = []
        for atom_string, atom in self.atoms.items():
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
        for atom in self.atoms.values():
            atomZ3 = atom.translated #TODO
            for symb in atom.unknown_symbols().keys():
                models[symb] = [] # models[symb][row] = [relevant atoms]
                break
        
        while solver.check() == sat and count < 50: # for each parametric model
            #for symb in self.symbols.values():
            #    print (symb, solver.model().eval(symb))

            # theory that forces irrelevant atoms to be irrelevant
            theory2 = And(theory, And(self.typeConstraints))

            atoms = [] # [LiteralQ]
            for atom_string, atom in self.atoms.items():
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
            solver2.add(self.typeConstraints) # without theory !
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


    #################
    # Output structure
    #################

    def initial_structure(self):
        out = Structure(self)
        for atom in self.atoms.values():
            out.initialise(self, atom, False, False, "")
        return out


    def model_to_json(self, s, reify, unreify):
        m = s.model()
        out = self.initial_structure()
        for atom in self.atoms.values():
            atomZ3 = atom.translated #TODO
            # atom might not have an interpretation in model (if "don't care")
            value = m.eval(reify[atom], model_completion=True)
            if is_bool(atomZ3): #TODO
                if not (is_true(value) or is_false(value)):
                    #TODO value may be an expression, e.g. for quantified expression --> assert a value ?
                    print("*** ", atomZ3, " is not defined, and assumed false")
                out.addAtom(self, atom, True if is_true(value) else False)
            else: #TODO check that value is numeric ?
                out.addValue(self, atom, value)
        return out.m
    

class Structure:
    def __init__(self, case):
        self.m = {}

    def initialise(self, case, atom, ct_true, ct_false, value=""):
        atomZ3 = atom.translated #TODO
        key = atom.str
        typ = atomZ3.sort().name()
        for symb in atom.unknown_symbols().keys():
            s = self.m.setdefault(symb, {})
            if typ == 'Bool':
                symbol = {"typ": typ, "ct": ct_true, "cf": ct_false}
            elif case.symbol_types[symb] in case.enums:
                symbol = { "typ": typ, "value": str(value)
                         , "values": [str(v) for v in case.enums[case.symbol_types[symb]]]}
            elif typ in ["Real", "Int"]:
                symbol = {"typ": typ, "value": str(value)} # default
            else:
                symbol = None
            if symbol: 
                if hasattr(atom, 'reading'):
                    symbol['reading'] = atom.reading
                symbol['normal'] = hasattr(atom, 'normal')
                s.setdefault(key, symbol)
                break

    def addAtom(self, case, atom, truth):
        if truth and type(atom) == Equality:
            self.addValue(case, atom.subtence, atom.value)
        atomZ3 = atom.translated
        if not is_bool(atomZ3): return
        key = atom.str
        for symb in atom.unknown_symbols().keys():
            s = self.m.setdefault(symb, {})
            if key in s:
                if truth is None: s[key]["unknown"] = True
                else:
                    s[key]["ct" if truth else "cf"] = True
                if hasattr(atom, 'reading'):
                    s[key]['reading'] = atom.reading

    def addValue(self, case, atom, value):
        symbol = atom.translated
        key = atom.str
        typ = symbol.sort().name()
        for symb in atom.unknown_symbols().keys():
            s = self.m.setdefault(str(symb), {})
            if key in s:
                if typ in ["Real", "Int"]:
                    s[key]["value"] = str(eval(str(value).replace('?', ''))) # compute fraction
                elif typ in case.enums: #TODO and type(atom) != IfExpr:
                    s[key]["value"] = str(value)

