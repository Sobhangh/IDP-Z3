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
Methods to simplify an expression using a set of assignments.

"""
from __future__ import annotations

from copy import copy, deepcopy
from itertools import product
from typing import Dict, List, Callable

from .Assignments import Status as S
from .Parse import (Import, TypeDeclaration, SymbolDeclaration,
    SymbolInterpretation, FunctionEnum, Enumeration, TupleIDP, ConstructedFrom,
    Definition, Rule)
from .Expression import (catch_error, RecDef, Symbol, SYMBOL, AIfExpr, IF, SymbolExpr, Expression, Constructor,
    AQuantification, Type, FORALL, IMPLIES, AND, AAggregate, AImplication, AConjunction,
    EQUIV, EQUALS, OR, AppliedSymbol, UnappliedSymbol, Quantee,
    Variable, VARIABLE, TRUE, FALSE, Number, ZERO, Extension)
from .Theory import Theory
from .utils import (BOOL, INT, RESERVED_SYMBOLS, CONCEPT, OrderedSet, DEFAULT,
                    GOAL_SYMBOL, EXPAND, CO_CONSTR_RECURSION_DEPTH, Semantics)


# class Expression  ###########################################################

# @log  # decorator patched in by tests/main.py
@catch_error
def substitute(self, e0, e1, assignments, tag=None):
    """ recursively substitute e0 by e1 in self (e0 is not a Variable)

    if tag is present, updates assignments with symbolic propagation of co-constraints.

    implementation for everything but AppliedSymbol, UnappliedSymbol and
    Fresh_variable
    """
    assert not isinstance(e0, Variable) or isinstance(e1, Variable), \
               f"Internal error in substitute {e0} by {e1}" # should use interpret instead
    assert self.co_constraint is None,  \
               f"Internal error in substitue: {self.co_constraint}" # see AppliedSymbol instead

    # similar code in AppliedSymbol !
    if self.code == e0.code:
        if self.code == e1.code:
            return self  # to avoid infinite loops
        return e1  # e1 is UnappliedSymbol or Number
    else:
        out = self.update_exprs(e.substitute(e0, e1, assignments, tag)
                                for e in self.sub_exprs)
        return out
Expression.substitute = substitute


# Class AppliedSymbol  ##############################################

# @log_calls  # decorator patched in by tests/main.py
@catch_error
def substitute(self, e0, e1, assignments, tag=None):
    """ recursively substitute e0 by e1 in self """

    assert not isinstance(e0, Variable) or isinstance(e1, Variable), \
        f"should use 'interpret instead of 'substitute for {e0}->{e1}"

    new_branch = None
    if self.co_constraint is not None:
        new_branch = self.co_constraint.substitute(e0, e1, assignments, tag)
        if tag is not None:
            new_branch.symbolic_propagate(assignments, tag)

    if self.as_disjunction is not None:
        self.as_disjunction = self.as_disjunction.substitute(e0, e1,        assignments, tag)
        if tag is not None:
            self.as_disjunction.symbolic_propagate(assignments, tag)

    if self.code == e0.code:
        return e1
    else:
        sub_exprs = [e.substitute(e0, e1, assignments, tag)
                     for e in self.sub_exprs]  # no simplification here
        return self._change(sub_exprs=sub_exprs, co_constraint=new_branch)
AppliedSymbol .substitute = substitute


# Class Variable  #######################################################

# @log  # decorator patched in by tests/main.py
@catch_error
def substitute(self, e0, e1, assignments, tag=None):
    if self.sort:
        self.sort = self.sort.substitute(e0,e1, assignments, tag)
    return e1 if self.code == e0.code else self
Variable.substitute = substitute


Done = True
