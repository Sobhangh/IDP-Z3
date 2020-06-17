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

Adds simplify to logic expression classes

( see docs/zettlr/Substitute.md )

"""

import copy
import sys

from debugWithYamlLog import *

from typing import List, Tuple
from Idp.Expression import Constructor, Expression, IfExpr, AQuantification, BinaryOperator, \
                    AEquivalence, AImplication, ADisjunction, AConjunction,  \
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate, \
                    AppliedSymbol, Variable, NumberConstant, Brackets, \
                    Fresh_Variable, TRUE, FALSE


# class Expression ############################################################

def _change(self, sub_exprs=None, ops=None, value=None, simpler=None, co_constraint=None):
    " change attributes of an expression, and resets derived attributes "

    if sub_exprs     is not None: self.sub_exprs     = sub_exprs
    if ops           is not None: self.operator      = ops
    if co_constraint is not None: self.co_constraint = co_constraint
    if value         is not None: self.value         = value
    elif simpler     is not None: 
        if type(simpler) in [Constructor, NumberConstant]:
            self.value   = simpler
        elif simpler.value is not None: # example: prime.idp
            self.value   = simpler.value
        else:
            self.simpler = simpler
    assert self.value is None or type(self.value) in [Constructor, NumberConstant]
    assert self.value is not self # avoid infinite loops
    
    # reset derived attributes
    self.str = sys.intern(str(self))

    return self
Expression._change = _change


def update_exprs(self, new_expr_generator):
    """ change sub_exprs and simplify. """
    #  default implementation, without simplification
    return self._change(sub_exprs=list(new_expr_generator))
#Expression.update_exprs = update_exprs
for i in [Constructor, AppliedSymbol, Variable, Fresh_Variable, NumberConstant]:
    i.update_exprs = update_exprs


def simplify1(self):
    return self.update_exprs(iter(self.sub_exprs))
Expression.simplify1 = simplify1



# Class IfExpr ################################################################

def update_exprs(self, new_expr_generator):
    sub_exprs = list(new_expr_generator)
    if_, then_, else_   = sub_exprs[0], sub_exprs[1], sub_exprs[2]
    if if_.same_as(TRUE):
            return self._change(simpler=then_, sub_exprs=sub_exprs)
    elif if_.same_as(FALSE):
            return self._change(simpler=else_, sub_exprs=sub_exprs)
    else:
        if then_.same_as(else_):
            return self._change(simpler=then_, sub_exprs=sub_exprs)
        elif then_.same_as(TRUE) and else_.same_as(FALSE):
            return self._change(simpler=if_  , sub_exprs=sub_exprs)
        elif then_.same_as(FALSE) and else_.same_as(TRUE):
            return self._change(simpler=AUnary.make('~', if_), sub_exprs=sub_exprs)
    return self._change(sub_exprs=sub_exprs)
IfExpr.update_exprs = update_exprs



# Class AQuantification #######################################################

def update_exprs(self, new_expr_generator):
    exprs = list(new_expr_generator)
    simpler = exprs[0] if not self.vars else None
    return self._change(simpler=simpler, sub_exprs=exprs)
AQuantification.update_exprs = update_exprs


# Class AImplication #######################################################

def update_exprs(self, new_expr_generator):
    exprs = list(new_expr_generator)
    value, simpler = None, None
    if exprs[0].same_as(FALSE): # (false => p) is true
        value = TRUE
        # exprs[0] may be false because exprs[1] was false
        exprs = [exprs[0], exprs[1] if self.sub_exprs[1].same_as(FALSE) else FALSE]
    if exprs[0].same_as(TRUE): # (true => p) is p
        simpler = exprs[1]
    if exprs[1].same_as(TRUE): # (p => true) is true
        value = TRUE
        exprs = [exprs[0] if self.sub_exprs[0].same_as(TRUE) else TRUE, exprs[1]]
    if exprs[1].same_as(FALSE): # (p => false) is ~p
        simpler = AUnary.make('~', exprs[0])
    return self._change(value=value, simpler=simpler, sub_exprs=exprs)
AImplication.update_exprs = update_exprs



# Class AEquivalence #######################################################

def update_exprs(self, new_expr_generator):
    exprs = list(new_expr_generator)
    if len(exprs)==1:
        return self._change(simpler=exprs[1], sub_exprs=exprs)
    for e in exprs:
        if e.same_as(TRUE): # they must all be true
            return self._change(simpler=AConjunction.make('∧', exprs), sub_exprs=exprs)
        if e.same_as(FALSE): # they must all be false
            return self._change(simpler=AConjunction.make('∧', [AUnary.make('~', e) for e in exprs]),
                              sub_exprs=exprs)
    return self._change(sub_exprs=exprs)
AEquivalence.update_exprs = update_exprs



# Class ADisjunction #######################################################

def update_exprs(self, new_expr_generator):
    exprs, other = [], []
    value, simpler = None, None
    for i, expr in enumerate(new_expr_generator):
        if expr.same_as(TRUE):
            # simplify only if one other sub_exprs was unknown
            if any(e.value is None and not i==j for j,e in enumerate(self.sub_exprs)):
                return self._change(value=TRUE, sub_exprs=[expr])
            value = TRUE
        exprs.append(expr)
        if not expr.same_as(FALSE):
            other.append(expr)

    if len(other) == 0: # all disjuncts are False
        value = FALSE
    if len(other) == 1:
         simpler=other[0]
    return self._change(value=value, simpler=simpler, sub_exprs=exprs)
ADisjunction.update_exprs = update_exprs



# Class AConjunction #######################################################

# same as ADisjunction, with TRUE and FALSE swapped
def update_exprs(self, new_expr_generator):
    exprs, other = [], []
    value, simpler = None, None
    for i, expr in enumerate(new_expr_generator):
        if expr.same_as(FALSE): 
            # simplify only if one other sub_exprs was unknown
            if any(e.value is None and not i==j for j,e in enumerate(self.sub_exprs)):
                return self._change(value=FALSE, sub_exprs=[expr])
            value = FALSE
        exprs.append(expr)
        if not expr.same_as(TRUE):
            other.append(expr)

    if len(other) == 0:  # all conjuncts are True
        value = TRUE
    if len(other) == 1:
        simpler = other[0]
    return self._change(value=value, simpler=simpler, sub_exprs=exprs)
AConjunction.update_exprs = update_exprs



# Class AComparison #######################################################

def update_exprs(self, new_expr_generator):
    operands = list(new_expr_generator)
    operands1 = [e.as_ground() for e in operands]
    if all(e is not None for e in operands1):
        acc, acc1 = operands[0], operands1[0]
        assert len(self.operator) == len(operands1[1:]), "Internal error"
        for op, expr, expr1 in zip(self.operator, operands[1:], operands1[1:]):
            if not (BinaryOperator.MAP[op]) (acc1.translate(), expr1.translate()):
                return self._change(value=FALSE, sub_exprs=[acc, expr], ops=[op])
            acc, acc1 = expr, expr1
        return self._change(value=TRUE, sub_exprs=operands)
    return self._change(sub_exprs=operands)
AComparison.update_exprs = update_exprs



#############################################################

def update_arith(self, family, new_expr_generator):
    operands = list(new_expr_generator)
    operands1 = [e.as_ground() for e in operands]
    if all(e is not None for e in operands1):
        out = operands1[0].translate()

        for e, op in zip(operands1[1:], self.operator):
            function = BinaryOperator.MAP[op]
            
            if op=='/' and self.type == 'int': # integer division
                out //= e.translate()
            else:
                out = function(out, e.translate())
        value = NumberConstant(number=str(out))
        return self._change(value=value, sub_exprs=operands)
    return self._change(sub_exprs=operands)



# Class ASumMinus #######################################################

def update_exprs(self, new_expr_generator):
    return update_arith(self, '+', new_expr_generator)
ASumMinus.update_exprs = update_exprs



# Class AMultDiv #######################################################

def update_exprs(self, new_expr_generator):
    if any(op == '%' for op in self.operator): # special case !
        operands = list(new_expr_generator)
        operands1 = [e.as_ground() for e in operands]
        if len(operands) == 2 \
        and all(e is not None for e in operands1):
            out = operands1[0].translate() % operands1[1].translate()
            return self._change(value=NumberConstant(number=str(out)), sub_exprs=operands)
        else:
            return self._change(sub_exprs=operands)
    return update_arith(self, '*', new_expr_generator)
AMultDiv.update_exprs = update_exprs



# Class APower #######################################################

def update_exprs(self, new_expr_generator):
    operands = list(new_expr_generator)
    operands1 = [e.as_ground() for e in operands]
    if len(operands) == 2 \
    and all(e is not None for e in operands1):
        out = operands1[0].translate() ** operands1[1].translate()
        return self._change(value=NumberConstant(number=str(out)), sub_exprs=operands)
    else:
        return self._change(sub_exprs=operands)
APower.update_exprs = update_exprs



# Class AUnary #######################################################

def update_exprs(self, new_expr_generator):
    operand = list(new_expr_generator)[0]
    if self.operator == '~':
        if operand.same_as(TRUE):
            return self._change(value=FALSE, sub_exprs=[operand])
        if operand.same_as(FALSE):
            return self._change(value=TRUE, sub_exprs=[operand])
    else: # '-'
        a = operand.as_ground()
        if a is not None:
            if type(a) == NumberConstant:
                return self._change(value=NumberConstant(number=str(- a.translate())), sub_exprs=[operand])
    return self._change(sub_exprs=[operand])
AUnary.update_exprs = update_exprs



# Class AAggregate #######################################################

def update_exprs(self, new_expr_generator):
    operands = list(new_expr_generator)
    operands1 = [e.as_ground() for e in operands]
    if all(e is not None for e in operands1):
        acc = 0
        for expr, expr1 in zip(operands, operands1):
            if expr1 is not None:
                acc += expr1.translate() if self.aggtype == 'sum' else 1
            else:
                exprs.add(expr)
        out = NumberConstant(number=str(acc))
        return self._change(value=out, sub_exprs=operands)

    return self._change(sub_exprs=operands)
AAggregate.update_exprs = update_exprs


     
# Class Brackets #######################################################

def update_exprs(self, new_expr_generator):
    expr = next(new_expr_generator)
    return self._change(sub_exprs=[expr], value=expr.value)
Brackets.update_exprs = update_exprs


