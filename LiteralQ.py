
from z3 import *

class LiteralQ(object):
    def __init__(self, truth, atomZ3):
        self.truth = truth
        self.atomZ3 = atomZ3

    def __hash__(self):
        return hash((self.truth, str(self.atomZ3)))

    def __eq__(self, other):
        return self.truth == other.truth and str(self.atomZ3) == str(other.atomZ3)

    def __repr__(self):
        return str(self.truth) + (self.atomZ3.reading if hasattr(self.atomZ3, 'reading') else str(self.atomZ3))


    def __str__(self):
        return ("" if self.truth else "? " if self.truth is None else "Not ") \
             + (self.atomZ3.reading if hasattr(self.atomZ3, 'reading') \
                 else self.atomZ3.atom_string if hasattr(self.atomZ3, 'atom_string') \
                 else str(self.atomZ3))

    def to_json(self): return str(self)

    def asZ3(self):
        return self.atomZ3 if self.truth else Not(self.atomZ3)