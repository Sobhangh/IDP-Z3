"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""

import itertools as it
import os
import re
import sys

from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or, Not, And, Const, ForAll, Exists, Z3Exception, \
    Sum, If, BoolVal, Function, FreshConst, Implies, EnumSort

from utils import applyTo, log, itertools, in_list, nl, mergeDicts
from Idp.Expression import Constructor, Expression, IfExpr, AQuantification, operation, \
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  \
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate, \
                    AppliedSymbol, Variable, Symbol, NumberConstant, Brackets, Arguments, \
                    Fresh_Variable, TRUE, FALSE


class Idp(object):
    def __init__(self, **kwargs):
        log("parsing done")
        self.vocabulary = kwargs.pop('vocabulary')
        self.decision = kwargs.pop('decision')
        self.theory = kwargs.pop('theory')
        self.interpretations = kwargs.pop('interpretations')

        self.goal = kwargs.pop('goal')
        if self.goal is None:
            self.goal = Goal(name="")
        self.view = kwargs.pop('view')
        if self.view is None:
            self.view = View(viewType='normal')
        
        self.translated = None # [Z3Expr]

        if self.decision is not None:
            for decl in self.vocabulary.symbol_decls.values():
                decl.environmental = True
            self.vocabulary.update(self.decision)

        if self.interpretations: self.interpretations.annotate(self.vocabulary)
        self.theory.annotate(self.vocabulary)
        self.goal.annotate(self.vocabulary)
        log("annotated")

        """
        for c in self.theory.constraints:
            print(repr(c))
        for c in self.theory.definitions:
            print(repr(c))
        """
        # translate

        self.vocabulary.translate(self)
        log("vocabulary translated")
        self.theory.translate(self)
        log("theory translated")
        #self.goal.translate()
        self.view.translate()

        self.translated = self.vocabulary.translated + self.theory.translated

    def unknown_symbols(self):
        todo = self.theory.unknown_symbols()

        out = {} # reorder per vocabulary order
        for symb in self.vocabulary.symbol_decls:
            if symb in todo:
                out[symb] = todo[symb]
        return out


################################ Vocabulary  ###############################


class Vocabulary(object):
    def __init__(self, **kwargs):
        self.declarations = kwargs.pop('declarations')
        self.terms = {} # {string: Variable or AppliedSymbol} not starting with '_'
        self.translated = []

        self.symbol_decls = {'int' : RangeDeclaration(name='int', elements=[]),
                             'real': RangeDeclaration(name='real', elements=[]),
                             'bool': ConstructedTypeDeclaration(name='bool', 
                                        constructors=[TRUE, FALSE]),
                             'true' : TRUE,
                             'false': FALSE}
        for s in self.declarations: 
            s.annotate(self.symbol_decls)

    def __str__(self):
        return ( f"vocabulary {{{nl}"
                 f"{nl.join(str(i) for i in self.declarations)}"
                 f"{nl}}}{nl}"
               )

    def update(self, other):
        self.declarations.extend(other.declarations)
        self.terms       .update(other.terms)
        self.symbol_decls.update(other.symbol_decls)

    def translate(self, idp):
        for i in self.declarations:
            if type(i) in [ConstructedTypeDeclaration, RangeDeclaration]:
                i.translate()
        for i in self.declarations:
            if type(i) == SymbolDeclaration:
                i.translate(idp)

        for v in self.symbol_decls.values():
            if v.is_var:
                self.terms.update(v.instances)

class Decision(Vocabulary):
    pass

class ConstructedTypeDeclaration(object):
    COUNT = -1
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.constructors = kwargs.pop('constructors')
        self.is_var = False
        self.range = self.constructors # functional constructors are expanded
        self.translated = None

        if self.name == 'bool':
            self.translated = BoolSort()
            self.constructors[0].type = 'bool'
            self.constructors[1].type = 'bool'
            self.constructors[0].translated = bool(True) 
            self.constructors[1].translated = bool(False)
        else:
            self.translated, cstrs = EnumSort(self.name, [c.name for c in self.constructors])
            for c, c3 in zip(self.constructors, cstrs):
                c.translated = c3
                c.index = ConstructedTypeDeclaration.COUNT
                ConstructedTypeDeclaration.COUNT -= 1

        self.type = None

    def __str__(self):
        return ( f"type {self.name} constructed from "
                 f"{{{','.join(map(str, self.constructors))}}}"
               )

    def annotate(self, symbol_decls):
        assert self.name not in symbol_decls, "duplicate declaration in vocabulary: " + self.name
        symbol_decls[self.name] = self
        for c in self.constructors:
            c.type = self
            symbol_decls[c.name] = c
        self.range = self.constructors #TODO constructor functions

    def check_bounds(self, var):
        return None

    def translate(self):
        return self.translated


class RangeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name') # maybe 'int', 'real'
        self.elements = kwargs.pop('elements')
        self.is_var = False
        self.translated = None

        self.range = []
        for x in self.elements:
            if x.toI is None:
                self.range.append(x.fromI)
            else: #TODO test that it is an integer ?
                for i in range(x.fromI.translated, x.toI.translated + 1):
                    self.range.append(NumberConstant(number=str(i)))

        if self.name == 'int':
            self.translated = IntSort() 
        elif self.name == 'real':
            self.translated = RealSort() 
        self.type = None

    def __str__(self):
        elements = ";".join([str(x.fromI) + ("" if x.toI is None else ".."+ str(x.toI)) for x in self.elements])
        return f"type {self.name} = {{{elements}}}"

    def annotate(self, symbol_decls):
        assert self.name not in symbol_decls, "duplicate declaration in vocabulary: " + self.name
        symbol_decls[self.name] = self

    def check_bounds(self, var):
        if not self.elements: return None
        sub_exprs = []
        for x in self.elements:
            if x.toI is None:
                e = operation('=', [x.fromI, var])
            else:
                e = operation(['≤', '≤'], [x.fromI, var, x.toI])
            sub_exprs.append(e)
        return operation('∨', sub_exprs)

    def translate(self):
        if self.translated is None:
            els = [e.translated for e in self.range]
            if all(map(lambda x: type(x) == int, els)):
                self.translated = IntSort()
            else:
                self.translated = RealSort()
        return self.translated


class SymbolDeclaration(object):
    def __init__(self, **kwargs):
        self.name = sys.intern(kwargs.pop('name').name) # a string, not a Symbol
        self.sorts = kwargs.pop('sorts')
        self.out = kwargs.pop('out')
        if self.out is None:
            self.out = Sort(name='bool')

        self.is_var = True # unless interpreted later
        self.typeConstraints = []
        self.translated = None

        self.type = None # a declaration object
        self.domain = None # all possible arguments
        self.instances = None # {string: Variable or AppliedSymbol} not starting with '_'
        self.range = None # all possible values
        self.interpretation = None # f:tuple -> Expression (only if it is given in a structure)
        self.environmental = False # true if in declared (environmental) vocabulary and there is a decision vocabulary

    def __str__(self):
        args = ','.join(map(str, self.sorts)) if 0<len(self.sorts) else ''
        return ( f"{self.name}"
                 f"{ '('+args+')' if args else ''}"
                 f"{'' if self.out.name == 'bool' else f' : {self.out.name}'}"
        )

    def annotate(self, symbol_decls, vocabulary=True):
        if vocabulary: 
            assert self.name not in symbol_decls, "duplicate declaration in vocabulary: " + self.name
            symbol_decls[self.name] = self
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
                self.instances[expr.code] = expr
            else:
                for arg in list(self.domain):
                    expr = AppliedSymbol(s=Symbol(name=self.name), args=Arguments(sub_exprs=arg))
                    expr.annotate(symbol_decls, {})
                    expr.normal = True
                    self.instances[expr.code] = expr
        
        if self.out.decl.name != 'bool' and self.range:
            for inst in self.instances.values():
                domain = self.out.decl.check_bounds(inst)
                if domain is not None:
                    domain.if_symbol = self.name
                    domain.reading = "Possible values for " + str(inst)
                    self.typeConstraints.append(domain)
        return self

    def check_bounds(self, vars):
        out = []
        for var in vars:
            check = var.decl.check_bounds(var)
            if check is not None:
                out.append(check)
        """ TODO
        if self.out.decl.name != 'bool' and self.range:
            applied = AppliedSymbol(s=Symbol(name=self.name), args=Arguments(sub_exprs=vars))
            applied.decl = self
            applied.type = applied.decl.type.name
            domain = self.out.decl.check_bounds(applied)
            if domain is not None:
                domain.reading = "Possible values for " + str(vars)
                out.append(domain)
        """
        return out

    def translate(self, idp):
        if self.translated is None:
            if len(self.sorts) == 0:
                self.translated = Const(self.name, self.out.translate())
                self.normal = True
            else:
                argL = list(map( lambda t: Fresh_Variable(str(t[0]), t[1].decl)
                               , enumerate(self.sorts)))

                if self.out.name == 'bool':
                    types = [x.translate() for x in self.sorts]
                    rel_vars = [t.getRange() for t in self.sorts]
                    self.translated = Function(self.name, types + [BoolSort()])

                    checks = self.check_bounds(argL)
                    checks = list(c.translate() for c in checks)
                    argL = list(c.translate() for c in argL)
                    if checks:
                        idp.vocabulary.translated.append(
                            ForAll(argL, Implies( (self.translated)(*argL), And(checks))))
                else:
                    types = [x.translate() for x in self.sorts] + [self.out.translate()]
                    self.translated = Function(self.name, types)

                    var = Fresh_Variable(str(len(self.sorts)), self.out.decl)
                    check = self.out.decl.check_bounds(var)
                    varZ3 = var.translate()
                    """
                    if check is not None: # Z3 cannot solve the constraint if infinite range, issue #2
                        checks.append(check.translate())
                        idp.vocabulary.translated.append(
                            ForAll(argL + [varZ3], Implies( (self.translated)(*argL) == varZ3, And(checks))))
                    """
        return self.translated


class Sort(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.code = sys.intern(self.name)
        self.decl = None

    def __str__(self): return self.code

    def annotate(self, symbol_decls):
        self.decl = symbol_decls[self.name]

    def translate(self):
        return self.decl.translated

    def getRange(self):
        return [e.translated for e in self.decl.range]


################################ Theory ###############################


class Theory(object):
    def __init__(self, **kwargs):
        self.constraints = kwargs.pop('constraints')
        self.definitions = kwargs.pop('definitions')
        self.symbol_decls = None # {string: decl}
        self.subtences = None # i.e., sub-sentences.  {string: Expression}
        self.translated = None

    def annotate(self, vocabulary):
        self.symbol_decls = vocabulary.symbol_decls

        self.subtences = {}
        self.constraints = [e.annotate(self.symbol_decls, {}) for e in self.constraints]
        #TODO check argument ranges
        self.constraints = [e.expand_quantifiers(self) for e in self.constraints]
        self.constraints = [e.interpret         (self) for e in self.constraints]
        for e in self.constraints:
            self.subtences.update({k: v for k, v in e.subtences().items() if v.unknown_symbols()})

        for decl in self.symbol_decls.values():
            if type(decl) == SymbolDeclaration:
                self.constraints.extend(decl.typeConstraints)

        self.definitions = [e.annotate(self.symbol_decls, {}) for e in self.definitions]
        self.definitions = [e.expand_quantifiers(self) for e in self.definitions]
        self.definitions = [e.interpret         (self) for e in self.definitions]
        for e in self.definitions:
            self.subtences.update({k: v for k, v in e.subtences().items() if v.unknown_symbols()})

    def unknown_symbols(self):
        return mergeDicts(c.unknown_symbols() 
            for c in self.constraints + self.definitions)

    def translate(self, idp):
        self.translated = []
        for i in self.constraints:
            log("translating " + str(i)[:20])
            self.translated.append(i.translate())
        for d in self.definitions:
            self.translated += d.translate(idp)



class Definition(object):
    def __init__(self, **kwargs):
        self.rules = kwargs.pop('rules')
        self.partition = None # {Symbol: [Transformed Rule]}
        self.q_decls = {} # {Symbol: {Variable: SymbolDeclaration}}
        self.translated = None

    def __str__(self):
        return "Definition(s) of " + ",".join([k.name for k in self.partition.keys()])

    def __repr__(self):
        out = []
        for symbol, rules in self.partition.items():
            for rule in rules:
                out.append(repr(rule))
        return nl.join(out)

    def annotate(self, symbol_decls, q_decls):
        self.rules = [r.annotate(symbol_decls, q_decls) for r in self.rules]

        self.partition = {}
        for r in self.rules:
            symbol = symbol_decls[r.symbol.name]
            if symbol not in self.q_decls:
                name = "$"+symbol.name+"$"
                q_v = { name+str(i): 
                    Fresh_Variable(name+str(i), symbol_decls[sort.name]) \
                        for i, sort in enumerate(symbol.sorts)}
                if symbol.out.name != 'bool':
                    q_v[name] = Fresh_Variable(name, symbol_decls[symbol.out.name])
                self.q_decls[symbol] = q_v
            new_rule = r.rename_args(self.q_decls[symbol])
            self.partition.setdefault(symbol, []).append(new_rule)
            #TODO attach interpretation to symbols
        return self

    def subtences(self):
        return mergeDicts(r.subtences() for r in self.rules)

    def expand_quantifiers(self, theory):
        for symbol, rules in self.partition.items():
            self.partition[symbol] = sum((r.expand_quantifiers(theory) for r in rules), [])
        return self

    def interpret(self, theory):
        for symbol, rules in self.partition.items():
            self.partition[symbol] = sum((r.interpret(theory) for r in rules), [])
        return self

    def unknown_symbols(self):
        out = {}
        for symbol, rules in self.partition.items():
            out[symbol.name] = symbol
            for r in rules: out.update(r.unknown_symbols())
        return out

    def translate(self, idp):
        self.translated = []
        for symbol, rules in self.partition.items():

            vars = [v.translate() for v in self.q_decls[symbol].values()]
            exprs, outputVar = [], False
            for i in rules:
                exprs.append(i.translate(vars))
                if i.out is not None:
                    outputVar = True
                    
            ors = list(e for e in exprs if e is not False)
            ors = exprs[0] if ors == [] else Or(ors)
            if outputVar:
                expr = ForAll(vars, 
                                (applyTo(symbol.translate(idp), vars[:-1]) == vars[-1]) == ors) 
            else:
                if len(vars) > 0:
                    expr = ForAll(vars, 
                                    applyTo(symbol.translate(idp), vars) == ors)
                else:
                    expr = symbol.translate(idp) == ors
            self.translated.append(expr)
        return self.translated


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
        self.q_decls = {}
        self.args = [] if self.args is None else self.args.sub_exprs
        if self.out is not None:
            self.args.append(self.out)
        if self.body is None:
            self.body = TRUE
        self.translated = None

    def __repr__(self):
        return ( f"Rule:∀{self.vars}[{self.sorts}]: "
                 f"{self.symbol}({','.join(str(e) for e in self.args)}) "
                 f"⇔{str(self.body)}" )

    def annotate(self, symbol_decls, q_decls):
        self.q_decls = {v:Fresh_Variable(v, symbol_decls[s.name]) \
                        for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_decls, **self.q_decls} # merge
        self.args = [arg.annotate(symbol_decls, q_v) for arg in self.args]
        self.out = self.out.annotate(symbol_decls, q_v) if self.out else self.out
        self.body = self.body.annotate(symbol_decls, q_v)
        return self

    def rename_args(self, new_vars):
        """ returns (?vars0,...: new_vars0=args0 & new_vars1=args1 .. & body(vars)) """
        out = []
        for new_var, arg in zip(new_vars.values(), self.args):
            eq = operation('=', [new_var, arg])
            eq.type = 'bool'
            out += [eq]
        out += [self.body]
        self.body = operation('∧', out)
        self.body.type = 'bool'
        
        return self

    def subtences(self):
        return self.body.subtences() if not self.vars else {}

    def expand_quantifiers(self, theory):
        forms = [(self.args, self.body.expand_quantifiers(theory))]
        vars = []
        for name, var in self.q_decls.items():
            if var.decl.range:
                forms = [([a.substitute(var, val) for a in args], 
                          f.substitute(var, val)
                         ) for val in var.decl.range for (args, f) in forms]
            else:
                vars.append(var)
        sorts = [] # not used anymore

        out = [Rule(reading=self.reading, vars=vars, sorts=sorts, symbol=self.symbol, 
                     args=Arguments(sub_exprs=args[:-1] if self.out else args), 
                     out=args[-1] if self.out else None, body=f) 
                for (args, f) in forms]
        return out

    def interpret(self, theory):
        self.body = self.body.interpret(theory)
        return [self]

    def unknown_symbols(self):
        out = mergeDicts(arg.unknown_symbols() for arg in self.args) # in case they are expressions
        if self.out is not None:
            out.update(self.out.unknown_symbols())
        out.update(self.body.unknown_symbols())
        return out

    def translate(self, new_vars):
        """ returns (?vars0,...: new_vars0=args0 & new_vars1=args1 .. & body(vars)) """

        log("translating rule " + str(self.body)[:20])
        for v in self.q_decls.values():
            v.translate()

        if len(self.vars) == 0:
            self.translated = self.body.translate()
        else:
            self.translated = Exists([v.translate() for v in self.vars], self.body.translate())
        return self.translated

# Expressions : see Expression.py

################################ Structure ###############################

class Interpretations(object):
    def __init__(self, **kwargs):
        self.interpretations = kwargs.pop('interpretations')

    def annotate(self, vocabulary):
        for i in self.interpretations:
            i.annotate(vocabulary.symbol_decls)

class Interpretation(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name').name
        self.tuples = kwargs.pop('tuples')
        self.default = kwargs.pop('default') # later set to false for predicates
        
        self.function = None # -1 if function else 0
        self.arity = None
        self.decl = None # symbol declaration

    def annotate(self, symbol_decls):
        self.decl = symbol_decls[self.name]
        for t in self.tuples:
            t.annotate(symbol_decls)
        self.function = 0 if self.decl.out.name == 'bool' else -1
        self.arity = len(self.tuples[0].args) # there must be at least one tuple !
        if self.function and 1 < self.arity and self.default is None:
            raise Exception("Default value required for function {} in structure.".format(self.name))
        self.default = self.default if self.function else Symbol(name='false')
        self.default = self.default.annotate(symbol_decls, {})

        def interpret(theory, rank, args, tuples=None):
            tuples = [tuple.interpret(theory) for tuple in self.tuples] if tuples == None else tuples
            if rank == self.arity + self.function: # valid tuple -> return a value
                if not self.function:
                    return TRUE
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
                        out = IfExpr(if_f=operation('=', [args[rank],val]), 
                                        then_f=interpret(theory, rank+1, args, list(tuples2)), 
                                        else_f=out)
                        out = out.simplify1()
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

    def translate(self):
        return [arg.translate() for arg in self.args]


################################ Goal, View ###############################

class Goal(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.decl = None

    def __str__(self):
        return self.name

    def annotate(self, vocabulary):
        if self.name in vocabulary.symbol_decls:
            self.decl = vocabulary.symbol_decls[self.name]


class View(object):
    def __init__(self, **kwargs):
        self.viewType = kwargs.pop('viewType')

    def translate(self):
        return

################################ Main ###############################

dslFile = os.path.join(os.path.dirname(__file__), 'Idp.tx')

idpparser = metamodel_from_file(dslFile, memoization=True, classes=
        [ Idp, 
          Vocabulary, Decision, ConstructedTypeDeclaration, Constructor, RangeDeclaration, SymbolDeclaration, Symbol, Sort,
          Theory, Definition, Rule, IfExpr, AQuantification, 
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate,
                    AppliedSymbol, Variable, NumberConstant, Brackets, Arguments,
          Interpretations, Interpretation, Tuple,
          Goal, View
        ])
