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

    def list_of_assumptions(self):
        return self.assumptions

    def consequences(self):
        satresult, consqs = self.solver.consequences(self.list_of_assumptions(), self.list_of_propositions())
        return [extractInfoFromConsequence(s) for s in consqs]

    def as_symbol(self, symbStr):
        return [sym for sym in self.symbols if str(sym) == symbStr][0]

    def loadStructure(self, assumptions):
        self.assumptions = assumptions

    def loadStructureFromJson(self, jsonstr):
        self.loadStructure(self.structureFromJson(jsonstr))

    def structureFromJson(self, jsonstr):
        obj = json.loads(jsonstr)
        return self.structureFromObject(obj)

    # Structure: symbol -> value -> {ct,cf} -> true/false
    def structureFromObject(self, object):
        return [Comparison(sign == "ct", self.as_symbol(sym), json.loads(val)).asAST()
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
        if self.sign:
            return self.symbol == self.value
        else:
            return self.symbol != self.value


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
    symbol, value = c.children()
    return Comparison(sign, symbol, value)
