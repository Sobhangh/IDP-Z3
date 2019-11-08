

import copy
import itertools as it
import os
import re
import sys

from z3 import Or, Not, And, ForAll, Exists, Z3Exception, Sum, If

from configcase import ConfigCase


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

    def substitute(self, e0, e1):
        if self == e0: # based on .str !
            return e1
        else:
            sub_exprs1 = [e.substitute(e0, e1) for e in self.sub_exprs]
            if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
                return self
            else:
                out = copy.copy(self)
                out.sub_exprs = sub_exprs1
                out.str = repr(out)
                return out.simplify1()

    def expand_quantifiers(self, theory):
        sub_exprs1 = [e.expand_quantifiers(theory) for e in self.sub_exprs]
        if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
            return self
        else:
            self.sub_exprs = sub_exprs1
            return self.simplify1()

    def interpret(self, theory):
        sub_exprs1 = [e.interpret(theory) for e in self.sub_exprs]
        if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
            return self
        else:
            self.sub_exprs = sub_exprs1
            return self.simplify1()


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
    def translate(self, case): return self.translated


def declare_var(name, sort):
    from DSLClasses import SymbolDeclaration
    return SymbolDeclaration(name=Symbol(name=name), sorts=[], out=sort)


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

    def translate(self, case: ConfigCase):
        self.translated =  If(self.sub_exprs[IfExpr.IF  ].translate(case)
                            , self.sub_exprs[IfExpr.THEN].translate(case)
                            , self.sub_exprs[IfExpr.ELSE].translate(case))
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
        self.translated = None
        self.type = 'bool'

        self.q_decls = {v:declare_var(v, s) \
                        for v, s in zip(self.vars, self.sorts)}

    def __repr__(self):
        return sys.intern(self.q \
            + "".join([v + "[" + s.str + "]" for v, s in zip(self.vars, self.sorts)]) \
            + " : " + self.sub_exprs[0].str)


    def annotate(self, symbol_decls, q_decls):
        for s in self.q_decls.values():
            s.annotate(symbol_decls, vocabulary=False)
        q_v = {**q_decls, **self.q_decls} # merge
        self.sub_exprs = [e.annotate(symbol_decls, q_v) for e in self.sub_exprs]
        return self

    def subtences(self):
        #TODO optionally add subtences of sub_exprs
        return {self.str: self}

    def expand_quantifiers(self, theory):
        forms = [self.sub_exprs[0].expand_quantifiers(theory)]
        final_vs = []
        for var, decl in self.q_decls.items():
            if decl.range:
                forms = [f.substitute(Symbol(name=var), val) for val in decl.range for f in forms]
            else:
                final_vs.append((var, decl))
        if 1 < len(forms):
            op = '∧' if self.q == '∀' else '∨'
            self.sub_exprs = [BinaryOperator(sub_exprs=forms, operator=[op]*(len(forms)-1))]
        else:
            self.sub_exprs = forms
        if final_vs:
            vs = list(zip(*final_vs))
            self.vars, self.sorts = vs[0], vs[1]
        else:
            self.vars, self.sorts = [], []
        return self

    def translate(self, case: ConfigCase):
        for v in self.q_decls.values():
            v.translate(case)
        if not self.vars:
            self.translated = self.sub_exprs[0].translate(case)
        else:
            finalvars, forms = self.vars, [f.translate(case) for f in self.sub_exprs]

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

    def translate(self, case: ConfigCase):
        # chained comparisons -> And()
        if self.operator[0] =='≠' and len(self.sub_exprs)==2:
            x = self.sub_exprs[0].translate(case)
            y = self.sub_exprs[1].translate(case)
            out = Not(x==y)
        elif self.operator[0] in '=<>≤≥≠':
            out = []
            for i in range(1, len(self.sub_exprs)):
                x = self.sub_exprs[i-1].translate(case)
                function = BinaryOperator.MAP[self.operator[i - 1]]
                y = self.sub_exprs[i].translate(case)
                try:
                    out = out + [function(x, y)]
                except Z3Exception as E:
                    raise DSLException("{}{}{}".format(str(x), self.operator[i - 1], str(y)))
            if 1 < len(out):
                out = And(out)
            else:
                out = out[0]
        elif self.operator[0] == '∧':
            out = And([e.translate(case) for e in self.sub_exprs])
        elif self.operator[0] == '∨':
            out = Or ([e.translate(case) for e in self.sub_exprs])
        else:
            out = self.sub_exprs[0].translate(case)

            for i in range(1, len(self.sub_exprs)):
                function = BinaryOperator.MAP[self.operator[i - 1]]
                out = function(out, self.sub_exprs[i].translate(case))
        self.translated = out
        return self.translated

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
        self.translated = None
        self.type = None

    def __repr__(self):
        return sys.intern(self.operator + self.sub_exprs[0].str)

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = self.sub_exprs[0].type
        return self

    def translate(self, case: ConfigCase):
        out = self.sub_exprs[0].translate(case)
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

        self.q_decls = {v:declare_var(v,s) \
                        for v, s in zip(self.vars, self.sorts)}
        self.sub_exprs = [self.f, self.out] if self.out else [self.f] # later: expressions to be summed
        self.str = repr(self)
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
        for s in self.q_decls.values():
            s.annotate(symbol_decls, vocabulary=False)
        q_v = {**q_decls, **self.q_decls} # merge
        self.sub_exprs = [e.annotate(symbol_decls, q_v) for e in self.sub_exprs]
        self.type = self.sub_exprs[AAggregate.OUT].type if self.out else 'int'
        return self
        
    def expand_quantifiers(self, theory):
        form = IfExpr(if_f=self.sub_exprs[AAggregate.CONDITION]
                    , then_f=NumberConstant(number='1') if self.out is None else self.sub_exprs[AAggregate.OUT]
                    , else_f=NumberConstant(number='0'))
        forms = [form.expand_quantifiers(theory)]
        for var, decl in self.q_decls.items():
            if decl.range:
                forms = [f.substitute(Symbol(name=var), val) for val in decl.range for f in forms]
            else:
                raise Exception('Can only quantify aggregates over finite domains')
        self.sub_exprs = forms
        return self

    def translate(self, case: ConfigCase):
        for v in self.q_decls.values():
            v.translate(case)
        self.translated = Sum([f.translate(case) for f in self.sub_exprs])
        return self.translated


class AppliedSymbol(Expression):
    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')
        self.sub_exprs = self.args.sub_exprs
        self.str = repr(self)
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
        out = super().subtences() # in case of predicate over boolean
        if self.type == 'bool': out[self.str] = self
        return out

    def interpret(self, theory):
        sub_exprs = [e.interpret(theory) for e in self.sub_exprs]
        if self.decl.interpretation is not None:
            return (self.decl.interpretation)(theory, 0, sub_exprs)
        else:
            return self


    def translate(self, case: ConfigCase):
        if self.translated is None:
            if self.s.name == 'abs':
                arg = self.sub_exprs[0].translate(case)
                self.translated = If(arg >= 0, arg, -arg)
            else:
                arg = [x.translate(case) for x in self.sub_exprs]
                self.translated = (self.decl.translated)(arg)
        return self.translated

class Arguments(object):
    def __init__(self, **kwargs):
        self.sub_exprs = kwargs.pop('sub_exprs')

class Variable(Expression):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.str = repr(self)
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

    def translate(self, case: ConfigCase):
        if self.translated is None:
            self.translated = self.decl.translated
        return self.translated
    
class Symbol(Variable): pass

    
class NumberConstant(Expression):
    def __init__(self, **kwargs):
        self.number = kwargs.pop('number')
        self.str = repr(self)
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

    def subtences(): return {}

    def translate(self, case: ConfigCase):
        return self.translated

class Brackets(Expression):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.reading = kwargs.pop('reading')
        self.sub_exprs = [self.f]
        self.str = repr(self)
        self.translated = None
        self.type = None

    def __repr__(self):
        return sys.intern("(" + self.sub_exprs[0].str + ")")

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = self.sub_exprs[0].type
        return self

    def translate(self, case: ConfigCase):
        self.translated = self.sub_exprs[0].translate(case)
        if self.reading: 
            self.sub_exprs[0].reading = self.reading
            self.translated.reading   = self.reading #TODO for explain
        return self.translated

