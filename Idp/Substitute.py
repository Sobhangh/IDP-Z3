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
import functools
import itertools as it
import os
import re
import sys

from z3 import DatatypeRef, FreshConst, Or, Not, And, ForAll, Exists, Z3Exception, Sum, If, Const, BoolSort
from utils import mergeDicts, unquote, Proof, Log, nl

from typing import List, Tuple
from Idp.Expression import Constructor, Expression, IfExpr, AQuantification, BinaryOperator, \
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  \
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate, \
                    AppliedSymbol, Variable, Symbol, NumberConstant, Brackets, Arguments, \
                    Fresh_Variable, TRUE, FALSE


# class Expression ############################################################

def _replace_by(self, by, proof=Proof()):
    " replace expression by a new Brackets node, to keep annotations "
    if type(self) == Fresh_Variable or type(by) == Fresh_Variable:
        return by # no need to have brackets
    out = Brackets(f=by, annotations=self.annotations) # by is not copied !

    # copy initial annotation
    out.code = self.code
    out.is_subtence = self.is_subtence
    out.fresh_vars = self.fresh_vars
    out.is_visible = self.is_visible
    out.type = self.type
    # out.normal is not set, normally
    if type(proof) == Proof and proof:
        out.proof = copy.copy(self.proof).update(proof)
    else:
        out.proof = self.proof
    return out
Expression._replace_by = _replace_by


def _change(self, sub_exprs=None, ops=None, just_branch=None):
    " change attributes of an expression, after copying it if really changed "

    # return self if not changed
    changed = False
    if sub_exprs is not None:   changed |= self.sub_exprs != sub_exprs
    if just_branch is not None: changed = True
    if not changed: return self

    out = copy.copy(self)
    if sub_exprs is not None :  out.sub_exprs = sub_exprs
    if ops       is not None :  out.operator  = ops
    if just_branch is not None: out.just_branch = just_branch
    
    # reset derived values
    out.str = sys.intern(str(out))
    out._unknown_symbols = None
    out._subtences = None
    out.translated = None

    return out
Expression._change = _change


def update_exprs(self, new_expr_generator):
    """ change sub_exprs and simplify. """
    #  default implementation, without simplification
    return self._change(sub_exprs=list(new_expr_generator))
Expression.update_exprs = update_exprs

indent = 0
def log(function):
    def _wrapper(*args, **kwds):
        global indent
        self = args[0]
        e0   = args[1]
        e1   = args[2]
        Log( f"{nl}|------------"
             f"{nl}|{'*' if self.is_subtence else ''}{str(self)}"
          f"{f'{nl}|proof: {str(self.proof)}' if self.proof else ''}"
             f"{nl}|+ {e0.code} -> {e1.code}{f'  (or {str(e0)} -> {str(e1)})' if e0.code!=str(e0) or e1.code!=str(e1) else ''}"
             , indent)
        indent +=4
        out = function(*args, *kwds)
        indent -=4
        Log( f"{nl}|== {'*' if out.is_subtence else ''}{str(out)}"
          f"{f'{nl}|   proof: {str(out.proof)}' if out.proof else ''}"
          , indent )
        return out    
    return _wrapper

@log
def substitute(self, e0, e1, todo=None, case=None):
    """ recursively substitute e0 by e1 in self, introducing a Bracket if changed """

    if self == e0 or self.code == e0.code: # first == based on repr !
        proof = Proof(e0 if e1 in [TRUE, FALSE] or type(e1) in [NumberConstant, Constructor] else None)
        return self._replace_by(e1, proof)
    else:
        out = self.update_exprs((e.substitute(e0, e1, todo, case) for e in self.sub_exprs))
        if out.just_branch is not None:
            new_branch = out.just_branch.substitute(e0, e1, todo, case)
            if new_branch == self: # justification is satisfied
                if todo is not None:
                    todo.append((self, True, Proof(new_branch).update(new_branch.proof)))
                    self.just_branch = None
                return self._replace_by(TRUE, new_branch.proof)
            if new_branch == AUnary.make('~', self): # justification is satisfied
                if todo is not None:
                    todo.append((self, False, Proof(new_branch).update(new_branch.proof)))
                    self.just_branch = None
                return self._replace_by(FALSE, new_branch.proof)
            out = out._change(just_branch= new_branch)
            # if todo is not None:
            #     todo0 = out.just_branch.expr_to_literal(case)
            #     todo.extend(todo0)
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


def interpret(self, theory):
    " use information in structure and simplify "
    return self.update_exprs(e.interpret(theory) for e in self.sub_exprs)
Expression.interpret = interpret



# Class IfExpr ################################################################

def update_exprs(self, new_expr_generator):
    proof = Proof()
    if isinstance(new_expr_generator, list):
        new_expr_generator = iter(new_expr_generator)
    if_ = next(new_expr_generator)
    if if_ == TRUE:
        return self._replace_by(next(new_expr_generator), proof=proof.add(if_))
    elif if_ == FALSE:
        next(new_expr_generator)
        return self._replace_by(next(new_expr_generator), proof=proof.add(if_))
    else:
        then_ = next(new_expr_generator)
        else_ = next(new_expr_generator)
        if then_ == TRUE:
            if else_ == TRUE:
                return self._replace_by(TRUE, proof=proof.add(then_).add(else_))
            elif else_ == FALSE:
                return self._replace_by(if_, proof=proof.add(then_).add(else_))
        elif then_ == FALSE:
            if else_ == FALSE:
                return self._replace_by(FALSE, proof=proof.add(then_).add(else_))
            elif else_ == TRUE:
                return self._replace_by(AUnary.make('~', if_), proof=proof.add(then_).add(else_))
    return self._change(sub_exprs=[if_, then_, else_])
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
                    new_f = f.substitute(var, val)
                    new_f.proof = Proof(AComparison.make('=', [var, val])).update(new_f.proof)
                    out.append(new_f)
            forms = out
        else:
            self.vars.append(var)
    if self.q == '∀':
        out = AConjunction.make('∧', forms)
    else:
        out = ADisjunction.make('∨', forms)
    if not self.vars:
        return self._replace_by(out, proof=out.proof)
    return self._change(sub_exprs=[out])
AQuantification.expand_quantifiers = expand_quantifiers



# Class AImplication #######################################################

def update_exprs(self, new_expr_generator):
    proof = Proof()
    exprs = list(new_expr_generator)
    if len(exprs) == 2: #TODO deal with associativity
        if exprs[0] == FALSE: # (false => p) is true
            return self._replace_by(TRUE, proof=proof.add(exprs[0]))
        if exprs[0] == TRUE: # (true => p) is p
            return self._replace_by(exprs[1], proof=proof.add(exprs[0]))
        if exprs[1] == TRUE: # (p => true) is true
            return self._replace_by(TRUE, proof=proof.add(exprs[1]))
        if exprs[1] == FALSE: # (p => false) is ~p
            return self._replace_by(AUnary.make('~', exprs[0]), proof=proof.add(exprs[1]))
    return self._change(sub_exprs=exprs)
AImplication.update_exprs = update_exprs



# Class AEquivalence #######################################################

def update_exprs(self, new_expr_generator):
    proof = Proof()
    exprs = list(new_expr_generator)
    for e in exprs:
        if e == TRUE:
            return self._replace_by(AConjunction.make('∧', exprs, self.is_subtence), 
                                    proof.add(e))
        if e == FALSE:
            return self._replace_by(AConjunction.make('∧', [AUnary.make('~', e) for e in exprs], self.is_subtence), 
                                    proof.add(e))
    return self._change(sub_exprs=exprs)
AEquivalence.update_exprs = update_exprs



# Class ADisjunction #######################################################

def update_exprs(self, new_expr_generator):
    # self = sub_exprs | not(disjunct of self.proof)
    
    exprs, is_true = [], False
    for expr in new_expr_generator:
        if expr == TRUE:
            # reset proof
            self.proof = Proof()
            return self._replace_by(TRUE, proof=self.proof.add(expr))
        if expr == FALSE: self.proof.add(expr)
        elif type(expr) == ADisjunction: # flatten
            for e in expr.sub_exprs:
                if e == TRUE:
                    # reset proof
                    self.proof = Proof()
                    return self._replace_by(TRUE, proof=self.proof.add(expr))
                elif e == FALSE: self.proof.add(expr)
                else:
                    exprs.append(e)
        else:
            exprs.append(expr)
            
    if len(exprs) == 0:
        return self._replace_by(FALSE, proof=self.proof)
    return self._change(sub_exprs=exprs)
ADisjunction.update_exprs = update_exprs



# Class AConjunction #######################################################

# same as ADisjunction, with TRUE and FALSE swapped
def update_exprs(self, new_expr_generator):
    # self = sub_exprs & not(conjunct of self.proof)
    
    exprs, is_false = [], False
    for expr in new_expr_generator:
        if expr == TRUE:    self.proof.add(expr)
        elif expr == FALSE: 
            # reset proof
            self.proof = Proof()
            return self._replace_by(FALSE, proof=self.proof.add(expr))
        elif type(expr) == AConjunction: # flatten
            for e in expr.sub_exprs:
                if e == TRUE:    self.proof.add(expr)
                elif e == FALSE: 
                    # reset proof
                    self.proof = Proof()
                    return self._replace_by(FALSE, proof=self.proof.add(expr))
                else:
                    exprs.append(e)
        else:
            exprs.append(expr)

    if len(exprs) == 0:
        return self._replace_by(TRUE, proof=self.proof)
    return self._change(sub_exprs=exprs)
AConjunction.update_exprs = update_exprs



# Class AComparison #######################################################

def update_exprs(self, new_expr_generator):
    operands = list(new_expr_generator)
    operands1 = [e.as_ground() for e in operands]
    if all(e is not None for e in operands1):
        self.proof.extend(operands)
        acc = operands1[0]
        assert len(self.operator) == len(operands1[1:]), "Internal error"
        for op, expr in zip(self.operator, operands1[1:]):
            if not (BinaryOperator.MAP[op]) (acc.translate(), expr.translate()):
                return self._replace_by(FALSE)
            acc = expr
        return self._replace_by(TRUE)
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
            self.proof.add(expr)
            self.proof.add(expr1)
            if op == '+':
                acc += expr1.translate()
            elif op == '-':
                acc -= expr1.translate()
            elif op == '*':
                acc *= expr1.translate()
            elif op == '/':
                if isinstance(acc, int) and expr.type == 'int': # integer division
                    acc //= expr1.translate()
                else:
                    acc /= expr1.translate()
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
        return self._change(ZERO)
    elif 0 < len(exprs) and ((ops[0] == '+' and acc == 0) or (ops[0] == '*' and acc == 1)):
        del ops[0]
    else:
        exprs = [NumberConstant(number=str(acc))] + exprs
    if len(exprs)==1:
        return self._replace_by(exprs[0])
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
            self.proof.extend(operands)
            out = operands1[0].translate() % operands1[1].translate()
            return self._replace_by(NumberConstant(number=str(out)))
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
        self.proof.extend(operands)
        out = operands1[0].translate() ** operands1[1].translate()
        return self._replace_by(NumberConstant(number=str(out)))
    else:
        return self._change(sub_exprs=operands)
APower.update_exprs = update_exprs



# Class AUnary #######################################################

def update_exprs(self, new_expr_generator):
    operand = list(new_expr_generator)[0]
    proof = operand.proof
    if self.operator == '~':
        if operand == TRUE:
            return self._replace_by(FALSE, proof)
        if operand == FALSE:
            return self._replace_by(TRUE, proof)
    else: # '-'
        a = operand.as_ground()
        if a is not None:
            if type(a) == NumberConstant:
                return self._replace_by(NumberConstant(number=str(- a.translate())))
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
            out = []
            for f in forms:
                for val in var.decl.range:
                    new_f = f.substitute(var, val)
                    new_f.proof = Proof(AComparison.make('=', [var, val])).update(new_f.proof)
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
        self.proof.extend(operands)
        acc = 0
        for expr, expr1 in zip(operands, operands1):
            if expr1 is not None:
                acc += expr1.translate() if self.aggtype == 'sum' else 1
            else:
                exprs.add(expr)
        out = NumberConstant(number=str(acc))
        out.proof = self.proof
        return self._replace_by(out, proof=self.proof)

    return self
AAggregate.update_exprs = update_exprs


# Class AppliedSymbol #######################################################

def interpret(self, theory):
    sub_exprs = [e.interpret(theory) for e in self.sub_exprs]
    if self.decl.interpretation is not None: # has a structure
        self.is_subtence = False
        out = (self.decl.interpretation)(theory, 0, sub_exprs)
        proof = Proof(AComparison.make('=', [self, out])).update(self.proof)
        return self._replace_by(out, proof=proof)
    elif self.name in theory.clark: # has a theory
        # no copying !
        self.sub_exprs = sub_exprs
        self.just_branch = theory.clark[self.name].instantiate_definition(sub_exprs, theory)
        return self
    else:
        return self
AppliedSymbol.interpret = interpret


     
# Class Brackets #######################################################

def update_exprs(self, new_expr_generator):
    expr = next(new_expr_generator)
    self.proof = self.proof.update(expr.proof)
    return self._change(sub_exprs=[expr])
Brackets.update_exprs = update_exprs