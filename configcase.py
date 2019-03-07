import ast

from z3 import *
import json

from utils import universe


class ConfigCase:

    def __init__(self, theory):
        self.relevantVals = {}
        self.symbols = []
        self.solver = Solver()
        theory(self)
        self.assumptions = []

    def relevantValsOf(self, var):
        stored_rels = self.relevantVals.get(var)
        if stored_rels:
            return stored_rels
        else:
            return universe(var.sort())

    def model(self):
        self.solver.check(self.list_of_assumptions())
        return self.solver.model()

    def json_model(self):
        return self.model_to_json(self.model())

    def model_to_json(self, m):
        output = {}
        for symb in self.symbols:
            val = m[symb]
            output[obj_to_string(symb)] = obj_to_string(val)
        return json.dumps(output)

    def list_of_propositions(self):
        return [sym == val for sym in self.symbols for val in self.relevantValsOf(sym)]

    def initialisationlist(self):
        out = {}
        for sym in self.symbols:
            out[str(sym)] = [[str(x)] for x in self.relevantValsOf(sym)]  # SINGLETON ALERT
        return out

    def list_of_assumptions(self):
        return self.assumptions

    def consequences(self):
        satresult, consqs = self.solver.consequences(self.list_of_assumptions(), self.list_of_propositions())
        print(consqs)
        return [extractInfoFromConsequence(s) for s in consqs]

    def outputstructure(self):
        out = Structure()
        for s in self.symbols:
            for v in self.relevantValsOf(s):
                out.initialise(s, v)
        return out

    def propagation(self):
        out = self.outputstructure()
        for ass, csq in self.consequences():
            out.addComparison(csq)
        return out.m

    def as_symbol(self, symbStr):
        return [sym for sym in self.symbols if str(sym) == symbStr][0]  # SINGLETON ALERT

    def loadStructure(self, assumptions):
        self.assumptions = assumptions

    def loadStructureFromJson(self, jsonstr):
        self.loadStructure(self.structureFromJson(jsonstr))

    def structureFromJson(self, json_data):
        json_data = ast.literal_eval(json_data)
        # obj = json.loads(json_data)
        return self.structureFromObject(json_data)

    # Structure: symbol -> value -> {ct,cf} -> true/false
    def structureFromObject(self, object):
        return [Comparison(sign == "ct", self.as_symbol(sym), json.loads(val)[0]).asAST()
                for sym in object
                for val in object[sym]
                for sign in {"ct", "cf"}
                if object[sym][val][sign]]


class Comparison:
    def __init__(self, sign, symbol, value):
        self.sign = sign
        self.symbol = symbol
        self.value = value

    def __repr__(self) -> str:
        return str((self.sign, self.symbol, self.value))

    def asAST(self):
        val = self.value
        if val == "True":
            val = True
        if self.sign:
            return self.symbol == val
        else:
            return self.symbol != val

    def symbName(self):
        return str(self.symbol)

    def valName(self):  # SINGLETON ALERT
        if type(self.value) in [str, int, float]:
            return json.dumps([str(self.value)])
        return json.dumps([obj_to_string(self.value)])


def extractInfoFromConsequence(s):
    assumptionE = s.children()[0]
    assumptions = []
    if is_true(assumptionE):
        pass
    elif is_and(assumptionE):
        assumptions = [extractInfoFromComparison(c) for c in assumptionE.children()]
    else:
        assumptions = [extractInfoFromComparison(assumptionE)]

    consequence = s.children()[1]
    comp = extractInfoFromComparison(consequence)
    return assumptions, comp


def extractInfoFromComparison(c):
    sign = not is_not(c)
    if not sign:
        c = c.children()[0]
    if not is_eq(c):
        sign = not sign
    arr = c.children()
    value, symbol = sorted(arr, key=lambda x: str(x))
    return Comparison(sign, symbol, value)


class Structure:
    def __init__(self):
        self.m = {}

    def getJSON(self):
        return json.dumps(self.m)

    def initialise(self, symbol, value):
        comp = Comparison(True, symbol, value)
        if comp.symbName() not in self.m:
            self.m[comp.symbName()] = {}
        if comp.valName() not in self.m[comp.symbName()]:
            self.m[comp.symbName()][comp.valName()] = {"ct": False, "cf": False}

    def addComparison(self, comp: Comparison):
        signstr = "cf"
        if comp.sign:
            signstr = "ct"

        # print(comp.symbName())
        # print(comp.valName())
        # print(self.m)
        # print(self.m[comp.symbName()])
        self.m[comp.symbName()][comp.valName()][signstr] = True
