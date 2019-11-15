

import copy
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

        
class Expression(object):
    # .str : normalized idp code, before transformations
    # .sub_exprs : list of (transformed) Expression, to be translated to Z3
    # .type : a declaration object, or 'bool', 'real', 'int', or None
    # .translated : the Z3 equivalent
    # ._unknown_symbols : list of uninterpreted symbols not starting with '_'
    
    def __eq__(self, other):
        return self.str == other.str
    
    def __hash__(self):
        return hash(self.str)

    def __str__(self): return self.str

    def subtences(self):
        out = {}
        for e in self.sub_exprs: out.update(e.subtences())
        return out

    def simplify1(self):
        "simplify this node only"
        return self

    def reset(self):
        # reset derived variables
        self._unknown_symbols = None
        self.translated = None

    def substitute(self, e0, e1):
        if self == e0: # based on .str !
            return e1
        else:
            sub_exprs1 = [e.substitute(e0, e1) for e in self.sub_exprs]
            if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
                return self
            else:
                out = copy.copy(self)
                out.reset()
                out.sub_exprs = sub_exprs1
                out.str = repr(out)
                return out.simplify1()

    def expand_quantifiers(self, theory):
        sub_exprs1 = [e.expand_quantifiers(theory) for e in self.sub_exprs]
        if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
            return self
        else:
            self.sub_exprs = sub_exprs1
            # no need to reset
            return self.simplify1()

    def interpret(self, theory):
        sub_exprs1 = [e.interpret(theory) for e in self.sub_exprs]
        if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
            return self
        else:
            self.sub_exprs = sub_exprs1
            self.reset()
            return self.simplify1()

    def unknown_symbols(self):
        if self._unknown_symbols is None:
            self._unknown_symbols = {}
            for e in self.sub_exprs:
                self._unknown_symbols.update(e.unknown_symbols())
        return self._unknown_symbols


class Constructor(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.is_var = False
        self.str = sys.intern(self.name)
        self.translated = None
        self.type = None
    
    def __str__(self): return self.str

    # A constructor behaves like an Expression
    def annotate(self, symbol_decls, q_decls): return self
    def subtences(self): return []
    def substitute(self, e0, e1): return self
    def expand_quantifiers(self, theory): return self
    def interpret(self, theory): return self
    def unknown_symbols(self): return {}
    def translate(self): return self.translated



class IfExpr(Expression):
    IF = 0
    THEN = 1
    ELSE = 2

    def __init__(self, **kwargs):
        self.if_f = kwargs.pop('if_f')
        self.then_f = kwargs.pop('then_f')
        self.else_f = kwargs.pop('else_f')

        self.sub_exprs = [self.if_f, self.then_f, self.else_f]
        self.str = repr(self)
        self._unknown_symbols = None
        self.translated = None
        self.type = None

    def __repr__(self):
        return sys.intern("if "    + self.sub_exprs[IfExpr.IF  ].str \
                        + " then " + self.sub_exprs[IfExpr.THEN].str \
                        + " else " + self.sub_exprs[IfExpr.ELSE].str)

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        #TODO verify consistency
        self.type = self.sub_exprs[IfExpr.THEN].type
        return self

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
        self.str = repr(self)
        self.q_decls = {}
        self._unknown_symbols = None
        self.translated = None
        self.type = 'bool'


    def __repr__(self):
        return sys.intern(self.q \
            + "".join([v + "[" + s.str + "]" for v, s in zip(self.vars, self.sorts)]) \
            + " : " + self.sub_exprs[0].str)


    def annotate(self, symbol_decls, q_decls):
        self.q_decls = {v:Fresh_Variable(v, symbol_decls[s.name]) \
                        for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_decls, **self.q_decls} # merge
        self.sub_exprs = [e.annotate(symbol_decls, q_v) for e in self.sub_exprs]
        return self

    def subtences(self):
        #TODO optionally add subtences of sub_exprs
        return {self.str: self}

    def expand_quantifiers(self, theory):
        forms = [self.sub_exprs[0].expand_quantifiers(theory)]
        self.vars = []
        for name, var in self.q_decls.items():
            if var.decl.range:
                forms = [f.substitute(var, val) for val in var.decl.range for f in forms]
            else:
                self.vars.append(var)
        op = '∧' if self.q == '∀' else '∨'
        self.sub_exprs = [ operation(op, forms) ]
        self.sorts = [] # not used
        return self

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
            '≠': lambda x, y: Not(x == y)
            }

    def __init__(self, **kwargs):
        self.sub_exprs = kwargs.pop('sub_exprs')
        self.operator = kwargs.pop('operator')
        self.operator = list(map(
            lambda op: "≤" if op == "=<" else "≥" if op == ">=" else "≠" if op == "~=" else \
                "⇔" if op == "<=>" else "⇐" if op == "<=" else "⇒" if op == "=>" else \
                "∨" if op == "|" else "∧" if op == "&" else op
            , self.operator))
        self.str = repr(self)
        self._unknown_symbols = None
        self.translated = None
        self.type = None

    def __repr__(self):
        temp = self.sub_exprs[0].str
        for i in range(1, len(self.sub_exprs)):
            temp += " " + self.operator[i-1] + " " + self.sub_exprs[i].str
        return sys.intern(temp)

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = 'bool' if self.operator[0] in '&|^∨⇒⇐⇔' \
               else 'bool' if self.operator[0] in '=<>≤≥≠' \
               else 'real' if any(e.type == 'real' for e in self.sub_exprs) \
               else 'int'
        return self

    def subtences(self):
        if self.operator[0] in '=<>≤≥≠':
            return {self.str: self} #TODO collect subtences of aggregates within comparisons
        return super().subtences()

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

def operation(op, operands):
    if len(operands) == 1:
        return operands[0]
    if isinstance(op, str):
        op = [op] * (len(operands)-1)
    return BinaryOperator(sub_exprs=operands, operator=op)

class AImplication(BinaryOperator): pass
class AEquivalence(BinaryOperator): pass
class ARImplication(BinaryOperator): pass
class ADisjunction(BinaryOperator): pass
class AConjunction(BinaryOperator): pass
class AComparison(BinaryOperator): pass
class ASumMinus(BinaryOperator): pass
class AMultDiv(BinaryOperator): pass
class APower(BinaryOperator): pass

class AUnary(Expression):
    MAP = {'-': lambda x: 0 - x,
           '~': lambda x: Not(x)
          }
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.operator = kwargs.pop('operator')
        self.sub_exprs = [self.f]
        self.str = repr(self)
        self._unknown_symbols = None
        self.translated = None
        self.type = None

    def __repr__(self):
        return sys.intern(self.operator + self.sub_exprs[0].str)

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = self.sub_exprs[0].type
        return self

    def translate(self):
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

        self.q_decls = {}
        self.sub_exprs = [self.f, self.out] if self.out else [self.f] # later: expressions to be summed
        self.str = repr(self)
        self._unknown_symbols = None
        self.translated = None
        self.type = None

        if self.aggtype == "sum" and self.out is None:
            raise Exception("Must have output variable for sum")
        if self.aggtype != "sum" and self.out is not None:
            raise Exception("Can't have output variable for #")

    def __repr__(self):
        out = self.aggtype + "{" + "".join([str(v) + "[" + str(s) + "]" for v, s in zip(self.vars, self.sorts)])
        out += ":" + self.sub_exprs[AAggregate.CONDITION].str
        if self.out: out += " : " + self.sub_exprs[AAggregate.OUT].str
        out += "}"
        return sys.intern(out)

    def annotate(self, symbol_decls, q_decls):   
        self.q_decls = {v:Fresh_Variable(v, symbol_decls[s.name]) \
                        for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_decls, **self.q_decls} # merge
        self.sub_exprs = [e.annotate(symbol_decls, q_v) for e in self.sub_exprs]
        self.type = self.sub_exprs[AAggregate.OUT].type if self.out else 'int'
        return self
        
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
        self.sub_exprs = forms
        return self

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
        self.str = repr(self)
        self._unknown_symbols = None
        self.translated = None
        self.decl = None
        self.type = None
        # .normal (only if ground) used on client side

    def __repr__(self):
        return sys.intern(self.s.str + "(" + ",".join([x.str for x in self.sub_exprs]) + ")")

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.decl = q_decls[self.s.name] if self.s.name in q_decls else symbol_decls[self.s.name]
        self.type = self.decl.type
        return self

    def subtences(self):
        out = super().subtences()
        if self.type == 'bool': out[self.str] = self
        return out

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

class Variable(Expression):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.str = repr(self)
        self._unknown_symbols = None
        self.translated = None
        self.sub_exprs = []
        if self.name == "true":
            self.type = 'bool'
            self.translated = bool(True)
        elif self.name == "false":
            self.type = 'bool'
            self.translated = bool(False)
        self.decl = None
        self.type = None
        # .normal (only if ground)

    def __repr__(self):
        return sys.intern(self.name)

    def annotate(self, symbol_decls, q_decls):
        if self.name in symbol_decls and type(symbol_decls[self.name]) == Constructor:
            return symbol_decls[self.name]
        self.decl = self if self.name in ['true', 'false'] \
            else q_decls[self.name] if self.name in q_decls \
            else symbol_decls[self.name]
        self.type = self.decl.type
        return self

    def subtences(self):
        return {} if self.name in ['true', 'false'] \
            else {self.str: self} if self.type == 'bool' \
            else {}

    def unknown_symbols(self):
        return {} if self.name in ['true', 'false'] \
            else {self.decl.name: self.decl} if not self.decl.name.startswith('_') and self.decl.interpretation is None \
            else {}

    def translate(self):
        if self.translated is None:
            self.translated = self.decl.translated
        return self.translated
    
class Symbol(Variable): pass
    

class Fresh_Variable(Expression):
    def __init__(self, name, decl):
        self.name = name
        self.str = repr(self)
        self.decl = decl
        self.type = self.decl.type
        self._unknown_symbols = {}
        self.translated = None
        self.sub_exprs = []

    def __repr__(self):
        return sys.intern(self.name)
    
    def subtences(self): return {}

    def translate(self):
        if self.translated is None:
            self.translated = FreshConst(self.decl.translated)
        return self.translated

class NumberConstant(Expression):
    def __init__(self, **kwargs):
        self.number = kwargs.pop('number')
        self.str = repr(self)
        self._unknown_symbols = None
        self.sub_exprs = []
        try:
            self.translated = int(self.number)
            self.type = 'int'
        except ValueError:
            self.translated = float(self.number)
            self.type = 'real'
    
    def __repr__(self):
        return sys.intern(self.number)

    def annotate(self, symbol_decls, q_decls): return self

    def subtences(self): return {}

    def translate(self):
        return self.translated

class Brackets(Expression):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.reading = kwargs.pop('reading')
        self.sub_exprs = [self.f]
        self.str = repr(self)
        self._unknown_symbols = None
        self.translated = None
        self.type = None

    def __repr__(self):
        return sys.intern("(" + self.sub_exprs[0].str + ")")

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = self.sub_exprs[0].type
        return self

    def translate(self):
        self.translated = self.sub_exprs[0].translate()
        if self.reading: 
            self.sub_exprs[0].reading = self.reading
            self.translated.reading   = self.reading #TODO for explain
        return self.translated

