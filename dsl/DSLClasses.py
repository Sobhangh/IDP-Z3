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
        self.var_scope = {}
        self.type_scope = {'Int': IntSort(), 'Bool': BoolSort(), 'Real': RealSort()}
        self.range_scope = {}
        self.level = 0 # depth of quantifier


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

        self.theory.annotate(self.vocabulary)
        log("annotated")

    def translate(self, case: ConfigCase):
        env = Environment(self)
        self.vocabulary.translate(case, env)
        log("vocabulary translated")
        if self.structure:
            self.structure.translate(case, env)
            log("structure translated")
        self.theory.translate(case, env)
        log("theory translated")
        self.goal.translate(case)
        self.view.translate(case)


################################ Vocabulary  ###############################


class Vocabulary(object):
    def __init__(self, **kwargs):
        self.declarations = kwargs.pop('declarations')

        self.symbol_decls = {'int' : RangeDeclaration(name='int', elements=[]),
                             'real': RangeDeclaration(name='real', elements=[])}
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
        self.range = [Symbol(name=c.name) for c in self.constructors] #TODO constructor functions

    def translate(self, case: ConfigCase, env: Environment):
        self.translated, cstrs = case.EnumSort(self.name, [c.name for c in self.constructors])
        for c, c3 in zip(self.constructors, cstrs):
            c.translated = c3

        env.type_scope[self.name] = self.translated
        for i in cstrs:
            env.var_scope[obj_to_string(i)] = i
        env.range_scope[self.name] = cstrs


class Constructor(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.is_var = False
        self.str = sys.intern(self.name)
        # .type
        # .translated
    
    def __str__(self): return self.str


class RangeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.elements = kwargs.pop('elements')
        self.is_var = False

        self.range = []
        for x in self.elements:
            if x.toI is None:
                self.range.append(x.fromI)
            else: #TODO test that it is an integer ?
                for i in range(x.fromI.translated, x.toI.translated + 1):
                    self.range.append(NumberConstant(number=str(i)))
        # self.type = None

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
        if all(map(lambda x: type(x) == int, els)):
            env.type_scope[self.name] = IntSort()
        else:
            env.type_scope[self.name] = RealSort()
        env.range_scope[self.name] = els


class SymbolDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name').name # a string, not a Symbol
        self.sorts = kwargs.pop('sorts')
        self.out = kwargs.pop('out')
        if self.out is None:
            self.out = Sort(name='Bool')
        self.is_var = True #TODO unless interpreted
        # .type : a declaration object, or 'Bool', 'real', 'int'
        # .domain: all possible arguments
        # .instances: {string: Z3expr} translated applied symbols, not starting with '_'

    def __str__(self):
        return ( self.name
               + ("({})".format(",".join(map(str, self.sorts))) if 0<len(self.sorts) else "")
               + ("" if self.out.name == 'Bool' else " : " + self.out.name)
        )

    def annotate(self, symbol_decls):
        symbol_decls[self.name] = self
        self.domain = list(itertools.product(*[symbol_decls[s.name].range for s in self.sorts]))
        if self.out.name == 'Bool':
            self.type = 'Bool'
            self.range = [Symbol(name="true"), Symbol(name="false")] #TODO annotate them 
        elif self.out.name in ['real', 'int']:
            self.type = self.out.name
            self.range = None
        elif self.out.name in symbol_decls:
            self.type = symbol_decls[self.out.name]
            self.range = self.type.range
        else:
            assert False, "Unknown type: " + self.out.name
        

    def translate(self, case: ConfigCase, env: Environment):
        case.symbol_types[self.name] = self.out.name
        if len(self.sorts) == 0:
            self.translated = case.Const(self.name, self.out.translate(env))
            self.normal = True
            if len(self.out.getRange(env)) > 1:
                domain = in_list(self.translated, self.out.getRange(env))
                domain.reading = "Possible values for " + self.name
                case.typeConstraints.append(domain)
        elif self.out.name == 'Bool':
            types = [x.translate(env) for x in self.sorts]
            rel_vars = [t.getRange(env) for t in self.sorts]
            self.translated = case.Predicate(self.name, types, rel_vars, True)
        else:
            types = [x.translate(env) for x in self.sorts] + [self.out.translate(env)]
            rel_vars = [t.getRange(env) for t in self.sorts + [self.out]]
            self.translated = case.Function(self.name, types, rel_vars, True)
        env.var_scope[self.name] = self.translated

        self.instances = {}
        if not self.name.startswith('_'):
            if len(self.sorts) == 0:
                expr = Variable(name=self.name)
                expr.translate(case, env)
                expr.normal = True
                self.instances[expr.str] = expr
            else:
                for arg in list(self.domain):
                    expr = AppliedSymbol(s=Symbol(name=self.name), args=Arguments(sub_exprs=arg))
                    expr.translate(case, env)
                    expr.normal = True
                    self.instances[expr.str] = expr
        return self.translated


class Sort(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.str = sys.intern(self.name)

    def __str__(self): return self.str

    def translate(self, env: Environment):
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
        for e in self.constraints:
            e.annotate(self.symbol_decls, {})
            self.subtences.update(e.subtences())
        self.constraints = [e.expand_quantifiers(self) for e in self.constraints]
        for e in self.definitions: 
            e.annotate(self.symbol_decls, {})
            self.subtences.update(e.subtences())
        self.definitions = [e.expand_quantifiers(self) for e in self.definitions]

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

    def annotate(self, symbol_decls, q_vars):
        for r in self.rules: r.annotate(symbol_decls, q_vars)

        self.partition = {}
        for i in self.rules:
            self.partition.setdefault(symbol_decls[i.symbol.name], []).append(i)

    def subtences(self):
        out = {}
        for r in self.rules: out.update(r.subtences())
        return out

    def expand_quantifiers(self, theory):
        for symbol, rules in self.partition.items():
            self.partition[symbol] = sum((r.expand_quantifiers(theory) for r in rules), [])
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
        self.args = [] if self.args is None else self.args.sub_exprs
        if self.out is not None:
            self.args.append(self.out)
        if self.body is None:
            self.body = Symbol(name='true')
        # .translated

    def annotate(self, symbol_decls, q_vars):
        q_v = q_vars.copy() # shallow copy
        for v, s in zip(self.vars, self.sorts):
            q_v[v] = symbol_decls[s.name]
        self.body.annotate(symbol_decls, q_v)

    def subtences(self):
        return self.body.subtences() if not self.vars else {}

    def expand_quantifiers(self, theory):
        forms = [(self.args, self.body.expand_quantifiers(theory))]
        final_vs = []
        for var, sort in zip(self.vars, self.sorts):
            if sort.name in theory.symbol_decls:
                range_ = theory.symbol_decls[sort.name].range
                forms = [([a.substitute(Symbol(name=var), val) for a in args], 
                          f.substitute(Symbol(name=var), val)) 
                          for val in range_ for (args, f) in forms]
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
        
    def translate(self, new_vars, case: ConfigCase, env: Environment):
        """ returns (?vars0,...: new_vars0=args0 & new_vars1=args1 .. & body(vars)) """

        log("translating rule " + str(self.body)[:20])

        # translate self.vars into z3vars
        backup, z3vars = env.var_scope.copy(), []
        for var, sort in zip(self.vars, self.sorts):
            z3var = Const(var, sort.translate(env))
            env.var_scope[var] = v
            z3vars.append(z3var)

        out = [] # new_vars0=args0 & new_vars1=args1 .. & body(vars)
        for new_var, arg in zip(new_vars, self.args):
            out.append(new_var == arg.translate(case, env))
        out.append(self.body.translate(case, env))

        env.var_scope = backup

        if len(z3vars) == 0:
            self.translated = And(out)
        else:
            self.translated = Exists(z3vars, And(out))
        print(self.translated)
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

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        #TODO verify consistency
        self.type = self.sub_exprs[IfExpr.THEN].type

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

    def __repr__(self):
        return sys.intern(self.q \
            + "".join([v + "[" + s.str + "]" for v, s in zip(self.vars, self.sorts)]) \
            + " : " + self.sub_exprs[0].str)


    def annotate(self, symbol_decls, q_vars):
        q_v = q_vars.copy() # shallow copy
        for v, s in zip(self.vars, self.sorts):
            q_v[v] = symbol_decls[s.name]
        for e in self.sub_exprs: e.annotate(symbol_decls, q_v)
        self.type = 'Bool'

    def subtences(self):
        #TODO optionally add subtences of sub_exprs
        return {self.str: self}

    def expand_quantifiers(self, theory):
        forms = [self.sub_exprs[0].expand_quantifiers(theory)]
        final_vs = []
        for var, sort in zip(self.vars, self.sorts):
            if sort.name in theory.symbol_decls:
                range_ = theory.symbol_decls[sort.name].range
                forms = [f.substitute(Symbol(name=var), val) for val in range_ for f in forms]
            else:
                final_vs.append((var, sort))
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

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        self.type = 'Bool' if self.operator[0] in '&|^∨⇒⇐⇔' \
               else 'Bool' if self.operator[0] in '=<>≤≥≠' \
               else 'real' if any(e.type == 'real' for e in self.sub_exprs) \
               else 'int'

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
                out.is_chained = True
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

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        self.type = self.sub_exprs[0].type

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

    def annotate(self, symbol_decls, q_vars):   
        q_v = q_vars.copy() # shallow copy
        for v, s in zip(self.vars, self.sorts):
            q_v[v] = symbol_decls[s.name]
        for e in self.sub_exprs: e.annotate(symbol_decls, q_v)
        self.type = self.sub_exprs[AAggregate.OUT].type if self.out else 'int'
        
    def expand_quantifiers(self, theory):
        form = IfExpr(if_f=self.sub_exprs[AAggregate.CONDITION]
                    , then_f=NumberConstant(number='1') if self.out is None else self.sub_exprs[AAggregate.OUT]
                    , else_f=NumberConstant(number='0'))
        forms = [form.expand_quantifiers(theory)]
        for var, sort in zip(self.vars, self.sorts):
            if sort.name in theory.symbol_decls:
                range_ = theory.symbol_decls[sort.name].range
                forms = [f.substitute(Symbol(name=var), val) for val in range_ for f in forms]
            else:
                raise Exception('Can only quantify aggregates over finite domains')
        self.sub_exprs = forms
        return self

    def translate(self, case: ConfigCase, env: Environment):
        self.translated = Sum([f.translate(case, env) for f in self.sub_exprs])
        return self.translated


class AppliedSymbol(Expression):
    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')
        self.sub_exprs = self.args.sub_exprs
        self.str = repr(self)

    def __repr__(self):
        return sys.intern(self.s.str + "(" + ",".join([x.str for x in self.sub_exprs]) + ")")

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        self.type = q_vars.get(self.s.name, symbol_decls[self.s.name].type)

    def subtences(self):
        out = super().subtences() # in case of predicate over boolean
        if self.type == 'Bool': out[self.str] = self
        return out

    def translate(self, case: ConfigCase, env: Environment):
        if self.s.name == 'abs':
            arg = self.sub_exprs[0].translate(case,env)
            self.translated = If(arg >= 0, arg, -arg)
        else:
            s = self.s.translate(case, env)
            arg = [x.translate(case, env) for x in self.sub_exprs]
            out = s(arg)
            if hasattr(s, 'interpretation'):
                out.interpretation = s.interpretation(0, arg)
                case.mark_atom(self, out)
                self.translated = out.interpretation
            else:
                case.mark_atom(self, out)
                self.translated = out
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

    def __repr__(self):
        return sys.intern(self.name)

    def annotate(self, symbol_decls, q_vars):
        self.type = 'Bool' if self.name in ['true', 'false'] \
            else q_vars[self.name] if self.name in q_vars \
            else symbol_decls[self.name].type

    def subtences(self):
        return {} if self.name in ['true', 'false'] \
            else {self.str: self} if self.type == 'Bool' \
            else {}

    def translate(self, case: ConfigCase, env: Environment):
        if not hasattr(self, 'translated'):
            out = env.var_scope[self.name]
            if hasattr(out, 'interpretation') and (not hasattr(out, 'arity') or out.arity() == 0):
                # exclude applied symbols
                try:
                    out.interpretation = out.interpretation(0, []) # if not computed yet
                except: pass
                case.mark_atom(self, out)
                self.translated = out.interpretation
            else:
                case.mark_atom(self, out)
                self.translated = out
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

    def annotate(self, symbol_decls, q_vars): pass

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

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        self.type = self.sub_exprs[0].type

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

    def translate(self, case: ConfigCase, env: Environment):
        for i in self.interpretations:
            i.translate(case, env)

class Interpretation(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name').name
        self.tuples = kwargs.pop('tuples')
        self.default = kwargs.pop('default')

    def translate(self, case: ConfigCase, env: Environment):
        symbol = env.var_scope[self.name]
        case.interpreted[self.name] = True
        function = -1 if symbol.__class__.__name__ == "ArithRef" or symbol.range() != BoolSort() else 0
        arity = len(self.tuples[0].args) # there must be at least one tuple !
        if function and 1 < arity and self.default is None:
            raise Exception("Default value required for function {} in structure.".format(self.name))

        # create a macro and attach it to the symbol
        def interpretation(rank, args, tuples=None):
            tuples = [tuple.translate(case, env) for tuple in self.tuples] if tuples == None else tuples
            if rank == arity+function: # return a value
                if not function:
                    return BoolVal(True)
                else:
                    if 1 < len(tuples):
                        #raise Exception("Duplicate values in structure for " + str(symbol))
                        print("Duplicate values in structure for " + str(symbol) + str(tuples[0]) )
                    return tuples[0][rank]
            else: # constructs If-then-else recursively
                out = self.default.translate(case, env) if function else BoolVal(False)

                tuples.sort(key=lambda t: str(t[rank]))
                groups = it.groupby(tuples, key=lambda t: t[rank])

                if type(args[rank]) == type(tuples[0][rank]): # immediately resolve
                    for val, tuples2 in groups:
                        if args[rank] == val:
                            out = interpretation(rank+1, args, list(tuples2))
                else:
                    for val, tuples2 in groups:
                        out = If(args[rank]==val, interpretation(rank+1, args, list(tuples2)), out)
                return out
        symbol.interpretation = interpretation

class Tuple(object):
    def __init__(self, **kwargs):
        self.args = kwargs.pop('args')

    def __str__(self):
        return ",".join([str(a) for a in self.args])

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
