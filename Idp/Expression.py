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

Classes to represent logic expressions.

(They are monkey patched by Substitute.py and Implicant.py)

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

def use_value(function):
    " decorator for str() "
    def _wrapper(*args, **kwds):
        self = args[0]
        if self.value  is not None : return (self.value.__class__.__dict__[function.__name__])(self.value)
        if self.simpler is not None: return (self.value.__class__.__dict__[function.__name__])(self.simpler)
        return function(self)
    return _wrapper

class Expression(object):
    COUNT = 0
    def __init__(self):
        # .sub_exprs : list of Expression, to be translated to Z3
        self.is_subtence = None           # True if sub-sentence in original code
        self.simpler = None               # a simplified version of the expression, or None
        self.value = None                 # a python value (bool, int, float, string) or None
        self.status = None                # explains how the value was found

        # .code uniquely identifies an expression, irrespective of its value
        self.code = sys.intern(str(self)) # normalized idp code, before transformations
        self.annotations = {'reading': self.code} # dict(String, String)

        self.str = self.code              # memoization of str(), representing its value
        self.fresh_vars = None            # Set[String]
        self.type = None                  # a declaration object, or 'bool', 'real', 'int', or None
        self._unknown_symbols = None      # Dict[name, Declaration] list of uninterpreted symbols not starting with '_'
        self.is_visible = None            # is shown to user -> need to find whether it is a consequence
        self._reified = None
        self.if_symbol = None             # (string) this constraint is relevant if Symbol is relevant
        self._subtences = None            # memoization of .subtences()
        self.just_branch = None           # Justification branch (Expression)
        # .normal : only set in .instances


    def copy(self):
        " create a deep copy (except for Constructor and NumberConstant) "
        out = copy.copy(self)
        out.sub_exprs = [e.copy() for e in out.sub_exprs]
        out.value       = None if out.value       is None else out.value      .copy()
        out.simpler     = None if out.simpler     is None else out.simpler    .copy()
        out.just_branch = None if out.just_branch is None else out.just_branch.copy()
        return out

    def __eq__(self, other):
        if self.value is not None and other.value is not None:
            return str(self.value) == str(other.value)
        # hack
        self  = self if self.value is None else self.value
        other = other if other.value is None else other.value
        if isinstance(self, Brackets):
            return self.sub_exprs[0] == other
        if isinstance(other, Brackets):
            return self == other.sub_exprs[0]
        if type(self)  in [AConjunction, ADisjunction] and len(self .sub_exprs)==1:
            return self.sub_exprs[0] == other
        if type(other) in [AConjunction, ADisjunction] and len(other.sub_exprs)==1:
            return self == other.sub_exprs[0]
        # beware: this does not ignore meaningless brackets deeper in the tree
        if self.str == other.str:
            if type(self)!=type(other)\
            and not(type(other).__name__=="Equality" and type(self)==AComparison)\
            and not(type(self)==Fresh_Variable and type(other)== Symbol):
                return False
            return True
        return False

    def __repr__(self): return str(self)
    
    def __hash__(self):
        return hash(self.code)

    def annotate(self, symbol_decls, q_vars):
        self.sub_exprs = [e.annotate(symbol_decls, q_vars) for e in self.sub_exprs]
        return self.annotate1()

    def annotate1(self): return self

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
            if self.just_branch is not None:
                self._subtences.update(self.just_branch.subtences())
        return self._subtences

    def as_ground(self): 
        " returns a NumberConstant or Constructor, or None "
        return self.value

    def unknown_symbols(self):
        if self._unknown_symbols is None:
            self._unknown_symbols = mergeDicts(e.unknown_symbols() for e in self.sub_exprs) \
                if self.if_symbol is None else {}
            if self.just_branch is not None:
                self._unknown_symbols.update(self.just_branch.unknown_symbols())
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
        if self.just_branch is not None:
            out.append(self.just_branch)
            out.extend(self.just_branch.justifications())
        return out

class Constructor(Expression):
    def __init__(self, **kwargs):
        self.name = unquote(kwargs.pop('name'))
        self.is_var = False
        self.sub_exprs = []
        self.index = None # int

        super().__init__()
    
    @use_value
    def __str__(self): return self.name

    def as_ground(self): return self
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

    @classmethod
    def make(cls, if_f, then_f, else_f):
        out = (cls)(if_f=if_f, then_f=then_f, else_f=else_f)
        return out.annotate1().simplify1()
        
    @use_value
    def __str__(self):
        return ( f" if   {str(self.sub_exprs[IfExpr.IF  ])}"
                 f" then {str(self.sub_exprs[IfExpr.THEN])}"
                 f" else {str(self.sub_exprs[IfExpr.ELSE])}" )

    def annotate1(self):
        self.type = self.sub_exprs[IfExpr.THEN].type
        return self

    @use_value
    def translate(self):
        return If(self.sub_exprs[IfExpr.IF  ].translate()
                , self.sub_exprs[IfExpr.THEN].translate()
                , self.sub_exprs[IfExpr.ELSE].translate())

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
        out = cls(q=q, vars=list(decls.values()), sorts=list(v.decl for v in decls.values()), f=f)
        out.q_vars = decls
        out.is_subtence = is_subtence
        return out

    @use_value
    def __str__(self):
        assert len(self.vars) == len(self.sorts), "Internal error"
        vars = ''.join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
        return f"{self.q}{vars} : {str(self.sub_exprs[0])}"

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

    @use_value
    def translate(self):
        for v in self.q_vars.values():
            v.translate()
        if not self.vars:
            return self.sub_exprs[0].translate()
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
            return forms

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
        return out.annotate1().simplify1()
        
    @use_value
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
    
    def annotate1(self):
        assert not (self.operator[0]=='⇒' and 2 < len(self.sub_exprs)), \
                "Implication is not associative.  Please use parenthesis."
        if self.type is None:
            self.type = 'real' if any(e.type == 'real' for e in self.sub_exprs) \
                   else 'int'  if any(e.type == 'int'  for e in self.sub_exprs) \
                   else self.sub_exprs[0].type # constructed type, without arithmetic
        return self

    def mark_subtences(self):
        super().mark_subtences()
        if self.operator[0] in '=<>≤≥≠':
            self.is_subtence = (len(self.fresh_vars)==0)
            self.fresh_vars.discard('!*') # indicates AppliedSymbol with complex expressions
        return self

    @use_value
    def translate(self):
        if self.operator[0] =='≠' and len(self.sub_exprs)==2:
            x = self.sub_exprs[0].translate()
            y = self.sub_exprs[1].translate()
            out = Not(x==y)
        elif self.operator[0] in '=<>≤≥≠':
            # chained comparisons -> And()
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
                return And(out)
            else:
                return out[0]
        elif self.operator[0] == '∧':
            if len(self.sub_exprs) == 1:
                out = self.sub_exprs[0].translate()
            else:
                out = And([e.translate() for e in self.sub_exprs])
        elif self.operator[0] == '∨':
            if len(self.sub_exprs) == 1:
                out = self.sub_exprs[0].translate()
            else:
                out = Or ([e.translate() for e in self.sub_exprs])
        else:
            out = self.sub_exprs[0].translate()

            for i in range(1, len(self.sub_exprs)):
                function = BinaryOperator.MAP[self.operator[i - 1]]
                out = function(out, self.sub_exprs[i].translate())
        return out
        
class AImplication(BinaryOperator):
    pass
class AEquivalence(BinaryOperator):
    pass

class ARImplication(BinaryOperator):
    def annotate(self, symbol_decls, q_vars):
        # reverse the implication
        self.sub_exprs.reverse()
        out = AImplication(sub_exprs=self.sub_exprs, operator=['⇒']*len(self.operator))
        return out.annotate(symbol_decls, q_vars)

class ADisjunction(BinaryOperator):
    pass


class AConjunction(BinaryOperator):
    pass


class AComparison(BinaryOperator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_assignment = None

    def annotate(self, symbol_decls, q_vars):
        # a≠b --> Not(a=b)
        if len(self.sub_exprs) == 2 and self.operator == ['≠']:
            out = AUnary.make('~', AComparison(sub_exprs=self.sub_exprs, operator='='))
            return out.annotate(symbol_decls, q_vars) # will annotate the AComparison too
        out = super().annotate(symbol_decls, q_vars)
        return self.annotate1()

    def annotate1(self):
        # f(x)=y
        self.is_assignment = len(self.sub_exprs) == 2 and self.operator in [['='], ['≠']] \
            and type(self.sub_exprs[0]).__name__ in ["AppliedSymbol", "Variable"] \
            and all(e.as_ground() is not None for e in self.sub_exprs[0].sub_exprs) \
            and self.sub_exprs[1].as_ground() is not None
        return super().annotate1()


class ASumMinus(BinaryOperator):
    pass
class AMultDiv(BinaryOperator):
    pass
class APower(BinaryOperator):
    pass
    
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
        return out.annotate1().simplify1()

    @use_value
    def __str__(self):
        return f"{self.operator}({str(self.sub_exprs[0])})"

    def annotate1(self):
        self.type = self.sub_exprs[0].type
        return self

    @use_value
    def translate(self):
        out = self.sub_exprs[0].translate()
        function = AUnary.MAP[self.operator]
        return function(out)

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

    @use_value
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

    @use_value
    def translate(self):
        return Sum([f.translate() for f in self.sub_exprs])


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
        return out.annotate1()

    @use_value
    def __str__(self):
        if len(self.sub_exprs) == 0:
            return str(self.s)
        else:
            return f"{str(self.s)}({','.join([str(x) for x in self.sub_exprs])})"

    def annotate(self, symbol_decls, q_vars):
        self.sub_exprs = [e.annotate(symbol_decls, q_vars) for e in self.sub_exprs]
        self.decl = q_vars[self.s.name].decl if self.s.name in q_vars else symbol_decls[self.s.name]
        self.normal = True
        return self.annotate1()

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

    def annotate1(self):
        self.type = self.decl.type.name
        return self

    def unknown_symbols(self):
        out = super().unknown_symbols()
        if self.decl.interpretation is None:
            out[self.decl.name] = self.decl
        return out

    @use_value
    def translate(self):
        if self.s.name == 'abs':
            arg = self.sub_exprs[0].translate()
            return If(arg >= 0, arg, -arg)
        else:
            if len(self.sub_exprs) == 0:
                return self.decl.translated
            else:
                arg = [x.translate() for x in self.sub_exprs]
                return (self.decl.translated)(arg)

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
        self.translated = None

    @use_value
    def __str__(self): return self.name

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

    @use_value
    def translate(self):
        return self.decl.translated
    
class Symbol(Variable): pass
    

class Fresh_Variable(Expression):
    def __init__(self, name, decl):
        self.name = name
        self.decl = decl

        super().__init__()

        self.type = self.decl.name
        self._unknown_symbols = {}
        self.sub_exprs = []
        self.translated = None

    @use_value
    def __str__(self): return self.name

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

    def as_ground(self): return self

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

    @use_value
    def __str__(self): return f"({str(self.sub_exprs[0])})"

    def as_ground(self): 
        return self.sub_exprs[0].as_ground()

    def annotate1(self):
        self.type = self.sub_exprs[0].type
        if self.annotations['reading']:
            self.sub_exprs[0].annotations = self.annotations
        return self

    @use_value
    def translate(self):
        return self.sub_exprs[0].translate()

