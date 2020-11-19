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

Computes the implicants of an expression, 
i.e., the sub-expressions that must be true (or false) for the expression to be true


"""

from typing import List, Tuple
from debugWithYamlLog import log_calls

from Idp.Expression import Constructor, Expression, AQuantification, \
                    ADisjunction, AConjunction,  \
                    AComparison, AUnary, Brackets, TRUE, FALSE


def _not(truth):
    return FALSE if truth.same_as(TRUE) else TRUE

# class Expression ############################################################

def implicants(self, assignments, truth=TRUE):
    " returns the implicants of self=truth that are in assignments "
    if self.value is not None: 
        return []
    out = [(self, truth)] if self.code in assignments else []
    if self.simpler is not None: 
        out = self.simpler.implicants(assignments, truth) + out
        return out
    out = self.implicants1(assignments, truth) + out
    return out
Expression.implicants = implicants

def implicants1(self, assignments, truth):
    " returns the list of implicants of self (default implementation) "
    return []
Expression.implicants1 = implicants1


# class Constructor ############################################################

def implicants(self, assignments, truth=TRUE): # dead code
    return [] # true or false
Constructor.implicants = implicants


# class AQuantification ############################################################

def implicants(self, assignments, truth=TRUE):
    out = [(self, truth)] if self.code in assignments else []
    if self.vars == []: # expanded
        return self.sub_exprs[0].implicants(assignments, truth) + out
    return out
AQuantification.implicants = implicants


# class ADisjunction ############################################################

def implicants1(self, assignments, truth=TRUE):
    if truth.same_as(FALSE):
        return sum( (e.implicants(assignments, truth) for e in self.sub_exprs), [])
    return []
ADisjunction.implicants1 = implicants1


# class AConjunction ############################################################

def implicants1(self, assignments, truth=TRUE):
    if truth.same_as(TRUE):
        return sum( (e.implicants(assignments, truth) for e in self.sub_exprs), [])
    return []
AConjunction.implicants1 = implicants1


# class AUnary ############################################################

def implicants1(self, assignments, truth=TRUE):
    return ( [] if self.operator != '¬' else
        self.sub_exprs[0].implicants(assignments, _not(truth)) )
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

def implicants(self, assignments, truth=TRUE):
    out = [(self, truth)] if self.code in assignments else []
    return self.sub_exprs[0].implicants(assignments, truth) + out
Brackets.implicants = implicants




Done = True