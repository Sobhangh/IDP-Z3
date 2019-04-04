import os

from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or, Not, And, obj_to_string, Const, ForAll, Exists, substitute, Z3Exception
from z3.z3 import _py2expr

from configcase import ConfigCase, singleton, in_list
from utils import is_number, universe


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

    def translate(self, case: ConfigCase, env: Environment):
        for i in self.constraints:
            c = i.translate(case, env)
            case.add(c)


class BinaryOperator(object):
    def __init__(self, **kwargs):
        self.fs = kwargs.pop('fs')
        self.operator = kwargs.pop('operator')
        self.mapping = {'&': lambda x, y: And(x, y),
                        '|': lambda x, y: Or(x, y),
                        '=>': lambda x, y: Or(Not(x), y),
                        '<=': lambda x, y: Or(x, Not(y)),
                        '<=>': lambda x, y: x == y,
                        '+': lambda x, y: x + y,
                        '-': lambda x, y: x - y,
                        '*': lambda x, y: x * y,
                        '=': lambda x, y: x == y,
                        '<': lambda x, y: x < y,
                        '>': lambda x, y: x > y,
                        '=<': lambda x, y: x <= y,
                        '>=': lambda x, y: x >= y,
                        '~=': lambda x, y: x != y
                        }

    def translate(self, case: ConfigCase, env: Environment):
        out = self.fs[0].translate(case, env)
        for i in range(1, len(self.fs)):
            function = self.mapping[self.operator[i - 1]]
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
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.operator = kwargs.pop('operator')
        self.mapping = {'-': lambda x: 0 - x,
                        '~': lambda x: Not(x)
                        }

    def translate(self, case: ConfigCase, env: Environment):
        out = self.f.translate(case, env)
        function = self.mapping[self.operator]
        return function(out)


class AQuantification(object):
    def __init__(self, **kwargs):
        self.q = kwargs.pop('q')
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.f = kwargs.pop('f')

    def translate(self, case: ConfigCase, env: Environment):
        bup = {}
        z3vars = []

        for var, sort in zip(self.vars, self.sorts):
            z3var = Const(var, sort.asZ3(env))
            if var in env.var_scope:
                bup[var] = env.var_scope[var]
            else:
                bup[var] = None
            env.var_scope[var] = z3var
            z3vars.append(z3var)

        form = self.f.translate(case, env)

        for var in self.vars:
            env.var_scope[var] = bup[var]

        forms = [form]
        finalvars = []

        for i in range(0, len(self.vars)):
            if self.sorts[i].name in env.range_scope:
                forms2 = []
                for f in forms:
                    for v in self.sorts[i].getRange(env):
                        try:
                            forms2.append(substitute(f, (z3vars[i], _py2expr(float(v)))))
                        except Z3Exception:
                            forms2.append(substitute(f, (z3vars[i], _py2expr(int(v)))))
                forms = forms2
            else:
                finalvars.append(z3vars[i])

        if self.q == '!':
            if len(finalvars) > 0:
                return ForAll(finalvars, And(forms))
            else:
                return And(forms)
        else:
            if len(finalvars) > 0:
                return Exists(finalvars, Or(forms))
            else:
                return Or(forms)


class AppliedSymbol(object):
    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')

    def translate(self, case: ConfigCase, env: Environment):
        s = self.s.translate(case, env)
        arg = [x.translate(case, env) for x in self.args.fs]
        return s(arg)


class Brackets(object):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')

    def translate(self, case: ConfigCase, env: Environment):
        return self.f.translate(case, env)


class Variable(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def translate(self, case: ConfigCase, env: Environment):
        return env.var_scope[self.name]


class Symbol(Variable): pass


class NumberConstant(object):
    def __init__(self, **kwargs):
        self.number = kwargs.pop('number')

    def translate(self, case: ConfigCase, env: Environment):
        try:
            return int(self.number)
        except ValueError:
            return float(self.number)


class Vocabulary(object):
    def __init__(self, **kwargs):
        self.declarations = kwargs.pop('declarations')

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

    def translate(self, case: ConfigCase, env: Environment):
        type, cstrs = case.EnumSort(self.name, self.constructors)
        env.type_scope[self.name] = type
        for i in cstrs:
            env.var_scope[obj_to_string(i)] = i


class RangeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.elements = kwargs.pop('elements')

    def translate(self, case: ConfigCase, env: Environment):
        els = []
        for x in self.elements:
            if x.to is None:
                els.append(x.fromI.translate(case, env))
            else:
                for i in range(x.fromI.translate(case, env), x.to.translate(case, env)):
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

    def asZ3(self, env: Environment):
        if self.name in env.type_scope:
            return env.type_scope[self.name]
        else:
            raise Exception("Unknown sort: " + self.name)

    def getRange(self, env: Environment):
        if self.name in env.range_scope:
            return env.range_scope[self.name]
        else:
            return universe(self.asZ3(env))

    def getZ3Range(self, env: Environment):
        return list(map(singleton, map(_py2expr, self.getRange(env))))


dslFile = os.path.join(os.path.dirname(__file__), 'DSL.tx')

idpparser = metamodel_from_file(dslFile, memoization=True,
                                classes=[File, Theory, Vocabulary, SymbolDeclaration, Sort,
                                         AConjunction, ADisjunction, AImplication, ARImplication, AEquivalence,
                                         AComparison,
                                         ASumMinus, AMultDiv, AUnary, NumberConstant, ConstructedTypeDeclaration,
                                         RangeDeclaration, AppliedSymbol,
                                         Variable, Symbol, AQuantification,
                                         Brackets])
