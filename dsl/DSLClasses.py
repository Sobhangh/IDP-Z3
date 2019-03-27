from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or, Not, And, obj_to_string

from configcase import ConfigCase


class Environment:
    def __init__(self):
        self.var_scope = {}
        self.type_scope = {'Int': IntSort(), 'Bool': BoolSort(), 'Real': RealSort()}


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
        self.numb = kwargs.pop('numb')

    def translate(self, case: ConfigCase, env: Environment):
        return self.numb


class Vocabulary(object):
    def __init__(self, **kwargs):
        self.declarations = kwargs.pop('declarations')

    def translate(self, case: ConfigCase, env: Environment):
        for i in self.declarations:
            if type(i) == TypeDeclaration:
                i.translate(case, env)
        for i in self.declarations:
            if type(i) == SymbolDeclaration:
                i.translate(case, env)


class TypeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.constructors = kwargs.pop('constructors')

    def translate(self, case: ConfigCase, env: Environment):
        type, cstrs = case.EnumSort(self.name, self.constructors)
        env.type_scope[self.name] = type
        for i in cstrs:
            env.var_scope[obj_to_string(i)] = i


class SymbolDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.args = kwargs.pop('args')
        self.out = kwargs.pop('out')
        if self.out is None:
            self.out = Sort(name='Bool')

    def translate(self, case: ConfigCase, env: Environment):
        if len(self.args) == 0:
            env.var_scope[self.name.name] = case.Const(self.name.name, self.out.asZ3(env))
        else:
            types = [x.asZ3(env) for x in self.args] + [self.out.asZ3(env)]
            # TODO This should change
            rel_vars = [[]] * len(types)
            env.var_scope[self.name.name] = case.Function(self.name.name, types, rel_vars)


class Sort(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def asZ3(self, env: Environment):
        return env.type_scope[self.name]


meta = metamodel_from_file('DSL.tx', memoization=True,
                           classes=[File, Theory, Vocabulary, SymbolDeclaration, Sort,
                                    AConjunction, ADisjunction, AImplication, ARImplication, AEquivalence, AComparison,
                                    ASumMinus, AMultDiv, AUnary, NumberConstant, TypeDeclaration, AppliedSymbol,
                                    Variable, Symbol,
                                    Brackets])
