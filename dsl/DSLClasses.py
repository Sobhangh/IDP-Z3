import itertools as it
import os
import re
import sys

from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or, Not, And, obj_to_string, Const, ForAll, Exists, substitute, Z3Exception, \
    Sum, If, FuncDeclRef, BoolVal
from z3.z3 import _py2expr

from configcase import ConfigCase, singleton, in_list
from utils import is_number, universe, applyTo, log, itertools
from ASTNode import Expression

class DSLException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message


class Environment:
    def __init__(self, idp):
        self.idp = idp
        self.type_scope = {'Int': IntSort(), 'Bool': BoolSort(), 'Real': RealSort()}
        self.range_scope = {}


class Idp(object):
    def __init__(self, **kwargs):
        log("parsing done")
        self.vocabulary = kwargs.pop('vocabulary')
        self.theory = kwargs.pop('theory')
        self.structure = kwargs.pop('structure')

        self.goal = kwargs.pop('goal')
        if self.goal is None:
            self.goal = Goal(name="")
        self.view = kwargs.pop('view')
        if self.view is None:
            self.view = View(viewType='normal')

        if self.structure: self.structure.annotate(self.vocabulary)
        self.theory.annotate(self.vocabulary)
        log("annotated")

    def translate(self, case: ConfigCase):
        env = Environment(self)
        self.vocabulary.translate(case, env)
        log("vocabulary translated")
        self.theory.translate(case, env)
        log("theory translated")
        self.goal.translate(case)
        self.view.translate(case)


################################ Vocabulary  ###############################


class Vocabulary(object):
    def __init__(self, **kwargs):
        self.declarations = kwargs.pop('declarations')

        self.symbol_decls = {'int' : RangeDeclaration(name='int', elements=[]),
                             'real': RangeDeclaration(name='real', elements=[]),
                             'Bool': ConstructedTypeDeclaration(name='Bool', 
                                        constructors=[Symbol(name='true'), Symbol(name='false')])}
        for s in self.declarations: 
            s.annotate(self.symbol_decls)

    def __str__(self):
        return ( "vocabulary {\n"
               + "\n".join(str(i) for i in self.declarations)
               + "\n}\n" )

    def translate(self, case: ConfigCase, env: Environment):
        for i in self.declarations:
            if type(i) in [ConstructedTypeDeclaration, RangeDeclaration]:
                i.translate(case, env)
        for i in self.declarations:
            if type(i) == SymbolDeclaration:
                i.translate(case, env)


class ConstructedTypeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.constructors = kwargs.pop('constructors')
        self.is_var = False
        self.range = self.constructors # functional constructors are expanded
        # .type = None
        # .translated
        # .range # list of constructors

    def __str__(self):
        return ( "type " + self.name
               + " constructed from {"
               + ",".join(map(str, self.constructors))
               + "}")

    def annotate(self, symbol_decls):
        symbol_decls[self.name] = self
        for c in self.constructors:
            c.type = self
            symbol_decls[c.name] = c
        self.type = None
        self.range = self.constructors #TODO constructor functions

    def translate(self, case: ConfigCase, env: Environment):
        self.translated, cstrs = case.EnumSort(self.name, [c.name for c in self.constructors])
        for c, c3 in zip(self.constructors, cstrs):
            c.translated = c3

        env.type_scope[self.name] = self.translated
        env.range_scope[self.name] = cstrs
        return self.translated


class Constructor(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.is_var = False
        self.str = sys.intern(self.name)
        # .type
        # .translated
    
    def __str__(self): return self.str

    # A constructor behaves like an Expression
    def annotate(self, symbol_decls, q_decls): return self
    def subtences(self): return []
    def substitute(self, e0, e1): return self
    def expand_quantifiers(self, theory): return self
    def interpret(self, theory): return self
    def translate(self, case, env): return self.translated


class RangeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name') # maybe 'int', 'real'
        self.elements = kwargs.pop('elements')
        self.is_var = False

        self.range = []
        for x in self.elements:
            if x.toI is None:
                self.range.append(x.fromI)
            else: #TODO test that it is an integer ?
                for i in range(x.fromI.translated, x.toI.translated + 1):
                    self.range.append(NumberConstant(number=str(i)))
        # .type = None
        # .translated

    def __str__(self):
        return ( "type " + self.name
               + " = {"
               + ";".join([str(x.fromI) + ("" if x.toI is None else ".."+ str(x.toI)) for x in self.elements])
               + "}")

    def annotate(self, symbol_decls): 
        symbol_decls[self.name] = self
        self.type = None

    def translate(self, case: ConfigCase, env: Environment):
        els = [e.translated for e in self.range]
        case.enums[self.name] = els
        if self.name == 'int':
            self.translated = IntSort() 
        elif self.name == 'real':
            self.translated = RealSort() 
        elif all(map(lambda x: type(x) == int, els)):
            self.translated = IntSort()
        else:
            self.translated = RealSort()
        env.range_scope[self.name] = els
        env.type_scope[self.name] = self.translated
        return self.translated


class SymbolDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name').name # a string, not a Symbol
        self.sorts = kwargs.pop('sorts')
        self.out = kwargs.pop('out')
        if self.out is None:
            self.out = Sort(name='Bool')

        self.is_var = True #TODO unless interpreted

        # .vocabulary: False if declared in quantifier, aggregate, rule
        # .type: a declaration object
        # .domain: all possible arguments
        # .instances: {string: Variable or AppliedSymbol} translated applied symbols, not starting with '_'
        # .range: all possible values
        # .translated
        # .interpretation : f:tuple -> Expression (only if it is given in a structure)

    def __str__(self):
        return ( self.name
               + ("({})".format(",".join(map(str, self.sorts))) if 0<len(self.sorts) else "")
               + ("" if self.out.name == 'Bool' else " : " + self.out.name)
        )

    def annotate(self, symbol_decls, vocabulary=True):
        self.vocabulary = vocabulary
        if vocabulary: symbol_decls[self.name] = self
        for s in self.sorts:
            s.annotate(symbol_decls)
        self.out.annotate(symbol_decls)
        self.domain = list(itertools.product(*[s.decl.range for s in self.sorts]))

        self.type = self.out.decl
        self.range = self.type.range

        self.instances = {}
        if vocabulary and not self.name.startswith('_'):
            if len(self.sorts) == 0:
                expr = Variable(name=self.name)
                expr.annotate(symbol_decls, {})
                expr.normal = True
                self.instances[expr.str] = expr
            else:
                for arg in list(self.domain):
                    expr = AppliedSymbol(s=Symbol(name=self.name), args=Arguments(sub_exprs=arg))
                    expr.annotate(symbol_decls, {})
                    expr.normal = True
                    self.instances[expr.str] = expr
        

    def translate(self, case: ConfigCase, env: Environment):
        case.symbol_types[self.name] = self.out.name
        if len(self.sorts) == 0:
            self.translated = case.Const(self.name, self.out.translate(case, env))
            self.normal = True
        elif self.out.name == 'Bool':
            types = [x.translate(case, env) for x in self.sorts]
            rel_vars = [t.getRange(env) for t in self.sorts]
            self.translated = case.Predicate(self.name, types, rel_vars, True)
        else:
            types = [x.translate(case, env) for x in self.sorts] + [self.out.translate(case, env)]
            rel_vars = [t.getRange(env) for t in self.sorts + [self.out]]
            self.translated = case.Function(self.name, types, rel_vars, True)

        for inst in self.instances.values():
            inst.translate(case, env)

        if self.vocabulary and len(self.sorts) == 0 and self.range: #TODO also for Functions ? (done in CaseConfig)
            domain = in_list(self.translated, [v.translated for v in self.range])
            domain.reading = "Possible values for " + self.name
            case.typeConstraints.append(domain)
        return self.translated


class Sort(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.str = sys.intern(self.name)
        # .decl

    def __str__(self): return self.str

    def annotate(self, symbol_decls):
        self.decl = symbol_decls[self.name]

    def translate(self, case, env: Environment):
        if self.name in env.type_scope:
            return env.type_scope[self.name]
        elif self.name == "int":
            return IntSort()
        elif self.name == "real":
            return RealSort()
        else:
            raise Exception("Unknown sort: " + self.name)

    def getRange(self, env: Environment):
        if self.name in env.range_scope:
            return env.range_scope[self.name]
        elif self.name == "int":
            return []
        elif self.name == "real":
            return []
        else:
            return universe(self.translate(env))


################################ Theory ###############################


class Theory(object):
    def __init__(self, **kwargs):
        self.constraints = kwargs.pop('constraints')
        self.definitions = kwargs.pop('definitions')
        # self.symbol_decls : {string: decl}
        # self.subtences, i.e., sub-sentences.  {string: Expression}

    def annotate(self, vocabulary):
        self.symbol_decls = vocabulary.symbol_decls
        self.subtences = {}
        self.constraints = [e.annotate(self.symbol_decls, {}) for e in self.constraints]
        for e in self.constraints:
            self.subtences.update(e.subtences())
        self.constraints = [e.expand_quantifiers(self) for e in self.constraints]
        self.constraints = [e.interpret         (self) for e in self.constraints]

        self.definitions = [e.annotate(self.symbol_decls, {}) for e in self.definitions]
        for e in self.definitions:
            self.subtences.update(e.subtences())
        self.definitions = [e.expand_quantifiers(self) for e in self.definitions]
        self.definitions = [e.interpret         (self) for e in self.definitions]

    def translate(self, case: ConfigCase, env: Environment):
        for i in self.constraints:
            log("translating " + str(i)[:20])
            c = i.translate(case, env)
            case.add(c, str(i))
        for d in self.definitions:
            d.translate(case, env)


class Definition(object):
    def __init__(self, **kwargs):
        self.rules = kwargs.pop('rules')
        # .partition : {Symbol: [Transformed Rule]}

    def annotate(self, symbol_decls, q_decls):
        self.rules = [r.annotate(symbol_decls, q_decls) for r in self.rules]

        self.partition = {}
        for i in self.rules:
            self.partition.setdefault(symbol_decls[i.symbol.name], []).append(i)
        return self

    def subtences(self):
        out = {}
        for r in self.rules: out.update(r.subtences())
        return out

    def expand_quantifiers(self, theory):
        for symbol, rules in self.partition.items():
            self.partition[symbol] = sum((r.expand_quantifiers(theory) for r in rules), [])
        return self

    def interpret(self, theory):
        for symbol, rules in self.partition.items():
            self.partition[symbol] = sum((r.interpret(theory) for r in rules), [])
        return self

    def translate(self, case: ConfigCase, env: Environment):
        for symbol, rules in self.partition.items():
            z3_symb = symbol.translate(case, env)
            if type(z3_symb) == FuncDeclRef:
                vars = [Const('ci'+str(i), z3_symb.domain(i)) for i in range(0, z3_symb.arity())] + [
                    Const('cout', z3_symb.range())]
            else:
                vars = [Const('c', z3_symb.sort())]

            exprs, outputVar = [], False
            for i in rules:
                exprs.append(i.translate(vars, case, env))
                if i.out is not None:
                    outputVar = True
                    
            if outputVar:
                case.add(ForAll(vars, 
                                (applyTo(symbol.translate(case, env), vars[:-1]) == vars[-1]) == Or(exprs)), 
                         str(self))
            else:
                if len(vars) > 1:
                    case.add(ForAll(vars, 
                                    applyTo(symbol.translate(case, env), vars[:-1]) == Or(exprs)), 
                             str(self))
                else:
                    case.add(symbol.translate(case, env) == Or(exprs), str(self))


class Rule(object):
    def __init__(self, **kwargs):
        self.reading = kwargs.pop('reading')
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.symbol = kwargs.pop('symbol')
        self.args = kwargs.pop('args') # later augmented with self.out, if any
        self.out = kwargs.pop('out')
        self.body = kwargs.pop('body')

        assert len(self.sorts) == len(self.vars)
        self.q_decls = {v:SymbolDeclaration(name=Symbol(name=v), sorts=[], out=s) \
                        for v, s in zip(self.vars, self.sorts)}
        self.args = [] if self.args is None else self.args.sub_exprs
        if self.out is not None:
            self.args.append(self.out)
        if self.body is None:
            self.body = Symbol(name='true')
        # .translated

    def annotate(self, symbol_decls, q_decls):
        for s in self.q_decls.values():
            s.annotate(symbol_decls, vocabulary=False)
        q_v = {**q_decls, **self.q_decls} # merge
        self.args = [arg.annotate(symbol_decls, q_v) for arg in self.args]
        self.out = self.out.annotate(symbol_decls, q_v) if self.out else self.out
        self.body = self.body.annotate(symbol_decls, q_v)
        return self

    def subtences(self):
        return self.body.subtences() if not self.vars else {}

    def expand_quantifiers(self, theory):
        forms = [(self.args, self.body.expand_quantifiers(theory))]
        final_vs = []
        for var, decl in self.q_decls.items():
            if decl.range:
                forms = [([a.substitute(Symbol(name=var), val) for a in args], 
                          f.substitute(Symbol(name=var), val)) 
                          for val in decl.range for (args, f) in forms]
            else:
                final_vs.append((var, sort))
        if final_vs:
            vs = list(zip(*final_vs))
            vars, sorts = vs[0], vs[1]
        else:
            vars, sorts = [], []

        return [Rule(reading=self.reading, vars=vars, sorts=sorts, symbol=self.symbol, 
                     args=Arguments(sub_exprs=args[:-1] if self.out else args), 
                     out=args[-1] if self.out else None, body=f) 
                for (args, f) in forms]

    def interpret(self, theory):
        self.body = self.body.interpret(theory)
        return [self]

    def translate(self, new_vars, case: ConfigCase, env: Environment):
        """ returns (?vars0,...: new_vars0=args0 & new_vars1=args1 .. & body(vars)) """

        log("translating rule " + str(self.body)[:20])
        for v in self.q_decls.values():
            v.translate(case, env)

        # translate self.vars into z3vars
        z3vars = []
        for var, sort in zip(self.vars, self.sorts):
            z3var = Const(var, sort.translate(env))
            z3vars.append(z3var)

        out = [] # new_vars0=args0 & new_vars1=args1 .. & body(vars) #TODO move to expand_quantifiers
        for new_var, arg in zip(new_vars, self.args):
            out.append(new_var == arg.translate(case, env))
        out.append(self.body.translate(case, env))

        if len(z3vars) == 0:
            self.translated = And(out)
        else:
            self.translated = Exists(z3vars, And(out))
        return self.translated

# Expressions

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
        # self.type

    def __repr__(self):
        return sys.intern("if "    + self.sub_exprs[IfExpr.IF  ].str \
                        + " then " + self.sub_exprs[IfExpr.THEN].str \
                        + " else " + self.sub_exprs[IfExpr.ELSE].str)

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        #TODO verify consistency
        self.type = self.sub_exprs[IfExpr.THEN].type
        return self

    def translate(self, case: ConfigCase, env: Environment):
        self.translated =  If(self.sub_exprs[IfExpr.IF  ].translate(case, env)
                            , self.sub_exprs[IfExpr.THEN].translate(case, env)
                            , self.sub_exprs[IfExpr.ELSE].translate(case, env))
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

        self.q_decls = {v:SymbolDeclaration(name=Symbol(name=v), sorts=[], out=s) \
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
        self.type = 'Bool'
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

    def translate(self, case: ConfigCase, env: Environment):
        for v in self.q_decls.values():
            v.translate(case, env)
        if not self.vars:
            self.translated = self.sub_exprs[0].translate(case, env)
        else:
            finalvars, forms = self.vars, [f.translate(case, env) for f in self.sub_exprs]

            if self.q == '∀':
                forms = And(forms) if 1<len(forms) else forms[0]
                if len(finalvars) > 0: # not fully expanded !
                    forms = ForAll(finalvars, forms)
            else:
                forms = Or(forms) if 1<len(forms) else forms[0]
                if len(finalvars) > 0: # not fully expanded !
                    forms = Exists(finalvars, forms)
            case.mark_atom(self, forms)
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

    def __repr__(self):
        temp = self.sub_exprs[0].str
        for i in range(1, len(self.sub_exprs)):
            temp += " " + self.operator[i-1] + " " + self.sub_exprs[i].str
        return sys.intern(temp)

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = 'Bool' if self.operator[0] in '&|^∨⇒⇐⇔' \
               else 'Bool' if self.operator[0] in '=<>≤≥≠' \
               else 'real' if any(e.type == 'real' for e in self.sub_exprs) \
               else 'int'
        return self

    def subtences(self):
        #TODO collect subtences of aggregates within comparisons
        return {self.str: self} if self.operator[0] in '=<>≤≥≠' \
            else super().subtences()

    def translate(self, case: ConfigCase, env: Environment):
        # chained comparisons -> And()
        if self.operator[0] =='≠' and len(self.sub_exprs)==2:
            x = self.sub_exprs[0].translate(case, env)
            y = self.sub_exprs[1].translate(case, env)
            atom = x==y
            case.mark_atom(self, atom)
            out = Not(atom)
        elif self.operator[0] in '=<>≤≥≠':
            out = []
            for i in range(1, len(self.sub_exprs)):
                x = self.sub_exprs[i-1].translate(case, env)
                function = BinaryOperator.MAP[self.operator[i - 1]]
                y = self.sub_exprs[i].translate(case, env)
                try:
                    out = out + [function(x, y)]
                except Z3Exception as E:
                    raise DSLException("{}{}{}".format(str(x), self.operator[i - 1], str(y)))
            if 1 < len(out):
                out = And(out)
            else:
                out = out[0]
            case.mark_atom(self, out)
        else:
            out = self.sub_exprs[0].translate(case, env)

            for i in range(1, len(self.sub_exprs)):
                function = BinaryOperator.MAP[self.operator[i - 1]]
                out = function(out, self.sub_exprs[i].translate(case, env))
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

    def __repr__(self):
        return sys.intern(self.operator + self.sub_exprs[0].str)

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = self.sub_exprs[0].type
        return self

    def translate(self, case: ConfigCase, env: Environment):
        out = self.sub_exprs[0].translate(case, env)
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

        self.q_decls = {v:SymbolDeclaration(name=Symbol(name=v), sorts=[], out=s) \
                        for v, s in zip(self.vars, self.sorts)}
        self.sub_exprs = [self.f, self.out] if self.out else [self.f] # later: expressions to be summed
        self.str = repr(self)

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

    def translate(self, case: ConfigCase, env: Environment):
        for v in self.q_decls.values():
            v.translate(case, env)
        self.translated = Sum([f.translate(case, env) for f in self.sub_exprs])
        return self.translated


class AppliedSymbol(Expression):
    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')
        self.sub_exprs = self.args.sub_exprs
        self.str = repr(self)
        # .decl 
        # .type
        # .normal (only if ground) used on client side
        # .translated

    def __repr__(self):
        return sys.intern(self.s.str + "(" + ",".join([x.str for x in self.sub_exprs]) + ")")

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.decl = q_decls[self.s.name] if self.s.name in q_decls else symbol_decls[self.s.name]
        self.type = self.decl.type
        return self

    def subtences(self):
        out = super().subtences() # in case of predicate over boolean
        if self.type == 'Bool': out[self.str] = self
        return out

    def interpret(self, theory):
        sub_exprs = [e.interpret(theory) for e in self.sub_exprs]
        if hasattr(self.decl, "interpretation"):
            return (self.decl.interpretation)(theory, 0, sub_exprs)
        else:
            return self


    def translate(self, case: ConfigCase, env: Environment):
        if not hasattr(self, "translated"):
            if self.s.name == 'abs':
                arg = self.sub_exprs[0].translate(case,env)
                self.translated = If(arg >= 0, arg, -arg)
            else:
                arg = [x.translate(case, env) for x in self.sub_exprs]
                self.translated = (self.decl.translated)(arg)
                case.mark_atom(self, self.translated)
        return self.translated

class Arguments(object):
    def __init__(self, **kwargs):
        self.sub_exprs = kwargs.pop('sub_exprs')

class Variable(Expression):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.str = repr(self)
        self.sub_exprs = []
        if self.name == "true":
            self.type = 'Bool'
            self.translated = bool(True)
        elif self.name == "false":
            self.type = 'Bool'
            self.translated = bool(False)
        # .decl
        # .type
        # .normal (only if ground)
        # .translated

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
            else {self.str: self} if self.type == 'Bool' \
            else {}

    def translate(self, case: ConfigCase, env: Environment):
        if not hasattr(self, 'translated'):
            out = self.decl.translated
            self.translated = out
            case.mark_atom(self, out) #TODO ??
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

    def translate(self, case: ConfigCase, env: Environment):
        return self.translated

class Brackets(Expression):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.reading = kwargs.pop('reading')
        self.sub_exprs = [self.f]
        self.str = repr(self)

    def __repr__(self):
        return sys.intern("(" + self.sub_exprs[0].str + ")")

    def annotate(self, symbol_decls, q_decls):
        self.sub_exprs = [e.annotate(symbol_decls, q_decls) for e in self.sub_exprs]
        self.type = self.sub_exprs[0].type
        return self

    def translate(self, case: ConfigCase, env: Environment):
        self.translated = self.sub_exprs[0].translate(case, env)
        if self.reading: 
            self.sub_exprs[0].reading = self.reading
            self.translated.reading   = self.reading #TODO for explain
        return self.translated


################################ Structure ###############################

class Structure(object):
    def __init__(self, **kwargs):
        self.interpretations = kwargs.pop('interpretations')

    def annotate(self, vocabulary):
        for i in self.interpretations:
            i.annotate(vocabulary.symbol_decls)

class Interpretation(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name').name
        self.tuples = kwargs.pop('tuples')
        self.default = kwargs.pop('default') # later set to False for predicates
        
        # .function : -1 if function else 0
        # .arity
        # .decl : symbol declaration

    def annotate(self, symbol_decls):
        self.decl = symbol_decls[self.name]
        for t in self.tuples:
            t.annotate(symbol_decls)
        self.function = 0 if self.decl.out.name == 'Bool' else -1
        self.arity = len(self.tuples[0].args) # there must be at least one tuple !
        if self.function and 1 < self.arity and self.default is None:
            raise Exception("Default value required for function {} in structure.".format(self.name))
        self.default = self.default if self.function else Symbol(name='false')

        def interpret(theory, rank, args, tuples=None):
            tuples = [tuple.interpret(theory) for tuple in self.tuples] if tuples == None else tuples
            if rank == self.arity + self.function: # valid tuple -> return a value
                if not self.function:
                    return Symbol(name='true')
                else:
                    if 1 < len(tuples):
                        #raise Exception("Duplicate values in structure for " + str(symbol))
                        print("Duplicate values in structure for " + str(self.name) + str(tuples[0]) )
                    return tuples[0].args[rank]
            else: # constructs If-then-else recursively
                out = self.default
                tuples.sort(key=lambda t: str(t.args[rank]))
                groups = it.groupby(tuples, key=lambda t: t.args[rank])

                if type(args[rank]) in [Constructor, NumberConstant]:
                    for val, tuples2 in groups: # try to resolve
                        if args[rank] == val:
                            out = interpret(theory, rank+1, args, list(tuples2))
                else:
                    for val, tuples2 in groups:
                        out = IfExpr(if_f=BinaryOperator(sub_exprs=[args[rank],val], operator='='), 
                                        then_f=interpret(theory, rank+1, args, list(tuples2)), 
                                        else_f=out)
                return out
        self.decl.interpretation = interpret
        self.decl.is_var = False



class Tuple(object):
    def __init__(self, **kwargs):
        self.args = kwargs.pop('args')

    def __str__(self):
        return ",".join([str(a) for a in self.args])

    def annotate(self, symbol_decls):
        self.args = [arg.annotate(symbol_decls, {}) for arg in self.args]

    def interpret(self, theory): return self #TODO ?

    def translate(self, case: ConfigCase, env: Environment):
        return [arg.translate(case, env) for arg in self.args]


################################ Goal, View ###############################

class Goal(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def translate(self, case: ConfigCase):
        case.goal = case.symbols[self.name] if self.name else ""
        return


class View(object):
    def __init__(self, **kwargs):
        self.viewType = kwargs.pop('viewType')

    def translate(self, case: ConfigCase):
        case.view = self.viewType
        return

################################ Main ###############################

dslFile = os.path.join(os.path.dirname(__file__), 'DSL.tx')

idpparser = metamodel_from_file(dslFile, memoization=True, classes=
        [ Idp, 
          Vocabulary, ConstructedTypeDeclaration, Constructor, RangeDeclaration, SymbolDeclaration, Symbol, Sort,
          Theory, Definition, Rule, IfExpr, AQuantification, 
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate,
                    AppliedSymbol, Variable, NumberConstant, Brackets, Arguments,
          Interpretation, Structure, Tuple,
          Goal, View
        ])
