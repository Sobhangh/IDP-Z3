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

Computes the consequences of an expression,
i.e., the sub-expressions that are necessarily true (or false)
if the expression is true (or false)

This module monkey-patches the Expression class and sub-classes.
"""

from copy import copy
from typing import Optional

from idp_engine.Expression import (AppliedSymbol, Expression, AQuantification,
                    ADisjunction, AConjunction,
                    AComparison, AUnary, Brackets, TRUE, FALSE)
from idp_engine.Assignments import Assignments


def _not(truth):
    return FALSE if truth.same_as(TRUE) else TRUE


# class Expression ############################################################

def simplify_with(self: Expression, assignments: "Assignments") -> Expression:
    """ simplify the expression using the assignments """
    if self.value is not None:
        return self
    value, simpler, new_e, co_constraint = None, None, None, None
    ass = assignments.get(self.code, None)
    if ass and ass.value is not None:
        value = ass.value
    if self.simpler is not None:
        simpler = self.simpler.simplify_with(assignments)
    if self.co_constraint is not None:
        co_constraint = self.co_constraint.simplify_with(assignments)
    new_e = [e.simplify_with(assignments) for e in self.sub_exprs]
    return self._change(sub_exprs=new_e, value=value, simpler=simpler,
                        co_constraint=co_constraint).simplify1()
Expression.simplify_with = simplify_with


def symbolic_propagate(self,
                       assignments: "Assignments",
                       tag: "Status",
                       truth: Optional[Expression] = TRUE
                       ):
    """updates assignments with the consequences of `self=truth`.

    The consequences are obtained by symbolic processing (no calls to Z3).

    Args:
        assignments (Assignments):
            The set of assignments to update.

        truth (Expression, optional):
            The truth value of the expression `self`. Defaults to TRUE.
    """
    if self.value is None:
        if self.code in assignments:
            assignments.assert__(self, truth, tag, False)
        if self.simpler is not None:
            self.simpler.symbolic_propagate(assignments, tag, truth)
        else:
            self.propagate1(assignments, tag, truth)
Expression.symbolic_propagate = symbolic_propagate


def propagate1(self, assignments, tag, truth):
    " returns the list of symbolic_propagate of self, ignoring value and simpler "
    return
Expression.propagate1 = propagate1


# class AQuantification  ######################################################

def symbolic_propagate(self, assignments, tag, truth=TRUE):
    if self.code in assignments:
        assignments.assert__(self, truth, tag, False)
    if not self.quantees:  # expanded
        assert len(self.sub_exprs) == 1  # a conjunction or disjunction
        self.sub_exprs[0].symbolic_propagate(assignments, tag, truth)
AQuantification.symbolic_propagate = symbolic_propagate


# class ADisjunction  #########################################################

def propagate1(self, assignments, tag, truth=TRUE):
    if truth.same_as(FALSE):
        for e in self.sub_exprs:
            e.symbolic_propagate(assignments, tag, truth)
ADisjunction.propagate1 = propagate1


# class AConjunction  #########################################################

def propagate1(self, assignments, tag, truth=TRUE):
    if truth.same_as(TRUE):
        for e in self.sub_exprs:
            e.symbolic_propagate(assignments, tag, truth)
AConjunction.propagate1 = propagate1


# class AUnary  ############################################################

def propagate1(self, assignments, tag, truth=TRUE):
    if self.operator == '¬':
        self.sub_exprs[0].symbolic_propagate(assignments, tag, _not(truth))
AUnary.propagate1 = propagate1


# class AComparison  ##########################################################

def propagate1(self, assignments, tag, truth=TRUE):
    if truth.same_as(TRUE) and len(self.sub_exprs) == 2 and self.operator == ['=']:
        # generates both (x->0) and (x=0->True)
        # generating only one from universals would make the second one
        # a consequence, not a universal
        operands1 = [e.value for e in self.sub_exprs]
        if (type(self.sub_exprs[0]) == AppliedSymbol
        and operands1[1] is not None):
            assignments.assert__(self.sub_exprs[0], operands1[1], tag, False)
        elif (type(self.sub_exprs[1]) == AppliedSymbol
        and operands1[0] is not None):
            assignments.assert__(self.sub_exprs[1], operands1[0], tag, False)
AComparison.propagate1 = propagate1


# class Brackets  ############################################################

def symbolic_propagate(self, assignments, tag, truth=TRUE):
    self.sub_exprs[0].symbolic_propagate(assignments, tag, truth)
Brackets.symbolic_propagate = symbolic_propagate




Done = True
