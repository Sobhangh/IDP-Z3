

import copy
import functools
import itertools as it
import os
import re
import sys

from z3 import FreshConst, Or, Not, And, ForAll, Exists, Z3Exception, Sum, If

from Inferences import ConfigCase


class DSLException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def immutable(func):
    @functools.wraps(func)
    def wrapper_decorator(self, new_expr_generator):
        value, ops = func(self, new_expr_generator), None
        if isinstance(value, tuple):
            ops = value[1]
            value = value[0]
        if isinstance(value, list):
            if all(id(e0) == id(e1) for (e0,e1) in zip(self.sub_exprs, value)): # not changed !
                return self
            else:
                out = copy.copy(self)
                out.sub_exprs = value
                # reset derived values
                out._unknown_symbols = None
                out.translated = None
                if ops: out.operator = ops
                return out
        out = copy.copy(value)
        # copy initial annotation
        out.code = self.code
        out.reading = self.reading
        out.is_subtence = self.is_subtence
        out.type = self.type
        return out
    return wrapper_decorator
        
class Expression(object):
    # .sub_exprs : list of (transformed) Expression, to be translated to Z3
    def __init__(self):
        self.code = sys.intern(str(self)) # normalized idp code, before transformations
        self.reading = None               # English reading
        self.is_subtence = None           # True if sub-sentence in original code
        self.type = None                  # a declaration object, or 'bool', 'real', 'int', or None
        self._unknown_symbols = None      # list of uninterpreted symbols not starting with '_'
        self.translated = None            # the Z3 equivalent

    def __eq__(self, other):
        return str(self) == str(other)
    
    def __hash__(self):
        return hash(self.code)

    def subtences(self):
        if self.is_subtence:
            return {self.code: self} #TODO possibly go deeper
        out = {}
        for e in self.sub_exprs: out.update(e.subtences())
        return out

    @immutable
    def update_exprs(self, new_expr_generator):
        return list(new_expr_generator)

    def substitute(self, e0, e1):
        if self == e0: # based on repr !
            return e1
        else:
            return self.update_exprs(e.substitute(e0, e1) for e in self.sub_exprs)

    def expand_quantifiers(self, theory):
        return self.update_exprs(e.expand_quantifiers(theory) for e in self.sub_exprs)

    def interpret(self, theory):
        return self.update_exprs(e.interpret(theory) for e in self.sub_exprs)

    def unknown_symbols(self):
        if self._unknown_symbols is None:
            self._unknown_symbols = {}
            for e in self.sub_exprs:
                self._unknown_symbols.update(e.unknown_symbols())
        return self._unknown_symbols


class Constructor(Expression):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.is_var = False
        self.sub_exprs = []

        super().__init__()
        
        self.is_subtence = False
    
    def __str__(self): return self.name
    def annotate(self, symbol_decls, q_decls): return self
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
        return "if "    + self.sub_exprs[IfExpr.IF  ].code \
             + " then " + self.sub_exprs[IfExpr.THEN].code \
             + " else " + self.sub_exprs[IfExpr.ELSE].code

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
        return self.q \
            + "".join([v + "[" + s.code + "]" for v, s in zip(self.vars, self.sorts)]) \
            + " : " + self.sub_exprs[0].code

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

        self.is_subtence = self.operator[0] in '=<>≤≥≠'

    def __str__(self):
        temp = self.sub_exprs[0].code
        for i in range(1, len(self.sub_exprs)):
            temp += " " + self.operator[i-1] + " " + self.sub_exprs[i].code
        return temp

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = 'bool' if self.operator[0] in '&|^∨⇒⇐⇔' \
               else 'bool' if self.operator[0] in '=<>≤≥≠' \
               else 'real' if any(e.type == 'real' for e in self.sub_exprs) \
               else 'int'
        return self

    def translate(self):
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

    @immutable
    def update_exprs(self, new_expr_generator):
        operands = list(new_expr_generator)
        if all(type(e) == NumberConstant for e in operands):
            acc = operands[0]
            for op, expr in zip(self.operator, operands[1:]):
                if not (BinaryOperator.MAP[op]) (acc.translated, expr.translated):
                    return FALSE
                acc = expr
            return TRUE
        return operands


def update_arith(self, family, new_expr_generator):
    # accumulate numbers in acc
    acc, ops, exprs = 0 if family == '+' else 1, [], []
    def add(op, expr):
        nonlocal acc, ops, exprs
        if type(expr) == NumberConstant:
            if op == '+':
                acc += expr.translated
            elif op == '-':
                acc -= expr.translated
            elif op == '*':
                acc *= expr.translated
            elif op == '/':
                if isinstance(acc, int) and expr.type == 'int': # integer division
                    acc //= expr.translated
                else:
                    acc /= expr.translated
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
            if len(operands) == 2 \
            and all(type(e) == NumberConstant for e in operands):
                out = operands[0].translated % operands[1].translated
                return NumberConstant(number=str(out))
            else:
                return operands
        return update_arith(self, '*', new_expr_generator)

class APower(BinaryOperator):

    @immutable
    def update_exprs(self, new_expr_generator):
        operands = list(new_expr_generator)
        if len(operands) == 2 \
        and all(type(e) == NumberConstant for e in operands):
            out = operands[0].translated ** operands[1].translated
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
            '=': AConjunction,
            '<': AConjunction,
            '>': AConjunction,
            '≤': AConjunction,
            '≥': AConjunction,
            '≠': AConjunction,
            }

def operation(ops, operands):
    if len(operands) == 1:
        return operands[0]
    if isinstance(ops, str):
        ops = [ops] * (len(operands)-1)
    out = (classes[ops[0]]) (sub_exprs=operands, operator=ops)
    return out.update_exprs(operands) # simplify it

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
        return self.operator + self.sub_exprs[0].code

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
        out = self.sub_exprs[0].translate()
        function = AUnary.MAP[self.operator]
        self.translated = function(out)
        return self.translated

def NOT(expr):
    out = AUnary(operator='~', f=expr)
    out.type = 'bool'
    return out.update_exprs(e for e in [expr]) # simplify if possible

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
        out = self.aggtype + "{" + "".join([str(v) + "[" + str(s) + "]" for v, s in zip(self.vars, self.sorts)])
        out += ":" + self.sub_exprs[AAggregate.CONDITION].code
        if self.out: out += " : " + self.sub_exprs[AAggregate.OUT].code
        out += "}"
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
        return forms

    def translate(self):
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
        return self.s.code + "(" + ",".join([x.code for x in self.sub_exprs]) + ")"

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
            return (self.decl.interpretation)(theory, 0, sub_exprs)
        else:
            return self

    def unknown_symbols(self):
        out = super().unknown_symbols()
        if not self.decl.name.startswith('_') and self.decl.interpretation is None:
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

    def __str__(self):
        return self.name

    def annotate(self, symbol_decls, q_decls):
        if self.name in symbol_decls and type(symbol_decls[self.name]) == Constructor:
            return symbol_decls[self.name]
        self.decl = q_decls[self.name] if self.name in q_decls \
            else symbol_decls[self.name]
        self.type = self.decl.type
        self.is_subtence = self.type == 'bool'
        return self

    def unknown_symbols(self):
        return {self.decl.name: self.decl} if not self.decl.name.startswith('_') and self.decl.interpretation is None \
            else {}

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

    def __str__(self):
        return self.name

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
            self.translated = float(self.number)
            self.type = 'real'
        self.is_subtence = False
    
    def __str__(self):
        return self.number

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

    def __str__(self):
        return "(" + self.sub_exprs[0].code + ")"

    def annotate(self, symbol_decls, q_decls):
        out = self.f.annotate(symbol_decls, q_decls)
        out.reading = self.reading
        return out

