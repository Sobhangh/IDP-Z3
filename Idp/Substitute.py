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

( see docs/zettlr/Substitute.md )

"""

import copy
import sys

from debugWithYamlLog import Log, nl

from typing import List, Tuple
from Idp.Expression import Constructor, Expression, IfExpr, AQuantification, BinaryOperator, \
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  \
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate, \
                    AppliedSymbol, Variable, Symbol, NumberConstant, Brackets, Arguments, \
                    Fresh_Variable, TRUE, FALSE, ZERO


# class Expression ############################################################

def _change(self, sub_exprs=None, ops=None, value=None, simpler=None, just_branch=None):
    " change attributes of an expression, and erase derive attributes "

    if sub_exprs   is not None: self.sub_exprs = sub_exprs
    if ops         is not None: self.operator  = ops
    if just_branch is not None: self.just_branch = just_branch
    if value       is not None: self.value     = value
    elif simpler   is not None: 
        if type(simpler) in [Constructor, NumberConstant]:
            self.value   = simpler
        elif simpler.value is not None: # example: prime.idp
            self.value   = simpler.value
        else:
            self.simpler = simpler
    assert value is None or type(value) in [Constructor, NumberConstant]
    
    # reset derived attributes
    self.str = sys.intern(str(self))
    self._unknown_symbols = None

    return self
Expression._change = _change


def update_exprs(self, new_expr_generator):
    """ change sub_exprs and simplify. """
    #  default implementation, without simplification
    return self._change(sub_exprs=list(new_expr_generator))
Expression.update_exprs = update_exprs

# @log  # decorator patched in by tests/main.py
def Expression_substitute(self, e0, e1, todo=None):
    """ recursively substitute e0 by e1 in self (e0 is not a Fresh_Variable) """

    assert not isinstance(e0, Fresh_Variable)
    # similar code in AppliedSymbol !
    if self.code == e0.code:
        return self._change(value=e1) # e1 is Constructor or NumberConstant
    else:
        out = self.update_exprs((e.substitute(e0, e1, todo) for e in self.sub_exprs))
    return out
Expression.substitute = Expression_substitute


def instantiate(self, e0, e1):
    """ recursively substitute Fresh_Variable e0 by e1 """
    
    assert isinstance(e0, Fresh_Variable)
    if self.code == e0.code:
        return e1

    out = copy.copy(self)

    if out.value is None:
        out.update_exprs((e.instantiate(e0, e1) for e in out.sub_exprs))
        out.original = out
        if out.just_branch is not None:
            out._change(just_branch=out.just_branch.instantiate(e0, e1))

    out.fresh_vars.discard(e0.name)
    if isinstance(e1, Fresh_Variable) or isinstance(e1, Variable):
        # e1 is Variable when instantiating some definitions
        out.fresh_vars.add(e1.name)
    out.code = str(out)
    return out
Expression.instantiate = instantiate


def simplify1(self):
    return self.update_exprs(iter(self.sub_exprs))
Expression.simplify1 = simplify1


def expand_quantifiers(self, theory):
    return self.update_exprs(e.expand_quantifiers(theory) for e in self.sub_exprs)
Expression.expand_quantifiers = expand_quantifiers


def interpret(self, theory):
    " use information in structure and simplify "
    out = self.update_exprs(e.interpret(theory) for e in self.sub_exprs)
    out.original = out
    return out
Expression.interpret = interpret



# Class IfExpr ################################################################

def update_exprs(self, new_expr_generator):
    sub_exprs = list(new_expr_generator)
    if_, then_, else_   = sub_exprs[0], sub_exprs[1], sub_exprs[2]
    if if_ == TRUE:
            return self._change(simpler=then_, sub_exprs=sub_exprs)
    elif if_ == FALSE:
            return self._change(simpler=else_, sub_exprs=sub_exprs)
    else:
        if then_ == else_:
            return self._change(simpler=then_, sub_exprs=sub_exprs)
        elif then_ == TRUE and else_ == FALSE:
            return self._change(simpler=if_  , sub_exprs=sub_exprs)
        elif then_ == FALSE and else_ == TRUE:
            return self._change(simpler=AUnary.make('~', if_), sub_exprs=sub_exprs)
    return self._change(sub_exprs=sub_exprs)
IfExpr.update_exprs = update_exprs



# Class AQuantification #######################################################

def expand_quantifiers(self, theory):
    forms = [self.sub_exprs[0].expand_quantifiers(theory)]
    self.vars = []
    self.sorts = [] # not used
    for name, var in self.q_vars.items():
        if var.decl.range:
            out = []
            for f in forms:
                for val in var.decl.range:
                    new_f = f.instantiate(var, val)
                    out.append(new_f)
            forms = out
        else:
            self.vars.append(var)
            self.sorts.append(var.decl)
    if not self.vars:
        if self.q == '∀':
            out = AConjunction.make('∧', forms)
        else:
            out = ADisjunction.make('∨', forms)
        return self._change(simpler=out, sub_exprs=[out])
    return self._change(sub_exprs=forms)
AQuantification.expand_quantifiers = expand_quantifiers

def update_exprs(self, new_expr_generator):
    exprs = list(new_expr_generator)
    simpler = exprs[0] if not self.vars else None
    return self._change(simpler=simpler, sub_exprs=exprs)
AQuantification.update_exprs = update_exprs


# Class AImplication #######################################################

def update_exprs(self, new_expr_generator):
    exprs = list(new_expr_generator)
    value, simpler = None, None
    if exprs[0] == FALSE: # (false => p) is true
        value = TRUE
        # exprs[0] may be false because exprs[1] was false
        exprs = [exprs[0], exprs[1] if self.sub_exprs[1]==FALSE else FALSE]
    if exprs[0] == TRUE: # (true => p) is p
        simpler = exprs[1]
    if exprs[1] == TRUE: # (p => true) is true
        value = TRUE
        exprs = [exprs[0] if self.sub_exprs[0]==TRUE else TRUE, exprs[1]]
    if exprs[1] == FALSE: # (p => false) is ~p
        simpler = AUnary.make('~', exprs[0])
    return self._change(value=value, simpler=simpler, sub_exprs=exprs)
AImplication.update_exprs = update_exprs



# Class AEquivalence #######################################################

def update_exprs(self, new_expr_generator):
    exprs = list(new_expr_generator)
    if len(exprs)==1:
        return self._change(simpler=exprs[1], sub_exprs=exprs)
    for e in exprs:
        if e == TRUE: # they must all be true
            return self._change(simpler=AConjunction.make('∧', exprs, self.is_subtence), sub_exprs=exprs)
        if e == FALSE: # they must all be false
            return self._change(simpler=AConjunction.make('∧', [AUnary.make('~', e) for e in exprs], self.is_subtence),
                              sub_exprs=exprs)
    return self._change(sub_exprs=exprs)
AEquivalence.update_exprs = update_exprs



# Class ADisjunction #######################################################

def update_exprs(self, new_expr_generator):
    exprs, other = [], []
    value, simpler = None, None
    for i, expr in enumerate(new_expr_generator):
        if expr == TRUE:
            # simplify only if one other sub_exprs was unknown
            if any(e.value is None and not i==j for j,e in enumerate(self.sub_exprs)):
                return self._change(value=TRUE, sub_exprs=[expr])
            value = TRUE
        exprs.append(expr)
        if expr != FALSE:
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
        if expr == FALSE: 
            # simplify only if one other sub_exprs was unknown
            if any(e.value is None and not i==j for j,e in enumerate(self.sub_exprs)):
                return self._change(value=FALSE, sub_exprs=[expr])
            value = FALSE
        exprs.append(expr)
        if expr != TRUE:
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
        if operand == TRUE:
            return self._change(value=FALSE, sub_exprs=[operand])
        if operand == FALSE:
            return self._change(value=TRUE, sub_exprs=[operand])
    else: # '-'
        a = operand.as_ground()
        if a is not None:
            if type(a) == NumberConstant:
                return self._change(value=NumberConstant(number=str(- a.translate())), sub_exprs=[operand])
    return self._change(sub_exprs=[operand])
AUnary.update_exprs = update_exprs



# Class AAggregate #######################################################

def expand_quantifiers(self, theory):
    form = IfExpr.make(if_f=self.sub_exprs[AAggregate.CONDITION]
                , then_f=NumberConstant(number='1') if self.out is None else self.sub_exprs[AAggregate.OUT]
                , else_f=NumberConstant(number='0'))
    forms = [form.expand_quantifiers(theory)]
    for name, var in self.q_vars.items():
        if var.decl.range:
            out = []
            for f in forms:
                for val in var.decl.range:
                    new_f = f.instantiate(var, val)
                    out.append(new_f)
            forms = out
        else:
            raise Exception('Can only quantify aggregates over finite domains')
    self.vars = None # flag to indicate changes
    return self._change(sub_exprs=forms)
AAggregate.expand_quantifiers = expand_quantifiers

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


# Class AppliedSymbol, Variable #######################################################

def interpret(self, theory):
    sub_exprs = [e.interpret(theory) for e in self.sub_exprs]
    if self.decl.interpretation is not None: # has a structure
        self.is_subtence = False
        out = (self.decl.interpretation)(theory, 0, sub_exprs)
        out = self._change(simpler=out, sub_exprs=sub_exprs)
    elif self.name in theory.clark: # has a theory
        # no copying !
        self.sub_exprs = sub_exprs
        self.just_branch = theory.clark[self.name].instantiate_definition(sub_exprs, theory)
        out = self
    else:
        out = self._change(sub_exprs=sub_exprs)
    out.original = self
    return out
AppliedSymbol.interpret = interpret
Variable     .interpret = interpret

# @log  # decorator patched in by tests/main.py
def substitute(self, e0, e1, todo=None):
    """ recursively substitute e0 by e1 in self, introducing a Bracket if changed """
    global Expression_substitute

    assert not isinstance(e0, Fresh_Variable)
    if type(e1) == Fresh_Variable:
        out = copy.copy(e1)
        out.code = self.code
        return out

    new_branch = None
    if self.just_branch is not None:
        Log(f"{nl} definition:")
        new_branch = self.just_branch.substitute(e0, e1, todo)
        if todo is not None:
            todo.extend(new_branch.implicants())
            
    if self.code == e0.code:
        return self._change(value=e1, just_branch=new_branch)
    else:
        new_exprs = [e.substitute(e0, e1, todo) for e in self.sub_exprs]
        value, new_branch = None, None
        return self._change(sub_exprs=new_exprs, value=value, just_branch=new_branch)
AppliedSymbol .substitute = substitute
Variable      .substitute = substitute


# Class Fresh_Variable #######################################################

def interpret(self, theory):
    return self
Fresh_Variable.interpret = interpret

# @log  # decorator patched in by tests/main.py
def substitute(self, e0, e1, todo=None):
    return e1 if self.code == e0.code else self
Fresh_Variable.substitute = substitute

     
# Class Brackets #######################################################

def update_exprs(self, new_expr_generator):
    expr = next(new_expr_generator)
    return self._change(sub_exprs=[expr], simpler=expr, value=expr.value)
Brackets.update_exprs = update_exprs