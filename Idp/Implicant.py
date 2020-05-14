"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""

"""

Computes the implicants of an expression, 
i.e., the sub-expressions that must be true for the expression to be true


"""

from typing import List, Tuple
from debugWithYamlLog import log_calls

from Idp.Expression import Constructor, Expression, IfExpr, AQuantification, BinaryOperator, \
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  \
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate, \
                    AppliedSymbol, Variable, Symbol, NumberConstant, Brackets, Arguments, \
                    Fresh_Variable, TRUE, FALSE, ZERO

def _if_subtence(self, truth):
    return [(self, truth)] if self.is_subtence or type(self) in [AppliedSymbol, Variable] \
      else []

def _not(truth):
    return FALSE if truth == TRUE else TRUE

# class Expression ############################################################

def implicants(self, truth=TRUE):
    if self.value is not None: 
        return []
    out = _if_subtence(self, truth)
    if self.simpler is not None: 
        out = self.simpler.implicants(truth) + out
        return out
    out = self.implicants1(truth) + out
    return out
Expression.implicants = implicants

def implicants1(self, truth):
    " returns the list of implicants of self (default implementation) "
    return []
Expression.implicants1 = implicants1


# class Constructor ############################################################

def implicants(self, truth=TRUE): # dead code
    return [] # true or false
Constructor.implicants = implicants


# class AQuantification ############################################################

def implicants(self, truth=TRUE):
    out = _if_subtence(self, truth)
    if self.vars == []: # expanded
        return self.sub_exprs[0].implicants(truth) + out
    return out
AQuantification.implicants = implicants


# class ADisjunction ############################################################

def implicants1(self, truth=TRUE):
    if truth == FALSE:
        return sum( (e.implicants(truth) for e in self.sub_exprs), [])
    return []
ADisjunction.implicants1 = implicants1


# class AConjunction ############################################################

def implicants1(self, truth=TRUE):
    if truth == TRUE:
        return sum( (e.implicants(truth) for e in self.sub_exprs), [])
    return []
AConjunction.implicants1 = implicants1


# class AUnary ############################################################

def implicants1(self, truth=TRUE):
    return self.sub_exprs[0].implicants(_not(truth)) if self.operator == '~' \
      else []
AUnary.implicants1 = implicants1


# class AComparison ############################################################

def implicants1(self, truth=TRUE):
    if truth == TRUE and len(self.sub_exprs) == 2 and self.operator == ['=']:
        # generates both (x->0) and (x=0->True)
        # generating only one from universals would make the second one a consequence, not a universal
        operands1 = [e.as_ground() for e in self.sub_exprs]
        if   operands1[1] is not None:
            return [(self.sub_exprs[0], operands1[1])]
        elif operands1[0] is not None:
            return [(self.sub_exprs[1], operands1[0])]
    return []
AComparison.implicants1 = implicants1


# class Brackets ############################################################

def implicants(self, truth=TRUE):
    return self.sub_exprs[0].implicants(truth) + _if_subtence(self, truth)
Brackets.implicants = implicants
