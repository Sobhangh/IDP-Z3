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
    " returns the list of implicants of self (default implementation) "
    if self.value is not None: 
        return []
    return _if_subtence(self, truth)
Expression.implicants = implicants


# class IfExpr ############################################################

def implicants(self, truth=TRUE):
    if self.value is not None: 
        return []
    out = _if_subtence(self, truth)
    if self.sub_exprs[0] == TRUE:
        return out + self.sub_exprs[1].implicants(truth)
    elif self.sub_exprs[0] == FALSE:
        return out + self.sub_exprs[2].implicants(truth)
    elif self.sub_exprs[1] == TRUE and self.sub_exprs[2] == FALSE:
        return out + self.sub_exprs[0].implicants(truth)
    elif self.sub_exprs[1] == FALSE and self.sub_exprs[2] == TRUE:
        return out + self.sub_exprs[0].implicants(truth)
    return out
IfExpr.implicants = implicants


# class AImplication ############################################################

def implicants(self, truth=TRUE):
    if self.value is not None: 
        return []
    out = _if_subtence(self, truth)
    if self.sub_exprs[0] == TRUE:
        return out + self.sub_exprs[1].implicants(truth)
    elif self.sub_exprs[1] == FALSE:
        return out + self.sub_exprs[0].implicants(_not(truth))
    return out
AImplication.implicants = implicants


# class AEquivalence ############################################################

def implicants(self, truth=TRUE):
    if self.value is not None: 
        return []
    out, trues, falses = [], 0, 0
    for e in self.sub_exprs: # FALSE or unknown
        if e == TRUE:
            trues += 1
        if e == FALSE:
            trues += 1
        else:
            out += e.implicants(truth)

    out = _if_subtence(self, truth)
    if len(out) == 1:
        return out + out[0].implicants(truth)
    if 0 < trues:
        return out + sum( (e.implicants(truth) for e in self.sub_exprs), [])
    if 0 < falses:
        return out + sum( (e.implicants(truth) for e in self.sub_exprs), [])
    return out
AEquivalence.implicants = implicants


# class ADisjunction ############################################################

def implicants(self, truth=TRUE):
    if self.value is not None: # one is TRUE or all are FALSE
        return []
    out, count = [], 0
    for e in self.sub_exprs: # FALSE or unknown
        out += e.implicants(truth)
        if not e == FALSE:
            count += 1
    # use out if truth=FALSE, or truth=TRUE and only one sub_expr is unknown
    return _if_subtence(self, truth) + (out if truth == FALSE or count == 1 else [])
ADisjunction.implicants = implicants


# class AConjunction ############################################################

def implicants(self, truth=TRUE):
    if self.value is not None: # one is FALSE or all are TRUE
        return []
    out, count = [], 0
    for e in self.sub_exprs: # TRUE or unknown
        out += e.implicants(truth)
        if not e == TRUE:
            count += 1
    # use out if truth=TRUE, or truth=FALSE and only one sub_expr is unknown
    return _if_subtence(self, truth) + (out if truth == TRUE or count == 1 else [])
AConjunction.implicants = implicants


# class AUnary ############################################################

def implicants(self, truth=TRUE):
    if self.value is not None: # one is FALSE or all are TRUE
        return []
    return _if_subtence(self, truth) + \
        ( self.sub_exprs[0].implicants(_not(truth)) if self.operator == '~' \
          else [] )
AUnary.implicants = implicants

# class Brackets ############################################################

def implicants(self, truth=TRUE):
    if self.value is not None: # one is FALSE or all are TRUE
        return []
    return _if_subtence(self, truth) + self.sub_exprs[0].implicants(truth)
Brackets.implicants = implicants
