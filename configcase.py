import ast
from typing import List

from z3 import *
import json

from z3.z3 import _py2expr

from utils import universe, in_list, is_number


class ConfigCase:

    def __init__(self, theory, solver=Solver()):
        self.relevantVals = {}
        self.symbols = []
        self.solver = solver
        self.assumptions = []
        self.valueMap = {"True": True}
        theory(self)

    def relevantValsOf(self, var):
        if var in self.relevantVals:
            return self.relevantVals[var]
        else:
            return universe(var.sort())

    def model(self):
        self.solver.check(self.list_of_assumptions())
        return self.solver.model()

    def json_model(self):
        return self.model_to_json(self.model())

    def model_to_json(self, m):
        output = self.outputstructure(True)
        for symb in self.symbols:
            val = m[symb]
            output.addComparison(Comparison(True, symb, self.z3_value(val)))
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
        satresult, consqs = self.solver.consequences(self.list_of_assumptions(), self.list_of_propositions())
        return [self.extractInfoFromConsequence(s) for s in consqs]

    def outputstructure(self, all_false=False, all_true=False):
        out = Structure()
        for symbol in self.symbols:
            for value in self.relevantValsOf(symbol):
                out.initialise(Comparison(True, symbol, self.z3_value(value)), all_false, all_true)
        return out

    def propagation(self):
        out = self.outputstructure()
        for ass, csq in self.consequences():
            out.addComparison(csq)
        return out.m

    def as_symbol(self, symb_str):
        return [sym for sym in self.symbols if str(sym) == symb_str][0]  # SINGLETON ALERT

    def loadStructure(self, assumptions):
        self.assumptions = assumptions

    def loadStructureFromJson(self, jsonstr):
        self.loadStructure(self.structureFromJson(jsonstr))

    def structureFromJson(self, json_data):
        json_data = ast.literal_eval(json_data)
        return self.structureFromObject(json_data)

    # Structure: symbol -> value -> {ct,cf} -> true/false
    def structureFromObject(self, obj):
        return [Comparison(sign == "ct", self.as_symbol(sym), self.z3_value(json.loads(val)[0])).asAST()
                for sym in obj
                for val in obj[sym]
                for sign in {"ct", "cf"}
                if obj[sym][val][sign]]

    def IntsInRange(self, txt: str, underbound: Int, upperbound: Int):
        ints = Ints(txt)
        values = list(map(_py2expr, range(underbound, upperbound + 1)))
        for i in ints:
            self.relevantVals[i] = values
            self.solver.add(underbound <= i)
            self.solver.add(i <= upperbound)
            self.symbols.append(i)
        return ints

    def Reals(self, txt: str, rang: List[float], restrictive=False):
        reals = Reals(txt)
        values: List[ArithRef] = list(map(_py2expr, rang))
        for i in reals:
            self.symbols.append(i)
            self.relevantVals[i] = values
            if restrictive:
                self.solver.add(in_list(i, values))
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

    def explain(self, symbol, value):
        out = self.outputstructure()
        for ass, csq in self.consequences():
            print(ass, csq)
            if (csq.symbName() == symbol) & (csq.valName() == value):
                for a in ass:
                    out.addComparison(a)
        return out.m

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
        if (obj_to_string(symbol) in self.valueMap) | is_number(obj_to_string(symbol)):
            temp = symbol
            symbol = value
            value = temp
        return Comparison(sign, symbol, self.z3_value(value))

    def z3_value(self, value):
        if value in self.valueMap:
            return self.valueMap[value]
        else:
            return value

    def minimize(self, symbol, minimize):
        s = self.as_symbol(symbol)
        if minimize:
            self.solver.minimize(s)
        else:
            self.solver.maximize(s)
            
        for assumption in self.list_of_assumptions():
            self.solver.add(assumption)
        self.solver.check()
        return self.model_to_json(self.solver.model())


class Comparison:
    def __init__(self, sign, symbol, value):
        self.sign = sign
        self.symbol = symbol
        self.value = value

    def __repr__(self) -> str:
        return str((self.sign, self.symbol, self.value))

    def asAST(self):
        val = self.value
        if self.sign:
            return self.symbol == val
        else:
            return self.symbol != val

    def symbName(self):
        return obj_to_string(self.symbol)

    def valName(self):  # SINGLETON ALERT
        if type(self.value) in [str, int, float]:
            return json.dumps([str(self.value)])
        return json.dumps([obj_to_string(self.value)])


class Structure:
    def __init__(self):
        self.m = {}

    def getJSON(self):
        return json.dumps(self.m)

    def initialise(self, comp, all_false, all_true):
        self.m.setdefault(comp.symbName(), {}).setdefault(comp.valName(), {"ct": all_true, "cf": all_false})

    def addComparison(self, comp: Comparison):
        signstr = "cf"
        if comp.sign:
            signstr = "ct"
        self.m.setdefault(comp.symbName(), {}).setdefault(comp.valName(), {})[signstr] = True
