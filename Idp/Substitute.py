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

Adds substitute, expand_quantifiers and simplify to logic expression classes

"""

import copy
import functools
import itertools as it
import os
import re
import sys

from z3 import DatatypeRef, FreshConst, Or, Not, And, ForAll, Exists, Z3Exception, Sum, If, Const, BoolSort
from utils import mergeDicts, unquote

from typing import List, Tuple
from Idp.Expression import Constructor, Expression, IfExpr, AQuantification, BinaryOperator, \
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  \
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate, \
                    AppliedSymbol, Variable, Symbol, NumberConstant, Brackets, Arguments, \
                    Fresh_Variable, TRUE, FALSE


# class Expression ############################################################

def _change(self, by=None, sub_exprs=None, ops=None, justification=None):
    " change expression, after copying it if really changed"
    if by is not None:
        return self.substitute(self, by)

    # return self if not changed
    changed = False
    if sub_exprs is not None:       changed |= self.sub_exprs != sub_exprs
    if justification is not None:   changed |= self.justification != justification
    if not changed: return self

    out = copy.copy(self)
    if sub_exprs is not None :      out.sub_exprs = sub_exprs
    if ops       is not None :      out.operator  = ops
    if justification is not None:   out.justification = justification
    
    # reset derived values
    out.str = sys.intern(str(out))
    out._unknown_symbols = None
    out._subtences = None
    out.translated = None

    return out
Expression._change = _change


def update_exprs(self, new_expr_generator):
    """ change sub_exprs and simplify. """
    #  default implementation 
    return self._change(sub_exprs=list(new_expr_generator))
Expression.update_exprs = update_exprs


def substitute(self, e0, e1, todo=None, case=None):
    """ recursively substitute e0 by e1 in self, introducing a Bracket if changed """
    if self == e0: # based on repr !
        if type(e0) == Fresh_Variable or type(e1) == Fresh_Variable:
            return e1 # no need to have brackets
        # replace by new Brackets node, to keep annotations
        out = Brackets(f=e1, annotations=self.annotations) # e1 is not copied !

        # copy initial annotation
        out.code = self.code
        out.is_subtence = self.is_subtence
        out.fresh_vars = self.fresh_vars
        out.is_visible = self.is_visible
        out.type = self.type
        # out.normal is not set, normally
    else:
        out = self.update_exprs(e.substitute(e0, e1, todo, case) for e in self.sub_exprs)
        if out.justification is not None:
            out = out._change(justification= out.justification.substitute(e0, e1, todo, case))
            if todo is not None:
                todo0 = out.justification.expr_to_literal(case)
                todo.extend(todo0)
    return out
Expression.substitute = substitute


def instantiate(self, e0, e1):
    """ recursively substitute e0 by e1, without Bracket """
    if self == e0: # based on repr !
        return e1
    else:
        out = copy.copy(self)
        out.sub_exprs = [e.instantiate(e0, e1) for e in out.sub_exprs]
        out = out.simplify1()
        out.code = out.code.replace(str(e0), str(e1))
        return out
Expression.instantiate = instantiate


def simplify1(self):
    return self.update_exprs(iter(self.sub_exprs))
Expression.simplify1 = simplify1


def expand_quantifiers(self, theory):
    return self.update_exprs(e.expand_quantifiers(theory) for e in self.sub_exprs)
Expression.expand_quantifiers = expand_quantifiers



# Class IfExpr ################################################################

def update_exprs(self, new_expr_generator):
    if isinstance(new_expr_generator, list):
        new_expr_generator = iter(new_expr_generator)
    if_ = next(new_expr_generator)
    if if_ == TRUE:
        return self._change(by=next(new_expr_generator))
    elif if_ == FALSE:
        next(new_expr_generator)
        return self._change(by=next(new_expr_generator))
    else:
        then_ = next(new_expr_generator)
        else_ = next(new_expr_generator)
        if then_ == TRUE:
            if else_ == TRUE:
                return self._change(by=TRUE)
            elif else_ == FALSE:
                return self._change(by=if_)
        elif then_ == FALSE:
            if else_ == FALSE:
                return self._change(by=FALSE)
            elif else_ == TRUE:
                return self._change(by=AUnary.make('~', if_))
    return self._change(sub_exprs=[if_, then_, else_])
IfExpr.update_exprs = update_exprs


# Class AQuantification #######################################################

def expand_quantifiers(self, theory):
    forms = [self.sub_exprs[0].expand_quantifiers(theory)]
    self.vars = []
    self.sorts = [] # not used
    for name, var in self.q_vars.items():
        if var.decl.range:
            forms = [f.substitute(var, val) for val in var.decl.range for f in forms]
        else:
            self.vars.append(var)
    if self.q == '∀':
        out = AConjunction.make('∧', forms)
    else:
        out = ADisjunction.make('∨', forms)
    if not self.vars:
        return self._change(by=out)
    return self._change(sub_exprs=[out])
AQuantification.expand_quantifiers = expand_quantifiers


# Class AImplication #######################################################

def update_exprs(self, new_expr_generator): 
    exprs = list(new_expr_generator)
    if len(exprs) == 2: #TODO deal with associativity
        if exprs[0] == FALSE: # (false => p) is true
            return self._change(by=TRUE)
        if exprs[0] == TRUE: # (true => p) is p
            return self._change(by=exprs[1])
        if exprs[1] == TRUE: # (p => true) is true
            return self._change(by=TRUE)
        if exprs[1] == FALSE: # (p => false) is ~p
            return self._change(by=AUnary.make('~', exprs[0]))
    return self._change(sub_exprs=exprs)
AImplication.update_exprs = update_exprs


# Class AEquivalence #######################################################

def update_exprs(self, new_expr_generator): 
    exprs = list(new_expr_generator)
    if any(e == TRUE for e in exprs):
        return self._change(by=AConjunction.make('∧', exprs))
    if any(e == FALSE for e in exprs):
        return self._change(by=AConjunction.make('∧', [AUnary.make('~', e) for e in exprs]))
    return self._change(sub_exprs=exprs)
AEquivalence.update_exprs = update_exprs


# Class ADisjunction #######################################################

def update_exprs(self, new_expr_generator):
    exprs = []
    for expr in new_expr_generator:
        if expr == TRUE:  return self._change(by=TRUE)
        if expr == FALSE: pass
        elif type(expr) == ADisjunction: # flatten
            for e in expr.sub_exprs:
                if e == TRUE:    return TRUE
                elif e == FALSE: pass
                exprs.append(e)
        else:
            exprs.append(expr)
    if len(exprs) == 0:
        return self._change(by=FALSE)
    if len(exprs) == 1:
        return self._change(by=exprs[0])
    return self._change(sub_exprs=exprs)
ADisjunction.update_exprs = update_exprs


# Class AConjunction #######################################################

def update_exprs(self, new_expr_generator):
    exprs = []
    for expr in new_expr_generator:
        if expr == TRUE:    pass
        elif expr == FALSE: return self._change(by=FALSE)
        elif type(expr) == AConjunction: # flatten
            for e in expr.sub_exprs:
                if e == TRUE:    pass
                elif e == FALSE: return self._change(by=FALSE)
                exprs.append(e)
        else:
            exprs.append(expr)
    if len(exprs) == 0:
        return self._change(by=TRUE)
    if len(exprs) == 1:
        return self._change(by=exprs[0])
    return self._change(sub_exprs=exprs)
AConjunction.update_exprs = update_exprs


# Class AComparison #######################################################

def update_exprs(self, new_expr_generator):
    operands = list(new_expr_generator)
    operands1 = [e.as_ground() for e in operands]
    if all(e is not None for e in operands1):
        acc = operands1[0]
        assert len(self.operator) == len(operands1[1:]), "Internal error"
        for op, expr in zip(self.operator, operands1[1:]):
            if not (BinaryOperator.MAP[op]) (acc, expr):
                return self._change(by=FALSE)
            acc = expr
        return self._change(by=TRUE)
    return self._change(sub_exprs=operands)
AComparison.update_exprs = update_exprs


#############################################################

def update_arith(self, family, new_expr_generator):
    new_expr_generator = iter(new_expr_generator)
    # accumulate numbers in acc
    if self.type == 'int':
        acc = 0 if family == '+' else 1
    else:
        acc = 0.0 if family == '+' else 1.0
    ops, exprs = [], []
    def add(op, expr):
        nonlocal acc, ops, exprs
        expr1 = expr.as_ground()
        if expr1 is not None:
            if op == '+':
                acc += expr1
            elif op == '-':
                acc -= expr1
            elif op == '*':
                acc *= expr1
            elif op == '/':
                if isinstance(acc, int) and expr.type == 'int': # integer division
                    acc //= expr1
                else:
                    acc /= expr1
        else:
            ops.append(op)
            exprs.append(expr)
    add(family, next(new_expr_generator)) # this adds an operator
    operands = list(new_expr_generator)
    assert len(self.operator) == len(operands), "Internal error"
    for op, expr in zip(self.operator, operands):
        add(op, expr)

    # analyse results
    if family == '*' and acc == 0:
        return self._change(by=ZERO)
    elif 0 < len(exprs) and ((ops[0] == '+' and acc == 0) or (ops[0] == '*' and acc == 1)):
        del ops[0]
    else:
        exprs = [NumberConstant(number=str(acc))] + exprs
    if len(exprs)==1:
        return self._change(by=exprs[0])
    return self._change(sub_exprs=exprs, ops=ops)


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
            out = operands1[0] % operands1[1]
            return self._change(by=NumberConstant(number=str(out)))
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
        out = operands1[0] ** operands1[1]
        return self._change(by=NumberConstant(number=str(out)))
    else:
        return self._change(sub_exprs=operands)
APower.update_exprs = update_exprs


# Class AUnary #######################################################

def update_exprs(self, new_expr_generator):
    operand = list(new_expr_generator)[0]
    if self.operator == '~':
        if operand == TRUE:
            return self._change(by=FALSE)
        if operand == FALSE:
            return self._change(by=TRUE)
    else: # '-'
        a = operand.as_ground()
        if a is not None:
            if type(a) in [int, float]:
                return self._change(by=NumberConstant(number=str(- a)))
    return self._change(sub_exprs=[operand])
AUnary.update_exprs = update_exprs


# Class AAggregate #######################################################

def expand_quantifiers(self, theory):
    form = IfExpr(if_f=self.sub_exprs[AAggregate.CONDITION]
                , then_f=NumberConstant(number='1') if self.out is None else self.sub_exprs[AAggregate.OUT]
                , else_f=NumberConstant(number='0'))
    forms = [form.expand_quantifiers(theory)]
    for name, var in self.q_vars.items():
        if var.decl.range:
            forms = [f.substitute(var, val) for val in var.decl.range for f in forms]
        else:
            raise Exception('Can only quantify aggregates over finite domains')
    self.vars = None # flag to indicate changes
    return self._change(sub_exprs=forms)
AAggregate.expand_quantifiers = expand_quantifiers


# Class Brackets #######################################################

def update_exprs(self, new_expr_generator):
    expr = next(new_expr_generator)
    return self._change(sub_exprs=[expr])
Brackets.update_exprs = update_exprs