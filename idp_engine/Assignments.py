# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""

Classes to store assignments of values to questions

"""
__all__ = ["Status", "Assignment", "Assignments"]

from copy import copy
from enum import Enum, auto
from typing import Optional
from z3 import BoolRef

from .Expression import Expression, TRUE, FALSE, AUnary, AComparison
from .utils import NEWL, BOOL


class Status(Enum):
    """Describes how the value of a question was obtained"""
    UNKNOWN = auto()
    GIVEN = auto()
    ENV_UNIV = auto()
    UNIVERSAL = auto()
    ENV_CONSQ = auto()
    CONSEQUENCE = auto()
    EXPANDED = auto()
    STRUCTURE = auto()


class Assignment(object):
    """Represent the assignment of a value to a question.
    Questions can be:

    * predicates and functions applied to arguments,
    * comparisons,
    * outermost quantified expressions

    A value is a rigid term.

    An assignment also has a reference to the symbol under which it should be
    displayed.

    Attributes:
        sentence (Expression): the question to be assigned a value

        value (Expression, optional): a rigid term

        status (Status, optional): qualifies how the value was obtained

        relevant (bool, optional): states whether the sentence is relevant

        symbol_decl (SymbolDeclaration): declaration of the symbol under which
        it should be displayed.
    """
    def __init__(self, sentence: Expression, value: Optional[Expression],
                 status: Optional[Status],
                 relevant: Optional[bool] = False):
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
            pre = "? "
        elif self.value.same_as(TRUE):
            pre = ""
        elif self.value.same_as(FALSE):
            pre = "Not "
        else:
            post = f" -> {str(self.value)}"
        return f"{pre}{self.sentence.annotations['reading']}{post}"

    def __repr__(self):
        return self.__str__()

    def __log__(self):
        return self.value

    def same_as(self, other:"Assignment") -> bool:
        """returns True if self has the same sentence and truth value as other.

        Args:
            other (Assignment): an assignment

        Returns:
            bool: True if self has the same sentence and truth value as other.
        """
        return (self.sentence.same_as(other.sentence)
                and ((self.value is None and other.value is None)
                     or (self.value is not None and other.value is not None
                         and self.value.same_as(other.value))))

    def to_json(self) -> str:  # for GUI
        return str(self)

    def formula(self):
        if self.value is None:
            raise Exception("can't translate unknown value")
        if self.sentence.type == BOOL:
            out = self.sentence if self.value.same_as(TRUE) else \
                AUnary.make('¬', self.sentence)
        else:
            out = AComparison.make('=', [self.sentence, self.value])
        return out

    def negate(self):
        """returns an Assignment for the same sentence, but an opposite truth value.

        Raises:
            AssertionError: Cannot negate a non-boolean assignment

        Returns:
            [type]: returns an Assignment for the same sentence, but an opposite truth value.
        """
        assert self.sentence.type == BOOL, "Cannot negate a non-boolean assignment"
        value = FALSE if self.value.same_as(TRUE) else TRUE
        return Assignment(self.sentence, value, self.status, self.relevant)

    def translate(self) -> BoolRef:
        return self.formula().translate()

    def as_set_condition(self):
        """returns an equivalent set condition, or None

        Returns:
            Tuple[Optional[AppliedSymbol], Optional[bool], Optional[Enumeration]]: meaning "appSymb is (not) in enumeration"
        """
        (x, y, z) = self.sentence.as_set_condition()
        if x:
            return (x, y if self.value.same_as(TRUE) else not y, z)
        return (None, None, None)

    def unset(self):
        """ Unsets the value of an assignment.

        Returns:
            None
        """
        self.value = None
        self.status = Status.UNKNOWN

class Assignments(dict):
    """Contains a set of Assignment"""
    def __init__(self, *arg, **kw):
        super(Assignments, self).__init__(*arg, **kw)
        self.symbols = {}  # { decl.name: decl }
        for a in self.values():
            if a.symbol_decl:
                self.symbols[a.symbol_decl.name] = a.symbol_decl

    def copy(self):
        return Assignments({k: v.copy() for k, v in self.items()})

    def extend(self, more):
        for v in more.values():
            self.assert_(v.sentence, v.value, v.status, v.relevant)

    def assert_(self, sentence: Expression,
                value: Optional[Expression],
                status: Optional[Status],
                relevant: Optional[bool]):
        sentence = sentence.copy()
        if sentence.code in self:
            # needed for explain of irrelevant symbols
            out = copy(self[sentence.code])
            out.value = value
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
