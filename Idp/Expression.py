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

import copy
import functools
import itertools as it
import os
import re
import sys

from z3 import DatatypeRef, FreshConst, Or, Not, And, ForAll, Exists, Z3Exception, Sum, If, Const, BoolSort
from utils import mergeDicts, unquote

from typing import List, Tuple


class DSLException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message


class Expression(object):
    COUNT = 0
    # .sub_exprs : list of (transformed) Expression, to be translated to Z3
    def __init__(self):
        self.code = sys.intern(self.str_())# normalized idp code, before transformations
        self.str = self.code              # memoization of str()
        self.annotations = {'reading': self.code} # dict(String, String)
        self.is_subtence = None           # True if sub-sentence in original code
        self.fresh_vars = None            # Set[String]
        self.type = None                  # a declaration object, or 'bool', 'real', 'int', or None
        self._unknown_symbols = None      # list of uninterpreted symbols not starting with '_'
        self.is_visible = None            # is shown to user -> need to find whether it is a consequence
        self.translated = None            # the Z3 equivalent
        self._reified = None
        self.if_symbol = None             # (string) this constraint is relevant if Symbol is relevant
        self._subtences = None            # memoization of .subtences()
        self.justification = None         # Expression
        # .normal : only set in .instances

    def __eq__(self, other):
        if isinstance(self, Brackets):
            return self.sub_exprs[0] == other
        if isinstance(other, Brackets):
            return self == other.sub_exprs[0]
        # beware: this does not ignore meaningless brackets deeper in the tree
        return self.str == other.str
    
    def __hash__(self):
        return hash(self.code)

    def mark_subtences(self):
        self.fresh_vars = set()
        for e in self.sub_exprs: 
            e.mark_subtences()
            self.fresh_vars = self.fresh_vars.union(e.fresh_vars)
        self.is_subtence = False # by default
        return self

    def subtences(self):
        if self._subtences is None:
            self._subtences = {}
            if self.is_subtence:
                self._subtences[self.code]= self
            self._subtences.update(mergeDicts(e.subtences() for e in self.sub_exprs))
            if self.justification is not None:
                self._subtences.update(self.justification.subtences())
        return self._subtences

    def as_ground(self): return None


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

    def update_exprs(self, new_expr_generator):
        """ change sub_exprs and simplify. """
        #  default implementation 
        return self._change(sub_exprs=list(new_expr_generator))

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

    def simplify1(self):
        return self.update_exprs(iter(self.sub_exprs))

    def expand_quantifiers(self, theory):
        return self.update_exprs(e.expand_quantifiers(theory) for e in self.sub_exprs)

    def interpret(self, theory):
        return self.update_exprs(e.interpret(theory) for e in self.sub_exprs)

    def unknown_symbols(self):
        if self._unknown_symbols is None:
            self._unknown_symbols = mergeDicts(e.unknown_symbols() for e in self.sub_exprs) \
                if self.if_symbol is None else {}
            if self.justification is not None:
                self._unknown_symbols.update(self.justification.unknown_symbols())
        return self._unknown_symbols

    def reified(self) -> DatatypeRef:
        if self._reified is None:
            if self.type == 'bool':
                self._reified = Const('*'+str(Expression.COUNT), BoolSort())
                Expression.COUNT += 1
            else:
                self._reified = self.translate()
        return self._reified

    def has_environmental(self, truth):
        # returns true if it contains a variable whose environmental property is 'truth
        return any(e.has_environmental(truth) for e in self.sub_exprs)
    
    def justifications(self):
        out = sum((e.justifications() for e in self.sub_exprs), [])
        if self.justification is not None:
            out.append(self.justification)
            out.extend(self.justification.justifications())
        return out

    def expr_to_literal(self, case: 'Case', truth: bool = True) -> List[Tuple['Expression', bool]]:
        # returns a literal for the matching atom in case.assignments, or []
        if self.code in case.assignments: # found it !
            return [(self, truth)]
        if isinstance(self, Brackets):
            return self.sub_exprs[0].expr_to_literal(case, truth)
        if isinstance(self, AUnary) and self.operator == '~':
            return self.sub_exprs[0].expr_to_literal(case, not truth )
        if truth and isinstance(self, AConjunction):
            return [l for e in self.sub_exprs for l in e.expr_to_literal(case, truth)]
        if not truth and isinstance(self, ADisjunction):
            return [l for e in self.sub_exprs for l in e.expr_to_literal(case, truth)]
        return []

class Constructor(Expression):
    def __init__(self, **kwargs):
        self.name = unquote(kwargs.pop('name'))
        self.is_var = False
        self.sub_exprs = []
        self.index = None # int

        super().__init__()
    
    def __str__(self): return self.name
    def str_   (self): return self.name
    def annotate(self, symbol_decls, q_vars): return self
    def as_ground(self): return self.index
    def translate(self): return self.translated

TRUE  = Constructor(name='true')
FALSE = Constructor(name='false')


class IfExpr(Expression):
    IF = 0
    THEN = 1
    ELSE = 2

    def __init__(self, **kwargs):
        self.if_f = kwargs.pop('if_f')
        self.then_f = kwargs.pop('then_f')
        self.else_f = kwargs.pop('else_f')

        self.sub_exprs = [self.if_f, self.then_f, self.else_f]
        super().__init__()

    def __str__(self):
        return ( f" if   {str(self.sub_exprs[IfExpr.IF  ])}"
                 f" then {str(self.sub_exprs[IfExpr.THEN])}"
                 f" else {str(self.sub_exprs[IfExpr.ELSE])}" )
    def str_(self):
        return ( f" if   {self.sub_exprs[IfExpr.IF  ].str}"
                 f" then {self.sub_exprs[IfExpr.THEN].str}"
                 f" else {self.sub_exprs[IfExpr.ELSE].str}" )

    def annotate(self, symbol_decls, q_vars):
        self.sub_exprs = [e.annotate(symbol_decls, q_vars) for e in self.sub_exprs]
        #TODO verify consistency
        self.type = self.sub_exprs[IfExpr.THEN].type
        return self

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

    def translate(self):
        if self.translated is None:
            self.translated =  If(self.sub_exprs[IfExpr.IF  ].translate()
                                , self.sub_exprs[IfExpr.THEN].translate()
                                , self.sub_exprs[IfExpr.ELSE].translate())
        return self.translated

class AQuantification(Expression):
    def __init__(self, **kwargs):
        self.q = kwargs.pop('q')
        self.q = '∀' if self.q == '!' else '∃' if self.q == "?" else self.q
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.f = kwargs.pop('f')

        self.sub_exprs = [self.f]
        super().__init__()

        self.q_vars = {} # dict[String, Fresh_Variable]
        self.type = 'bool'

    @classmethod
    def make(cls, q, decls, f, is_subtence=False):
        "make and annotate a quantified formula"
        out = cls(q=q, vars=list(decls.values()), sorts=[], f=f)
        out.q_vars = decls
        out.is_subtence = is_subtence
        return out


    def __str__(self):
        assert len(self.vars) == len(self.sorts), "Internal error"
        vars = ''.join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
        return f"{self.q}{vars} : {str(self.sub_exprs[0])}"
    def str_(self):
        # assert len(self.vars) == len(self.sorts), "Internal error"
        vars = ''.join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
        return f"{self.q}{vars} : {self.sub_exprs[0].str}"

    def annotate(self, symbol_decls, q_vars):
        assert len(self.vars) == len(self.sorts), "Internal error"
        self.q_vars = {v:s.fresh(v, symbol_decls) \
                        for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_vars, **self.q_vars} # merge
        self.sub_exprs = [e.annotate(symbol_decls, q_v) for e in self.sub_exprs]
        return self

    def mark_subtences(self):
        super().mark_subtences()
        # remove q_vars
        self.fresh_vars = self.fresh_vars.difference(set(self.q_vars.keys()))
        self.is_subtence = (len(self.fresh_vars)==0)
        return self

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

    def translate(self):
        if self.translated is None:
            for v in self.q_vars.values():
                v.translate()
            if not self.vars:
                self.translated = self.sub_exprs[0].translate()
            else:
                finalvars, forms = self.vars, [f.translate() for f in self.sub_exprs]

                if self.q == '∀':
                    forms = And(forms) if 1<len(forms) else forms[0]
                    if len(finalvars) > 0: # not fully expanded !
                        forms = ForAll(finalvars, forms)
                else:
                    forms = Or(forms) if 1<len(forms) else forms[0]
                    if len(finalvars) > 0: # not fully expanded !
                        forms = Exists(finalvars, forms)
                self.translated = forms
        return self.translated

class BinaryOperator(Expression):
    MAP = { '∧': lambda x, y: And(x, y),
            '∨': lambda x, y: Or(x, y),
            '⇒': lambda x, y: Or(Not(x), y),
            '⇐': lambda x, y: Or(x, Not(y)),
            '⇔': lambda x, y: x == y,
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '%': lambda x, y: x % y,
            '^': lambda x, y: x ** y,
            '=': lambda x, y: x == y,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '≤': lambda x, y: x <= y,
            '≥': lambda x, y: x >= y,
            '≠': lambda x, y: x != y
            }

    def __init__(self, **kwargs):
        self.sub_exprs = kwargs.pop('sub_exprs')
        self.operator = kwargs.pop('operator')

        self.operator = list(map(
            lambda op: "≤" if op == "=<" else "≥" if op == ">=" else "≠" if op == "~=" else \
                "⇔" if op == "<=>" else "⇐" if op == "<=" else "⇒" if op == "=>" else \
                "∨" if op == "|" else "∧" if op == "&" else op
            , self.operator))

        super().__init__()

        self.type = 'bool' if self.operator[0] in '&|∧∨⇒⇐⇔' \
               else 'bool' if self.operator[0] in '=<>≤≥≠' \
               else None

    @classmethod
    def make(cls, ops, operands, is_subtence=False):
        """ creates a BinaryOp
            beware: cls must be specific for ops !"""
        if len(operands) == 1:
            return operands[0]
        if isinstance(ops, str):
            ops = [ops] * (len(operands)-1)
        operands1 = []
        for o in operands:
            if type(o) not in [Constructor, AppliedSymbol, Variable, Symbol, Fresh_Variable, NumberConstant, Brackets, AComparison]:
                # add () around operands, to avoid ambiguity in str()
                o = Brackets(f=o, annotations={'reading': None})
            operands1.append(o)
        out = (cls)(sub_exprs=operands1, operator=ops)
        out.is_subtence = is_subtence
        return out._derive().simplify1()
        
    def __str__(self):
        def parenthesis(x):
            # add () around operands, to avoid ambiguity in str()
            if type(x) not in [Constructor, AppliedSymbol, Variable, Symbol, Fresh_Variable, NumberConstant, Brackets]:
                return f"({str(x)})"
            else:
                return f"{str(x)}"
        temp = parenthesis(self.sub_exprs[0])
        for i in range(1, len(self.sub_exprs)):
            temp += f" {self.operator[i-1]} {parenthesis(self.sub_exprs[i])}"
        return temp
    def str_(self):
        def parenthesis(x):
            # add () around operands, to avoid ambiguity in str()
            if type(x) not in [Constructor, AppliedSymbol, Variable, Symbol, Fresh_Variable, NumberConstant, Brackets]:
                return f"({x.str})"
            else:
                return f"{x.str}"
        temp = parenthesis(self.sub_exprs[0])
        for i in range(1, len(self.sub_exprs)):
            temp += f" {self.operator[i-1]} {parenthesis(self.sub_exprs[i])}"
        return temp

    def annotate(self, symbol_decls, q_vars):
        self.sub_exprs = [e.annotate(symbol_decls, q_vars) for e in self.sub_exprs]
        return self._derive()
    
    def _derive(self):
        if self.type is None:
            self.type = 'real' if any(e.type == 'real' for e in self.sub_exprs) \
               else 'int'
        return self

    def mark_subtences(self):
        super().mark_subtences()
        if self.operator[0] in '=<>≤≥≠':
            self.is_subtence = (len(self.fresh_vars)==0)
            self.fresh_vars.discard('!*') # indicates AppliedSymbol with complex expressions
        return self

    def translate(self):
        if self.translated is None:
            # chained comparisons -> And()
            if self.operator[0] =='≠' and len(self.sub_exprs)==2:
                x = self.sub_exprs[0].translate()
                y = self.sub_exprs[1].translate()
                out = Not(x==y)
            elif self.operator[0] in '=<>≤≥≠':
                out = []
                for i in range(1, len(self.sub_exprs)):
                    x = self.sub_exprs[i-1].translate()
                    function = BinaryOperator.MAP[self.operator[i - 1]]
                    y = self.sub_exprs[i].translate()
                    try:
                        out = out + [function(x, y)]
                    except Z3Exception as E:
                        raise DSLException("{}{}{}".format(str(x), self.operator[i - 1], str(y)))
                if 1 < len(out):
                    out = And(out)
                else:
                    out = out[0]
            elif self.operator[0] == '∧':
                out = And([e.translate() for e in self.sub_exprs])
            elif self.operator[0] == '∨':
                out = Or ([e.translate() for e in self.sub_exprs])
            else:
                out = self.sub_exprs[0].translate()

                for i in range(1, len(self.sub_exprs)):
                    function = BinaryOperator.MAP[self.operator[i - 1]]
                    out = function(out, self.sub_exprs[i].translate())
            self.translated = out
        return self.translated

class AImplication(BinaryOperator):

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
        
class AEquivalence(BinaryOperator):

    def update_exprs(self, new_expr_generator): 
        exprs = list(new_expr_generator)
        if any(e == TRUE for e in exprs):
            return self._change(by=AConjunction.make('∧', exprs))
        if any(e == FALSE for e in exprs):
            return self._change(by=AConjunction.make('∧', [AUnary.make('~', e) for e in exprs]))
        return self._change(sub_exprs=exprs)
    
class ARImplication(BinaryOperator):
    def annotate(self, symbol_decls, q_vars):
        # reverse the implication
        self.sub_exprs.reverse()
        out = AImplication(sub_exprs=self.sub_exprs, operator=['⇒']*len(self.operator))
        return out.annotate(symbol_decls, q_vars)

class ADisjunction(BinaryOperator):

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
        
class AConjunction(BinaryOperator):

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

class AComparison(BinaryOperator):
    def annotate(self, symbol_decls, q_vars):
        # a≠b --> Not(a=b)
        if len(self.sub_exprs) == 2 and self.operator == ['≠']:
            out = AUnary.make('~', AComparison(sub_exprs=self.sub_exprs, operator='='))
            return out.annotate(symbol_decls, q_vars)
        return super().annotate(symbol_decls, q_vars)

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


class ASumMinus(BinaryOperator):

    def update_exprs(self, new_expr_generator):
        return update_arith(self, '+', new_expr_generator)

class AMultDiv(BinaryOperator):

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

class APower(BinaryOperator):

    def update_exprs(self, new_expr_generator):
        operands = list(new_expr_generator)
        operands1 = [e.as_ground() for e in operands]
        if len(operands) == 2 \
        and all(e is not None for e in operands1):
            out = operands1[0] ** operands1[1]
            return self._change(by=NumberConstant(number=str(out)))
        else:
            return self._change(sub_exprs=operands)

class AUnary(Expression):
    MAP = {'-': lambda x: 0 - x,
           '~': lambda x: Not(x)
          }
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.operator = kwargs.pop('operator')

        self.sub_exprs = [self.f]
        super().__init__()

    @classmethod
    def make(cls, op, expr, is_subtence=False):
        out = AUnary(operator=op, f=expr)
        out.is_subtence = is_subtence
        return out._derive().simplify1()

    def __str__(self):
        return f"{self.operator}({str(self.sub_exprs[0])})"
    def str_(self):
        return f"{self.operator}({self.sub_exprs[0].str})"

    def annotate(self, symbol_decls, q_vars):
        self.sub_exprs = [e.annotate(symbol_decls, q_vars) for e in self.sub_exprs]
        self.type = self.sub_exprs[0].type
        return self._derive()

    def _derive(self):
        self.type = self.sub_exprs[0].type
        return self

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

    def translate(self):
        if self.translated is None:
            out = self.sub_exprs[0].translate()
            function = AUnary.MAP[self.operator]
            self.translated = function(out)
        return self.translated

class AAggregate(Expression):
    CONDITION = 0
    OUT = 1

    def __init__(self, **kwargs):
        self.aggtype = kwargs.pop('aggtype')
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.f = kwargs.pop('f')
        self.out = kwargs.pop('out')

        self.sub_exprs = [self.f, self.out] if self.out else [self.f] # later: expressions to be summed
        super().__init__()

        self.q_vars = {}

        if self.aggtype == "sum" and self.out is None:
            raise Exception("Must have output variable for sum")
        if self.aggtype != "sum" and self.out is not None:
            raise Exception("Can't have output variable for #")

    def __str__(self):
        if self.vars is not None:
            assert len(self.vars) == len(self.sorts), "Internal error"
            vars = "".join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
            output = f" : {str(self.sub_exprs[AAggregate.OUT])}" if self.out else ""
            out = ( f"{self.aggtype}{{{vars} : "
                    f"{str(self.sub_exprs[AAggregate.CONDITION])}"
                    f"{output}}}"
                )
        else:
            out = ( f"{self.aggtype}{{"
                    f"{','.join(str(e) for e in self.sub_exprs)}"
                    f"}}"
            )
        return out
    def str_(self):
        assert len(self.vars) == len(self.sorts), "Internal error"
        vars = "".join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
        output = f" : {self.sub_exprs[AAggregate.OUT].str}" if self.out else ""
        out = ( f"{self.aggtype}{{{vars} : "
                f"{self.sub_exprs[AAggregate.CONDITION].str}"
                f"{output}}}"
              )
        return out

    def annotate(self, symbol_decls, q_vars):
        assert len(self.vars) == len(self.sorts), "Internal error"
        self.q_vars = {v:s.fresh(v, symbol_decls) \
                        for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_vars, **self.q_vars} # merge
        self.sub_exprs = [e.annotate(symbol_decls, q_v) for e in self.sub_exprs]
        self.type = self.sub_exprs[AAggregate.OUT].type if self.out else 'int'
        return self

    def mark_subtences(self):
        super().mark_subtences()
        # remove q_vars
        self.fresh_vars = self.fresh_vars.difference(set(self.q_vars.keys()))
        return self

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

    def translate(self):
        if self.translated is None:
            for v in self.q_vars.values():
                v.translate()
            self.translated = Sum([f.translate() for f in self.sub_exprs])
        return self.translated


class AppliedSymbol(Expression):
    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')

        self.sub_exprs = self.args.sub_exprs
        super().__init__()

        self.decl = None
        self.name = self.s.name

    @classmethod
    def make(cls, s, args, is_subtence=False):
        if 0 < len(args):
            out = cls(s=Symbol(name=s.name), args=Arguments(sub_exprs=args))
            out.sub_exprs = args
        else:
            out = Variable(name=s.name)
        # annotate
        out.decl = s.decl
        out.is_subtence = is_subtence
        return out._derive()

    def __str__(self):
        return f"{str(self.s)}({','.join([str(x) for x in self.sub_exprs])})"
    def str_(self):
        return f"{self.s.str}({','.join([x.str for x in self.sub_exprs])})"

    def annotate(self, symbol_decls, q_vars):
        self.sub_exprs = [e.annotate(symbol_decls, q_vars) for e in self.sub_exprs]
        self.decl = q_vars[self.s.name].decl if self.s.name in q_vars else symbol_decls[self.s.name]
        self.normal = True
        return self._derive()

    def mark_subtences(self):
        super().mark_subtences()
        if any(type(e) in [Brackets, AppliedSymbol, AUnary, BinaryOperator] for e in self.sub_exprs):
            self.is_subtence = False
            if self.type == 'bool':
                self.fresh_vars.discard('!*')
            else:
                self.fresh_vars.add('!*')
        else:
            self.is_subtence = self.type == 'bool' and len(self.fresh_vars)==0
        return self

    def _derive(self):
        self.type = self.decl.type.name
        return self

    def interpret(self, theory):
        sub_exprs = [e.interpret(theory) for e in self.sub_exprs]
        if self.decl.interpretation is not None: # has a structure
            self.is_subtence = False
            out = (self.decl.interpretation)(theory, 0, sub_exprs)
            return self._change(by=out)
        elif self.name in theory.clark: # has a theory
            self.justification = theory.clark[self.name].instantiate(self.sub_exprs, theory)
            return self
        else:
            return self

    def unknown_symbols(self):
        out = super().unknown_symbols()
        if self.decl.interpretation is None:
            out[self.decl.name] = self.decl
        return out
        
    def translate(self):
        if self.translated is None:
            if self.s.name == 'abs':
                arg = self.sub_exprs[0].translate()
                self.translated = If(arg >= 0, arg, -arg)
            else:
                arg = [x.translate() for x in self.sub_exprs]
                self.translated = (self.decl.translated)(arg)
        return self.translated

    def has_environmental(self, truth):
        return self.decl.environmental == truth \
            or any(e.has_environmental(truth) for e in self.sub_exprs)

class Arguments(object):
    def __init__(self, **kwargs):
        self.sub_exprs = kwargs.pop('sub_exprs')
        super().__init__()

class Variable(AppliedSymbol):
    def __init__(self, **kwargs):
        self.name = unquote(kwargs.pop('name'))

        Expression.__init__(self)

        self.sub_exprs = []
        self.decl = None

    def __str__(self): return self.name
    def str_   (self): return self.name

    def annotate(self, symbol_decls, q_vars):
        if self.name in symbol_decls and type(symbol_decls[self.name]) == Constructor:
            return symbol_decls[self.name]
        if self.name in q_vars:
            return q_vars[self.name]
        else: # in symbol_decls
            self.decl = symbol_decls[self.name]
            self.type = self.decl.type.name
            self.normal = True # make sure it is visible in GUI
        return self

    def mark_subtences(self):
        self.fresh_vars = set()
        self.is_subtence = self.type == 'bool'
        return self

    def reified(self):
        return self.translate()

    def translate(self):
        if self.translated is None:
            self.translated = self.decl.translated
        return self.translated
    
class Symbol(Variable): pass
    

class Fresh_Variable(Expression):
    def __init__(self, name, decl):
        self.name = name
        self.decl = decl

        super().__init__()

        self.type = self.decl.name
        self._unknown_symbols = {}
        self.sub_exprs = []

    def __str__(self): return self.name
    def str_   (self): return self.name

    def annotate(self, symbol_decls, q_vars):
        return self

    def mark_subtences(self):
        self.fresh_vars = set([self.name])
        return self

    def translate(self):
        if self.translated is None:
            self.translated = FreshConst(self.decl.out.decl.translated)
        return self.translated

class NumberConstant(Expression):
    def __init__(self, **kwargs):
        self.number = kwargs.pop('number')

        super().__init__()

        self.sub_exprs = []
        try:
            self.translated = int(self.number)
            self.type = 'int'
        except ValueError:
            self.translated = float(eval(self.number))
            self.type = 'real'
    
    def __str__(self): return self.number
    def str_   (self): return self.number

    def as_ground(self): return self.translated

    def annotate(self, symbol_decls, q_vars): return self

    def translate(self):
        return self.translated

ZERO = NumberConstant(number='0')
ONE  = NumberConstant(number='1')

class Brackets(Expression):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        annotations = kwargs.pop('annotations')
        self.sub_exprs = [self.f]

        super().__init__()
        if type(annotations) == dict:
            self.annotations = annotations
        elif annotations is None:
            self.annotations['reading'] = None
        else: # Annotations instance
            self.annotations = annotations.annotations

    def __str__(self): return f"({str(self.sub_exprs[0])})"
    def str_   (self): return f"({self.sub_exprs[0].str})"

    def as_ground(self): 
        return self.sub_exprs[0].as_ground()

    def annotate(self, symbol_decls, q_vars):
        self.sub_exprs = [self.sub_exprs[0].annotate(symbol_decls, q_vars)]
        self.type = self.sub_exprs[0].type
        if self.annotations['reading']:
            self.sub_exprs[0].annotations = self.annotations
        return self

    def update_exprs(self, new_expr_generator):
        expr = next(new_expr_generator)
        return self._change(sub_exprs=[expr])

    def translate(self):
        self.translated = self.sub_exprs[0].translate()
        return self.translated

