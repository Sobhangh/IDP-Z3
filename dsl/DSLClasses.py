import os

from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or, Not, And, obj_to_string, Const, ForAll, Exists, substitute, Z3Exception, \
    Sum, If, FuncDeclRef
from z3.z3 import _py2expr

from configcase import ConfigCase, singleton, in_list
from utils import is_number, universe, applyTo


class Environment:
    def __init__(self):
        self.var_scope = {'True': True, 'False': False}
        self.type_scope = {'Int': IntSort(), 'Bool': BoolSort(), 'Real': RealSort()}
        self.range_scope = {}


class File(object):
    def __init__(self, **kwargs):
        self.theory = kwargs.pop('theory')
        self.vocabulary = kwargs.pop('vocabulary')

    def translate(self, case: ConfigCase):
        env = Environment()
        self.vocabulary.translate(case, env)
        self.theory.translate(case, env)


class Theory(object):
    def __init__(self, **kwargs):
        self.constraints = kwargs.pop('constraints')
        self.definitions = kwargs.pop('definitions')

    def translate(self, case: ConfigCase, env: Environment):
        for i in self.constraints:
            c = i.translate(case, env)
            case.add(c)
        for d in self.definitions:
            d.translate(case, env)


class Definition(object):
    def __init__(self, **kwargs):
        self.rules = kwargs.pop('rules')

    def rulePartition(self):
        out = {}
        for i in self.rules:
            out.setdefault(i.symbol.name, []).append(i)
        return out

    def translate(self, case: ConfigCase, env: Environment):
        partition = self.rulePartition()
        for symbol in partition.keys():
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
                case.add(ForAll(vars, (applyTo(symbol.translate(case, env), vars[:-1]) == vars[-1]) == Or(exprs)))
            else:
                if len(vars) > 1:
                    case.add(ForAll(vars, applyTo(symbol.translate(case, env), vars[:-1]) == Or(exprs)))
                else:
                    case.add(symbol.translate(case, env) == Or(exprs))

    def makeGlobalVars(self, symb, case, env):
        z3_symb = symb.translate(case, env)
        if type(z3_symb) == FuncDeclRef:
            return [Const('ci', z3_symb.domain(i)) for i in range(0, z3_symb.arity())] + [
                Const('cout', z3_symb.range())]
        else:
            return [Const('c', z3_symb.sort())]


class Rule(object):
    def __init__(self, **kwargs):
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.symbol = kwargs.pop('symbol')
        self.args = kwargs.pop('args')
        self.out = kwargs.pop('out')
        self.body = kwargs.pop('body')

    def translate(self, vars, case: ConfigCase, env: Environment):
        args = []
        if self.args is not None:
            args = self.args.fs

        def function():
            out = []
            for var, expr in zip(vars, args):
                out.append(var == expr.translate(case, env))
            if self.out is not None:
                out.append(vars[-1] == self.out.translate(case, env))
            if self.body is not None:
                out.append(self.body.translate(case, env))
            return out

        lvars = []
        if lvars is not None:
            lvars = self.vars
        sorts = []
        if sorts is not None:
            sorts = self.sorts

        outp, vars = with_local_vars(case, env, function, sorts, lvars)

        if len(vars) == 0:
            return And(outp)
        else:
            return Exists(vars, And(outp))


class BinaryOperator(object):
    MAP = {  '&': lambda x, y: And(x, y),
            '|': lambda x, y: Or(x, y),
            '=>': lambda x, y: Or(Not(x), y),
            '<=': lambda x, y: Or(x, Not(y)),
            '<=>': lambda x, y: x == y,
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '=': lambda x, y: x == y,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '=<': lambda x, y: x <= y,
            '>=': lambda x, y: x >= y,
            '~=': lambda x, y: x != y,
            '≤': lambda x, y: x <= y,
            '≥': lambda x, y: x >= y,
            '≠': lambda x, y: x != y
            }

    def __init__(self, **kwargs):
        self.fs = kwargs.pop('fs')
        self.operator = kwargs.pop('operator')

    def __str__(self):
        out = str(self.fs[0])
        for i in range(1, len(self.fs)):
            op = self.operator[i-1]
            op = "≤" if op == "=<" else "≥" if op == ">=" else "≠" if op == "~=" else op
            out = out + " " + op + " " + str(self.fs[i])
        return out

    def translate(self, case: ConfigCase, env: Environment):
        # chained comparisons -> And()
        if self.operator[0] in ['=', '<', '>', '=<', '>=', '~=', "≤", "≥", "≠"]:
            out = []
            for i in range(1, len(self.fs)):
                x = self.fs[i-1].translate(case, env)
                function = BinaryOperator.MAP[self.operator[i - 1]]
                y = self.fs[i].translate(case, env)
                out = out + [function(x, y)]
            if 1 < len(out):
                out = And(out)
                out.is_chained = True
            else:
                out = out[0]
            case.Atom(str(self), out)
        else:
            out = self.fs[0].translate(case, env)

            for i in range(1, len(self.fs)):
                function = BinaryOperator.MAP[self.operator[i - 1]]
                out = function(out, self.fs[i].translate(case, env))
        return out


class AConjunction(BinaryOperator): pass


class ADisjunction(BinaryOperator): pass


class AImplication(BinaryOperator): pass


class ARImplication(BinaryOperator): pass


class AEquivalence(BinaryOperator): pass


class AComparison(BinaryOperator): pass


class ASumMinus(BinaryOperator): pass


class AMultDiv(BinaryOperator): pass

class AUnary(object):
    MAP = {'-': lambda x: 0 - x,
           '~': lambda x: Not(x)
          }
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.operator = kwargs.pop('operator')

    def __str__(self):
        return self.operator + str(self.f)

    def translate(self, case: ConfigCase, env: Environment):
        out = self.f.translate(case, env)
        function = AUnary.MAP[self.operator]
        return function(out)


class AQuantification(object):
    def __init__(self, **kwargs):
        self.q = kwargs.pop('q')
        self.q = '∀' if self.q == '!' else '∃' if self.q == "?" else self.q
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.f = kwargs.pop('f')

    def __str__(self):
        out  = self.q
        out += "".join([str(v) + "[" + str(s) + "]" for v, s in zip(self.vars, self.sorts)])
        out += " : " + str(self.f)
        return out

    def translate(self, case: ConfigCase, env: Environment):
        finalvars, forms = expand_formula(self.vars, self.sorts, self.f, case, env)

        if self.q == '∀':
            forms = And(forms) if 1<len(forms) else forms[0]
            if len(finalvars) > 0: # not fully expanded !
                out = ForAll(finalvars, forms)
                case.Atom(str(self), out)
                return out
            else:
                case.Atom(str(self), forms)
                return forms
        else:
            forms = Or(forms) if 1<len(forms) else forms[0]
            if len(finalvars) > 0: # not fully expanded !
                out = Exists(finalvars, forms)
                case.Atom(str(self), out)
                return out
            else:
                case.Atom(str(self), forms)
                return forms


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


class AAggregate(object):
    def __init__(self, **kwargs):
        self.aggtype = kwargs.pop('aggtype')
        self.set = kwargs.pop('set')
        if self.aggtype == "sum" and self.set.out is None:
            raise Exception("Must have output variable for sum")
        if self.aggtype != "sum" and self.set.out is not None:
            raise Exception("Can't have output variable for #")

    def __str__(self):
        return self.aggtype + str(self.set)

    def translate(self, case: ConfigCase, env: Environment):
        return Sum(self.set.translate(case, env))


class IfExpr(object):
    def __init__(self, **kwargs):
        self.if_f = kwargs.pop('if_f')
        self.then_f = kwargs.pop('then_f')
        self.else_f = kwargs.pop('else_f')

    def __str__(self):
        return "if " + str(self.if_f) + " then " + str(self.then_f) + " else " + str(self.else_f)

    def translate(self, case: ConfigCase, env: Environment):
        return If(self.if_f.translate(case, env), self.then_f.translate(case, env), self.else_f.translate(case, env))


class SetExp(object):
    def __init__(self, **kwargs):
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.f = kwargs.pop('f')
        self.out = kwargs.pop('out')

    def __str__(self):
        out = "{" + "".join([str(v) + "[" + str(s) + "]" for v, s in zip(self.vars, self.sorts)])
        out += ":" + str(self.f)
        if self.out: out += " : " + str(self.out)
        out += "}"
        return out

    def translate(self, case: ConfigCase, env: Environment):
        form = IfExpr(if_f=self.f, then_f=NumberConstant(number='1'), else_f=NumberConstant(number='0'))
        if self.out is not None:
            form = AMultDiv(operator='*', fs=[form, self.out])
        fvars, forms = expand_formula(self.vars, self.sorts, form, case, env)
        if len(fvars) > 0:
            raise Exception('Can only quantify over finite domains')
        return forms


class AppliedSymbol(object):
    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')

    def __str__(self):
        return str(self.s) + "(" + ",".join([str(x) for x in self.args.fs]) + ")"

    def translate(self, case: ConfigCase, env: Environment):
        s = self.s.translate(case, env)
        arg = [x.translate(case, env) for x in self.args.fs]
        out = s(arg)
        case.Atom(str(self), out)
        return out


class Brackets(object):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')

    def __str__(self): return "(" + str(self.f) + ")"

    def translate(self, case: ConfigCase, env: Environment):
        return self.f.translate(case, env)


class Variable(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def __str__(self): return self.name

    def translate(self, case: ConfigCase, env: Environment):
        if self.name == "true":
            return bool(True)
        if self.name == "false":
            return bool(False)
        out = env.var_scope[self.name]
        case.Atom(self.name, out)
        return out


class Symbol(Variable): pass


class NumberConstant(object):
    def __init__(self, **kwargs):
        self.number = kwargs.pop('number')

    def __str__(self):
        return str(self.number)

    def translate(self, case: ConfigCase, env: Environment):
        try:
            return int(self.number)
        except ValueError:
            return float(self.number)


class Vocabulary(object):
    def __init__(self, **kwargs):
        self.declarations = kwargs.pop('declarations')

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

    def __str__(self):
        return ( "type " + self.name
               + " constructed from {"
               + ",".join(map(str, self.constructors))
               + "}")

    def translate(self, case: ConfigCase, env: Environment):
        type, cstrs = case.EnumSort(self.name, self.constructors)
        env.type_scope[self.name] = type
        for i in cstrs:
            env.var_scope[obj_to_string(i)] = i
        env.range_scope[self.name] = cstrs


class RangeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.elements = kwargs.pop('elements')

    def __str__(self):
        return ( "type " + self.name
               + " = {"
               + ",".join([str(x.fromI) + ("" if x.to is None else ".."+ str(x.to)) for x in self.elements])
               + "}")

    def translate(self, case: ConfigCase, env: Environment):
        els = []
        for x in self.elements:
            if x.to is None:
                els.append(x.fromI.translate(case, env))
            else:
                for i in range(x.fromI.translate(case, env), x.to.translate(case, env) + 1):
                    els.append(i)
        if all(map(lambda x: type(x) == int, els)):
            env.type_scope[self.name] = IntSort()
        else:
            env.type_scope[self.name] = RealSort()
        env.range_scope[self.name] = els


class SymbolDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.args = kwargs.pop('args')
        self.out = kwargs.pop('out')
        if self.out is None:
            self.out = Sort(name='Bool')

    def __str__(self):
        return ( self.name.name
               + ("({})".format(",".join(map(str, self.args))) if 0<len(self.args) else "")
               + ("" if self.out.name == 'Bool' else " : " + self.out.name)
        )

    def translate(self, case: ConfigCase, env: Environment):
        if len(self.args) == 0:
            const = case.Const(self.name.name, self.out.asZ3(env))
            env.var_scope[self.name.name] = const
            case.relevantVals[const] = self.out.getZ3Range(env)
            if len(self.out.getRange(env)) > 1:
                case.typeConstraints.append(in_list(const, self.out.getRange(env)))
        elif self.out.name == 'Bool':
            types = [x.asZ3(env) for x in self.args]
            rel_vars = [t.getRange(env) for t in self.args]
            env.var_scope[self.name.name] = case.Predicate(self.name.name, types, rel_vars, True)
        else:
            types = [x.asZ3(env) for x in self.args] + [self.out.asZ3(env)]
            rel_vars = [t.getRange(env) for t in self.args + [self.out]]
            env.var_scope[self.name.name] = case.Function(self.name.name, types, rel_vars, True)


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

    def getZ3Range(self, env: Environment):
        return list(map(singleton, map(_py2expr, self.getRange(env))))


dslFile = os.path.join(os.path.dirname(__file__), 'DSL.tx')

idpparser = metamodel_from_file(dslFile, memoization=True,
                                classes=[File, Theory, Vocabulary, SymbolDeclaration, Sort,
                                         AConjunction, ADisjunction, AImplication, ARImplication, AEquivalence,
                                         AComparison, AAggregate, SetExp,
                                         ASumMinus, AMultDiv, AUnary, NumberConstant, ConstructedTypeDeclaration,
                                         RangeDeclaration, AppliedSymbol, Definition, Rule,
                                         Variable, Symbol, AQuantification,
                                         Brackets])
