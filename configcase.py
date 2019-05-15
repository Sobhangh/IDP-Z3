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
        theory(self)

    #################
    # BUILDER FUNCTIONS
    #################

    def IntsInRange(self, txt: str, underbound: Int, upperbound: Int):
        int_consts = Ints(txt) # an unknown constant function of type int
        values = list(map(singleton, map(_py2expr, range(underbound, upperbound + 1))))
        for int_const in int_consts:
            self.relevantVals[int_const] = values
            self.typeConstraints.append(underbound <= int_const)
            self.typeConstraints.append(int_const <= upperbound)
            self.symbols.append(int_const)
        return int_consts

    def Reals(self, txt: str, rang: List[float], restrictive=False):
        real_consts = Reals(txt)
        values: List[ArithRef] = list(map(_py2expr, rang))
        for real_const in real_consts:
            self.symbols.append(real_const)
            self.relevantVals[real_const] = list(map(singleton, values))
            if restrictive:
                self.typeConstraints.append(in_list(real_const, values))
        return real_consts

    def Bools(self, txt: str):
        bool_consts = Bools(txt)
        for bool_const in bool_consts:
            self.symbols.append(bool_const)
        return bool_consts

    def Consts(self, txt: str, sort):
        consts = Consts(txt, sort)
        for const in consts:
            self.symbols.append(const)
        return consts

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

    #################
    # UTILITIES
    #################

    def add(self, constraint):
        self.constraints.append(constraint)

    def mk_solver(self):
        s = Solver()
        s.add(self.constraints)
        s.add(self.typeConstraints)
        return s

    def model(self):
        solver = self.mk_solver()
        solver.add(self.assumptions)
        solver.check()
        return solver.model()

    def model_to_json(self, m):
        out = Structure(self)
        for atomZ3 in self.atoms().values():
            if m.eval(atomZ3, model_completion=True): # 'if' needed to avoid BoolRef not JSONable
                out.initialise(self, atomZ3, False, True)
            else:
                out.initialise(self, atomZ3, True, False)
        return out.m

    def atoms(self): # get the ordered set of atoms in the constraints
        def getAtoms(expr):
            out = {}  # Ordered dict: string -> Z3 object
            for child in expr.children():
                out.update(getAtoms(child))
            if expr.sort().name() == 'Bool' and len(out) == 0:
                if not any([is_var(child) for child in expr.children()]):
                    out = {atom_as_string(expr): expr}
            return out

        atoms = {}
        for constraint in self.constraints:
            atoms.update(getAtoms(constraint))
        return atoms

    def outputstructure(self, all_false=False, all_true=False):
        out = Structure(self)
        for atomZ3 in self.atoms().values():
            out.initialise(self, atomZ3, all_false, all_true)
        return out

    def as_symbol(self, symb_str):
        #print(symb_str)
        return list(filter(lambda s: str(s)==symb_str, self.symbols)) [0]

    # Structure: symbol -> atom -> {ct,cf} -> true/false
    def loadStructureFromJson(self, jsonstr):
        atoms = self.atoms()
        json_data = ast.literal_eval(jsonstr)
        self.assumptions = []
        for sym in json_data:
            for atom in json_data[sym]:
                atomZ3 = atoms[atom[2:-2]]
                if json_data[sym][atom]["ct"]:
                    self.assumptions.append(atomZ3)
                if json_data[sym][atom]["cf"]:
                    self.assumptions.append(Not(atomZ3))

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
        out = self.outputstructure()

        solver = Solver()
        theo1 = And(self.constraints)
        solver.add(self.typeConstraints + self.assumptions)

        for s in self.symbols:
            solver.push()
            if type(s) == FuncDeclRef:
                type_list = [s.domain(i) for i in range(0, s.arity())] + [s.range()]
                c = Function("temporaryFunction", type_list)

                constants = [Const('ci', s.domain(i)) for i in range(0, s.arity())]
                arg_fill = [Const('ci2', s.domain(i)) for i in range(0, s.arity())]
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
        solver = self.mk_solver()
        to_explain = self.atoms()[value[2:-2]] # value is an atom string
        _, consqs = solver.consequences(self.assumptions, [to_explain])

        out = Structure(self)
        for cons in consqs:
            assumption_expr = cons.children()[0]
            if is_true(assumption_expr):
                pass
            elif is_and(assumption_expr):
                for c in assumption_expr.children():
                     out.addAtom(self, c)
            else:
                out.addAtom(self, assumption_expr)
        return out.m

    def optimize(self, symbol, minimize):
        solver = Optimize()
        solver.add(self.constraints)
        solver.add(self.typeConstraints)
        s = self.as_symbol(symbol)
        if minimize:
            solver.minimize(s)
        else:
            solver.maximize(s)

        for assumption in self.assumptions:
            solver.add(assumption)
        solver.check()
        return self.model_to_json(solver.model())

    def propagation(self):
        solver = self.mk_solver()
        solver.add(self.assumptions)
        proplist = list(self.atoms().values())
        _, consqs = solver.consequences([], proplist)
        out = self.outputstructure()
        for s in consqs:
            out.addAtom(self, s.children()[1]) # take the consequence
        return out.m

    def atomsGrouped(self):
        #solver = self.mk_solver()
        #solver.add(self.assumptions)
        out = {} # {symbol_string : [atom_string, "?"]}
        for atom_string, atomZ3 in self.atoms().items():
            for groupBy in self.symbols_of(atomZ3):
                d = out.setdefault(groupBy, [])
                #if "[]" not in d and type(self.as_symbol(groupBy)) != BoolRef:
                #    d.append("[]")
                d.append(json.dumps([atom_string]))
        return out

    def symbols_of(self, expr):
        if (obj_to_string(expr) in self.valueMap) or is_number(obj_to_string(expr)) \
        or is_true(expr) or is_false(expr):
            return [] # a literal value
        name = expr.decl().name()
        if name in ['not', '<=', '>=', 'distinct', '=', '<', '>', '+', '-', '*', '/']:
            out = []
            for child in expr.children():
                out.extend(self.symbols_of(child))
            return out
        else:
            return [name]
            #return [obj_to_string(expr)]

    def first_symbol(self, expr):
        symbs = self.symbols_of(expr)
        return symbs[0] if symbs != [] else None


    def parametric(self):
        solver = self.mk_solver()
        solver.add(self.assumptions)
        models, count = {}, 0

        # create keys for models using first symbol of atoms
        for atomZ3 in self.atoms().values():
            for symb in self.symbols_of(atomZ3):
                models[symb] = []

        while solver.check() == sat: # for each parametric model
            #for symb in self.symbols:
            #    print (symb, solver.model().eval(symb))

            atoms = [] # [(atom_string, atomZ3)]
            for atom_string, atomZ3 in self.atoms().items():
                truth = solver.model().eval(atomZ3)
                if truth == True:
                    atoms += [ (atom_string, atomZ3) ]
                elif truth == False:
                    atoms += [ ("Not " + atom_string, Not(atomZ3) ) ]
                else: # undefined
                    atoms += [ ("? " + atom_string, BoolVal(True)) ]
                # models.setdefault(groupBy, [[]] * count) # create keys for models using first symbol of atoms

            # check if atoms are relevant
            # atoms1 = atoms
            # for current, (atom_string, atomZ3) in enumerate(atoms):
            #     print("step 1")
            #     solver.push()
            #     alternative = And([ Not(a) if j==current else a for j, (_,a) in enumerate(atoms1) ])
            #     print("step 2")
            #     solver.add(alternative)
            #     print("step 3")
            #     if solver.check() == sat: # atom can be true or false !
            #         print( "Dropping: ", atom_string)
            #         atoms[current] = ("? " + atom_string, True)
            #     solver.pop()

            # add constraint to eliminate this model
            modelZ3 = And( [atomZ3 for (_, atomZ3) in atoms] )
            solver.add(Not(modelZ3))

            # group atoms by symbols
            model = {}
            for atom_string, atomZ3 in atoms:
                for symb in self.symbols_of(atomZ3):
                    model.setdefault(symb, []).append([ atom_string ])
            # add to models
            for k,v in models.items(): # add model
                models[k] = v + [ model[k] if k in model else [] ]
            count +=1

        # build table of models
        out = [[ [k] for k in models.keys()]]
        for i in range(count):
            out += [[v[i] for v in models.values()]]
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

    def initialise(self, case, atomZ3, all_false, all_true):
        for symb in case.symbols_of(atomZ3):
            s = self.m.setdefault(symb, {})
            key = json.dumps([atom_as_string(atomZ3)])
            s.setdefault(key, {"ct": all_true, "cf": all_false})

    def addAtom(self, case, atomZ3):
        sgn = "ct"
        if is_not(atomZ3):
            atomZ3, sgn = atomZ3.arg(0), "cf"
        for symb in case.symbols_of(atomZ3):
            s = self.m.setdefault(symb, {})
            s.setdefault(json.dumps([atom_as_string(atomZ3)]), {})[sgn] = True


def atom_as_string(expr):
    return str(expr).replace("==", "=").replace("!=", "~=").replace("<=", "=<")

def string_as_atom(string):
    return str(string).replace("=", "==").replace("~=", "!=").replace("=<", "<=")