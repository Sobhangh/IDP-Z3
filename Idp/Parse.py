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
from enum import Enum
import itertools as it
import os
import re
import sys

from debugWithYamlLog import Log, NEWL
from textx import metamodel_from_file
from z3 import (IntSort, BoolSort, RealSort, Or, And, Const, ForAll, Exists,
                Z3Exception, Sum, If, Function, FreshConst, Implies, EnumSort, BoolVal)

from .Assignments import *
from .Expression import (Constructor, Expression, IfExpr, AQuantification,
                         BinaryOperator, ARImplication, AEquivalence,
                         AImplication, ADisjunction, AConjunction,
                         AComparison, ASumMinus, AMultDiv, APower, AUnary,
                         AAggregate, AppliedSymbol, Variable,
                         NumberConstant, Brackets, Arguments,
                         Fresh_Variable, TRUE, FALSE)
from .utils import applyTo, itertools, in_list, mergeDicts, log, unquote, OrderedSet


class ViewType(Enum):
    HIDDEN = "hidden"
    NORMAL = "normal"
    EXPANDED = "expanded"


class Idp(object):
    def __init__(self, **kwargs):
        #log("parsing done")
        self.vocabularies = {v.name : v for v in kwargs.pop('vocabularies')}
        self.theories = {t.name : t for t in kwargs.pop('theories')}
        self.structures = {s.name : s for s in kwargs.pop('structures')}
        self.goal = kwargs.pop('goal')
        self.view = kwargs.pop('view')
        self.display = kwargs.pop('display')
        self.procedures = {p.name: p for p in kwargs.pop('procedures')}

        self.translated = None  # [Z3Expr]

        assert self.display is None or 'main' not in self.procedures, \
            "Cannot have both a 'display and a 'main block"
        if self.display is not None:
            assert len(self.vocabularies) in [1,2], \
                "Maximum 2 vocabularies are allowed in Interactive Consultant"
            assert len(self.theories) in [1,2], \
                "Maximum 2 theories are allowed in Interactive Consultant"

            if len(self.vocabularies)==2:
                assert 'environment' in self.vocabularies and 'decision' in self.vocabularies, \
                    "The 2 vocabularies in Interactive Consultant must be 'environment' and 'decision'"
            if len(self.theories)==2:
                assert 'environment' in self.theories and 'decision' in self.theories, \
                    "The 2 theories in Interactive Consultant must be 'environment' and 'decision'"

        if self.goal    is None: self.goal    = Goal(name="")
        if self.view    is None: self.view    = View(viewType='normal')
        if self.display is None: self.display = Display(constraints=[])
        
        for voc in self.vocabularies.values():
            voc.annotate(self)

        # determine default vocabulary, theory
        if list(self.vocabularies.keys()) == ['environment', 'decision']:
            self.vocabulary = self.vocabularies['decision']
        else:
            self.vocabulary = next(iter(self.vocabularies.values())) # get first vocabulary
        if list(self.theories.keys()) == ['environment', 'decision']:
            self.theory = self.theories['decision']
            self.theory.constraints.extend(self.theories['environment'].constraints)
            self.theory.definitions.extend(self.theories['environment'].definitions)
        else:
            self.theory = next(iter(self.theories.values())) # get first theory
        for struct in self.structures.values():
            struct.annotate(self) # attaches an interpretation to the vocabulary

        self.goal.annotate(self)
        self.view.annotate(self)
        self.display.annotate(self)
        self.display.run(self)
        self.theory.annotate(self)
        self.subtences = {**self.theory.subtences, **self.goal.subtences()}

    def unknown_symbols(self):
        todo = self.theory.unknown_symbols()

        out = {}  # reorder per vocabulary order
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
            p = s.split(':', 1)
            if len(p) == 2:
                try:
                    # Do we have a Slider?
                    # The format of p[1] is as follows:
                    # (lower_sym, upper_sym): (lower_bound, upper_bound)
                    pat = r"\(((.*?), (.*?))\)"
                    arg = re.findall(pat, p[1])
                    l_symb = arg[0][1]
                    u_symb = arg[0][2]
                    l_bound = arg[1][1]
                    u_bound = arg[1][2]
                    slider_arg = {'lower_symbol': l_symb,
                                'upper_symbol': u_symb,
                                'lower_bound': l_bound,
                                'upper_bound': u_bound}
                    return(p[0], slider_arg)
                except: # could not parse the slider data
                    return (p[0], p[1])
            else:
                return ('reading', p[0])

        self.annotations = dict((pair(t) for t in self.annotations))


class Vocabulary(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.declarations = kwargs.pop('declarations')
        self.terms = {}  # {string: Variable or AppliedSymbol}
        self.idp = None # parent object
        self.translated = []

        self.name = 'V' if not self.name else self.name

        # define reserved symbols
        self.symbol_decls = {'int' : RangeDeclaration(name='int' , elements=[]),
                             'real': RangeDeclaration(name='real', elements=[])
                            }
        for name, constructors in [
            ('bool',      [TRUE, FALSE]),
            ('`Symbols', [Constructor(name=f"`{s.name}") for s in self.declarations if type(s)==SymbolDeclaration]), 
        ]:
            ConstructedTypeDeclaration(name=name, constructors=constructors) \
                .annotate(self) # add it to symbol_decls

    def annotate(self, idp):
        self.idp = idp

        # annotate declarations
        for s in self.declarations:
            s.block = self
            s.annotate(self) # updates self.symbol_decls

        for constructor in self.symbol_decls['`Symbols'].constructors:
            constructor.symbol = Symbol(name=constructor.name[1:]).annotate(self, {})

        for v in self.symbol_decls.values():
            if v.is_var:
                self.terms.update(v.instances)


    def __str__(self):
        return (f"vocabulary {{{NEWL}"
                f"{NEWL.join(str(i) for i in self.declarations)}"
                f"{NEWL}}}{NEWL}")


class Extern(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def __str__(self):
        return f"extern vocabulary {self.name}"

    def annotate(self, voc):
        other = voc.idp.vocabularies[self.name]
        voc.symbol_decls = {**other.symbol_decls, **voc.symbol_decls} #TODO merge while respecting order


class ConstructedTypeDeclaration(object):
    COUNT = -1

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.constructors = kwargs.pop('constructors')
        self.is_var = False
        self.range = self.constructors  # functional constructors are expanded
        self.translated = None

        if self.name == 'bool':
            self.translated = BoolSort()
            self.constructors[0].type = 'bool'
            self.constructors[1].type = 'bool'
            self.constructors[0].translated = BoolVal(True)
            self.constructors[1].translated = BoolVal(False)
        else:
            self.translated, cstrs = EnumSort(self.name, [c.name for c in
                                                          self.constructors])
            assert len(self.constructors) == len(cstrs), "Internal error"
            for c, c3 in zip(self.constructors, cstrs):
                c.translated = c3
                c.index = ConstructedTypeDeclaration.COUNT
                ConstructedTypeDeclaration.COUNT -= 1

        self.type = None

    def __str__(self):
        return (f"type {self.name} constructed from "
                f"{{{','.join(map(str, self.constructors))}}}")

    def annotate(self, voc, idp=None):
        assert self.name not in voc.symbol_decls, "duplicate declaration in vocabulary: " + self.name
        voc.symbol_decls[self.name] = self
        for c in self.constructors:
            c.type = self.name
            assert c.name not in voc.symbol_decls, "duplicate constructor in vocabulary: " + c.name
            voc.symbol_decls[c.name] = c
        self.range = self.constructors  # TODO constructor functions

    def check_bounds(self, var):
        if self.name == 'bool':
            out = [var, AUnary.make('~', var)]
        else:
            out = [AComparison.make('=', [var, c]) for c in self.constructors]
        out = ADisjunction.make('∨', out)
        return out

    def translate(self):
        return self.translated


class RangeDeclaration(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')  # maybe 'int', 'real'
        self.elements = kwargs.pop('elements')
        self.is_var = False
        self.translated = None

        self.type = 'int'
        self.range = []
        for x in self.elements:
            if x.toI is None:
                self.range.append(x.fromI)
                if type(x.fromI.translated) != int:
                    self.type = 'real'
            elif x.fromI.type == 'int' and x.toI.type == 'int':
                for i in range(x.fromI.translated, x.toI.translated + 1):
                    self.range.append(NumberConstant(number=str(i)))
            else:
                assert False, "Can't have a range over reals: " + self.name

        if self.name == 'int':
            self.translated = IntSort()
        elif self.name == 'real':
            self.translated = RealSort()
            self.type = 'real'

    def __str__(self):
        elements = ";".join([str(x.fromI) + ("" if x.toI is None else ".." + str(x.toI)) for x in self.elements])
        return f"type {self.name} = {{{elements}}}"

    def annotate(self, voc, idp=None):
        assert self.name not in voc.symbol_decls, "duplicate declaration in vocabulary: " + self.name
        voc.symbol_decls[self.name] = self

    def check_bounds(self, var):
        if not self.elements: 
            return None
        if self.range and len(self.range) < 20:
            es = [AComparison.make('=', [var, c]) for c in self.range]
            e = ADisjunction.make('∨', es)
            return e
        sub_exprs = []
        for x in self.elements:
            if x.toI is None:
                e = AComparison.make('=', [var, x.fromI])
            else:
                e = AComparison.make(['≤', '≤'], [x.fromI, var, x.toI])
            sub_exprs.append(e)
        return ADisjunction.make('∨', sub_exprs)

    def translate(self):
        if self.translated is None:
            if self.type == 'int':
                self.translated = IntSort()
            else:
                self.translated = RealSort()
        return self.translated


class SymbolDeclaration(object):
    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')
        self.name = sys.intern(kwargs.pop('name').name)  # a string, not a Symbol
        self.sorts = kwargs.pop('sorts')
        self.out = kwargs.pop('out')
        if self.out is None:
            self.out = Sort(name='bool')

        self.function = (self.out.name != 'bool')
        self.arity = len(self.sorts)
        self.annotations = self.annotations.annotations if self.annotations else {}
        
        self.is_var = True  # unless interpreted later
        self.typeConstraints = []
        self.translated = None

        self.type = None  # a declaration object
        self.domain = None  # all possible arguments
        self.range = None  # all possible values
        self.instances = None  # {string: Variable or AppliedSymbol} not starting with '_'
        self.block = None  # vocabulary where it is declared
        self.view = ViewType.NORMAL # "hidden" | "normal" | "expanded" whether the symbol box should show atoms that contain that symbol, by default

    def __str__(self):
        args = ','.join(map(str, self.sorts)) if 0 < len(self.sorts) else ''
        return (f"{self.name}"
                f"{ '('+args+')' if args else ''}"
                f"{'' if self.out.name == 'bool' else f' : {self.out.name}'}")

    def annotate(self, voc, idp=None, vocabulary=True):
        if vocabulary:
            assert self.name not in voc.symbol_decls, "duplicate declaration in vocabulary: " + self.name
            voc.symbol_decls[self.name] = self
        for s in self.sorts:
            s.annotate(voc)
        self.out.annotate(voc)
        self.domain = list(itertools.product(*[s.decl.range for s in self.sorts]))

        self.type  = self.out.decl.name
        self.range = self.out.decl.range

        # create instances
        self.instances = {}
        if vocabulary:   # and not self.name.startswith('_'):
            if len(self.sorts) == 0:
                expr = Variable(s=Symbol(name=self.name))
                expr.annotate(voc, {})
                expr.normal = True
                self.instances[expr.code] = expr
            else:
                for arg in list(self.domain):
                    expr = AppliedSymbol(s=Symbol(name=self.name), args=Arguments(sub_exprs=arg))
                    expr.annotate(voc, {})
                    expr.normal = True
                    self.instances[expr.code] = expr

        # determine typeConstraints
        if self.out.decl.name != 'bool' and self.range and self.is_var:
            for inst in self.instances.values():
                domain = self.out.decl.check_bounds(inst)
                if domain is not None:
                    domain.block = self.block
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

    def annotate(self, voc):
        self.decl = voc.symbol_decls[self.name]

    def translate(self):
        return self.decl.translate()

    
class Symbol(object): 
    def __init__(self, **kwargs):
        self.name = unquote(kwargs.pop('name'))

    def annotate(self, voc, q_vars):
        self.decl = voc.symbol_decls[self.name]
        self.type = self.decl.type
        self.normal = True # make sure it is visible in GUI
        return self

    def __str__(self): return self.name

################################ Theory ###############################


class Theory(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.vocab_name = kwargs.pop('vocab_name')
        self.constraints = OrderedSet(kwargs.pop('constraints'))
        self.definitions = kwargs.pop('definitions')

        self.name = "T" if not self.name else self.name
        self.vocab_name = 'V' if not self.vocab_name else self.vocab_name

        self.clark = {}  # {Declaration: Rule}
        self.subtences = None  # i.e., sub-sentences.  {string: Expression}
        self.assignments = Assignments()
        self.translated = None

        for constraint in self.constraints:
            constraint.block = self
        for definition in self.definitions:
            for rule in definition.rules:
                rule.block = self

    def __str__(self):
        return self.name

    def annotate(self, idp):
        assert self.vocab_name in idp.vocabularies, "Unknown vocabulary: " + self.vocab_name
        voc = idp.vocabularies[self.vocab_name]

        self.definitions = [e.annotate(self, voc, {}) for e in self.definitions]
        # squash multiple definitions of same symbol declaration
        for d in self.definitions:
            for decl, rule in d.clark.items():
                if decl in self.clark:
                    new_rule = copy(rule)  # not elegant, but rare
                    new_rule.body = AConjunction.make('∧', [self.clark[decl].body, rule.body])
                    self.clark[decl] = new_rule
                else:
                    self.clark[decl] = rule

        self.constraints = OrderedSet([e.annotate(voc, {})        for e in self.constraints])
        self.constraints = OrderedSet([e.expand_quantifiers(self) for e in self.constraints])
        self.constraints = OrderedSet([e.interpret         (self) for e in self.constraints])

        for decl in voc.symbol_decls.values():
            if type(decl) == SymbolDeclaration:
                self.constraints.extend(decl.typeConstraints)

        self.subtences = {}
        for e in self.constraints:
            self.subtences.update({k: v for k, v in e.subtences().items()})

    def unknown_symbols(self):
        return mergeDicts(c.unknown_symbols()
                          for c in list(self.constraints) + self.definitions)

    def translate(self, idp):
        out = []
        for i in self.constraints:
            out.append(i.translate())
        for d in self.definitions:
            out += d.translate()
        return out


class Definition(object):
    def __init__(self, **kwargs):
        self.rules = kwargs.pop('rules')
        self.clark = None  # {Declaration: Transformed Rule}
        self.def_vars = {}  # {String: {String: Fresh_Variable}} Fresh variables for arguments & result
        self.translated = None

    def __str__(self):
        return "Definition(s) of " + ",".join([k.name for k in self.clark.keys()])

    def __repr__(self):
        out = []
        for rule in self.clark.values():
            out.append(repr(rule))
        return NEWL.join(out)

    def annotate(self, theory, voc, q_vars):
        self.rules = [r.annotate(voc, q_vars) for r in self.rules]

        # create common variables, and rename vars in rule
        self.clark = {}
        for r in self.rules:
            decl = voc.symbol_decls[r.symbol.name]
            if decl.name not in self.def_vars:
                name = f"${decl.name}$"
                q_v = {f"${decl.name}!{str(i)}$":
                       Fresh_Variable(f"${decl.name}!{str(i)}$", sort)
                       for i, sort in enumerate(decl.sorts)}
                if decl.out.name != 'bool':
                    q_v[name] = Fresh_Variable(name, decl.out)
                self.def_vars[decl.name] = q_v
            new_rule = r.rename_args(self.def_vars[decl.name])
            self.clark.setdefault(decl, []).append(new_rule)

        # join the bodies of rules
        for decl, rules in self.clark.items():
            exprs = sum(([rule.body] for rule in rules), [])
            rules[0].body = ADisjunction.make('∨', exprs)
            self.clark[decl] = rules[0]

        # expand quantifiers and interpret symbols with structure
        for decl, rule in self.clark.items():
            self.clark[decl] = rule.compute(theory)

        return self

    def unknown_symbols(self):
        out = {}
        for decl, rule in self.clark.items():
            out[decl.name] = decl
            out.update(rule.unknown_symbols())
        return out

    def translate(self):
        return [rule.translate() for rule in self.clark.values()]


class Rule(object):
    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')
        self.vars = kwargs.pop('vars')
        self.sorts = kwargs.pop('sorts')
        self.symbol = kwargs.pop('symbol')
        self.args = kwargs.pop('args')  # later augmented with self.out, if any
        self.out = kwargs.pop('out')
        self.body = kwargs.pop('body')
        self.expanded = None  # Expression
        self.block = None  # theory where it occurs

        self.annotations = self.annotations.annotations if self.annotations else {}

        assert len(self.vars) == len(self.sorts), "Internal error"
        self.q_vars = {}  # {string: Fresh_Variable}
        self.args = [] if self.args is None else self.args.sub_exprs
        if self.out is not None:
            self.args.append(self.out)
        if self.body is None:
            self.body = TRUE
        self.translated = None

    def __repr__(self):
        return (f"Rule:∀{','.join(f'{str(v)}[{str(s)}]' for v, s in zip(self.vars,self.sorts))}: "
                f"{self.symbol}({','.join(str(e) for e in self.args)}) "
                f"⇔{str(self.body)}")

    def annotate(self, voc, q_vars):
        # create head variables
        assert len(self.vars) == len(self.sorts), "Internal error"
        for s in self.sorts:
            s.annotate(voc)
        self.q_vars = {v:Fresh_Variable(v, s)
                       for v, s in zip(self.vars, self.sorts)}
        q_v = {**q_vars, **self.q_vars}  # merge

        self.symbol = self.symbol.annotate(voc, q_v)
        self.args = [arg.annotate(voc, q_v) for arg in self.args]
        self.out = self.out.annotate(voc, q_v) if self.out else self.out
        self.body = self.body.annotate(voc, q_v)
        return self

    def rename_args(self, new_vars):
        """ for Clark's completion
            input : '!v: f(args) <- body(args)'
            output: '!nv: f(nv) <- ?v: nv=args & body(args)' """

        subst = {}
        assert len(self.args) == len(new_vars), "Internal error"
        for arg, nv in zip(self.args, new_vars.values()):
            if type(arg) in [Variable, Fresh_Variable]:
                if arg.name not in subst:  # if new arg variable
                    if arg.name in self.vars:  # re-use var name
                        subst[arg.name] = nv
                        self.body = self.body.instantiate(arg, nv)
                    else:
                        eq = AComparison.make('=', [nv, arg])
                        self.body = AConjunction.make('∧', [eq, self.body])
                else:  # repeated arg var, e.g., same(x)=x
                    eq = AComparison.make('=', [nv, subst[arg.name]])
                    self.body = AConjunction.make('∧', [eq, self.body])
            elif type(arg) in [NumberConstant, Constructor]:
                eq = AComparison.make('=', [nv, arg])
                self.body = AConjunction.make('∧', [eq, self.body])
            else:  # same(f(x))
                eq = AComparison.make('=', [nv, arg])
                self.body = AConjunction.make('∧', [eq, self.body])

        # Any leftover ?
        for var in self.vars:
            if str(var) in subst:
                pass
            else:
                self.body = AQuantification.make('∃', {var: self.q_vars[var]},
                                                 self.body)

        self.args = list(new_vars.values())
        self.vars = list(new_vars.keys())
        self.sorts = [v.sort for v in new_vars.values()]
        self.q_vars = new_vars
        return self

    def compute(self, theory):
        """ expand quantifiers and interpret """

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
        self.expanded = self.expanded.interpret(theory) # definition constraint, expanded
        return self

    def instantiate_definition(self, new_args, theory, value=None):
        out = self.body
        assert len(new_args) == len(self.args) or len(new_args)+1 == len(self.args), "Internal error"
        for old, new in zip(self.args, new_args):
            out = out.instantiate(old, new)
        out = out.expand_quantifiers(theory)
        out = out.interpret(theory)  # add justification recursively
        instance = AppliedSymbol.make(self.symbol, new_args)
        instance.normal = True
        if len(new_args)+1 == len(self.args):  # a function
            if value is not None:
                head = AComparison.make("=", [instance, value])
                out = out.instantiate(self.args[-1], value)
                out = AEquivalence.make('⇔', [head, out])
            else:
                out = out.instantiate(self.args[-1], instance)
        else:
            out = AEquivalence.make('⇔', [instance, out])
        out.block = self.block
        return out

    def unknown_symbols(self):
        out = mergeDicts(arg.unknown_symbols() for arg in self.args)  # in case they are expressions
        if self.out is not None:
            out.update(self.out.unknown_symbols())
        out.update(self.body.unknown_symbols())
        return out

    def translate(self):
        return self.expanded.translate()


# Expressions : see Expression.py

################################ Structure ###############################

class Structure(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.vocab_name = kwargs.pop('vocab_name')
        self.interpretations = {i.name: i for i in kwargs.pop('interpretations')}

        self.name = 'S' if not self.name else self.name
        self.vocab_name = 'V' if not self.vocab_name else self.vocab_name

        self.voc = None
        self.assignments = Assignments()

    def annotate(self, idp):
        assert self.vocab_name in idp.vocabularies, "Unknown vocabulary: " + self.vocab_name
        self.voc = idp.vocabularies[self.vocab_name]
        for i in self.interpretations.values():
            i.annotate(self) # this updates self.assignments

    def __str__(self):
        return self.name


class Interpretation(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name').name
        self.tuples = kwargs.pop('tuples')
        self.default = kwargs.pop('default')  # later set to false for predicates

        self.decl = None  # symbol declaration

    def annotate(self, struct):
        voc = struct.voc
        self.decl = voc.symbol_decls[self.name]
        if self.decl.function and 0 < self.decl.arity and self.default is None:
            raise Exception("Default value required for function {} in structure.".format(self.name))
        self.default = FALSE if not self.decl.function and self.tuples else self.default
        self.default = self.default.annotate(voc, {})
        assert self.default.as_ground() is not None, f"Must be a ground term: {self.default}"

        # annotate tuple and compute self.data
        count, symbol = 0, Symbol(name=self.name).annotate(voc, {})
        for t in self.tuples:
            t.annotate(voc)
            assert all(a.as_ground() is not None for a in t.args), f"Must be a ground term: {t}"
            if self.decl.function:
                expr = AppliedSymbol.make(symbol, t.args[:-1])
                struct.assignments.assert_(expr, t.args[-1], Status.UNIVERSAL, False)
            else:
                expr = AppliedSymbol.make(symbol, t.args)
                struct.assignments.assert_(expr, TRUE, Status.UNIVERSAL, False)
            count += 1

        # set default value
        if count < len(self.decl.instances):
            for code, expr in self.decl.instances.items():
                if code not in struct.assignments:
                    struct.assignments.assert_(expr, self.default, Status.UNIVERSAL, False)

        self.decl.is_var = False


class Tuple(object):
    def __init__(self, **kwargs):
        self.args = kwargs.pop('args')

    def __str__(self):
        return ",".join([str(a) for a in self.args])

    def annotate(self, voc):
        self.args = [arg.annotate(voc, {}) for arg in self.args]

    def interpret(self, theory): return self  # TODO ?

    def translate(self):
        return [arg.translate() for arg in self.args]


################################ Goal, View ###############################

class Goal(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.decl = None
        self.justification = None
        self.constraint = None

    def __str__(self):
        return self.name

    def annotate(self, idp):
        voc = idp.vocabulary

        # define reserved symbol
        if '__relevant' not in voc.symbol_decls:
            relevants = SymbolDeclaration(annotations='', name=Symbol(name='__relevant'),
                                    sorts=[], out=None)
            relevants.is_var = False
            relevants.block = self
            relevants.annotate(voc)

        if self.name in voc.symbol_decls:
            self.decl = voc.symbol_decls[self.name]
            self.decl.view = ViewType.EXPANDED # the goal is always expanded
            instances = self.decl.instances.values()
            if instances:
                goal = Symbol(name='__relevant').annotate(voc, {})
                constraint = AppliedSymbol.make(goal, instances) # ??
                constraint.block = self
                idp.theory.constraints.append(constraint)
            else:
                raise Exception("goals must be instantiable.")
        elif self.name not in [None, '']:
            raise Exception("Unknown goal: " + self.name)

    def subtences(self):
        return {}


class View(object):
    def __init__(self, **kwargs):
        self.viewType = kwargs.pop('viewType')

    def annotate(self, idp):
        if self.viewType == 'expanded':
            for s in idp.vocabulary.symbol_decls.values():
                s.expanded = True



################################ Display ###############################

class Display(object):
    def __init__(self, **kwargs):
        self.constraints = kwargs.pop('constraints')
        self.moveSymbols = False
        self.optionalPropagation = False
        self.name = "display"

    def annotate(self, idp):
        self.voc = idp.vocabulary

        #add display predicates

        viewType = ConstructedTypeDeclaration(name='View', 
            constructors=[Constructor(name='normal'), Constructor(name='expanded')])
        viewType.annotate(self.voc)

        for name, out in [
            ('goal', None),
            ('expand', None),
            ('relevant', None),
            ('hide', None),
            ('view', Sort(name='View')),
            ('moveSymbols', None),
            ('optionalPropagation', None)
        ]:
            symbol_decl = SymbolDeclaration(annotations='', name=Symbol(name=name), 
                sorts=[], out=out)
            symbol_decl.is_var = False
            symbol_decl.annotate(self.voc)
            symbol_decl.translate()

        # annotate constraints
        for constraint in self.constraints:
            constraint.annotate(self.voc, {})

    def run(self, idp):
        for constraint in self.constraints:
            if type(constraint)==AppliedSymbol:
                symbols = []
                for symbol in constraint.sub_exprs:
                    assert isinstance(symbol, Constructor), f"argument '{str(symbol)}' of '{constraint.name}' should be a Constructor, not a {type(symbol)}"
                    assert symbol.name.startswith('`'), f"argument '{symbol.name}' of '{constraint.name}' must start with a tick '`'"
                    assert symbol.name[1:] in self.voc.symbol_decls, f"argument '{symbol.name}' of '{constraint.name}' must be a symbol'"
                    symbols.append(self.voc.symbol_decls[symbol.name[1:]])

                if constraint.name == 'goal': #e.g.,  goal(Prime)
                    assert len(constraint.sub_exprs)==1, f'goal can have only one argument'
                    goal = Goal(name=constraint.sub_exprs[0].name[1:])
                    goal.annotate(idp)
                    idp.goal = goal
                elif constraint.name == 'expand': # e.g. expand(Length, Angle)
                    for symbol in symbols:
                        self.voc.symbol_decls[symbol.name].view = ViewType.EXPANDED
                elif constraint.name == 'hide': # e.g. hide(Length, Angle)
                    for symbol in symbols:
                        self.voc.symbol_decls[symbol.name].view = ViewType.HIDDEN
                elif constraint.name == 'relevant': # e.g. relevant(Tax)
                    for symbol in symbols:
                        instances = symbol.instances.values()
                        if instances:
                            goal = Symbol(name='__relevant').annotate(self.voc, {})
                            constraint = AppliedSymbol.make(goal, instances) # ??
                            constraint.block = self
                            idp.theory.constraints.append(constraint)
                        else:
                            raise Exception("relevant symbols must be instantiable.")
                else:
                    raise Exception("unknown display contraint: ", constraint)
            elif type(constraint)==AComparison: # e.g. view = normal
                assert constraint.is_assignment
                if constraint.sub_exprs[0].name == 'view':
                    if constraint.sub_exprs[1].name == 'expanded':
                        for s in self.voc.symbol_decls.values():
                            if type(s)==SymbolDeclaration and s.view == ViewType.NORMAL:
                                s.view = ViewType.EXPANDED # don't change hidden symbols
                    else:
                        assert constraint.sub_exprs[1].name == 'normal', f"unknown display contraint: {constraint}"
                else:
                    raise Exception("unknown display contraint: ", constraint)
            elif type(constraint)==Variable:
                if constraint.name == "moveSymbols":
                    self.moveSymbols = True
                elif constraint.name == "optionalPropagation":
                    self.optionalPropagation = True
                else:
                    raise Exception("unknown display contraint: ", constraint)
            else:
                raise Exception("unknown display contraint: ", constraint)



################################ Main ##################################

class Procedure(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.args = kwargs.pop('args')
        self.pystatements = kwargs.pop('pystatements')

    def __str__(self):
        return f"{NEWL.join(str(s) for s in self.pystatements)}"


class Call1(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.args = kwargs.pop('args')
        self.kwargs = kwargs.pop('kwargs')

    def __str__(self):
        kwargs = "" if len(self.kwargs)==0 else f",{','.join(str(a) for a in self.kwargs)}"
        return f"{self.name}({','.join(str(a) for a in self.args)}{kwargs})"


class Call0(object):
    def __init__(self, **kwargs):
        self.pyExpr = kwargs.pop('pyExpr')

    def __str__(self):
        return str(self.pyExpr)


class String(object):
    def __init__(self, **kwargs):
        self.literal = kwargs.pop('literal')

    def __str__(self):
        return f'{self.literal}'


class PyList(object):
    def __init__(self, **kwargs):
        self.elements = kwargs.pop('elements')

    def __str__(self):
        return f"[{','.join(str(e) for e in self.elements)}]"


class PyAssignment(object):
    def __init__(self, **kwargs):
        self.var = kwargs.pop('var')
        self.val = kwargs.pop('val')

    def __str__(self):
        return f'{self.var} = {self.val}'


########################################################################


dslFile = os.path.join(os.path.dirname(__file__), 'Idp.tx')

idpparser = metamodel_from_file(dslFile, memoization=True,
                                classes=[Idp, Annotations,

                                         Vocabulary, Extern,
                                         ConstructedTypeDeclaration,
                                         Constructor, RangeDeclaration,
                                         SymbolDeclaration, Symbol, Sort,

                                         Theory, Definition, Rule, IfExpr,
                                         AQuantification, ARImplication,
                                         AEquivalence, AImplication,
                                         ADisjunction, AConjunction,
                                         AComparison, ASumMinus, AMultDiv,
                                         APower, AUnary, AAggregate,
                                         AppliedSymbol, Variable,
                                         NumberConstant, Brackets, Arguments,

                                         Structure, Interpretation,
                                         Tuple, Goal, View, Display,

                                         Procedure, Call1, Call0, String, PyList, PyAssignment])
