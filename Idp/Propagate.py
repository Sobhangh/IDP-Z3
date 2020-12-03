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

from typing import List, Tuple
from debugWithYamlLog import log_calls

from Idp.Expression import Constructor, Expression, AQuantification, \
                    ADisjunction, AConjunction,  \
                    AComparison, AUnary, Brackets, TRUE, FALSE


def _not(truth):
    return FALSE if truth.same_as(TRUE) else TRUE

# class Expression ############################################################

def symbolic_propagate(self, assignments, truth=TRUE):
    if self.value is not None: 
        return []
    out = [(self, truth)] if self.code in assignments else []
    if self.simpler is not None: 
        out = self.simpler.symbolic_propagate(assignments, truth) + out
        return out
    out = self.implicants1(assignments, truth) + out
    return out
Expression.symbolic_propagate = symbolic_propagate

def implicants1(self, assignments, truth):
    " returns the list of symbolic_propagate of self (default implementation) "
    return []
Expression.implicants1 = implicants1


# class Constructor ############################################################

def symbolic_propagate(self, assignments, truth=TRUE): # dead code
    return [] # true or false
Constructor.symbolic_propagate = symbolic_propagate


# class AQuantification ############################################################

def symbolic_propagate(self, assignments, truth=TRUE):
    out = [(self, truth)] if self.code in assignments else []
    if self.vars == []: # expanded
        return self.sub_exprs[0].symbolic_propagate(assignments, truth) + out
    return out
AQuantification.symbolic_propagate = symbolic_propagate


# class ADisjunction ############################################################

def implicants1(self, assignments, truth=TRUE):
    if truth.same_as(FALSE):
        return sum( (e.symbolic_propagate(assignments, truth) for e in self.sub_exprs), [])
    return []
ADisjunction.implicants1 = implicants1


# class AConjunction ############################################################

def implicants1(self, assignments, truth=TRUE):
    if truth.same_as(TRUE):
        return sum( (e.symbolic_propagate(assignments, truth) for e in self.sub_exprs), [])
    return []
AConjunction.implicants1 = implicants1


# class AUnary ############################################################

def implicants1(self, assignments, truth=TRUE):
    return ( [] if self.operator != '¬' else
        self.sub_exprs[0].symbolic_propagate(assignments, _not(truth)) )
AUnary.implicants1 = implicants1


# class AComparison ############################################################

def implicants1(self, assignments, truth=TRUE):
    if truth.same_as(TRUE) and len(self.sub_exprs) == 2 and self.operator == ['=']:
        # generates both (x->0) and (x=0->True)
        # generating only one from universals would make the second one a consequence, not a universal
        operands1 = [e.as_rigid() for e in self.sub_exprs]
        if   operands1[1] is not None:
            return [(self.sub_exprs[0], operands1[1])]
        elif operands1[0] is not None:
            return [(self.sub_exprs[1], operands1[0])]
    return []
AComparison.implicants1 = implicants1


# class Brackets ############################################################

def symbolic_propagate(self, assignments, truth=TRUE):
    """returns the consequences of `self=truth` that are in assignments.

    The consequences are obtained by symbolic processing (no calls to Z3).

    Args:
        assignments ([Assignments]):
            The set of questions to chose from. Their value is ignored.

        truth ([type], optional):
            The truth value of the expression `self`. Defaults to TRUE.

    Returns:
        A list of pairs (Expression, bool), descring the literals that are implicant
    """
    out = [(self, truth)] if self.code in assignments else []
    return self.sub_exprs[0].symbolic_propagate(assignments, truth) + out
Brackets.symbolic_propagate = symbolic_propagate




Done = True