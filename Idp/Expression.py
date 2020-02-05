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

from z3 import FreshConst, Or, Not, And, ForAll, Exists, Z3Exception, Sum, If, Const, BoolSort
from utils import mergeDicts



class DSLException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def immutable(func):
    @functools.wraps(func)
    def wrapper_decorator(self, new_expr_generator):
        if isinstance(new_expr_generator, list):
            new_expr_generator = iter(new_expr_generator)
        value, ops = func(self, new_expr_generator), None
        if isinstance(value, tuple):
            ops = value[1]
            value = value[0]
        if isinstance(value, list):
            if all(id(e0) == id(e1) for (e0,e1) in zip(self.sub_exprs, value)): # not changed !
                return self
            else: # create a modified copy
                out = copy.copy(self)
                out.sub_exprs = value
                # reset derived values
                out.str = sys.intern(str(out))
                out._unknown_symbols = None
                out._subtences = None
                out.translated = None
                if ops: out.operator = ops
                return out
        if id(value) == id(self): # not changed !
            return self
        return self.substitute(self, value)
    return wrapper_decorator
        
class Expression(object):
    COUNT = 0
    # .sub_exprs : list of (transformed) Expression, to be translated to Z3
    def __init__(self):
        self.code = sys.intern(self.str_())# normalized idp code, before transformations
        self.str = self.code              # memoization of str()
        self.reading = self.code          # English reading
        self.is_subtence = None           # True if sub-sentence in original code
        self.type = None                  # a declaration object, or 'bool', 'real', 'int', or None
        self._unknown_symbols = None      # list of uninterpreted symbols not starting with '_'
        self.is_visible = None            # is shown to user -> need to find whether it is a consequence
        self.translated = None            # the Z3 equivalent
        self._reified = None
        self.if_symbol = None             # (string) this constraint is relevant if Symbol is relevant
        self._subtences = None            # memoization of .subtences()
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

    def subtences(self):
        if self._subtences is None:
            if self.is_subtence:
                self._subtences = {self.code: self} #TODO possibly go deeper
            else:
                self._subtences = mergeDicts(e.subtences() for e in self.sub_exprs)
        return self._subtences

    def as_ground(self): return None

    @immutable
    def update_exprs(self, new_expr_generator):
        return list(new_expr_generator)

    def substitute(self, e0, e1):
        if self == e0: # based on repr !
            if type(e0) == Fresh_Variable:
                return e1 # no need to have brackets
            # replace by new Brackets node, to keep annotations
            e1.is_subtence = self.is_subtence
            out = Brackets(f=e1, reading=self.reading)
            # copy initial annotation
            out.code = self.code
            out.is_subtence = self.is_subtence
            out.is_visible = self.is_visible
            out.type = self.type
            # out.normal is not set, normally
            return out
        else:
            return self.update_exprs(e.substitute(e0, e1) for e in self.sub_exprs)

    def simplify1(self):
        return self.update_exprs(self.sub_exprs)

    def expand_quantifiers(self, theory):
        return self.update_exprs(e.expand_quantifiers(theory) for e in self.sub_exprs)

    def interpret(self, theory):
        return self.update_exprs(e.interpret(theory) for e in self.sub_exprs)

    def unknown_symbols(self):
        if self._unknown_symbols is None:
            self._unknown_symbols = mergeDicts(e.unknown_symbols() for e in self.sub_exprs) \
                if self.if_symbol is None else {}
        return self._unknown_symbols

    def reified(self):
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

class Constructor(Expression):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.is_var = False
        self.sub_exprs = []
        self.index = None # int

        super().__init__()
        
        self.is_subtence = False
    
    def __str__(self): return self.name
    def str_   (self): return self.name
    def annotate(self, symbol_decls, q_decls): return self
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

        self.is_subtence = False

    def __str__(self):
        return ( f" if   {str(self.sub_exprs[IfExpr.IF  ])}"
                 f" then {str(self.sub_exprs[IfExpr.THEN])}"
                 f" else {str(self.sub_exprs[IfExpr.ELSE])}" )
    def str_(self):
        return ( f" if   {self.sub_exprs[IfExpr.IF  ].str}"
                 f" then {self.sub_exprs[IfExpr.THEN].str}"
                 f" else {self.sub_exprs[IfExpr.ELSE].str}" )

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        #TODO verify consistency
        self.type = self.sub_exprs[IfExpr.THEN].type
        return self

    @immutable
    def update_exprs(self, new_expr_generator):
        if_ = next(new_expr_generator)
        if if_ == TRUE:
            return next(new_expr_generator)
        elif if_ == FALSE:
            next(new_expr_generator)
            return next(new_expr_generator)
        else:
            then_ = next(new_expr_generator)
            else_ = next(new_expr_generator)
            if then_ == TRUE:
                if else_ == TRUE:
                    return TRUE
                elif else_ == FALSE:
                    return if_
            elif then_ == FALSE:
                if else_ == FALSE:
                    return FALSE
                elif else_ == TRUE:
                    return NOT(if_)
        return [if_, then_, else_]

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

        self.q_decls = {}
        self.type = 'bool'
        self.is_subtence = True

    def __str__(self):
        vars = ''.join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
        return f"{self.q}{vars} : {str(self.sub_exprs[0])}"
    def str_(self):
        vars = ''.join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
        return f"{self.q}{vars} : {self.sub_exprs[0].str}"

    def annotate(self, symbol_decls, q_decls):
        self.q_decls = {v:Fresh_Variable(v, symbol_decls[s.name]) \
                        for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_decls, **self.q_decls} # merge
        self.sub_exprs = [e.annotate(symbol_decls, q_v) for e in self.sub_exprs]
        return self

    @immutable
    def expand_quantifiers(self, theory):
        forms = [self.sub_exprs[0].expand_quantifiers(theory)]
        self.vars = []
        self.sorts = [] # not used
        for name, var in self.q_decls.items():
            if var.decl.range:
                forms = [f.substitute(var, val) for val in var.decl.range for f in forms]
            else:
                self.vars.append(var)
        op = '∧' if self.q == '∀' else '∨'
        out = operation(op, forms)
        return out if not self.vars else [out]

    def translate(self):
        if self.translated is None:
            for v in self.q_decls.values():
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

        self.is_subtence = self.operator[0] in '=<>≤≥≠'

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

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        if self.type is None:
            self.type = 'real' if any(e.type == 'real' for e in self.sub_exprs) \
               else 'int'
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

    @immutable
    def update_exprs(self, new_expr_generator): 
        exprs = list(new_expr_generator)
        if len(exprs) == 2: #TODO deal with associativity
            if exprs[0] == FALSE: # (false => p) is true
                return TRUE
            if exprs[0] == TRUE: # (true => p) is p
                return exprs[1]
            if exprs[1] == TRUE: # (p => true) is true
                return TRUE
            if exprs[1] == FALSE: # (p => false) is ~p
                return NOT(exprs[0])
        return exprs
        
class AEquivalence(BinaryOperator):

    @immutable
    def update_exprs(self, new_expr_generator): 
        exprs = list(new_expr_generator)
        if any(e == TRUE for e in exprs):
            return operation('∧', exprs)
        if any(e == FALSE for e in exprs):
            return operation('∧', [NOT(e) for e in exprs])
        return exprs
    
class ARImplication(BinaryOperator):
    def annotate(self, symbol_decls, q_decls):
        # reverse the implication
        self.sub_exprs.reverse()
        out = AImplication(sub_exprs=self.sub_exprs, operator=['⇒']*len(self.operator))
        return out.annotate(symbol_decls, q_decls)

class ADisjunction(BinaryOperator):

    @immutable
    def update_exprs(self, new_expr_generator):
        exprs = []
        for expr in new_expr_generator:
            if expr == TRUE:
                return TRUE
            if expr == FALSE:
                pass
            else:
                exprs.append(expr)
        if len(exprs) == 0:
            return FALSE
        if len(exprs) == 1:
            return exprs[0]
        return exprs
        
class AConjunction(BinaryOperator):

    @immutable
    def update_exprs(self, new_expr_generator):
        exprs = []
        for expr in new_expr_generator:
            if expr == TRUE:
                pass
            elif expr == FALSE:
                return FALSE
            else:
                exprs.append(expr)
        if len(exprs) == 0:
            return TRUE
        if len(exprs) == 1:
            return exprs[0]
        return exprs

class AComparison(BinaryOperator):
    def annotate(self, symbol_decls, q_decls):
        # a≠b --> Not(a=b)
        if len(self.sub_exprs) == 2 and self.operator == ['≠']:
            out = NOT(AComparison(sub_exprs=self.sub_exprs, operator='='))
            return out.annotate(symbol_decls, q_decls)
        return super().annotate(symbol_decls, q_decls)

    @immutable
    def update_exprs(self, new_expr_generator):
        operands = list(new_expr_generator)
        operands1 = [e.as_ground() for e in operands]
        if all(e is not None for e in operands1):
            acc = operands1[0]
            for op, expr in zip(self.operator, operands1[1:]):
                if not (BinaryOperator.MAP[op]) (acc, expr):
                    return FALSE
                acc = expr
            return TRUE
        return operands


def update_arith(self, family, new_expr_generator):
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
    for op, expr in zip(self.operator, new_expr_generator):
        add(op, expr)

    # analyse results
    if family == '*' and acc == 0:
        return ZERO
    elif (family == '+' and acc != 0) or (family == '*' and acc != 1):
        exprs = [NumberConstant(number=str(acc))] + exprs
    else:
        del ops[0]
    if len(exprs)==1: 
        return exprs[0]
    return (exprs, ops)


class ASumMinus(BinaryOperator):

    @immutable
    def update_exprs(self, new_expr_generator):
        return update_arith(self, '+', new_expr_generator)

class AMultDiv(BinaryOperator):

    @immutable
    def update_exprs(self, new_expr_generator):
        if any(op == '%' for op in self.operator): # special case !
            operands = list(new_expr_generator)
            operands1 = [e.as_ground() for e in operands]
            if len(operands) == 2 \
            and all(e is not None for e in operands1):
                out = operands1[0] % operands1[1]
                return NumberConstant(number=str(out))
            else:
                return operands
        return update_arith(self, '*', new_expr_generator)

class APower(BinaryOperator):

    @immutable
    def update_exprs(self, new_expr_generator):
        operands = list(new_expr_generator)
        operands1 = [e.as_ground() for e in operands]
        if len(operands) == 2 \
        and all(e is not None for e in operands1):
            out = operands1[0] ** operands1[1]
            return NumberConstant(number=str(out))
        else:
            return operands

classes = { '∧': AConjunction,
            '∨': ADisjunction,
            '⇒': AImplication,
            '⇐': ARImplication,
            '⇔': AEquivalence,
            '+': ASumMinus,
            '-': ASumMinus,
            '*': AMultDiv,
            '/': AMultDiv,
            '%': AMultDiv,
            '^': APower,
            '=': AComparison,
            '<': AComparison,
            '>': AComparison,
            '≤': AComparison,
            '≥': AComparison,
            '≠': AComparison,
            }

def operation(ops, operands):
    if len(operands) == 1:
        return operands[0]
    if isinstance(ops, str):
        ops = [ops] * (len(operands)-1)
    operands1 = []
    for o in operands:
        if type(o) not in [Constructor, AppliedSymbol, Variable, Symbol, Fresh_Variable, NumberConstant, Brackets]:
            # add () around operands, to avoid ambiguity in str()
            o = Brackets(f=o, reading='')
        operands1.append(o)
    out = (classes[ops[0]]) (sub_exprs=operands, operator=ops)
    return out.simplify1()

class AUnary(Expression):
    MAP = {'-': lambda x: 0 - x,
           '~': lambda x: Not(x)
          }
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.operator = kwargs.pop('operator')

        self.sub_exprs = [self.f]
        super().__init__()

        self.is_subtence = False

    def __str__(self):
        return f"{self.operator}({str(self.sub_exprs[0])})"
    def str_(self):
        return f"{self.operator}({self.sub_exprs[0].str})"

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = self.sub_exprs[0].type
        return self

    @immutable
    def update_exprs(self, new_expr_generator):
        operand = next(new_expr_generator)
        if self.operator == '~':
            if operand == TRUE:
                return FALSE
            if operand == FALSE:
                return TRUE
        return [operand]

    def translate(self):
        if self.translated is None:
            out = self.sub_exprs[0].translate()
            function = AUnary.MAP[self.operator]
            self.translated = function(out)
        return self.translated

def NOT(expr):
    out = AUnary(operator='~', f=expr)
    out.type = 'bool'
    return out.simplify1()

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

        self.q_decls = {}
        self.is_subtence = False

        if self.aggtype == "sum" and self.out is None:
            raise Exception("Must have output variable for sum")
        if self.aggtype != "sum" and self.out is not None:
            raise Exception("Can't have output variable for #")

    def __str__(self):
        if self.vars is not None:
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
        vars = "".join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
        output = f" : {self.sub_exprs[AAggregate.OUT].str}" if self.out else ""
        out = ( f"{self.aggtype}{{{vars} : "
                f"{self.sub_exprs[AAggregate.CONDITION].str}"
                f"{output}}}"
              )
        return out

    def annotate(self, symbol_decls, q_decls):   
        self.q_decls = {v:Fresh_Variable(v, symbol_decls[s.name]) \
                        for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_decls, **self.q_decls} # merge
        self.sub_exprs = [e.annotate(symbol_decls, q_v) for e in self.sub_exprs]
        self.type = self.sub_exprs[AAggregate.OUT].type if self.out else 'int'
        return self
        
    @immutable
    def expand_quantifiers(self, theory):
        form = IfExpr(if_f=self.sub_exprs[AAggregate.CONDITION]
                    , then_f=NumberConstant(number='1') if self.out is None else self.sub_exprs[AAggregate.OUT]
                    , else_f=NumberConstant(number='0'))
        forms = [form.expand_quantifiers(theory)]
        for name, var in self.q_decls.items():
            if var.decl.range:
                forms = [f.substitute(var, val) for val in var.decl.range for f in forms]
            else:
                raise Exception('Can only quantify aggregates over finite domains')
        self.vars = None # flag to indicate changes
        return forms

    def translate(self):
        if self.translated is None:
            for v in self.q_decls.values():
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

    def __str__(self):
        return f"{str(self.s)}({','.join([str(x) for x in self.sub_exprs])})"
    def str_(self):
        return f"{self.s.str}({','.join([x.str for x in self.sub_exprs])})"

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.decl = q_decls[self.s.name] if self.s.name in q_decls else symbol_decls[self.s.name]
        self.type = self.decl.type.name
        self.is_subtence = self.type == 'bool'
        return self

    @immutable
    def interpret(self, theory):
        sub_exprs = [e.interpret(theory) for e in self.sub_exprs]
        if self.decl.interpretation is not None:
            self.is_subtence = False
            out = (self.decl.interpretation)(theory, 0, sub_exprs)
            return out
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

class Variable(Expression):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

        super().__init__()

        self.sub_exprs = []
        self.decl = None

    def __str__(self): return self.name
    def str_   (self): return self.name

    def annotate(self, symbol_decls, q_decls):
        if self.name in symbol_decls and type(symbol_decls[self.name]) == Constructor:
            return symbol_decls[self.name]
        if self.name in q_decls:
            self.decl = q_decls[self.name]
            self.type = self.decl.type
            self.is_subtence = False
        else:
            self.decl = symbol_decls[self.name]
            self.type = self.decl.type.name
            self.is_subtence = self.type == 'bool'
            self.normal = True # make sure it is visible in GUI
        return self

    def unknown_symbols(self):
        return {self.decl.name: self.decl} if self.decl.interpretation is None \
            else {}

    def reified(self):
        return self.translate()

    def has_environmental(self, truth):
        return self.decl.environmental == truth

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
        self.is_subtence = False

    def __str__(self): return self.name
    def str_   (self): return self.name

    def substitute(self, e0, e1):
        return e1 if self == e0 else self

    def translate(self):
        if self.translated is None:
            self.translated = FreshConst(self.decl.translated)
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
        self.is_subtence = False
    
    def __str__(self): return self.number
    def str_   (self): return self.number

    def as_ground(self): return self.translated

    def annotate(self, symbol_decls, q_decls): return self

    def translate(self):
        return self.translated

ZERO = NumberConstant(number='0')
ONE  = NumberConstant(number='1')

class Brackets(Expression):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        reading = kwargs.pop('reading')
        self.sub_exprs = [self.f]

        super().__init__()
        self.reading = reading

        self.is_subtence = False

    def __str__(self): return f"({str(self.sub_exprs[0])})"
    def str_   (self): return f"({self.sub_exprs[0].str})"

    def as_ground(self): 
        return self.sub_exprs[0].as_ground()

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [self.sub_exprs[0].annotate(symbol_decls, q_decls)]
        self.type = self.sub_exprs[0].type
        if self.reading:
            self.sub_exprs[0].reading = self.reading
        return self

    @immutable
    def update_exprs(self, new_expr_generator):
        expr = next(new_expr_generator)
        return [expr]

    def translate(self):
        self.translated = self.sub_exprs[0].translate()
        return self.translated

