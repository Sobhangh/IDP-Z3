import ast
import json
import time
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
        ints = Ints(txt)
        values = list(map(singleton, map(_py2expr, range(underbound, upperbound + 1))))
        for i in ints:
            self.relevantVals[i] = values
            self.typeConstraints.append(underbound <= i)
            self.typeConstraints.append(i <= upperbound)
            self.symbols.append(i)
        return ints

    def Reals(self, txt: str, rang: List[float], restrictive=False):
        reals = Reals(txt)
        values: List[ArithRef] = list(map(_py2expr, rang))
        for i in reals:
            self.symbols.append(i)
            self.relevantVals[i] = list(map(singleton, values))
            if restrictive:
                self.typeConstraints.append(in_list(i, values))
        return reals

    def Bools(self, txt: str):
        bools = Bools(txt)
        for i in bools:
            self.symbols.append(i)
        return bools

    def Consts(self, txt: str, sort):
        out = Consts(txt, sort)
        for i in out:
            self.symbols.append(i)
        return out

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

    def relevantValsOf(self, var):
        if var in self.relevantVals:
            return self.relevantVals[var]
        else:
            return list(map(singleton, universe(var.sort())))

    def mk_solver(self):
        s = Solver()
        s.add(self.constraints)
        s.add(self.typeConstraints)
        return s

    def model(self):
        solver = self.mk_solver()
        solver.add(self.list_of_assumptions())
        solver.check()
        return solver.model()

    def model_to_json(self, m):
        output = self.outputstructure(True)
        for symb in self.symbols:
            for args, val in self.relevantValsOf(symb):
                val = m.eval(applyTo(symb, args))
                output.addComparison(Comparison(True, symb, args, val))
        return output.m

    def list_of_propositions(self):
        out = []
        for sym in self.symbols:
            for arg, val in self.relevantValsOf(sym):
                out.append(applyTo(sym, arg) == val)
        return out

    def list_of_assumptions(self):
        return self.assumptions

    def outputstructure(self, all_false=False, all_true=False):
        out = Structure()
        for symbol in self.symbols:
            for args, value in self.relevantValsOf(symbol):
                out.initialise(Comparison(True, symbol, list(map(self.z3_value, args)), self.z3_value(value)),
                               all_false, all_true)
        return out

    def as_symbol(self, symb_str):
        return [sym for sym in self.symbols if str(sym) == symb_str][0]

    def loadStructure(self, assumptions):
        self.assumptions = assumptions

    def loadStructureFromJson(self, jsonstr):
        self.loadStructure(self.structureFromJson(jsonstr))

    def structureFromJson(self, json_data):
        json_data = ast.literal_eval(json_data)
        return self.structureFromObject(json_data)

    def args(self, val):
        a, l = splitLast(list(map(self.z3_value, json.loads(val))))
        return a

    def outVal(self, val):
        a, l = splitLast(list(map(self.z3_value, json.loads(val))))
        return l

    # Structure: symbol -> value -> {ct,cf} -> true/false
    def structureFromObject(self, obj):
        return [Comparison(sign == "ct", self.as_symbol(sym), self.args(val), self.outVal(val)).asAST()
                for sym in obj
                for val in obj[sym]
                for sign in {"ct", "cf"}
                if obj[sym][val][sign]]

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
        out = {"title": "Z3 Interactive Configuration", "timeout": 3, "symbols": symbols, "values": []}
        return out

    def extractInfoFromConsequence(self, s):
        assumption_expr = s.children()[0]
        assumptions = []
        if is_true(assumption_expr):
            pass
        elif is_and(assumption_expr):
            assumptions = [self.extractInfoFromComparison(c) for c in assumption_expr.children()]
        else:
            assumptions = [self.extractInfoFromComparison(assumption_expr)]
        consequence = s.children()[1]
        comp = self.extractInfoFromComparison(consequence)
        return assumptions, comp

    def extractInfoFromComparison(self, c):
        sign = not is_not(c)
        if not sign:
            c = c.children()[0]
        if not is_eq(c):
            sign = not sign
        value, symbol = c.children()
        if (obj_to_string(symbol) in self.valueMap) | is_number(obj_to_string(symbol)) | \
                self.is_symbol(value):
            temp = symbol
            symbol = value
            value = temp
        args = []
        if isinstance(symbol, ExprRef):
            args = symbol.children()
            symbol = symbol.decl()
        return Comparison(sign, symbol, args, self.z3_value(value))

    def z3_value(self, value):
        if value in self.valueMap:
            return self.valueMap[value]
        else:
            return value

    def is_symbol(self, symb):
        if is_expr(symb):
            symb = obj_to_string(symb)
        for c in self.symbols:
            if obj_to_string(c) == symb:
                return True
        return False

    #################
    # INFERENCES
    #################

    def brelevance(self):
        g = Goal()
        g.add(self.constraints)
        g.add(self.assumptions)
        simplified = Tactic('ctx-solver-simplify')(g)[0]
        total = []
        for i in simplified:
            total += flattenexpr(i, self.symbols)
        total = list(set(total))

        out = self.outputstructure()
        for i in total:
            out.fillApp(i)
        return out.m

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
            for arg, val in self.relevantValsOf(s):
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
        arg, l = splitLast(json.loads(value))
        arg = list(map(self.z3_value, arg))
        to_explain = [applyTo(self.as_symbol(symbol), arg) == self.z3_value(l)]
        satresult, consqs = solver.consequences(self.assumptions, to_explain)

        out = self.outputstructure()
        for cons in consqs:
            ass, csq = self.extractInfoFromConsequence(cons)
            for a in ass:
                out.addComparison(a)
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

        for assumption in self.list_of_assumptions():
            solver.add(assumption)
        solver.check()
        return self.model_to_json(solver.model())

    def json_model(self):
        return self.model_to_json(self.model())

    def propagation(self):
        solver = self.mk_solver()
        solver.add(self.assumptions)
        satresult, consqs = solver.consequences([], self.list_of_propositions())
        out = self.outputstructure()
        for consequence in consqs:
            ass, csq = self.extractInfoFromConsequence(consequence)
            out.addComparison(csq)
        return out.m

    def initialisationlist(self):
        out = {}
        for sym in self.symbols:
            ls = []
            for arg, val in self.relevantValsOf(sym):
                ls.append(json.dumps(list(map(obj_to_string, list(arg) + [val]))))
            out[obj_to_string(sym)] = ls
        return out


class Comparison:
    def __init__(self, sign: bool, symbol, args: List, value):
        self.sign = sign
        self.symbol = symbol
        self.args = args
        self.value = value

    def __repr__(self) -> str:
        return str((self.sign, self.symbol, self.args, self.value))

    def astSymb(self):
        if len(self.args) == 0:
            return self.symbol
        return self.symbol(self.args)

    def asAST(self):
        val = self.value
        if self.sign:
            return self.astSymb() == val
        else:
            return self.astSymb() != val

    def symbName(self):
        return obj_to_string(self.symbol)

    def graphedValue(self):
        strVal = self.value
        if type(self.value) in [str, int, float]:
            strVal = str(self.value)
        else:
            strVal = obj_to_string(strVal)
        lst = [obj_to_string(x) for x in self.args]
        lst.append(strVal)
        return json.dumps(lst)


class Structure:
    def __init__(self):
        self.m = {}

    def getJSON(self):
        return json.dumps(self.m)

    def initialise(self, comp, all_false, all_true):
        self.m.setdefault(comp.symbName(), {}).setdefault(comp.graphedValue(), {"ct": all_true, "cf": all_false})

    def addComparison(self, comp: Comparison):
        signstr = "cf"
        if comp.sign:
            signstr = "ct"
        self.m.setdefault(comp.symbName(), {}).setdefault(comp.graphedValue(), {})[signstr] = True

    def fillSymbol(self, s):
        map = self.m[obj_to_string(s)]
        for i in self.m[obj_to_string(s)]:
            map[i]['ct'] = True
            map[i]['cf'] = True

    def fillApp(self, s):
        if not is_app(s):
            self.fillSymbol(s)
            return
        func = obj_to_string(s.decl())
        args = [obj_to_string(x) for x in s.children()]
        found = False
        for fargs in self.m[func]:
            argp, l = splitLast(json.loads(fargs))
            if argp == args:
                self.m[func][fargs]['ct'] = True
                self.m[func][fargs]['cf'] = True
                found = True
        if not found:
            self.fillSymbol(s.decl())
