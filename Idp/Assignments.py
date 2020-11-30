"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""

Classes to represent assignments of values to expressions

"""

from copy import copy
from enum import Enum, auto
from typing import Optional
from z3 import Not, BoolRef

from .Expression import Expression, TRUE, FALSE, AUnary, AComparison, \
                        AppliedSymbol
from .Parse import *

class Status(Enum):
    UNKNOWN     = auto()
    GIVEN       = auto()
    ENV_UNIV    = auto()
    UNIVERSAL   = auto()
    ENV_CONSQ   = auto()
    CONSEQUENCE = auto()
    EXPANDED    = auto()
    STRUCTURE   = auto()
    DEFAULT = auto()

class Assignment(object):
    def __init__(self, sentence: Expression, value: Optional[Expression], 
                       status: Status, relevant:bool=False):
        self.sentence = sentence
        self.value = value
        self.status = status
        self.relevant = relevant

        # first symbol in the sentence that does not start with '_'
        self.symbol_decl = None
        self.symbols = sentence.unknown_symbols(co_constraints=False).values()
        for d in self.symbols:
            if not d.name.startswith('_'):
                self.symbol_decl = d
                break

    def copy(self):
        out = copy(self)
        out.sentence = out.sentence.copy()
        return out

    def __str__(self):
        pre, post = '', ''
        if self.value is None:
            pre = f"? "
        elif self.value.same_as(TRUE):
            pre = ""
        elif self.value.same_as(FALSE):
            pre = f"Not "
        else:
            post = f" -> {str(self.value)}"
        return f"{pre}{self.sentence.annotations['reading']}{post}"

    def __log__(self):
        return self.value

    def to_json(self) -> str: # for GUI
        return str(self)

    def formula(self):
        if self.value is None:
            raise Exception("can't translate unknown value")
        if self.sentence.type == 'bool':
            out = self.sentence.original if self.value.same_as(TRUE) else \
                AUnary.make('¬', self.sentence.original)
        else:
            out = AComparison.make('=', [self.sentence.original, self.value])
        return out

    def translate(self) -> BoolRef:
        return self.formula().translate()

class Assignments(dict):
    def __init__(self,*arg,**kw):
        super(Assignments, self).__init__(*arg, **kw)
        self.symbols = {} # { decl.name: decl }
        for a in self.values():
            if a.symbol_decl:
                self.symbols[a.symbol_decl.name] = a.symbol_decl

    def copy(self):
        return Assignments({k: v.copy() for k,v in self.items()})

    def extend(self, more):
        for v in more.values():
            self.assert_(v.sentence, v.value, v.status, v.relevant)

    def assert_(self, sentence: Expression,
                value: Optional[Expression],
                status: Optional[Status],
                relevant: Optional[bool]):
        sentence = sentence.copy()
        if sentence.code in self:
            out = copy(self[sentence.code])  # needed for explain of irrelevant symbols
            # don't overwrite
            if out.value is None:
                out.value = value
            else:
                pass  # issue #35 error will be caught later by Z3
            if out.status is None or out.status == Status.UNKNOWN:
                out.status = status
            if relevant is not None:
                out.relevant = relevant
        else:
            out = Assignment(sentence, value, status, relevant)
            if out.symbol_decl:
                self.symbols[out.symbol_decl.name] = out.symbol_decl
        self[sentence.code] = out
        return out

    def __str__(self):
        out = {}
        for a in self.values():
            if a.value is not None and not a.sentence.is_reified():
                c = ",".join(str(e) for e in a.sentence.sub_exprs)
                c = f"({c})" if c else c 
                c = f"{c}->{str(a.value)}"
                out[a.symbol_decl.name] = out.get(a.symbol_decl.name, []) + [c]
        return NEWL.join(f"{k}:={{{ '; '.join(s for s in a) }}}"
                         for k, a in out.items())
