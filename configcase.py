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
from typing import List

from z3.z3 import _py2expr

from utils import *

from LiteralQ import *
from Theory import *

class ConfigCase:

    def __init__(self, theory):
        self.relevantVals = {}
        self.enums = {} # {string: string[]}
        self.symbols = {} # {string: Z3Expr}
        self.assumptions = [] # [atomZ3]
        self.assumptionLs = {} # {literalQ : True} (needed for propagate)
        self.valueMap = {"True": True}
        self.constraints = {} # {Z3expr: string}
        self.interpreted = {} # from structure: {string: True}
        self.typeConstraints = []
        self.atoms = {} # {atom_string: Z3expr} atoms + numeric terms !
        self.Z3atoms = {} # {Z3_code: Z3expr}
        theory.translate(self)

        out = {}
        for atomZ3 in self.atoms.values(): # add numeric terms first
            out.update(self.getNumericTerms(atomZ3))
        if "Tax" in self.symbols: #TODO hack for video
            out.update(self.symbols)
            out.update({k:v for (k,v) in self.atoms.items() if "Tax" in k})
        else:
            out.update(self.atoms) # then other atoms
        self.atoms = out

    #################
    # BUILDER FUNCTIONS
    #################

    def Const(self, txt: str, sort):
        const = Const(txt, sort)
        self.symbols[str(const)] = const
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
        values = list(itertools.product(args, vals))
        self.symbols[str(out)] = out
        self.relevantVals[out] = values
        if restrictive:
            for arg in list(args):
                exp = in_list(out(*arg), vals)
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


    #################
    # EXPRESSIONS
    #################

    def getNumericTerms(self, expr): # to be shown as atoms
        out = {}  # Ordered dict: string -> Z3 object
        if not is_app(expr): return out
        name = expr.decl().name()
        typ = expr.sort().name()
        if is_symbol(name, self.symbols) \
            and ( typ in ["Real", "Int"] or typ in self.enums ) \
            and not is_really_constant(expr, self.valueMap) \
            and has_ground_children(expr, self.valueMap) \
            and expr.decl().name() not in ["+", "-", "*", "/"]:
                out[atom_as_string(expr)] = expr

        for child in expr.children():
            out.update(self.getNumericTerms(child))
        return out

    def getAtoms(self, expr):
        out = {}  # Ordered dict: string -> Z3 object
        for child in expr.children():
            out.update(self.getAtoms(child))
        if is_bool(expr) and len(out) == 0 and \
            ( not has_local_var(expr, self.valueMap, self.symbols) or is_quantifier(expr) ): # for quantified formulas
            out = {atom_as_string(expr): expr}
        return out


    #################
    # UTILITIES
    #################

    def add(self, constraint, source_code):
        self.constraints[constraint] = source_code

    def theory(self, with_assumptions=False):
        return And(list(self.constraints.keys()) 
            + self.typeConstraints
            + (self.assumptions if with_assumptions else []))

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
                if atom[2:-2] in self.atoms:
                    atomZ3 = self.atoms[atom[2:-2]]
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

    def args(self, val):
        a, _ = splitLast(list(map(self.z3_value, json.loads(val))))
        return a

    def outVal(self, val):
        _, l = splitLast(list(map(self.z3_value, json.loads(val))))
        return l

    def metaJSON(self):
        symbols = []
        for i in self.symbols.values():
            symbol_type = "function"
            if type(i) == BoolRef:
                symbol_type = "proposition"
            symbols.append({
                "idpname": str(i),
                "type": symbol_type,
                "priority": "core",
                "showOptimize": type(i) == ArithRef
            })
        out = {"title": "Interactive Consultant", "symbols": symbols, "values": []}
        return out

    def z3_value(self, value):
        if value in self.valueMap:
            return self.valueMap[value]
        else:
            return value

    #################
    # INFERENCES
    #################

    def atomsGrouped(self):
        out = {} # {symbol_string : [atom_string, []]}
        for atom_string, atomZ3 in self.atoms.items():
            for groupBy in symbols_of(atomZ3, self.symbols, self.interpreted).keys():
                d = out.setdefault(groupBy, [])
                temp = json.dumps([atom_string])
                if temp not in d: # test: x=y(x).
                    d.append(temp)
                break
        return out


    def propagation(self):
        out = self.initial_structure()

        amf = consequences(self.theory(with_assumptions=True), self.atoms.values(), {})
        for literalQ in amf:
            out.addAtom(self, literalQ.atomZ3, literalQ.truth)

        # useful for non linear assumptions
        amf = consequences(self.theory(with_assumptions=False), self.atoms.values(), amf)
        for literalQ in amf:
            out.addAtom(self, literalQ.atomZ3, literalQ.truth)

        for literalQ in self.assumptionLs.keys(): # needed to keep some numeric assignments
            out.addAtom(self, literalQ.atomZ3, literalQ.truth)
        return out.m

    def expand(self):
        theory = self.theory(with_assumptions=True)
        solver, reify, unreify = mk_solver(theory, self.atoms.values())
        solver.check()
        return self.model_to_json(solver, reify, unreify)

    def relevance(self): # not used
        out = self.initial_structure()

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
        return out.m

    def optimize(self, symbol, minimize):
        solver = Optimize()
        solver.add(self.theory(with_assumptions=True))
        s = self.symbols[symbol]
        if minimize:
            solver.minimize(s)
        else:
            solver.maximize(s)

        (reify, unreify) = reifier(self.atoms.values(), solver)
        solver.check()
        return self.model_to_json(solver, reify, unreify)

    def explain(self, symbol, value):
        out = self.initial_structure()
        for ass in self.assumptions: # add numeric assumptions
            for atomZ3 in self.getAtoms(ass).values():
                out.initialise(self, atomZ3, False, False, "")

        value = value.replace("\\u2264", "≤").replace("\\u2265", "≥").replace("\\u2260", "≠") \
            .replace("\\u2200", "∀").replace("\\u2203", "∃") \
            .replace("\\u21d2", "⇒").replace("\\u21d4", "⇔").replace("\\u21d0", "⇐") \
            .replace("\\u2228", "∨").replace("\\u2227", "∧")
        if value[2:-2] in self.atoms:
            to_explain = self.atoms[value[2:-2]] # value is an atom string

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
        relevants = self.getAtoms(simplified) # includes reified !

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
        done = done.union(set(irrelevant))

        # create keys for models using first symbol of atoms
        for atomZ3 in self.atoms.values():
            for symb in symbols_of(atomZ3, self.symbols, self.interpreted).keys():
                models[symb] = [] # models[symb][row] = [relevant atoms]
                break
        
        while solver.check() == sat and count < 50: # for each parametric model
            #for symb in self.symbols.values():
            #    print (symb, solver.model().eval(symb))

            atoms = [] # [LiteralQ]
            for atom_string, atomZ3 in self.atoms.items():
                if is_bool(atomZ3) \
                and not LiteralQ(True , atomZ3) in done \
                and not LiteralQ(False, atomZ3) in done \
                and not atom_string in relevants :
                    truth = solver.model().eval(reify[atomZ3])
                    if truth == True:
                        atoms += [ LiteralQ(True,  atomZ3) ]
                    elif truth == False:
                        atoms += [ LiteralQ(False, atomZ3) ]
                    # models.setdefault(groupBy, [[]] * count) # create keys for models using first symbol of atoms

            # remove atoms that are consequences of others
            solver2 = Solver()
            solver2.add(self.typeConstraints)  # ignore theory !
            (reify2, _) = reifier([l.atomZ3 for l in atoms], solver2)
            for i, literalQ in enumerate(atoms):
                solver2.push()
                solver2.add(And([l.asZ3() for j, l in enumerate(atoms) if j != i]))

                a = reify2[literalQ.atomZ3] if not literalQ.truth else Not(reify2[literalQ.atomZ3])
                result, consq = solver2.consequences([], [a])
                if result!=sat or consq: # remove it if it's a consequence
                    atoms[i] = LiteralQ(True, BoolVal(True))
                solver2.pop()

            # add constraint to eliminate this model
            modelZ3 = And( [l.asZ3() for l in atoms] )
            solver.add(Not(modelZ3))

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

class Structure:
    def __init__(self, case):
        self.m = {} # {symbol_string: {atom : {ct: Bool}, "[]": {args: value}? }
        # print("Structure")
        # for symb in case.symbols.values():
        #     s = self.m.setdefault(str(symb), {})
        #     for arg, val in case.relevantVals[symb]:
        #         if type(symb) != BoolRef:
        #             # symbol can have a numeric value
        #             print(symb, arg, val)

    def initialise(self, case, atomZ3, ct_true, ct_false, value=""):
        key = json.dumps([atom_as_string(atomZ3)])
        typ = atomZ3.sort().name()
        for symb in symbols_of(atomZ3, case.symbols, case.interpreted):
            s = self.m.setdefault(symb, {})
            if typ == 'Bool':
                symbol = {"typ": typ, "ct": ct_true, "cf": ct_false}
            elif typ in ["Real", "Int"]:
                symb = case.symbols[atomZ3.decl().name()]
                if symb in case.relevantVals and case.relevantVals[symb]:
                    values = [] #TODO refactor using enumeration type of symbol
                    for _,b in case.relevantVals[symb]:
                        v = str(eval(str(b)))
                        if v in values: break
                        values.append(v)
                    symbol = {"typ": typ, "value": str(value), "values": values}
                else:
                    symbol = {"typ": typ, "value": str(value)}
            elif typ in case.enums:
                symbol = {"typ": typ, "value": str(value), "values": case.enums[typ]}
            else:
                symbol = None
            if symbol: 
                if hasattr(atomZ3, 'reading'):
                    symbol['reading'] = atomZ3.reading
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
        key = json.dumps([atom_as_string(atomZ3)])
        for symb in symbols_of(atomZ3, case.symbols, case.interpreted).keys():
            s = self.m.setdefault(symb, {})
            if key in s:
                if truth is None: s[key]["unknown"] = True
                else:
                    s[key]["ct" if truth else "cf"] = True
                if hasattr(atomZ3, 'reading'):
                    s[key]['reading'] = atomZ3.reading

    def addValue(self, case, symbol, value):
        key = json.dumps([atom_as_string(symbol)])
        typ = symbol.sort().name()
        for symb in symbols_of(symbol, case.symbols, case.interpreted).keys():
            s = self.m.setdefault(str(symb), {})
            if key in s:
                if typ in ["Real", "Int"]:
                    s[key]["value"] = str(eval(str(value).replace('?', ''))) # compute fraction
                elif typ in case.enums and value.decl().name() != "if":
                    s[key]["value"] = str(value)



def atom_as_string(expr):
    if hasattr(expr, 'atom_string'): return expr.atom_string
    return str(expr).replace("==", "=").replace("!=", "≠").replace("<=", "≤")