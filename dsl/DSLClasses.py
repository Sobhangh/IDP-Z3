from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or, Not, And

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
                        '/': lambda x, y: x / y,
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


class Brackets(object):
    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')

    def translate(self, case: ConfigCase, env: Environment):
        return self.f.translate(case, env)


class Variable(object):
    def __init__(self, **kwargs):
        self.var = kwargs.pop('var')

    def translate(self, case: ConfigCase, env: Environment):
        return env.var_scope[self.var]


class Vocabulary(object):
    def __init__(self, **kwargs):
        self.declarations = kwargs.pop('declarations')

    def translate(self, case: ConfigCase, env: Environment):
        for i in self.declarations:
            i.translate(case, env)


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
            raise Exception("Not Implemented Yet")


class Sort(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def asZ3(self, env: Environment):
        return env.type_scope[self.name]


meta = metamodel_from_file('DSL.tx', memoization=True,
                           classes=[File, Theory, Vocabulary, SymbolDeclaration, Sort,
                                    AConjunction, ADisjunction, AImplication, ARImplication, AEquivalence, AComparison,
                                    ASumMinus, AMultDiv, AUnary,
                                    Variable,
                                    Brackets])
