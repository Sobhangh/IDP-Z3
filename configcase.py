import ast
import json
from typing import List
from utils import universe, in_list, is_number, splitLast
from z3 import *
from z3.z3 import _py2expr


class ConfigCase:

    def __init__(self, theory):
        self.relevantVals = {}
        self.symbols = []
        self.assumptions = []
        self.valueMap = {"True": True}
        self.constraints = []
        theory(self)

    #################
    # BUILDER FUNCTIONS
    #################

    def IntsInRange(self, txt: str, underbound: Int, upperbound: Int):
        ints = Ints(txt)
        values = list(map(_py2expr, range(underbound, upperbound + 1)))
        for i in ints:
            self.relevantVals[i] = values
            self.constraints.append(underbound <= i)
            self.constraints.append(i <= upperbound)
            self.symbols.append(i)
        return ints

    def Reals(self, txt: str, rang: List[float], restrictive=False):
        reals = Reals(txt)
        values: List[ArithRef] = list(map(_py2expr, rang))
        for i in reals:
            self.symbols.append(i)
            self.relevantVals[i] = values
            if restrictive:
                self.constraints.append(in_list(i, values))
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

    #################
    # UTILITIES
    #################

    def add(self, constraint):
        self.constraints.append(constraint)

    def relevantValsOf(self, var):
        if var in self.relevantVals:
            return self.relevantVals[var]
        else:
            return universe(var.sort())

    def mk_solver(self):
        s = Solver()
        for c in self.constraints:
            s.add(c)
        return s

    def model(self):
        solver = self.mk_solver()
        solver.check(self.list_of_assumptions())
        return solver.model()

    def model_to_json(self, m):
        output = self.outputstructure(True)
        for symb in self.symbols:
            val = m[symb]
            output.addComparison(Comparison(True, symb, [], self.z3_value(val)))  # SINGLETON ALERT
        return output.m

    def list_of_propositions(self):
        return [sym == val for sym in self.symbols for val in self.relevantValsOf(sym)]

    def initialisationlist(self):
        out = {}
        for sym in self.symbols:
            out[obj_to_string(sym)] = [[obj_to_string(x)] for x in self.relevantValsOf(sym)]  # SINGLETON ALERT
        return out

    def list_of_assumptions(self):
        return self.assumptions

    def consequences(self):
        solver = self.mk_solver()
        satresult, consqs = solver.consequences(self.list_of_assumptions(), self.list_of_propositions())
        return [self.extractInfoFromConsequence(s) for s in consqs]

    def outputstructure(self, all_false=False, all_true=False):
        out = Structure()
        for symbol in self.symbols:
            for value in self.relevantValsOf(symbol):
                out.initialise(Comparison(True, symbol, [], self.z3_value(value)), all_false, all_true)
                # SINGLETON ALERT
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
        if type(symb) == str:
            return len([c for c in self.symbols if obj_to_string(c) == symb]) > 0
        if is_expr(symb):
            return len([c for c in self.symbols if obj_to_string(c) == obj_to_string(symb)]) > 0
        return False

    #################
    # INFERENCES
    #################

    def explain(self, symbol, value):
        out = self.outputstructure()
        for ass, csq in self.consequences():
            if (csq.symbName() == symbol) & (csq.graphedValue() == value):
                for a in ass:
                    out.addComparison(a)
        return out.m

    def minimize(self, symbol, minimize):
        solver = Optimize()
        for c in self.constraints:
            solver.add(c)
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
        out = self.outputstructure()
        for ass, csq in self.consequences():
            out.addComparison(csq)
        return out.m


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
