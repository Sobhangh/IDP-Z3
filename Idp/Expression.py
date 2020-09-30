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
from collections import ChainMap
import functools
import itertools as it
import os
import re
import sys

from z3 import DatatypeRef, Q, Const, BoolSort, FreshConst
from typing import List, Tuple

from consultant.utils import mergeDicts, unquote, OrderedSet


class DSLException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class Expression(object):
    __slots__ = ('sub_exprs', 'simpler', 'value', 'status', 'code', 'annotations', 'original',
        'str', 'fresh_vars', 'type', 'is_visible', '_reified', 'if_symbol', 'co_constraint',
        'normal', 'questions', 'relevant' )

    COUNT = 0
    def __init__(self):
        # .sub_exprs : list of Expression, to be translated to Z3
        self.simpler = None               # a simplified version of the expression, or None
        self.value = None                 # a python value (bool, int, float, string) or None
        self.status = None                # explains how the value was found

        # .code uniquely identifies an expression, irrespective of its value
        self.code = sys.intern(str(self)) # normalized idp code, before transformations
        self.annotations = {'reading': self.code} # dict(String, String)
        self.original = self              # untouched version of the expression, from IDP code or Expr.make()

        self.str = self.code              # memoization of str(), representing its value
        self.fresh_vars = None            # Set[String]: over approximated list of fresh_vars (ignores simplifications)
        self.no_fresh_vars_before_expansion = None # Bool
        self.type = None                  # String (e.g. 'bool', 'real', 'int', 'color'), or None
        self.is_visible = None            # is shown to user -> need to find whether it is a consequence
        self._reified = None
        self.if_symbol = None             # (string) this constraint is relevant if Symbol is relevant
        self.co_constraint = None         # constraint attached to the node, e.g. instantiated definition (Expression)
        # .normal : only set in .instances
        self.is_assignment = None         # for comparisons only

        # attributes of the top node of a (co-)constraint
        # .questions
        # .relevant
        # .block


    def copy(self):
        " create a deep copy (except for Constructor and NumberConstant) "
        if type(self) in [Constructor, NumberConstant]:
            return self
        out = copy.copy(self)
        out.sub_exprs = [e.copy() for e in out.sub_exprs]
        out.value         = None if out.value         is None else out.value        .copy()
        out.simpler       = None if out.simpler       is None else out.simpler      .copy()
        out.co_constraint = None if out.co_constraint is None else out.co_constraint.copy()
        if hasattr(self, 'questions'):
            out.questions = copy.copy(self.questions)
        return out

    def same_as(self, other):
        if self.value   is not None: return self.value  .same_as(other)
        if self.simpler is not None: return self.simpler.same_as(other)
        if other.value   is not None: return self.same_as(other.value)
        if other.simpler is not None: return self.same_as(other.simpler)

        if type(self)==Brackets or (type(self  )==AQuantification and len(self.vars) ==0):
            return self.sub_exprs[0].same_as(other)
        if type(other)==Brackets or (type(other)==AQuantification and len(other.vars)==0):
            return self.same_as(other.sub_exprs[0])

        return self.str == other.str and type(self)==type(other)

    def __repr__(self): return str(self)

    def __str__(self):
        assert self.value is not self
        if self.value   is not None: 
            return str(self.value)
        if self.simpler is not None: 
            return str(self.simpler)
        return self.__str1__()
    
    def __log__(self): # for debugWithYamlLog
        return { 'class': type(self).__name__
            , 'code': self.code
            , 'str': self.str
            , 'co_constraint': self.co_constraint }

    def annotate(self, voc, q_vars):
        " annotate tree after parsing "
        self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
        return self.annotate1()

    def annotate1(self):
        " annotations that are common to __init__ and make() "
        self.fresh_vars = set()
        if self.value is not None:
            pass
        if self.simpler is not None:
            self.fresh_vars = self.simpler.fresh_vars
        else:
            for e in self.sub_exprs: 
                self.fresh_vars.update(e.fresh_vars)
        self.no_fresh_vars_before_expansion = (len(self.fresh_vars)==0)
        return self

    def collect(self, questions, all_=True, co_constraints=True):
        """collects the questions in self.  

        'questions is an OrderedSet of Expression
        Questions are the terms and the simplest sub-formula that can be evaluated.
        'collect uses the simplified version of the expression.

        all_=False : ignore expanded formulas
                 and AppliedSymbol interpreted in a structure
        co_constraints=False : ignore co_constraints

        default implementation for Constructor, IfExpr, AUnary, Fresh_Variable, Number_constant, Brackets
        """

        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)

    def _questions(self): # for debugging
        questions = OrderedSet()
        self.collect(questions)
        return questions

    def subtences(self):
        " returns questions of type bool "
        questions = OrderedSet()
        self.collect(questions, all_=False)
        out = {k: v for k, v in questions.items() if v.type == 'bool'}
        return out

    def unknown_symbols(self, co_constraints=True):
        """ returns the list of symbols in self, ignoring type constraints
        
        returns Dict[name, Declaration] 
        """
        if self.if_symbol is not None: # ignore type constraints
            return {}
        questions = OrderedSet()
        self.collect(questions, all_=True, co_constraints=co_constraints)
        out = {e.decl.name: e.decl for e in questions.values() if hasattr(e, 'decl')}
        return out

    def co_constraints(self, co_constraints):
        """ collects the constraints attached to AST nodes, e.g. instantiated definitions 
        
        'co_constraints is an OrderedSet of Expression
        """
        if self.co_constraint is not None:
            co_constraints.append(self.co_constraint)
            self.co_constraint.co_constraints(co_constraints)
        for e in self.sub_exprs:
            e.co_constraints(co_constraints)

    def as_ground(self): 
        " returns a NumberConstant or Constructor, or None "
        return self.value

    def reified(self) -> DatatypeRef:
        if self._reified is None:
            if self.type == 'bool':
                self._reified = Const('*'+str(Expression.COUNT), BoolSort())
                Expression.COUNT += 1
            else:
                self._reified = self.translate()
        return self._reified

    def has_decision(self):
        # returns true if it contains a variable declared in decision vocabulary
        return any(e.has_decision() for e in self.sub_exprs)

    def type_inference(self):
        # returns a dictionary {Fresh_Variable : Sort}
        return dict(ChainMap(*(e.type_inference() for e in self.sub_exprs)))


class Constructor(Expression):
    PRECEDENCE = 200
    def __init__(self, **kwargs):
        self.name = unquote(kwargs.pop('name'))
        self.is_var = False
        self.sub_exprs = []
        self.index = None # int

        super().__init__()
        self.fresh_vars = set()
        self.no_fresh_vars_before_expansion = (len(self.fresh_vars)==0)
        self.symbol = None # set only for `Symbols constructors
    
    def __str1__(self): return self.name

    def as_ground(self): return self

TRUE  = Constructor(name='true')
FALSE = Constructor(name='false')


class IfExpr(Expression):
    PRECEDENCE = 10
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
        
    def __str1__(self):
        return ( f" if   {self.sub_exprs[IfExpr.IF  ].str}"
                 f" then {self.sub_exprs[IfExpr.THEN].str}"
                 f" else {self.sub_exprs[IfExpr.ELSE].str}" )

    def annotate1(self):
        self.type = self.sub_exprs[IfExpr.THEN].type
        return super().annotate1()

class Quantee(object):
    def __init__(self, var, sort):
        self.var = var
        self.sort = sort

class AQuantification(Expression):
    PRECEDENCE = 20
    def __init__(self, **kwargs):
        self.q = kwargs.pop('q')
        self.quantees = kwargs.pop('quantees')
        self.f = kwargs.pop('f')

        self.q = '∀' if self.q == '!' else '∃' if self.q == "?" else self.q
        self.vars, self.sorts = [], []
        for q in self.quantees:
            self.vars.append(q.var)
            self.sorts.append(q.sort)

        self.sub_exprs = [self.f]
        super().__init__()

        self.q_vars = {} # dict[String, Fresh_Variable]
        self.type = 'bool'

    @classmethod
    def make(cls, q, q_vars, f):
        "make and annotate a quantified formula"
        quantees = [Quantee(v.name, v.sort) for v in q_vars.values()]
        out = cls(q=q, quantees=quantees, f=f)
        out.q_vars = q_vars
        return out.annotate1()

    def __str1__(self):
        assert len(self.vars) == len(self.sorts), "Internal error"
        vars = ''.join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
        return f"{self.q}{vars} : {self.sub_exprs[0].str}"

    def annotate(self, voc, q_vars):
        for v in self.vars:
            assert v not in voc.symbol_decls, f"the quantifier variable '{v}' cannot have the same name as another symbol."
        assert len(self.vars) == len(self.sorts), "Internal error"
        self.q_vars = {}
        for v, s in zip(self.vars, self.sorts):
            if s:
                s.annotate(voc)
                self.q_vars[v] = Fresh_Variable(v,s)
        q_v = {**q_vars, **self.q_vars} # merge
        self.sub_exprs = [e.annotate(voc, q_v) for e in self.sub_exprs]
        return self.annotate1()

    def annotate1(self):
        super().annotate1()
        # remove q_vars
        self.fresh_vars = self.fresh_vars.difference(set(self.q_vars.keys()))
        self.no_fresh_vars_before_expansion = (len(self.fresh_vars)==0)
        return self

    def collect(self, questions, all_=True, co_constraints=True):
        if self.no_fresh_vars_before_expansion \
        or (all_ and len(self.fresh_vars)==0):
            questions.append(self)
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)


class BinaryOperator(Expression):

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
    def make(cls, ops, operands):
        """ creates a BinaryOp
            beware: cls must be specific for ops !"""
        if len(operands) == 1:
            return operands[0]
        if isinstance(ops, str):
            ops = [ops] * (len(operands)-1)
        out = (cls)(sub_exprs=operands, operator=ops)
        return out.annotate1().simplify1()
        
    def __str1__(self):
        def parenthesis(precedence, x):
            return f"({x.str})" if type(x).PRECEDENCE <= precedence else f"{x.str}"
        precedence = type(self).PRECEDENCE
        temp = parenthesis(precedence, self.sub_exprs[0])
        for i in range(1, len(self.sub_exprs)):
            temp += f" {self.operator[i-1]} {parenthesis(precedence, self.sub_exprs[i])}"
        return temp
    
    def annotate1(self):
        assert not (self.operator[0]=='⇒' and 2 < len(self.sub_exprs)), \
                "Implication is not associative.  Please use parenthesis."
        if self.type is None:
            self.type = 'real' if any(e.type == 'real' for e in self.sub_exprs) \
                   else 'int'  if any(e.type == 'int'  for e in self.sub_exprs) \
                   else self.sub_exprs[0].type # constructed type, without arithmetic
        return super().annotate1()

    def collect(self, questions, all_=True, co_constraints=True):
        if self.operator[0] in '=<>≤≥≠' \
        and (self.no_fresh_vars_before_expansion or (all_ and len(self.fresh_vars)==0)) :
            questions.append(self)
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)
        
class AImplication(BinaryOperator):
    PRECEDENCE = 50
    
class AEquivalence(BinaryOperator):
    PRECEDENCE = 40

class ARImplication(BinaryOperator):
    PRECEDENCE = 30
    def annotate(self, voc, q_vars):
        # reverse the implication
        self.sub_exprs.reverse()
        out = AImplication(sub_exprs=self.sub_exprs, operator=['⇒']*len(self.operator))
        if hasattr(self, "block"):
            out.block = self.block
        return out.annotate(voc, q_vars)

class ADisjunction(BinaryOperator):
    PRECEDENCE = 60


class AConjunction(BinaryOperator):
    PRECEDENCE = 70


class AComparison(BinaryOperator):
    PRECEDENCE = 80
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_assignment = None

    def annotate(self, voc, q_vars):
        # a≠b --> Not(a=b)
        if len(self.sub_exprs) == 2 and self.operator == ['≠']:
            self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
            out = AUnary.make('~', AComparison.make('=', self.sub_exprs))
            return out
        return super().annotate(voc, q_vars)

    def annotate1(self):
        # f(x)=y
        self.is_assignment = len(self.sub_exprs) == 2 and self.operator in [['='], ['≠']] \
            and type(self.sub_exprs[0]).__name__ in ["AppliedSymbol", "Variable"] \
            and all(e.as_ground() is not None for e in self.sub_exprs[0].sub_exprs) \
            and self.sub_exprs[1].as_ground() is not None
        return super().annotate1()


class ASumMinus(BinaryOperator):
    PRECEDENCE = 90
    
class AMultDiv(BinaryOperator):
    PRECEDENCE = 100

class APower(BinaryOperator):
    PRECEDENCE = 110
    
class AUnary(Expression):
    PRECEDENCE = 120

    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.operator = kwargs.pop('operator')

        self.sub_exprs = [self.f]
        super().__init__()

    @classmethod
    def make(cls, op, expr):
        out = AUnary(operator=op, f=expr)
        return out.annotate1().simplify1()

    def __str1__(self):
        return f"{self.operator}({self.sub_exprs[0].str})"

    def annotate1(self):
        self.type = self.sub_exprs[0].type
        return super().annotate1()

class AAggregate(Expression):
    PRECEDENCE = 130
    CONDITION = 0
    OUT = 1

    def __init__(self, **kwargs):
        self.aggtype = kwargs.pop('aggtype')
        self.quantees = kwargs.pop('quantees')
        self.f = kwargs.pop('f')
        self.out = kwargs.pop('out')

        self.vars, self.sorts = [], []
        for q in self.quantees:
            self.vars.append(q.var)
            self.sorts.append(q.sort)
        self.sub_exprs = [self.f, self.out] if self.out else [self.f] # later: expressions to be summed
        super().__init__()

        self.q_vars = {}

        if self.aggtype == "sum" and self.out is None:
            raise Exception("Must have output variable for sum")
        if self.aggtype != "sum" and self.out is not None:
            raise Exception("Can't have output variable for #")

    def __str1__(self):
        if self.vars is not None:
            assert len(self.vars) == len(self.sorts), "Internal error"
            vars = "".join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
            output = f" : {self.sub_exprs[AAggregate.OUT].str}" if self.out else ""
            out = ( f"{self.aggtype}{{{vars} : "
                    f"{self.sub_exprs[AAggregate.CONDITION].str}"
                    f"{output}}}"
                )
        else:
            out = ( f"{self.aggtype}{{"
                    f"{','.join(e.str for e in self.sub_exprs)}"
                    f"}}"
            )
        return out

    def annotate(self, voc, q_vars):
        for v in self.vars:
            assert v not in voc.symbol_decls, f"the quantifier variable '{v}' cannot have the same name as another symbol."
        assert len(self.vars) == len(self.sorts), "Internal error"
        self.q_vars = {}
        for v, s in zip(self.vars, self.sorts):
            if s:
                s.annotate(voc)
                self.q_vars[v] = Fresh_Variable(v,s)
        q_v = {**q_vars, **self.q_vars} # merge
        self.sub_exprs = [e.annotate(voc, q_v) for e in self.sub_exprs]
        self.type = self.sub_exprs[AAggregate.OUT].type if self.out else 'int'
        self = self.annotate1()
        # remove q_vars after annotate1
        self.fresh_vars = self.fresh_vars.difference(set(self.q_vars.keys()))
        self.no_fresh_vars_before_expansion = (len(self.fresh_vars)==0)
        return self

    def collect(self, questions, all_=True, co_constraints=True):
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)


class AppliedSymbol(Expression):
    PRECEDENCE = 200
    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')

        self.sub_exprs = self.args.sub_exprs
        super().__init__()

        self.decl = None
        self.name = self.s.name

    @classmethod
    def make(cls, symbol, args):
        out = cls(s=symbol, args=Arguments(sub_exprs=args))
        out.sub_exprs = args
        # annotate
        out.decl = symbol.decl
        return out.annotate1()

    def __str1__(self):
        if len(self.sub_exprs) == 0:
            return str(self.s)
        else:
            return f"{str(self.s)}({','.join([x.str for x in self.sub_exprs])})"

    def annotate(self, voc, q_vars):
        self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
        self.decl = q_vars[self.s.name].sort.decl if self.s.name in q_vars else voc.symbol_decls[self.s.name]
        self.normal = True
        return self.annotate1()

    def annotate1(self):
        self.type = self.decl.type if self.decl else None
        return super().annotate1()

    def collect(self, questions, all_=True, co_constraints=True):
        if self.decl.is_var \
        and self.simpler is None and self.name != '__relevant' \
        and (self.no_fresh_vars_before_expansion or (all_ and len(self.fresh_vars)==0)):
            questions.append(self)
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)
        if co_constraints and self.co_constraint is not None:
            self.co_constraint.collect(questions, all_, co_constraints)

    def has_decision(self):
        assert self.decl.block is not None
        return not self.decl.block.name=='environment' \
            or any(e.has_decision() for e in self.sub_exprs)

    def type_inference(self):
        out = {}
        for i, e in enumerate(self.sub_exprs):
            if self.decl.name != '`Symbols' and isinstance(e, Variable):
                out[e.name] = self.decl.sorts[i]
            else:
                out.update(e.type_inference())
        return out

class Arguments(object):
    def __init__(self, **kwargs):
        self.sub_exprs = kwargs.pop('sub_exprs')
        super().__init__()

class Variable(AppliedSymbol):
    PRECEDENCE = 200
    def __init__(self, **kwargs):
        self.name = unquote(kwargs.pop('name'))

        Expression.__init__(self)

        self.sub_exprs = []
        self.decl = None
        self.translated = None

    def __str1__(self): return self.name

    def annotate(self, voc, q_vars):
        if self.name in voc.symbol_decls and type(voc.symbol_decls[self.name]) == Constructor:
            return voc.symbol_decls[self.name]
        if self.name in q_vars:
            return q_vars[self.name]
        elif self.name in voc.symbol_decls: # in symbol_decls
            self.decl = voc.symbol_decls[self.name]
            self.type = self.decl.type
            self.normal = True # make sure it is visible in GUI
        else: pass # a quantification variable without known type yet
        return self.annotate1()

    def collect(self, questions, all_=True, co_constraints=True):
        if self.decl and self.decl.is_var:
            questions.append(self)
        if co_constraints and self.co_constraint is not None:
            self.co_constraint.collect(questions, all_, co_constraints)

    def reified(self):
        return self.translate()
    

class Fresh_Variable(Expression):
    PRECEDENCE = 200
    def __init__(self, name, sort):
        self.name = name
        self.sort = sort

        super().__init__()

        self.type = self.sort.name
        self.sub_exprs = []
        self.translated = FreshConst(self.sort.decl.translate())
        self.fresh_vars = set([self.name])

    def __str1__(self): return self.name


class NumberConstant(Expression):
    PRECEDENCE = 200
    def __init__(self, **kwargs):
        self.number = kwargs.pop('number')

        super().__init__()

        self.sub_exprs = []
        self.fresh_vars = set()

        ops = self.number.split("/")
        if len(ops) == 2: # possible with str_to_IDP on Z3 value
            self.translated = Q(int(ops[0]), int(ops[1]))
            self.type = 'real'
        elif '.' in self.number:
            self.translated = float(eval(self.number if not self.number.endswith('?') else self.number[:-1]))
            self.type = 'real'
        else:
            self.translated = int(self.number)
            self.type = 'int'
    
    def __str__(self): return self.number

    def as_ground(self)     : return self

ZERO = NumberConstant(number='0')
ONE  = NumberConstant(number='1')

class Brackets(Expression):
    PRECEDENCE = 200
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

    # don't @use_value, to have parenthesis
    def __str__(self): return f"({self.sub_exprs[0].str})"
    def __str1__(self): return str(self)

    def as_ground(self): 
        return self.sub_exprs[0].as_ground()

    def annotate1(self):
        self.type = self.sub_exprs[0].type
        if self.annotations['reading']:
            self.sub_exprs[0].annotations = self.annotations
        self.fresh_vars = self.sub_exprs[0].fresh_vars
        self.no_fresh_vars_before_expansion = (len(self.fresh_vars)==0)
        return self

