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

from typing import List, Tuple, Optional

from idp_engine.Expression import (Expression, AQuantification,
                    ADisjunction, AConjunction,
                    AComparison, AUnary, Brackets, TRUE, FALSE)
from idp_engine.Assignments import Assignments


def _not(truth):
    return FALSE if truth.same_as(TRUE) else TRUE

# class Expression  ###########################################################


def symbolic_propagate(self,
                       assignments: "Assignments",
                       truth: Optional[Expression] = TRUE
                       ) -> List[Tuple[Expression]]:
    """returns the consequences of `self=truth` that are in assignments.

    The consequences are obtained by symbolic processing (no calls to Z3).

    Args:
        assignments (Assignments):
            The set of questions to chose from. Their value is ignored.

        truth (Expression, optional):
            The truth value of the expression `self`. Defaults to TRUE.

    Returns:
        A list of pairs (Expression, bool), descring the literals that
        are implicant
    """
    if self.value is not None:
        return []
    out = [(self, truth)] if self.code in assignments else []
    if self.simpler is not None:
        out = self.simpler.symbolic_propagate(assignments, truth) + out
        return out
    out = self.propagate1(assignments, truth) + out
    return out


Expression.symbolic_propagate = symbolic_propagate


def propagate1(self, assignments, truth):
    " returns the list of symbolic_propagate of self (default implementation) "
    return []


Expression.propagate1 = propagate1


# class AQuantification  ######################################################

def symbolic_propagate(self, assignments, truth=TRUE):
    out = [(self, truth)] if self.code in assignments else []
    if not self.quantees:  # expanded
        return self.sub_exprs[0].symbolic_propagate(assignments, truth) + out
    return out
AQuantification.symbolic_propagate = symbolic_propagate


# class ADisjunction  #########################################################

def propagate1(self, assignments, truth=TRUE):
    if truth.same_as(FALSE):
        return sum( (e.symbolic_propagate(assignments, truth) for e in self.sub_exprs), [])
    return []
ADisjunction.propagate1 = propagate1


# class AConjunction  #########################################################

def propagate1(self, assignments, truth=TRUE):
    if truth.same_as(TRUE):
        return sum( (e.symbolic_propagate(assignments, truth) for e in self.sub_exprs), [])
    return []
AConjunction.propagate1 = propagate1


# class AUnary  ############################################################

def propagate1(self, assignments, truth=TRUE):
    return ( [] if self.operator != '¬' else
        self.sub_exprs[0].symbolic_propagate(assignments, _not(truth)) )
AUnary.propagate1 = propagate1


# class AComparison  ##########################################################

def propagate1(self, assignments, truth=TRUE):
    if truth.same_as(TRUE) and len(self.sub_exprs) == 2 and self.operator == ['=']:
        # generates both (x->0) and (x=0->True)
        # generating only one from universals would make the second one
        # a consequence, not a universal
        operands1 = [e.value for e in self.sub_exprs]
        if   operands1[1] is not None:
            return [(self.sub_exprs[0], operands1[1])]
        elif operands1[0] is not None:
            return [(self.sub_exprs[1], operands1[0])]
    return []
AComparison.propagate1 = propagate1


# class Brackets  ############################################################

def symbolic_propagate(self, assignments, truth=TRUE):
    out = [(self, truth)] if self.code in assignments else []
    return self.sub_exprs[0].symbolic_propagate(assignments, truth) + out
Brackets.symbolic_propagate = symbolic_propagate




Done = True
