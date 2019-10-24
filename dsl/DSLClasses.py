import itertools as it
import os
import re

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

        self.symbol_decls = {}
        for s in self.declarations: self.symbol_decls.update(s.symbol_decls)

        for s in self.declarations: s.annotate(self.symbol_decls)

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
        self.symbol_decls = {self.name : self }
        self.is_var = False
        for c in self.constructors:
            c.type = self
            self.symbol_decls[c.name] = self
        # .type = None
        # .translated
        # .range # list of constructors

    def __str__(self):
        return ( "type " + self.name
               + " constructed from {"
               + ",".join(map(str, self.constructors))
               + "}")

    def annotate(self, symbol_decls):
        self.type = None
        self.range = self.constructors #TODO constructor functions

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
        # .type
        # .translated
    
    def __str__(self): return self.name

    def translate(self, case, env):
        return self.translated


class RangeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.elements = kwargs.pop('elements')
        self.symbol_decls = {self.name : self }
        self.is_var = False

        self.range = []
        for x in self.elements:
            if x.toI is None:
                self.range.append(x.fromI)
            else: #TODO test that it is an integer ?
                for i in range(x.fromI.translated, x.toI.translated + 1):
                    self.range.append(NumberConstant(number=str(i)))
        # self.type = None

    def annotate(self, symbol_decls): 
        self.type = None

    def __str__(self):
        return ( "type " + self.name
               + " = {"
               + ";".join([str(x.fromI) + ("" if x.toI is None else ".."+ str(x.toI)) for x in self.elements])
               + "}")

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
        self.symbol_decls = {self.name : self }
        self.is_var = True #TODO unless interpreted
        # .type : a declaration object, or 'Bool', 'real', 'int'
        # .domain: all possible arguments

    def __str__(self):
        return ( self.name
               + ("({})".format(",".join(map(str, self.sorts))) if 0<len(self.sorts) else "")
               + ("" if self.out.name == 'Bool' else " : " + self.out.name)
        )

    def annotate(self, symbol_decls):
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
            self.translated = case.Const(self.name, self.out.asZ3(env), normal=True)
            if len(self.out.getRange(env)) > 1:
                domain = in_list(self.translated, self.out.getRange(env))
                domain.reading = "Possible values for " + self.name
                case.typeConstraints.append(domain)
        elif self.out.name == 'Bool':
            types = [x.asZ3(env) for x in self.sorts]
            rel_vars = [t.getRange(env) for t in self.sorts]
            self.translated = case.Predicate(self.name, types, rel_vars, True)
        else:
            types = [x.asZ3(env) for x in self.sorts] + [self.out.asZ3(env)]
            rel_vars = [t.getRange(env) for t in self.sorts + [self.out]]
            self.translated = case.Function(self.name, types, rel_vars, True)
        env.var_scope[self.name] = self.translated


class Sort(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def __str__(self):
        return self.name

    def asZ3(self, env: Environment):
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
            return universe(self.asZ3(env))


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
        for e in self.definitions: 
            e.annotate(self.symbol_decls, {})
            self.subtences.update(e.subtences())

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

    def annotate(self, symbol_decls, q_vars):
        for r in self.rules: r.annotate(symbol_decls, q_vars)

    def subtences(self):
        out = {}
        for r in self.rules: out.update(r.subtences())
        return out

    def rulePartition(self):
        out = {}
        for i in self.rules:
            out.setdefault(i.symbol.name, []).append(i)
        return out

    def translate(self, case: ConfigCase, env: Environment):
        partition = self.rulePartition()
        for symbol in partition.keys():
            log("symbol " + symbol)
            rules = partition[symbol]
            symbol = Symbol(name=symbol)
            vars = self.makeGlobalVars(symbol, case, env)
            exprs = []

            outputVar = False
            for i in rules:
                exprs.append(i.translate(vars, case, env))
                if i.out is not None:
                    outputVar = True
            if outputVar:
                case.add(ForAll(vars, (applyTo(symbol.translate(case, env), vars[:-1]) == vars[-1]) == Or(exprs)), str(self))
            else:
                if len(vars) > 1:
                    case.add(ForAll(vars, applyTo(symbol.translate(case, env), vars[:-1]) == Or(exprs)), str(self))
                else:
                    case.add(symbol.translate(case, env) == Or(exprs), str(self))

    def makeGlobalVars(self, symb, case, env):
        z3_symb = symb.translate(case, env)
        if type(z3_symb) == FuncDeclRef:
            return [Const('ci'+str(i), z3_symb.domain(i)) for i in range(0, z3_symb.arity())] + [
                Const('cout', z3_symb.range())]
        else:
            return [Const('c', z3_symb.sort())]

class Rule(object):
    def __init__(self, **kwargs):
        self.reading = kwargs.pop('reading')
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.symbol = kwargs.pop('symbol')
        self.args = kwargs.pop('args')
        self.out = kwargs.pop('out')
        self.body = kwargs.pop('body')
        # .translated

    def annotate(self, symbol_decls, q_vars):
        if self.body:
            q_v = q_vars.copy() # shallow copy
            for v, s in zip(self.vars, self.sorts):
                q_v[v] = symbol_decls[s.name]
            self.body.annotate(symbol_decls, q_v)

    def subtences(self):
        return self.body.subtences() if self.body else {}
        
    def translate(self, vars, case: ConfigCase, env: Environment):
        log("translating rule " + str(self.body)[:20])
        args = []
        if self.args is not None:
            args = self.args.sub_exprs

        def function():
            out = []
            for var, expr in zip(vars, args):
                out.append(var == expr.translate(case, env))
            if self.out is not None:
                out.append(vars[-1] == self.out.translate(case, env))
            if self.body is not None:
                out.append(self.body.translate(case, env))
            return out

        #TODO if empty --> type inference
        lvars = self.vars
        sorts = self.sorts

        outp, vars = with_local_vars(case, env, function, sorts, lvars)

        if len(vars) == 0:
            self.translated = And(outp)
        else:
            self.translated = Exists(vars, And(outp))
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
        # self.type

    def __str__(self):
        return "if " + str(self.if_f) + " then " + str(self.then_f) + " else " + str(self.else_f)

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        #TODO verify consistency
        self.type = self.sub_exprs[THEN].type

    def translate(self, case: ConfigCase, env: Environment):
        self.translated =  If(self.sub_exprs[IfExpr.IF  ].translate(case, env)
                            , self.sub_exprs[IfExpr.THEN].translate(case, env)
                            , self.sub_exprs[IfExpr.ELSE].translate(case, env))
        return self.translated

def expand_formula(vars, sorts, f, case, env):
    form, z3vars = with_local_vars(case, env, lambda: f.translate(case, env), sorts, vars)
    forms = [form]
    finalvars = []
    for i in range(0, len(vars)):
        if sorts[i].name in env.range_scope:
            forms2 = []
            for f in forms:
                for v in sorts[i].getRange(env):
                    try:
                        forms2.append(substitute(f, (z3vars[i], _py2expr(float(v)))))
                    except:
                        try:
                            forms2.append(substitute(f, (z3vars[i], _py2expr(int(v)))))
                        except:
                            forms2.append(substitute(f, (z3vars[i], v)))
            forms = forms2
        else:
            finalvars.append(z3vars[i])
    return finalvars, forms


def with_local_vars(case, env, f, sorts, vars):
    backup = {}
    z3vars = []
    assert len(sorts) == len(vars)
    for var, sort in zip(vars, sorts):
        z3var = Const(var, sort.asZ3(env))
        if var in env.var_scope:
            backup[var] = env.var_scope[var]
        else:
            backup[var] = None
        env.var_scope[var] = z3var
        z3vars.append(z3var)

    out = f()
    for var in vars:
        env.var_scope[var] = backup[var]
    return out, z3vars

class AQuantification(Expression):
    def __init__(self, **kwargs):
        self.q = kwargs.pop('q')
        self.q = '∀' if self.q == '!' else '∃' if self.q == "?" else self.q
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.f = kwargs.pop('f')
        self.sub_exprs = [self.f]

    def __str__(self):
        out  = self.q
        out += "".join([str(v) + "[" + str(s) + "]" for v, s in zip(self.vars, self.sorts)])
        out += " : " + str(self.f)
        return out

    def annotate(self, symbol_decls, q_vars):
        q_v = q_vars.copy() # shallow copy
        for v, s in zip(self.vars, self.sorts):
            q_v[v] = symbol_decls[s.name]
        for e in self.sub_exprs: e.annotate(symbol_decls, q_v)
        self.type = 'Bool'

    def subtences(self):
        #TODO optionally add subtences of sub_exprs
        return {str(self): self}

    def translate(self, case: ConfigCase, env: Environment):
        env.level += 1
        finalvars, forms = expand_formula(self.vars, self.sorts, self.sub_exprs[0], case, env)
        env.level -= 1

        if self.q == '∀':
            forms = And(forms) if 1<len(forms) else forms[0]
            if len(finalvars) > 0: # not fully expanded !
                out = ForAll(finalvars, forms)
                if env.level==0: case.mark_atom(self, out)
                self.translated = out
            else:
                if env.level==0: case.mark_atom(self, forms)
                self.translated = forms
        else:
            forms = Or(forms) if 1<len(forms) else forms[0]
            if len(finalvars) > 0: # not fully expanded !
                out = Exists(finalvars, forms)
                if env.level==0: case.mark_atom(self, out)
                self.translated = out
            else:
                if env.level==0: case.mark_atom(self, forms)
                self.translated = forms
        return self.translated

class BinaryOperator(Expression):
    MAP = { '&': lambda x, y: And(x, y),
            '|': lambda x, y: Or(x, y),
            '∧': lambda x, y: And(x, y),
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

    def __str__(self):
        out = str(self.sub_exprs[0])
        for i in range(1, len(self.sub_exprs)):
            out = out + " " + self.operator[i-1] + " " + str(self.sub_exprs[i])
        return out

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        self.type = 'Bool' if self.operator[0] in '&|^∨⇒⇐⇔' \
               else 'Bool' if self.operator[0] in '=<>≤≥≠' \
               else 'real' if any(e.type == 'real' for e in self.sub_exprs) \
               else 'int'

    def subtences(self):
        #TODO collect subtences of aggregates within comparisons
        return {str(self): self} if self.operator[0] in '=<>≤≥≠' \
            else super().subtences()

    def translate(self, case: ConfigCase, env: Environment):
        # chained comparisons -> And()
        if self.operator[0] in ['≠', '~='] and len(self.sub_exprs)==2:
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

    def __str__(self):
        return self.operator + str(self.f)

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
        self.sub_exprs = [self.f, self.out] if self.out else [self.f]

        if self.aggtype == "sum" and self.out is None:
            raise Exception("Must have output variable for sum")
        if self.aggtype != "sum" and self.out is not None:
            raise Exception("Can't have output variable for #")

    def __str__(self):
        out = self.aggtype + "{" + "".join([str(v) + "[" + str(s) + "]" for v, s in zip(self.vars, self.sorts)])
        out += ":" + str(self.f)
        if self.out: out += " : " + str(self.out)
        out += "}"
        return out

    def annotate(self, symbol_decls, q_vars):
        q_v = q_vars.copy() # shallow copy
        for v, s in zip(self.vars, self.sorts):
            q_v[v] = symbol_decls[s.name]
        for e in self.sub_exprs: e.annotate(symbol_decls, q_v)
        self.type = self.sub_exprs[AAggregate.OUT].type if self.out else 'int'

    def translate(self, case: ConfigCase, env: Environment):
        form = IfExpr(if_f=self.sub_exprs[AAggregate.CONDITION]
                    , then_f=NumberConstant(number='1')
                    , else_f=NumberConstant(number='0'))
        if self.sub_exprs[AAggregate.OUT] is not None:
            form = AMultDiv(operator='*', sub_exprs=[form, self.sub_exprs[AAggregate.OUT]])
        fvars, forms = expand_formula(self.vars, self.sorts, form, case, env)
        if len(fvars) > 0:
            raise Exception('Can only quantify over finite domains')
        self.translated = Sum(forms)
        return self.translated


class AppliedSymbol(Expression):
    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')
        self.sub_exprs = self.args.sub_exprs

    def __str__(self):
        return str(self.s) + "(" + ",".join([str(x) for x in self.args.sub_exprs]) + ")"

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        self.type = q_vars.get(self.s.name, symbol_decls[self.s.name].type)

    def subtences(self):
        out = super().subtences() # in case of predicate over boolean
        if self.type == 'Bool': out[str(self)] = self
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

class Variable(Expression):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        if self.name == "true":
            self.type = 'Bool'
            self.translated = bool(True)
        elif self.name == "false":
            self.type = 'Bool'
            self.translated = bool(False)

    def __str__(self): return self.name

    def annotate(self, symbol_decls, q_vars):
        self.type = 'Bool' if self.name in ['true', 'false'] \
            else q_vars[self.name] if self.name in q_vars \
            else symbol_decls[self.name].type

    def subtences(self):
        return {} if self.name in ['true', 'false'] \
            else {str(self): self} if self.type == 'Bool' \
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
        try:
            self.translated = int(self.number)
            self.type = 'int'
        except ValueError:
            self.translated = float(self.number)
            self.type = 'real'

    def __str__(self):
        return str(self.number)

    def annotate(self, symbol_decls, q_vars): pass

    def subtences(): return {}

    def translate(self, case: ConfigCase, env: Environment):
        return self.translated

class Brackets(Expression):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.reading = kwargs.pop('reading')
        self.sub_exprs = [self.f]

    def __str__(self): return "(" + str(self.f) + ")"

    def annotate(self, symbol_decls, q_vars):
        for e in self.sub_exprs: e.annotate(symbol_decls, q_vars)
        self.type = self.sub_exprs[0].type

    def translate(self, case: ConfigCase, env: Environment):
        self.translated = self.sub_exprs[0].translate(case, env)
        if self.reading: 
            self.translated.reading = self.reading
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
        if function and 1 < arity and self.default == None:
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
                    AppliedSymbol, Variable, NumberConstant, Brackets,
          Interpretation, Structure, Tuple,
          Goal, View
        ])
