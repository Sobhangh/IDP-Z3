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

from copy import copy
import itertools as it
import os
import re
import sys

from textx import metamodel_from_file
from z3 import IntSort, BoolSort, RealSort, Or, And, Const, ForAll, Exists, Z3Exception, \
    Sum, If, Function, FreshConst, Implies, EnumSort

from utils import applyTo, log, itertools, in_list, nl, mergeDicts
from Idp.Expression import Constructor, Expression, IfExpr, AQuantification, BinaryOperator, \
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  \
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate, \
                    AppliedSymbol, Variable, Symbol, NumberConstant, Brackets, Arguments, \
                    Fresh_Variable, TRUE, FALSE

import Idp.Substitute
import Idp.Implicant


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
        self.goal.annotate(self)
        self.subtences = {**self.theory.subtences, **self.goal.subtences()}
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
        log("theory translated")
        self.goal.translate()
        self.view.translate()

    def unknown_symbols(self):
        todo = self.theory.unknown_symbols()

        out = {} # reorder per vocabulary order
        for symb in self.vocabulary.symbol_decls:
            if symb in todo:
                out[symb] = todo[symb]
        return out

    def translate(self):
        return self.theory.translate(self)


################################ Vocabulary  ###############################

class Annotations(object):
    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')

        def pair(s):
            p = s.split(':',1)
            if len(p) == 2:
                return (p[0], p[1])
            else:
                return ('reading', p[0])

        self.annotations = dict((pair(t) for t in self.annotations))

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
        return []

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
            assert len(self.constructors) == len(cstrs), "Internal error"
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
        out = [AComparison.make('=', [var, c], True) for c in self.constructors]
        out = ADisjunction.make('∨', out)
        return out

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
            elif x.fromI.type == 'int' and x.toI.type == 'int': 
                for i in range(x.fromI.translated, x.toI.translated + 1):
                    self.range.append(NumberConstant(number=str(i)))
            else:
                self.range = []
                break

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
        if not self.elements: 
            return None
        if self.range and len(self.range) < 20:
            es = [AComparison.make('=', [var, c], True) for c in self.range]
            e = ADisjunction.make('∨', es)
            return e
        sub_exprs = []
        for x in self.elements:
            if x.toI is None:
                e = AComparison.make('=', [var, x.fromI], True)
            else:
                e = AComparison.make(['≤', '≤'], [x.fromI, var, x.toI], True)
            sub_exprs.append(e)
        return ADisjunction.make('∨', sub_exprs)

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
        self.annotations = kwargs.pop('annotations')
        if self.annotations is not None:
            self.annotations = self.annotations.annotations
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
        self.range = None # all possible values
        self.instances = None # {string: Variable or AppliedSymbol} not starting with '_'
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

        # create instances
        self.instances = {}
        if vocabulary and not self.name.startswith('_'):
            if len(self.sorts) == 0:
                expr = Variable(name=self.name)
                expr.annotate(symbol_decls, {})
                expr.mark_subtences()
                expr.normal = True
                self.instances[expr.code] = expr
            else:
                for arg in list(self.domain):
                    expr = AppliedSymbol(s=Symbol(name=self.name), args=Arguments(sub_exprs=arg))
                    expr.annotate(symbol_decls, {})
                    expr.mark_subtences()
                    expr.normal = True
                    self.instances[expr.code] = expr

        # determine typeConstraint
        if self.out.decl.name != 'bool' and self.range:
            for inst in self.instances.values():
                domain = self.type.check_bounds(inst)
                if domain is not None:
                    domain.if_symbol = self.name
                    domain.annotations['reading'] = "Possible values for " + str(inst)
                    self.typeConstraints.append(domain)
        return self

    def translate(self, idp=None):
        if self.translated is None:
            if len(self.sorts) == 0:
                self.translated = Const(self.name, self.out.translate())
                self.normal = True
            else:

                if self.out.name == 'bool':
                    types = [x.translate() for x in self.sorts]
                    rel_vars = [t.getRange() for t in self.sorts]
                    self.translated = Function(self.name, types + [BoolSort()])
                else:
                    types = [x.translate() for x in self.sorts] + [self.out.translate()]
                    self.translated = Function(self.name, types)
        return self.translated


class Sort(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.code = sys.intern(self.name)
        self.decl = None

    def __str__(self): return self.code

    def annotate(self, symbol_decls):
        self.decl = symbol_decls[self.name]

    def fresh(self, name, symbol_decls):
        decl = SymbolDeclaration(annotations=Annotations(annotations=[]), name=Symbol(name=name), sorts=[], out=self)
        decl.annotate(symbol_decls, False)
        return Fresh_Variable(name, decl)

    def translate(self):
        return self.decl.translate()

    def getRange(self):
        return [e.translated for e in self.decl.range]


################################ Theory ###############################


class Theory(object):
    def __init__(self, **kwargs):
        self.constraints = kwargs.pop('constraints')
        self.definitions = kwargs.pop('definitions')
        self.clark = {} # {Symbol: Rule}
        self.symbol_decls = None # {string: decl}
        self.subtences = None # i.e., sub-sentences.  {string: Expression}
        self.translated = None

    def annotate(self, vocabulary):
        self.symbol_decls = vocabulary.symbol_decls

        self.definitions = [e.annotate(self, self.symbol_decls, {}) for e in self.definitions]
        # squash multiple definitions of same symbol
        for d in self.definitions:
            for symbol, rule in d.clark.items():
                if symbol in self.clark:
                    new_rule = copy(rule) # not elegant, but rare
                    new_rule.body = AConjunction.make('∧', [self.clark[symbol.name].body, rule.body])
                    self.clark[symbol.name] = new_rule
                else:
                    self.clark[symbol.name] = rule

        self.constraints = [e.annotate(self.symbol_decls, {}) for e in self.constraints]
        self.constraints = [e.mark_subtences()         for e in self.constraints]
        self.constraints = [e.expand_quantifiers(self) for e in self.constraints]
        self.constraints = [e.interpret         (self) for e in self.constraints]
        

        for decl in self.symbol_decls.values():
            if type(decl) == SymbolDeclaration:
                self.constraints.extend(decl.typeConstraints)

        self.subtences = {}
        for e in self.constraints:
            self.subtences.update({k: v for k, v in e.subtences().items()})

    def unknown_symbols(self):
        return mergeDicts(c.unknown_symbols()
            for c in self.constraints + self.definitions)

    def translate(self, idp):
        out = []
        for i in self.constraints:
            out.append(i.translate())
            # optional : self.translated.extend(i.justifications())
        for d in self.definitions:
            out += d.translate(idp)
        return out


class Definition(object):
    def __init__(self, **kwargs):
        self.rules = kwargs.pop('rules')
        self.clark = None # {Symbol: Transformed Rule}
        self.q_vars = {} # {Symbol: {String: Fresh_Variable}} Fresh variables for arguments & result
        self.translated = None

    def __str__(self):
        return "Definition(s) of " + ",".join([k.name for k in self.clark.keys()])

    def __repr__(self):
        out = []
        for symbol, rule in self.clark.items():
            out.append(repr(rule))
        return nl.join(out)

    def annotate(self, theory, symbol_decls, q_vars):
        self.rules = [r.annotate(symbol_decls, q_vars) for r in self.rules]

        # create common variables, and rename vars in rule
        self.clark = {}
        for r in self.rules:
            symbol = symbol_decls[r.symbol.name]
            if symbol not in self.q_vars:
                name = f"${symbol.name}$"
                q_v = { f"${symbol.name}!{str(i)}$":
                    sort.fresh(f"${symbol.name}!{str(i)}$", symbol_decls) \
                        for i, sort in enumerate(symbol.sorts)}
                if symbol.out.name != 'bool':
                    q_v[name] = symbol.out.fresh(name, symbol_decls)
                self.q_vars[symbol] = q_v
            new_rule = r.rename_args(self.q_vars[symbol])
            self.clark.setdefault(symbol, []).append(new_rule)

        # join the bodies of rules
        for symbol, rules in self.clark.items():
            exprs = sum(([rule.body] for rule in rules), [])
            rules[0].body = ADisjunction.make('∨', exprs)
            rules[0].body.mark_subtences()
            self.clark[symbol] = rules[0]
            
        # expand quantifiers and interpret symbols with structure
        for symbol, rule in self.clark.items():
            self.clark[symbol] = rule.compute(theory)

        return self

    def unknown_symbols(self):
        out = {}
        for symbol, rule in self.clark.items():
            out[symbol.name] = symbol
            out.update(rule.unknown_symbols())
        return out

    def translate(self, idp):
        return [rule.translate() for rule in self.clark.values()]


class Rule(object):
    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.symbol = kwargs.pop('symbol')
        self.args = kwargs.pop('args') # later augmented with self.out, if any
        self.out = kwargs.pop('out')
        self.body = kwargs.pop('body')
        self.expanded = None # Expression

        self.annotations = self.annotations.annotations if self.annotations else {}

        assert len(self.vars) == len(self.sorts), "Internal error"
        self.q_vars = {} # {string: Fresh_Variable}
        self.args = [] if self.args is None else self.args.sub_exprs
        if self.out is not None:
            self.args.append(self.out)
        if self.body is None:
            self.body = TRUE
        self.translated = None

    def __repr__(self):
        return ( f"Rule:∀{self.vars}{self.sorts}: "
                 f"{self.symbol}({','.join(str(e) for e in self.args)}) "
                 f"⇔{str(self.body)}" )

    def annotate(self, symbol_decls, q_vars):
        # create head variables
        assert len(self.vars) == len(self.sorts), "Internal error"
        self.q_vars = {v:s.fresh(v, symbol_decls) \
                        for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_vars, **self.q_vars} # merge

        self.symbol = self.symbol.annotate(symbol_decls, q_v).mark_subtences()
        self.args = [arg.annotate(symbol_decls, q_v).mark_subtences() for arg in self.args]
        self.out = self.out.annotate(symbol_decls, q_v).mark_subtences() if self.out else self.out
        self.body = self.body.annotate(symbol_decls, q_v).mark_subtences()
        return self

    def rename_args(self, new_vars):
        """ for Clark's completion
            input : '!v: f(args) <- body(args)'
            output: '!nv: f(nv) <- ?v: nv=args & body(args)' """

        subst = {}
        assert len(self.args) == len(new_vars), "Internal error"
        for arg, nv in zip(self.args, new_vars.values()):
            if type(arg) in [Variable, Fresh_Variable]:
                if arg.name not in subst:
                    if arg.name in self.vars:
                        subst[arg.name] = nv
                        self.body = self.body.instantiate(arg, nv)
                    else:
                        eq = AComparison.make('=', [nv, arg])
                        self.body = AConjunction.make('∧', [eq, self.body])
                else: # same(x)=x
                    eq = AComparison.make('=', [nv, subst[arg.name]])
                    self.body = AConjunction.make('∧', [eq, self.body])
            else: #same(f(x))
                eq = AComparison.make('=', [nv, arg])
                for v0, v1 in subst.items():
                    eq = eq.instantiate(Symbol(name=v0), v1)
                self.body = AConjunction.make('∧', [eq, self.body])

        # Any leftover ?
        for var in self.vars:
            if str(var) in subst:
                pass
            else:
                self.body = AQuantification.make('∃', {var: self.q_vars[var]}, self.body)

        self.args = list(new_vars.values())
        self.vars = list(new_vars.keys())
        self.sorts = [] # ignored
        self.q_vars = new_vars
        return self

    def compute(self, theory):
        """ expand quantifiers and interpret """
        self.body = self.body.expand_quantifiers(theory)

        # compute self.expanded, by expanding:
        # ∀ v: f(v)=out <=> body
        # (after joining the rules of the same symbols)
        if self.out:
            expr = AppliedSymbol.make(self.symbol, self.args[:-1])
            expr = AComparison.make('=', [expr, self.args[-1]])
        else:
            expr = AppliedSymbol.make(self.symbol, self.args)
        expr = AEquivalence.make('⇔', [expr, self.body])
        expr = AQuantification.make('∀', {**self.q_vars}, expr)
        self.expanded = expr.expand_quantifiers(theory)
        
        # interpret structures
        self.body     = self.body    .interpret(theory)
        self.expanded = self.expanded.interpret(theory)
        return self

    def instantiate_definition(self, new_args, theory, value=None):
        out = self.body
        assert len(new_args) == len(self.args) or len(new_args)+1 == len(self.args), "Internal error"
        for old, new in zip(self.args, new_args):
            out = out.instantiate(old, new)
        out = out.interpret(theory) # add justification recursively
        instance = AppliedSymbol.make(self.symbol, new_args)
        instance.normal = True
        if len(new_args)+1 == len(self.args): # a function
            if value is not None:
                head = AComparison.make("=", [instance, value])
                out = out.instantiate(self.args[-1], value)
                out = AEquivalence.make('⇔', [head, out])
            else:
                out = out.instantiate(self.args[-1], instance)
        else:
            out = AEquivalence.make('⇔', [instance, out])
        out.mark_subtences()
        return out

    def unknown_symbols(self):
        out = mergeDicts(arg.unknown_symbols() for arg in self.args) # in case they are expressions
        if self.out is not None:
            out.update(self.out.unknown_symbols())
        out.update(self.body.unknown_symbols())
        return out

    def translate(self):
        return self.expanded.translate()


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
                        out = IfExpr.make(AComparison.make('=', [args[rank],val]),
                                          interpret(theory, rank+1, args, list(tuples2)),
                                          out)
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
        self.justification = None

    def __str__(self):
        return self.name

    def annotate(self, idp):
        if self.name in idp.vocabulary.symbol_decls:
            self.decl = idp.vocabulary.symbol_decls[self.name]
            if self.name in idp.theory.clark: # defined goal
                rule = idp.theory.clark[self.name]
                just = []
                for args in self.decl.domain:
                    if self.decl.type.name == 'bool':
                        instance = rule.instantiate_definition(args, idp.theory)
                        just.append(instance)
                        just.extend(instance.justifications())
                    else:
                        just1 = []
                        for out in self.decl.range:
                            instance = rule.instantiate_definition(args, idp.theory, out)
                            just1.append(instance)
                            just.extend(instance.justifications())
                        just.append(ADisjunction.make('∨', just1))
                self.justification = AConjunction.make('∧', just)

    def subtences(self):
        return {} if self.justification is None else \
               self.justification.subtences()

    def translate(self):
        if self.justification is not None:
            return self.justification.translate()
        return None


class View(object):
    def __init__(self, **kwargs):
        self.viewType = kwargs.pop('viewType')

    def translate(self):
        return

################################ Main ###############################

dslFile = os.path.join(os.path.dirname(__file__), 'Idp.tx')

idpparser = metamodel_from_file(dslFile, memoization=True, classes=
        [ Idp, Annotations,
          Vocabulary, Decision, ConstructedTypeDeclaration, Constructor, RangeDeclaration, SymbolDeclaration, Symbol, Sort,
          Theory, Definition, Rule, IfExpr, AQuantification,
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate,
                    AppliedSymbol, Variable, NumberConstant, Brackets, Arguments,
          Interpretations, Interpretation, Tuple,
          Goal, View
        ])
