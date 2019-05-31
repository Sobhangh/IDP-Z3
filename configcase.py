import ast
import json
from typing import List

from z3.z3 import _py2expr

from utils import *


class ConfigCase:

    def __init__(self, theory=(lambda x: 0)):
        self.relevantVals = {}
        self.symbols = []
        self.assumptions = []
        self.valueMap = {"True": True}
        self.constraints = []
        self.typeConstraints = []
        self.atoms = {}
        theory(self)

        out = {}
        for atomZ3 in self.atoms.values(): # add terms first
            out.update(self.getTerms(atomZ3))
        out.update(self.atoms) # then other atoms
        self.atoms = out

    #################
    # BUILDER FUNCTIONS
    #################

    def Const(self, txt: str, sort):
        const = Const(txt, sort)
        self.symbols.append(const)
        return const

    def EnumSort(self, name, objects):
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
        self.symbols.append(out)
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

    def Atom(self, atom_string, atomZ3):
        if is_bool(atomZ3) and (is_quantifier(atomZ3) or not self.has_local_var(atomZ3)):
            atomZ3.atom_string = atom_string
            self.atoms.update({atom_string: atomZ3})

    #################
    # UTILITIES
    #################

    def add(self, constraint):
        self.constraints.append(constraint)

    def mk_solver(self, with_assumptions=False):
        s = Solver()
        s.add(self.constraints)
        s.add(self.typeConstraints)
        if with_assumptions: s.add(self.assumptions)
        return s

    def expand(self):
        solver = self.mk_solver(with_assumptions=True)
        (reify, unreify) = self.quantified(solver)
        solver.check()
        return self.model_to_json(solver, reify, unreify)

    def initial_structure(self):
        out = Structure(self)
        for atomZ3 in self.atoms.values():
            out.initialise(self, atomZ3, False, False, "")
        return out


    def quantified(self, s):
        # creates predicates equivalent to the infinitely-quantified formulas
        # returns ({atomZ3: predicate}, {predicate: atomZ3})
        count, (reify, unreify) = 0, ({}, {})
        for atomZ3 in self.atoms.values():
            if is_quantifier(atomZ3) or hasattr(atomZ3, 'atom_string'):
                count += 1
                const = Const("iuzctedvqsdgqe"+str(count), BoolSort())
                s.add(const == atomZ3)
                reify[atomZ3] = const
                unreify[const] = atomZ3
            else:
                reify[atomZ3] = atomZ3
                unreify[atomZ3] = atomZ3
        return (reify, unreify)

    def model_to_json(self, s, reify, unreify):
        m = s.model()
        out = self.initial_structure()
        for atomZ3 in self.atoms.values():
            # atom might not have an interpretation in model (if "don't care")
            value = m.eval(reify[atomZ3], model_completion=True)
            if atomZ3.sort().name() == 'Bool':
                value = True if value else False
                out.addAtom(self, atomZ3, unreify, value, "")
            else:
                out.addAtom(self, atomZ3, unreify, True, value)
        return out.m

    def is_really_constant(self, expr):
        return (obj_to_string(expr) in self.valueMap) \
            or is_number(obj_to_string(expr)) \
            or is_true(expr) or is_false(expr)

    def has_ground_children(self, expr):
        return all([self.is_ground(child) for child in expr.children()])

    def is_ground(self, expr):
        return self.is_really_constant(expr) or \
            (0 < len(expr.children()) and self.has_ground_children(expr))

    def has_local_var(self, expr):
        out = ( 0==len(expr.children()) and not self.is_symbol(expr) \
                and not self.is_really_constant(expr)) \
           or ( 0 < len(expr.children()) \
                and any([self.has_local_var(child) for child in expr.children()]))
        return out

    def getTerms(self, expr):
        out = {}  # Ordered dict: string -> Z3 object
        if not is_app(expr): return out
        if expr.sort().name() in ["Real", "Int"] and not self.is_really_constant(expr) \
           and self.has_ground_children(expr) and expr.decl().name() not in ["+", "-", "*", "/"]:
                out = {atom_as_string(expr): expr}
        for child in expr.children():
                out.update(self.getTerms(child))
        return out

    def getAtoms(self, expr):
        out = {}  # Ordered dict: string -> Z3 object
        for child in expr.children():
            out.update(self.getAtoms(child))
        if is_bool(expr) and len(out) == 0 and \
            ( not self.has_local_var(expr) or is_quantifier(expr) ): # for quantified formulas
            out = {atom_as_string(expr): expr}
        return out

    def as_symbol(self, symb_str):
        #print(symb_str)
        return list(filter(lambda s: str(s)==symb_str, self.symbols)) [0]

    # Structure: symbol -> atom -> {ct,cf} -> true/false
    def loadStructureFromJson(self, jsonstr):
        json_data = ast.literal_eval(jsonstr \
            .replace("\\\\u2264", "≤").replace("\\\\u2265", "≥").replace("\\\\u2260", "≠")
            .replace("\\\\u2200", "∀").replace("\\\\u2203", "∃"))

        self.assumptions = []
        for sym in json_data:
            for atom in json_data[sym]:
                json_atom = json_data[sym][atom]
                atomZ3 = self.atoms[atom[2:-2]]
                if json_atom["typ"] == "Bool":
                    if "ct" in json_atom and json_atom["ct"]:
                        self.assumptions.append(atomZ3)
                    if "cf" in json_atom and json_atom["cf"]:
                        self.assumptions.append(Not(atomZ3))
                elif json_atom["value"]:
                    if json_atom["typ"] == "Int":
                        value = int(json_atom["value"])
                    elif json_atom["typ"] == "Real":
                        value = float(json_atom["value"])
                    else:
                        value = json_atom["value"]
                    self.assumptions.append(atomZ3 == value)

    def args(self, val):
        a, _ = splitLast(list(map(self.z3_value, json.loads(val))))
        return a

    def outVal(self, val):
        _, l = splitLast(list(map(self.z3_value, json.loads(val))))
        return l

    def metaJSON(self):
        symbols = []
        for i in self.symbols:
            symbol_type = "function"
            if type(i) == BoolRef:
                symbol_type = "proposition"
            symbols.append({
                "idpname": str(i),
                "type": symbol_type,
                "priority": "core",
                "showOptimize": type(i) == ArithRef
            })
        out = {"title": "Interactive Configurator", "symbols": symbols, "values": []}
        return out

    def z3_value(self, value):
        if value in self.valueMap:
            return self.valueMap[value]
        else:
            return value

    def is_symbol(self, symb):
        if is_expr(symb):
            symb = obj_to_string(symb)
        return any(obj_to_string(c) == symb for c in self.symbols)

    #################
    # INFERENCES
    #################

    def relevance(self):
        out = self.initial_structure()

        solver = Solver()
        theo1 = And(self.constraints)
        solver.add(self.typeConstraints + self.assumptions)

        for s in self.symbols:
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

    def explain(self, symbol, value):
        value = value.replace("\\u2264", "≤").replace("\\u2265", "≥").replace("\\u2260", "≠") \
            .replace("\\u2200", "∀").replace("\\u2203", "∃")
        to_explain = self.atoms[value[2:-2]] # value is an atom string

        out = self.initial_structure()
        for ass in self.assumptions: # add numeric assumptions
            for atomZ3 in self.getAtoms(ass).values():
                out.initialise(self, atomZ3, False, False, "")

        solver = self.mk_solver()
        (reify, unreify) = self.quantified(solver)
        def r1(a): return reify[a] if a in reify else a
        def r2(a): return Not(r1(a.children()[0])) if is_not(a) else r1(a)
        _, consqs = solver.consequences([r2(a) for a in self.assumptions], [to_explain])

        for cons in consqs:
            assumption_expr = cons.children()[0]
            if is_true(assumption_expr):
                pass
            elif is_and(assumption_expr): # multiple atoms needed to justify to_explain
                for c in assumption_expr.children():
                    out.addAtom(self, c, unreify, True, "")
            else:
                out.addAtom(self, assumption_expr, unreify, True, "")
        return out.m

    def optimize(self, symbol, minimize):
        solver = Optimize()
        solver.add(self.constraints)
        solver.add(self.typeConstraints)
        solver.add(self.assumptions)
        s = self.as_symbol(symbol)
        if minimize:
            solver.minimize(s)
        else:
            solver.maximize(s)

        (reify, unreify) = self.quantified(solver)
        solver.check()
        return self.model_to_json(solver, reify, unreify)

    def propagation(self):
        out = self.initial_structure()
        solver = self.mk_solver(with_assumptions=True)
        (_, unreify) = self.quantified(solver)

        for atom in unreify.keys(): # numeric variables or atom !
            result, consq = solver.consequences([], [atom])

            if result==sat:
                if consq:
                    consq = consq[0].children()[1]
                    if is_not(consq):
                        out.addAtom(self, atom, unreify, False, "")
                    elif not is_bool(atom): # numeric value
                        out.addAtom(self, consq, unreify, True, "")
                    else:
                        out.addAtom(self, atom, unreify, True, "")
            else: # unknown -> restart solver
                solver = self.mk_solver(with_assumptions=True)
                (_, unreify) = self.quantified(solver)

        return out.m

    def atomsGrouped(self):
        out = {} # {symbol_string : [atom_string, "?"]}
        for atom_string, atomZ3 in self.atoms.items():
            for groupBy in self.symbols_of(atomZ3).keys():
                d = out.setdefault(groupBy, [])
                temp = json.dumps([atom_string])
                if temp not in d: # test: x=y(x).
                    d.append(temp)
        return out

    def symbols_of(self, expr): # returns a dict
        out = {} # for unicity (ordered set)
        try:
            name = expr.decl().name()
            if self.is_symbol(name):
                out[name] = name
        except: pass
        for child in expr.children():
            out.update(self.symbols_of(child))
        return out

    def first_symbol(self, expr):
        symbs = self.symbols_of(expr).keys()
        return symbs[0] if symbs != [] else None


    def abstract(self):
        out = {} # universals, assumptions, consequences, variable

        def _consequences(done, with_assumptions=True):
            out = {} # ordered set of atom_as_string
            solver = self.mk_solver(with_assumptions)
            (reify, _) = self.quantified(solver)

            for atomZ3 in self.atoms.values():# numeric variables or atom !
                if not atom_as_string(atomZ3) in done:
                    result, consq = solver.consequences([], [reify[atomZ3]])

                    if result==sat:
                        if consq:
                            consq = consq[0].children()[1]
                            if is_not(consq):
                                if not ("Not " + atom_as_string(atomZ3)) in done:
                                    out["Not " + atom_as_string(atomZ3)] = True
                            elif not is_bool(atomZ3):
                                if not atom_as_string(consq) in done:
                                    out[atom_as_string(consq)] = True
                            else:
                                out[atom_as_string(atomZ3)] = True
                    else: # unknown -> restart solver
                        solver = self.mk_solver(with_assumptions)
                        (reify, _) = self.quantified(solver)
            return out

        # extract fixed atoms from constraints
        universal = _consequences({}, with_assumptions=False)
        out["universal"] = list(universal.keys())

        out["given"] = []
        for assumption in self.assumptions:
            universal[atom_as_string(assumption)] = True
            out["given"] += [atom_as_string(assumption)]

        # extract assumptions and their consequences
        fixed = _consequences(universal, with_assumptions=True)
        out["fixed"] = list(fixed.keys())

        solver = self.mk_solver(with_assumptions=True)
        models, count = {}, 0
        done = out["universal"] + out["given"] + out["fixed"]

        # create keys for models using first symbol of atoms
        for atomZ3 in self.atoms.values():
            for symb in self.symbols_of(atomZ3).keys():
                models[symb] = [] # models[symb][row] = [relevant atoms]
        (reify, _) = self.quantified(solver)

        while solver.check() == sat: # for each parametric model
            #for symb in self.symbols:
            #    print (symb, solver.model().eval(symb))

            atoms = [] # [(atom_string, atomZ3)]
            for atom_string, atomZ3 in self.atoms.items():
                if is_bool(atomZ3) and not atom_string in done and not ("Not " + atom_string) in done:
                    truth = solver.model().eval(reify[atomZ3])
                    if truth == True:
                        atoms += [ (atom_string, atomZ3) ]
                    elif truth == False:
                        atoms += [ ("Not " + atom_string, Not(atomZ3) ) ]
                    else: # undefined
                        atoms += [ ("? " + atom_string, BoolVal(True)) ]
                    # models.setdefault(groupBy, [[]] * count) # create keys for models using first symbol of atoms

            # add constraint to eliminate this model
            modelZ3 = And( [atomZ3 for (_, atomZ3) in atoms] )
            solver.add(Not(modelZ3))

            # group atoms by symbols
            model = {}
            for atom_string, atomZ3 in atoms:
                for symb in self.symbols_of(atomZ3).keys():
                    model.setdefault(symb, []).append([ atom_string ])
            # add to models
            for k,v in models.items(): # add model
                models[k] = v + [ model[k] if k in model else [] ]
            count +=1

        # join disjuncts
        # TODO

        # detect symbols with atoms
        active_symbol = {}
        for symb in models.keys():
            for i in range(count):
                if not models[symb][i] == []:
                    active_symbol[symb] = True

        # build table of models
        out["variable"] = [[ [symb] for symb in models.keys() if symb in active_symbol ]]
        for i in range(count):
            out["variable"] += [[ models[symb][i] for symb in models.keys() if symb in active_symbol ]]
        return out

class Structure:
    def __init__(self, case):
        self.m = {} # {symbol_string: {atom : {ct: Bool}, "[]": {args: value}? }
        # print("Structure")
        # for symb in case.symbols:
        #     s = self.m.setdefault(str(symb), {})
        #     for arg, val in case.relevantVals[symb]:
        #         if type(symb) != BoolRef:
        #             # symbol can have a numeric value
        #             print(symb, arg, val)

    def getJSON(self):
        return json.dumps(self.m)

    def initialise(self, case, atomZ3, ct_true, ct_false, value=""):
        key = json.dumps([atom_as_string(atomZ3)])
        typ = atomZ3.sort().name()
        for symb in case.symbols_of(atomZ3):
            s = self.m.setdefault(symb, {})
            if typ == 'Bool':
                s.setdefault(key, {"typ": typ, "ct": ct_true, "cf": ct_false})
            elif typ in ["Real", "Int"]:
                s.setdefault(key, {"typ": typ, "value": str(value)})

    def addAtom(self, case, atomZ3, unreify, truth, value):
        if is_eq(atomZ3): # try to interpret it as an assignment
            if atomZ3.arg(1).__class__.__name__ in \
                ["IntNumRef", "RatNumRef", "AlgebraicNumRef"]: # is this really a value ?
                self.addAtom(case, atomZ3.arg(0), unreify, truth, atomZ3.arg(1))
        sgn = "ct" if truth else "cf"
        if is_not(atomZ3):
            atomZ3, sgn, truth = atomZ3.arg(0), "cf" if truth else "ct", truth
        atomZ3 = unreify[atomZ3] if atomZ3 in unreify else atomZ3
        key = json.dumps([atom_as_string(atomZ3)])
        typ = atomZ3.sort().name()
        for symb in case.symbols_of(atomZ3).keys():
            s = self.m.setdefault(symb, {})
            if key in s:
                if typ == 'Bool':
                    s[key][sgn] = True
                elif typ in ["Real", "Int"] :
                    s[key]["typ"] = ""
                    s[key]["value"] = str(eval(str(value))) # compute fraction


def atom_as_string(expr):
    if hasattr(expr, 'atom_string'): return expr.atom_string
    return str(expr).replace("==", "=").replace("!=", "~=").replace("<=", "=<")

def string_as_atom(string):
    return str(string).replace("=", "==").replace("~=", "!=").replace("=<", "<=")