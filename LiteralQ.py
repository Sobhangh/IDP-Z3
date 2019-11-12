
from z3 import *
import ast

class LiteralQ(object):
    def __init__(self, truth, subtence):
        self.truth = truth # Bool, "irrelevant", None = unknown, 
        self.subtence = subtence

    def __hash__(self):
        return hash((self.truth, str(self.subtence)))

    def __eq__(self, other):
        return self.truth == other.truth \
            and type(self.subtence) == type (other.subtence) \
            and str(self.subtence) == str(other.subtence)

    def __repr__(self):
        return str(self.truth) + ( self.subtence.reading if hasattr(self.subtence, 'reading')
                                   else str(self.subtence)
                                 )


    def __str__(self):
        if self.truth == "irrelevant":
            return ""
        return ("" if self.truth else "? " if self.truth is None else "Not ") \
             + (self.subtence.reading if hasattr(self.subtence, 'reading')
                 else str(self.subtence))

    def to_json(self): return str(self)

    def asZ3(self):
        if self.truth == "irrelevant":
            return BoolVal(True)
        return self.subtence.translated if self.truth else Not(self.subtence.translated)

class Equality(object):
    def __init__(self, subtence, value):
        self.subtence = subtence # an Expression
        self.value = value # a Z3 value
        self.str = subtence.str + " = " + str(value)
        self.type = 'bool'
        self.translated = (subtence.translated == value) #TODO

    def __str__(self): return self.str


#################
# load user's choices
# see docs/REST.md
#################

def loadStructure(idp, jsonstr):
    json_data = ast.literal_eval(jsonstr \
        .replace("\\\\u2264", "≤").replace("\\\\u2265", "≥").replace("\\\\u2260", "≠")
        .replace("\\\\u2200", "∀").replace("\\\\u2203", "∃")
        .replace("\\\\u21d2", "⇒").replace("\\\\u21d4", "⇔").replace("\\\\u21d0", "⇐")
        .replace("\\\\u2228", "∨").replace("\\\\u2227", "∧"))

    structure = {}
    for sym in json_data:
        for atom in json_data[sym]:
            json_atom = json_data[sym][atom]
            if atom in idp.theory.subtences:
                atom = idp.theory.subtences[atom]
            else:
                symbol = idp.vocabulary.symbol_decls[sym]
                atom = symbol.instances[atom]
            if json_atom["typ"] == "Bool":
                if "ct" in json_atom and json_atom["ct"]:
                    literalQ = LiteralQ(True, atom)
                if "cf" in json_atom and json_atom["cf"]:
                    literalQ = LiteralQ(False, atom)
            elif json_atom["value"]:
                if json_atom["typ"] in ["Int", "Real"]:
                    value = eval(json_atom["value"])
                else:
                    value = idp.vocabulary.symbol_decls[json_atom["value"]].translated
                literalQ = LiteralQ(True, Equality(atom, value))
            else:
                literalQ = None #TODO error ?
            if literalQ is not None:
                structure[literalQ] = literalQ.asZ3()
    return structure