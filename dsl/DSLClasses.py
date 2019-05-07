import os

from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or, Not, And, obj_to_string, Const, ForAll, Exists, substitute, Z3Exception, \
    Sum, If, FuncDeclRef, Function, Var, Int
from z3.z3 import _py2expr

from configcase import ConfigCase, singleton, in_list
from utils import is_number, universe, applyTo, rewrite


class Environment:
    def __init__(self):
        self.var_scope = {'True': True, 'False': False}
        self.type_scope = {'Int': IntSort(), 'Bool': BoolSort(), 'Real': RealSort()}
        self.range_scope = {}
        self.symbol_type = {}
        self.level_scope = {}


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
        self.wellFounded = kwargs.pop('wellFounded')

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

            z3symbol = symbol.translate(case, env)

            vars = self.makeGlobalVars(symbol, case, env)
            types = env.symbol_type[symbol.name]
            exprs = []

            outputVar = False
            for i in rules:
                exprs.append(i.translate(vars, case, env))
                if i.out is not None:
                    outputVar = True
            if outputVar:
                case.add(conjunctive(
                    *expand_z3formula(vars, types, (applyTo(z3symbol, vars[:-1]) == vars[-1]) == Or(exprs), case, env)))
            else:
                vars = vars[:-1]
                # boolean output
                case.add(conjunctive(
                    *expand_z3formula(vars, types[:-1], applyTo(z3symbol, vars) == Or(exprs), case, env)))

                if self.wellFounded:
                    lvlSymb = self.makeLevelSymbol(z3symbol)
                    lvlVars = [Var(i, lvlSymb.domain(i)) for i in range(0, len(vars))]

                    comparison = And(applyTo(lvlSymb, lvlVars) < applyTo(lvlSymb, vars), applyTo(z3symbol, lvlVars))
                    if len(vars) == 0:
                        newExpr = substitute(Or(exprs), (z3symbol, comparison))
                    else:
                        newExpr = rewrite(Or(exprs), z3symbol, comparison)

                    case.add(
                        conjunctive(*expand_z3formula(vars, types[:-1], applyTo(z3symbol, vars) == newExpr, case, env)))

    def makeLevelSymbol(self, symbol):
        if not hasattr(symbol, 'arity'):
            return Int("lvl")
        type_list = [symbol.domain(i) for i in range(0, symbol.arity())] + [IntSort()]
        return Function("lvl", type_list)

    def makeGlobalVars(self, symb, case, env):
        z3_symb = symb.translate(case, env)
        if type(z3_symb) == FuncDeclRef:
            return [Const('ci' + str(i), z3_symb.domain(i)) for i in range(0, z3_symb.arity())] + [
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
        self.graphArgs = []
        if self.args is not None:
            self.graphArgs = self.args.fs
        if self.out is not None:
            self.graphArgs.append(self.out)

    def translate(self, vars, case: ConfigCase, env: Environment):
        lvars = []
        if lvars is not None:
            lvars = self.vars
        sorts = []
        if sorts is not None:
            sorts = self.sorts

        def function():
            out = []
            for var, expr in zip(vars, self.graphArgs):
                out.append(var == expr.translate(case, env))
            if self.body is not None:
                out.append(self.body.translate(case, env))
            return And(out)

        outp, z3vars = with_local_vars(case, env, function, sorts, lvars)

        return disjunctive(*expand_z3formula(z3vars, sorts, outp, case, env))


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
        if self.q == '!':
            return conjunctive(*expand_formula(self.vars, self.sorts, self.f, case, env))
        else:
            out = disjunctive(*expand_formula(self.vars, self.sorts, self.f, case, env))
            return out


def conjunctive(finalvars, forms):
    if len(finalvars) > 0:
        return ForAll(finalvars, And(forms))
    else:
        return And(forms)


def disjunctive(finalvars, forms):
    if len(finalvars) > 0:
        return Exists(finalvars, And(forms))
    else:
        return Or(forms)


def expand_formula(vars, sorts, f, case, env):
    form, z3vars = with_local_vars(case, env, lambda: f.translate(case, env), sorts, vars)
    return expand_z3formula(z3vars, sorts, form, case, env)


def expand_z3formula(z3vars, sorts, form, case, env):
    forms = [form]
    finalvars = []
    for i in range(0, len(z3vars)):
        if sorts[i].name in env.range_scope:
            forms2 = []
            for f in forms:
                for v in sorts[i].getRange(env):
                    try:
                        forms2.append(substitute(f, (z3vars[i], _py2expr(float(v)))))
                    except Z3Exception:
                        try:
                            forms2.append(substitute(f, (z3vars[i], _py2expr(int(v)))))
                        except Z3Exception:
                            forms2.append(substitute(f, (z3vars[i], _py2expr(bool(v)))))

            forms = forms2
        else:
            finalvars.append(z3vars[i])
    return finalvars, forms


def with_local_vars(case, env, f, sorts, vars):
    bup = {}
    z3vars = []
    assert len(sorts) == len(vars)
    for var, sort in zip(vars, sorts):
        z3var = Const(var, sort.asZ3(env))
        if var in env.var_scope:
            bup[var] = env.var_scope[var]
        else:
            bup[var] = None
        env.var_scope[var] = z3var
        z3vars.append(z3var)

    out = f()
    for var in vars:
        env.var_scope[var] = bup[var]
    return out, z3vars


class AAggregate(object):
    def __init__(self, **kwargs):
        self.aggtype = kwargs.pop('aggtype')
        self.set = kwargs.pop('set')
        if self.aggtype == "sum" and self.set.out is None:
            raise Exception("Must have output variable for sum")
        if self.aggtype != "sum" and self.set.out is not None:
            raise Exception("Can't have output variable for #")

    def translate(self, case: ConfigCase, env: Environment):
        return Sum(self.set.translate(case, env))


class IfExpr(object):
    def __init__(self, **kwargs):
        self.if_f = kwargs.pop('if_f')
        self.then_f = kwargs.pop('then_f')
        self.else_f = kwargs.pop('else_f')

    def translate(self, case: ConfigCase, env: Environment):
        return If(self.if_f.translate(case, env), self.then_f.translate(case, env), self.else_f.translate(case, env))


class SetExp(object):
    def __init__(self, **kwargs):
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.f = kwargs.pop('f')
        self.out = kwargs.pop('out')

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

    def translate(self, case: ConfigCase, env: Environment):
        env.symbol_type[self.name.name] = [x for x in self.args] + [self.out]
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
                                         AComparison, AAggregate, SetExp,
                                         ASumMinus, AMultDiv, AUnary, NumberConstant, ConstructedTypeDeclaration,
                                         RangeDeclaration, AppliedSymbol, Definition, Rule,
                                         Variable, Symbol, AQuantification,
                                         Brackets])
