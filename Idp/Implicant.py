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

def use_value(function):
    " decorator for implicants() "
    def _wrapper(*args, **kwds):
        self = args[0]
        truth = args[1] if len(args) == 2 else TRUE
        if self.value   is not None: 
            return []
        out = _if_subtence(self, truth)
        if self.simpler is not None: 
            # call the (possibly inherited) 'function' method of simpler's class
            for cls in self.simpler.__class__.__mro__:
                if function.__name__ in cls.__dict__:
                    out = out + (cls.__dict__[function.__name__])(self.simpler, truth)
                    return out
            assert False, "Internal error in Implicant.use_value"
        out = out + function(self, truth)
        return out
    return _wrapper

# class Expression ############################################################

@use_value
def implicants(self, truth):
    " returns the list of implicants of self (default implementation) "
    return []
Expression.implicants = implicants
IfExpr.implicants = implicants
AEquivalence.implicants = implicants
AImplication.implicants = implicants
Brackets.implicants = implicants


# class ADisjunction ############################################################

@use_value
def implicants(self, truth=TRUE):
    if truth == FALSE:
        return sum( (e.implicants(truth) for e in self.sub_exprs), [])
    return []
ADisjunction.implicants = implicants


# class AConjunction ############################################################

@use_value
def implicants(self, truth=TRUE):
    if truth == TRUE:
        return sum( (e.implicants(truth) for e in self.sub_exprs), [])
    return []
AConjunction.implicants = implicants


# class AUnary ############################################################

@use_value
def implicants(self, truth=TRUE):
    return self.sub_exprs[0].implicants(_not(truth)) if self.operator == '~' \
      else []
AUnary.implicants = implicants


# class AComparison ############################################################

@use_value
def implicants(self, truth=TRUE):
    if truth == TRUE and len(self.sub_exprs) == 2 and self.operator == ['=']:
        operands1 = [e.as_ground() for e in self.sub_exprs]
        if   operands1[1] is not None:
            return [(self.sub_exprs[0], operands1[1])]
        elif operands1[0] is not None:
            return [(self.sub_exprs[1], operands1[0])]
    return []
AComparison.implicants = implicants