from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or

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


class AEquivalence(object):
    def __init__(self, **kwargs):
        self.fs = kwargs.pop('fs')
        self.operator = kwargs.pop('operator')

    def translate(self, case: ConfigCase, env: Environment):
        # TODO: N-Ary
        a = self.fs[0].translate(case, env)
        b = self.fs[1].translate(case, env)
        return a == b


class ADisjunction(object):
    def __init__(self, **kwargs):
        self.fs = kwargs.pop('fs')
        self.operator = kwargs.pop('operator')

    def translate(self, case: ConfigCase, env: Environment):
        # TODO: N-Ary
        a = self.fs[0].translate(case, env)
        b = self.fs[1].translate(case, env)
        return Or(a, b)


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
                           classes=[File, Theory, Vocabulary, SymbolDeclaration, Sort, AEquivalence, ADisjunction,
                                    Variable,
                                    Brackets])
