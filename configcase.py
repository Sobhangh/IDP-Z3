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
import ast
import json
import re
from typing import List
from z3.z3 import _py2expr

from LiteralQ import *
from Theory import *
from utils import *

class ConfigCase:

    def __init__(self, theory):
        self.enums = {} # {string: [string] } idp_type -> DSLobject
        self.valueMap = {"True": True}

        self.symbols = {} # {string: Z3Expr}
        self.args = {} # {Z3Expr: [ (Z3expr) ]}
        self.symbol_types = {} # {string: string} symbol -> idp_type
        self.interpreted = {} # from structure: {string: True}

        self.atoms = {} # {atom_string: Z3expr} atoms + numeric terms !
        self.Z3atoms = {} # {Z3_code: Z3expr}

        self.assumptions = [] # [atomZ3]
        self.assumptionLs = {} # {literalQ : True} (needed for propagate)
        self.constraints = {} # {Z3expr: string}
        self.typeConstraints = []
        
        theory.translate(self)

        # remove atoms based only on interpreted symbols
        self.atoms = {k:v for (k,v) in self.atoms.items() \
            if symbols_of(v, self.symbols, self.interpreted) }


    #################
    # Helpers for translating idp code
    #################

    def Const(self, txt: str, sort, normal=False):
        const = self.symbols.setdefault(txt, Const(txt, sort))
        if normal: # this is a declared constant
            const.normal = True
            if not txt.startswith('_'):
                self.atoms[txt] = const
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
        self.args[out] = args
        for arg in list(args):
            expr = out(*arg)
            expr.normal = True
            if not str(expr).startswith('_'):
                self.atoms[str(expr)] = expr
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

    def Atom(self, atomZ3, atom_string=None):
        """
            Z3_code:    ASCII, with ==, <=, !=
            atom_string:original code, using UTF-8 characters for connectives
            reading:    string from code annotation
            proposition:qsdfvqe13435(Z3_code)
        """
        if is_bool(atomZ3) and (is_quantifier(atomZ3) or not has_local_var(atomZ3, self.valueMap, self.symbols)): # AtomQ !
            atom_string = atom_string if atom_string else atom_as_string(atomZ3)
            atomZ3.atom_string = atom_string
            self.atoms.update({atom_string: atomZ3})

            if hasattr(atomZ3, 'reading'): # then use it
                self.atoms[atom_string].reading = atomZ3.reading
            elif not hasattr(self.atoms[atom_string], 'reading'): # then use default value
                self.atoms[atom_string].reading = atom_string

            self.Z3atoms[str(atomZ3)] = self.atoms[atom_string]

    def add(self, constraint, source_code):
        self.constraints[constraint] = source_code



    #################
    # Helpers to load user's choices
    #################

    # Structure: symbol -> atom -> {ct,cf} -> true/false
    def loadStructureFromJson(self, jsonstr):
        json_data = ast.literal_eval(jsonstr \
            .replace("\\\\u2264", "≤").replace("\\\\u2265", "≥").replace("\\\\u2260", "≠")
            .replace("\\\\u2200", "∀").replace("\\\\u2203", "∃")
            .replace("\\\\u21d2", "⇒").replace("\\\\u21d4", "⇔").replace("\\\\u21d0", "⇐")
            .replace("\\\\u2228", "∨").replace("\\\\u2227", "∧"))

        self.assumptions, self.assumptionLs = [], {}
        for sym in json_data:
            for atom in json_data[sym]:
                json_atom = json_data[sym][atom]
                if atom in self.atoms:
                    atomZ3 = self.atoms[atom]
                    if json_atom["typ"] == "Bool":
                        if "ct" in json_atom and json_atom["ct"]:
                            literalQ = LiteralQ(True, atomZ3)
                        if "cf" in json_atom and json_atom["cf"]:
                            literalQ = LiteralQ(False, atomZ3)
                    elif json_atom["value"]:
                        if json_atom["typ"] == "Int":
                            value = int(json_atom["value"])
                        elif json_atom["typ"] == "Real":
                            value = float(json_atom["value"])
                        else:
                            value = self.valueMap[json_atom["value"]]
                        literalQ = LiteralQ(True, atomZ3 == value)
                    else:
                        literalQ = None #TODO error ?
                    if literalQ is not None:
                        self.assumptions.append(literalQ.asZ3())
                        self.assumptionLs[literalQ] = True

    #################
    # INFERENCES
    #################

    def theory(self, with_assumptions=False):
        return And(list(self.constraints.keys()) 
            + self.typeConstraints
            + (self.assumptions if with_assumptions else []))

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


    def propagation(self):
        out = self.initial_structure()

        amf = consequences(self.theory(with_assumptions=True), self.atoms.values(), {})
        for literalQ in amf:
            out.addAtom(self, literalQ.atomZ3, literalQ.truth)

        # useful for non linear assumptions
        """
        amf = consequences(self.theory(with_assumptions=False), self.atoms.values(), amf)
        for literalQ in amf:
            out.addAtom(self, literalQ.atomZ3, literalQ.truth)
        """

        for literalQ in self.assumptionLs.keys(): # needed to keep some numeric assignments
            out.addAtom(self, literalQ.atomZ3, literalQ.truth)
        return out.m

    def expand(self):
        theory = self.theory(with_assumptions=True)
        solver, reify, unreify = mk_solver(theory, self.atoms.values())
        solver.check()
        return self.model_to_json(solver, reify, unreify)

    def relevance(self): 
        out = self.initial_structure()
        """ # not used, not working
        solver = Solver()
        theo1 = And(list(self.constraints.keys()))
        solver.add(self.typeConstraints + self.assumptions)

        for s in self.symbols.values():
            solver.push()
            if type(s) == FuncDeclRef:
                type_list = [s.domain(i) for i in range(0, s.arity())] + [s.range()]
                c = Function("temporaryFunction", type_list)

                constants = [Const('vx'+str(i), s.domain(i)) for i in range(0, s.arity())]
                arg_fill = [Const('vy'+str(i), s.domain(i)) for i in range(0, s.arity())]
                solver.add(
                    ForAll(constants,
                           Or(And(pairwiseEquals(arg_fill, constants)),
                              s(constants) == c(constants))))
                var_list = [Var(i, s.domain(i)) for i in range(0, s.arity())]
                theo2 = rewrite(theo1, s, applyTo(c, var_list))
                type_transform = rewrite(And(self.typeConstraints + self.assumptions), s, applyTo(c, var_list))
            else:
                c = Const('temporaryConstant', s.sort())
                solver.add(c != s)
                theo2 = substitute(theo1, (s, c))
                type_transform = substitute(And(self.typeConstraints + self.assumptions), (s, c))
                arg_fill = []
            solver.add(type_transform)
            solver.add(theo1 != theo2)

            argshandled = {}
            for arg, val in self.relevantVals[s]:
                strargs = json.dumps([obj_to_string(x) for x in arg])
                if strargs in argshandled:
                    continue
                argshandled[strargs] = True

                solver.push()
                solver.add(And(pairwiseEquals(arg_fill, arg)))
                a = solver.check()
                solver.pop()
                if not (a == unsat):
                    out.fillApp(applyTo(s, arg))

            solver.pop()
        """
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
        for ass in self.assumptions: # add numeric assumptions
            for atomZ3 in getAtoms(ass,self.valueMap, self.symbols).values():
                out.initialise(self, atomZ3, False, False, "")    

        value = value.replace("\\u2264", "≤").replace("\\u2265", "≥").replace("\\u2260", "≠") \
            .replace("\\u2200", "∀").replace("\\u2203", "∃") \
            .replace("\\u21d2", "⇒").replace("\\u21d4", "⇔").replace("\\u21d0", "⇐") \
            .replace("\\u2228", "∨").replace("\\u2227", "∧")
        if value in self.atoms:
            to_explain = self.atoms[value] # value is an atom string

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
            constraints = list(self.constraints.keys()) + self.typeConstraints + self.assumptions
            for i, constraint in enumerate(constraints):
                p = Const("wsdraqsesdf"+str(i), BoolSort())
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
                for a1 in self.assumptions:
                    for a2 in s.unsat_core():
                        if str(a1) == str(ps[a2]): #TODO we might miss some equality
                            out.addAtom(self, a1, True)
                out.m["*laws*"] = []
                for a1 in self.constraints.keys():
                    for a2 in s.unsat_core():
                        if str(a1) == str(ps[a2]):
                            out.m["*laws*"].append(a1.reading if hasattr(a1, "reading") else self.constraints[a1])
                for a1 in self.typeConstraints:
                    for a2 in s.unsat_core():
                        if str(a1) == str(ps[a2]):
                            out.m["*laws*"].append(a1.reading if hasattr(a1, "reading") else a1)

        return out.m

    def abstract(self):
        out = {} # {category : [LiteralQ]}

        theory = self.theory(with_assumptions=False)
        solver, reify, unreify = mk_solver(theory, self.atoms.values())

        # extract fixed atoms from constraints
        universal = consequences(theory, self.atoms.values(), {}, solver, reify, unreify)
        out["universal"] = [k for k in universal.keys() if k.truth is not None]

        out["given"] = []
        for assumption in self.assumptions:
            if is_not(assumption):
                ass = LiteralQ(False, assumption.children()[0])
            else:
                ass = LiteralQ(True, assumption)
            universal[ass] = True
            out["given"] += [ass]

        # extract assumptions and their consequences
        solver.add(self.assumptions)
        theory2 = And([theory] + self.assumptions)
        fixed = consequences(theory2, self.atoms.values(), universal, solver, reify, unreify)
        out["fixed"] = [k for k in fixed.keys() if k.truth is not None]

        models, count = {}, 0
        done = set(out["universal"] + out["given"] + out["fixed"])

        # substitutions = [(quantifier/chained, reified)] + [(consequences, truthvalue)]
        substitutions = []
        reified = Function("qsdfvqe13435", StringSort(), BoolSort())
        for atom_string, atomZ3 in self.atoms.items():
            if hasattr(atomZ3, 'atom_string'):
                substitutions += [(atomZ3, reified(StringVal(atom_string.encode('utf8'))))]
        for literalQ in done:
            if is_bool(literalQ.atomZ3):
                substitutions += [(literalQ.atomZ3, BoolVal(literalQ.truth))]

        # relevants = getAtoms(simplify(substitute(self.constraints, substitutions)))
        simplified = simplify(substitute(And(list(self.constraints.keys())), substitutions)) # it starts by the last substitution ??
        relevants = getAtoms(simplified, self.valueMap, self.symbols) # includes reified !

        # --> irrelevant
        irrelevant = []
        for atom_string, atomZ3 in self.atoms.items():
            if is_bool(atomZ3) \
            and not LiteralQ(True , atomZ3) in done \
            and not LiteralQ(False, atomZ3) in done:
                string2 = atom_as_string(reified(StringVal(atom_string.encode('utf8'))))
                if not string2 in relevants:
                    irrelevant += [LiteralQ(True, atomZ3)]
        out["irrelevant"] = irrelevant
        done2 = done.union(set(irrelevant))

        # create keys for models using first symbol of atoms
        for atomZ3 in self.atoms.values():
            for symb in symbols_of(atomZ3, self.symbols, self.interpreted).keys():
                models[symb] = [] # models[symb][row] = [relevant atoms]
                break
        
        while solver.check() == sat and count < 50: # for each parametric model
            #for symb in self.symbols.values():
            #    print (symb, solver.model().eval(symb))

            # theory that forces irrelevant atoms to be irrelevant
            theory2 = And(theory, And(self.typeConstraints))

            atoms = [] # [LiteralQ]
            for atom_string, atomZ3 in self.atoms.items():
                if is_bool(atomZ3) \
                and not LiteralQ(True , atomZ3) in done2 \
                and not LiteralQ(False, atomZ3) in done2 \
                and not atom_string in relevants :
                    truth = solver.model().eval(reify[atomZ3])
                    if truth == True:
                        atoms += [ LiteralQ(True,  atomZ3) ]
                    elif truth == False:
                        atoms += [ LiteralQ(False, atomZ3) ]
                    else: #unknown
                        theory2 = And(theory2, 
                                      substitute(theory2, [(atomZ3, BoolVal(True))]),  # don't simplify !
                                      substitute(theory2, [(atomZ3, BoolVal(False))])) # it would break later substitutions
                    # models.setdefault(groupBy, [[]] * count) # create keys for models using first symbol of atoms

            # start with negations !
            atoms.sort(key=lambda l: (l.truth, str(l.atomZ3)))

            # remove atoms that are irrelevant in AMF
            solver2 = Solver()
            solver2.add(theory2)
            solver2.add([l.asZ3() for l in done]) # universal + given + fixed (ignore irrelevant)
            (reify2, _) = reifier([l.atomZ3 for l in atoms], solver2)
            for i, literalQ in enumerate(atoms):
                if not is_true(literalQ.atomZ3):
                    solver2.push()
                    a = reify2[literalQ.atomZ3] if not literalQ.truth else Not(reify2[literalQ.atomZ3])
                    solver2.add(a)
                    solver2.add(And([l.asZ3() for j, l in enumerate(atoms) if j != i]))
                    result = solver2.check()
                    solver2.pop()
                    if result == sat:
                        theory2 = And(theory2, 
                                    substitute(theory2, [(literalQ.atomZ3, BoolVal(True))]),
                                    substitute(theory2, [(literalQ.atomZ3, BoolVal(False))]))
                        solver2.add(theory2)
                        atoms[i] = LiteralQ(True, BoolVal(True))

            # remove atoms that are consequences of others in the AMF
            solver2 = Solver()
            solver2.add(self.typeConstraints) # without theory !
            (reify2, _) = reifier([l.atomZ3 for l in atoms], solver2)
            for i, literalQ in enumerate(atoms):
                if not is_true(literalQ.atomZ3):
                    solver2.push()
                    solver2.add(And([l.asZ3() for j, l in enumerate(atoms) if j != i]))

                    # evaluate not(literalQ)
                    a = reify2[literalQ.atomZ3] if not literalQ.truth else Not(reify2[literalQ.atomZ3])
                    result, consq = solver2.consequences([], [a])
                    if result!=sat or consq: # remove it if it's a consequence
                        atoms[i] = LiteralQ(True, BoolVal(True))
                        # ??? theory2 = substitute(theory2, [(literalQ.atomZ3, BoolVal(literalQ.truth))])
                    solver2.pop()

            # add constraint to eliminate this model
            modelZ3 = Not(And( [l.asZ3() for l in atoms] ))
            theory = And(theory, modelZ3)
            solver.add(modelZ3)

            # group atoms by symbols
            model = {}
            for l in atoms:
                for symb in symbols_of(l.atomZ3, self.symbols, self.interpreted).keys():
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
        for atomZ3 in self.atoms.values():
            out.initialise(self, atomZ3, False, False, "")
        return out


    def model_to_json(self, s, reify, unreify):
        m = s.model()
        out = self.initial_structure()
        for atomZ3 in self.atoms.values():
            # atom might not have an interpretation in model (if "don't care")
            value = m.eval(reify[atomZ3], model_completion=True)
            if atomZ3.sort().name() == 'Bool':
                if not (is_true(value) or is_false(value)):
                    #TODO value may be an expression, e.g. for quantified expression --> assert a value ?
                    print("*** ", atomZ3, " is not defined, and assumed false")
                out.addAtom(self, atomZ3, True if is_true(value) else False)
            else: #TODO check that value is numeric ?
                out.addValue(self, atomZ3, value)
        return out.m
    

class Structure:
    def __init__(self, case):
        self.m = {}

    def initialise(self, case, atomZ3, ct_true, ct_false, value=""):
        key = atom_as_string(atomZ3)
        typ = atomZ3.sort().name()
        for symb in symbols_of(atomZ3, case.symbols, case.interpreted):
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
                if hasattr(atomZ3, 'reading'):
                    symbol['reading'] = atomZ3.reading
                symbol['normal'] = hasattr(atomZ3, 'normal')
                s.setdefault(key, symbol)
                break

    def addAtom(self, case, atomZ3, truth):
        if atomZ3.sort().name() != 'Bool': return
        if truth and is_eq(atomZ3): # try to interpret it as an assignment
            if atomZ3.arg(1).__class__.__name__ in ["IntNumRef", "RatNumRef", "AlgebraicNumRef", "DatatypeRef"]:  # is this really a value ?
                self.addValue(case, atomZ3.arg(0), atomZ3.arg(1))
            if atomZ3.arg(0).__class__.__name__ in ["IntNumRef", "RatNumRef", "AlgebraicNumRef", "DatatypeRef"]:  # is this really a value ?
                self.addValue(case, atomZ3.arg(1), atomZ3.arg(0))
        if is_not(atomZ3):
            atomZ3 = atomZ3.arg(0)
            truth = None if truth is None else not truth
        key = atom_as_string(atomZ3)
        for symb in symbols_of(atomZ3, case.symbols, case.interpreted).keys():
            s = self.m.setdefault(symb, {})
            if key in s:
                if truth is None: s[key]["unknown"] = True
                else:
                    s[key]["ct" if truth else "cf"] = True
                if hasattr(atomZ3, 'reading'):
                    s[key]['reading'] = atomZ3.reading

    def addValue(self, case, symbol, value):
        key = atom_as_string(symbol)
        typ = symbol.sort().name()
        for symb in symbols_of(symbol, case.symbols, case.interpreted).keys():
            s = self.m.setdefault(str(symb), {})
            if key in s:
                if typ in ["Real", "Int"]:
                    s[key]["value"] = str(eval(str(value).replace('?', ''))) # compute fraction
                elif typ in case.enums and value.decl().name() != "if":
                    s[key]["value"] = str(value)

