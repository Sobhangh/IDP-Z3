
from z3 import *

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
                 else self.subtence.atom_string if hasattr(self.subtence, 'atom_string')
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
        self.type = 'Bool'
        self.translated = (subtence.translated == value) #TODO

    def __str__(self): return self.str