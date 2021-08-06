# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

Methods to annotate the Abstract Syntax Tree (AST) of an IDP-Z3 program.

"""

from copy import copy

from .Parse import (Vocabulary, Extern, TypeDeclaration,
                    SymbolDeclaration, Symbol,
                    Theory, Definition, Rule,
                    Structure, SymbolInterpretation, Enumeration, FunctionEnum,
                    Tuple, ConstructedFrom, Display)
from .Expression import (Expression, Constructor, IfExpr, AQuantification, Quantee,
                         ARImplication, AImplication, AEquivalence, ADisjunction,
                         AConjunction, Operator, AComparison, AUnary, AAggregate,
                         AppliedSymbol, UnappliedSymbol, Variable, Brackets,
                         FALSE, SymbolExpr, Number)

from .utils import (BOOL, INT, REAL, DATE, SYMBOL, OrderedSet, IDPZ3Error,
                    DEF_SEMANTICS, Semantics)


# Class Vocabulary  #######################################################

def annotate(self, idp):
    self.idp = idp

    # annotate declarations
    for s in self.declarations:
        s.block = self
        s.annotate(self)  # updates self.symbol_decls

    for constructor in self.symbol_decls[SYMBOL].constructors:
        constructor.symbol = (Symbol(name=constructor.name[1:])
                                .annotate(self, {}))
    self.symbol_decls[SYMBOL].translate()  # to populate .map
Vocabulary.annotate = annotate


# Class Extern  #######################################################

def annotate(self, voc):
    other = voc.idp.vocabularies[self.name]
    #TODO merge while respecting order
    voc.symbol_decls = {**other.symbol_decls, **voc.symbol_decls}
Extern.annotate = annotate


# Class TypeDeclaration  #######################################################

def annotate(self, voc):
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc, {})
    self.out.annotate(voc, {})
    for c in self.constructors:
        c.type = self.name
        self.check(c.name not in voc.symbol_decls or self.name == SYMBOL,
                    f"duplicate '{c.name}' constructor for '{self.name}' type")
        voc.symbol_decls[c.name] = c
    if self.interpretation:
        self.interpretation.annotate(voc)
TypeDeclaration.annotate = annotate


# Class SymbolDeclaration  #######################################################

def annotate(self, voc):
    self.voc = voc
    self.check(self.name is not None, "Internal error")
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc, {})
    self.out.annotate(voc, {})
    self.type = self.out.decl.name
    return self
SymbolDeclaration.annotate = annotate


# Class Symbol  #######################################################

def annotate(self, voc, q_vars):
    if self.name in q_vars:
        return q_vars[self.name]
    self.decl = voc.symbol_decls[self.name]
    self.type = self.decl.type
    return self
Symbol.annotate = annotate


# Class Theory  #######################################################

def annotate(self, idp):
    self.check(self.vocab_name in idp.vocabularies,
                f"Unknown vocabulary: {self.vocab_name}")
    self.voc = idp.vocabularies[self.vocab_name]

    for i in self.interpretations.values():
        i.annotate(self)
    self.voc.add_voc_to_block(self)

    self.definitions = [e.annotate(self, self.voc, {}) for e in self.definitions]

    self.constraints = OrderedSet([e.annotate(self.voc, {})
                                    for e in self.constraints])
Theory.annotate = annotate


# Class Definition  #######################################################

def annotate(self, theory, voc, q_vars):
    self.rules = [r.annotate(voc, q_vars) for r in self.rules]
    self.set_level_symbols()

    # create common variables, and rename vars in rule
    self.canonicals = {}
    for r in self.rules:
        decl = voc.symbol_decls[r.definiendum.decl.name]
        if decl.name not in self.def_vars:
            name = f"${decl.name}$"
            q_v = {f"${decl.name}!{str(i)}$":
                    Variable(name=f"${decl.name}!{str(i)}$", sort=sort)
                    for i, sort in enumerate(decl.sorts)}
            if decl.out.name != BOOL:
                q_v[name] = Variable(name=name, sort=decl.out)
            self.def_vars[decl.name] = q_v
        new_rule = r.rename_args(self.def_vars[decl.name])
        self.canonicals.setdefault(decl, []).append(new_rule)

    # join the bodies of rules
    for decl, rules in self.canonicals.items():
        new_rule = copy(rules[0])
        exprs = [rule.body for rule in rules]
        new_rule.body = ADisjunction.make('∨', exprs)
        self.clarks[decl] = new_rule
    return self
Definition.annotate = annotate

def get_instantiables(self, for_explain=False):
    """ compute Definition.instantiables, with level-mapping if definition is inductive

    Uses implications instead of equivalence if `for_explain` is True

    Example: `{ p() <- q(). p() <- r().}`
    Result when not for_explain: `p() <=> q() | r()`
    Result when for_explain    : `p() <= q(). p() <= r(). p() => (q() | r()).`

    Args:
        for_explain (Bool):
            Use implications instead of equivalence, for rule-specific explanations
    """
    result = {}
    for decl, rules in self.canonicals.items():
        rule = rules[0]
        rule.is_whole_domain = all(s.decl.range  # not None nor []
                               for s in rule.definiendum.decl.sorts)
        if not rule.is_whole_domain:
            self.check(rule.definiendum.symbol.decl not in self.level_symbols,
                       f"Cannot have inductive definitions on infinite domain")
        else:
            if rule.out:
                expr = AppliedSymbol.make(rule.definiendum.symbol,
                                        rule.definiendum.sub_exprs[:-1])
                expr.in_head = True
                head = AComparison.make('=', [expr, rule.definiendum.sub_exprs[-1]])
            else:
                head = AppliedSymbol.make(rule.definiendum.symbol,
                                        rule.definiendum.sub_exprs)
                head.in_head = True

            inductive = (not rule.out and DEF_SEMANTICS != Semantics.COMPLETION
                and rule.definiendum.symbol.decl in rule.parent.level_symbols)

            # determine reverse implications, if any
            bodies, out = [], []
            for r in rules:
                if not inductive:
                    bodies.append(r.body)
                    if for_explain and 1 < len(rules):  # not simplified -> no need to make copies
                        out.append(ARImplication.make('⇐', [head, r.body],
                                                      r.annotations))
                else:
                    new = r.body.split_equivalences()
                    bodies.append(new)
                    if for_explain:
                        new = new.copy().add_level_mapping(rule.parent.level_symbols,
                                             rule.definiendum, False, False)
                        out.append(ARImplication.make('⇐', [head, new],
                                                      r.annotations))

            all_bodies = ADisjunction.make('∨', bodies)
            if not inductive:
                if out:  # already contains reverse implications
                    out.append(ARImplication.make('⇒', [head, all_bodies],
                                                  self.annotations))
                else:
                    out = [AEquivalence.make('⇔', [head, all_bodies],
                                             self.annotations)]
            else:
                if not out:  # no reverse implication yet
                    new = all_bodies.copy().add_level_mapping(rule.parent.level_symbols,
                                             rule.definiendum, False, False)
                    out = [ARImplication.make('⇐', [head.copy(), new],
                                              self.annotations)]
                all_bodies = all_bodies.copy().add_level_mapping(rule.parent.level_symbols,
                                        rule.definiendum, True, True)
                out.append(AImplication.make('⇒', [head, all_bodies],
                                             self.annotations))
            result[decl] = out
    return result
Definition.get_instantiables = get_instantiables


# Class Rule  #######################################################

def annotate(self, voc, q_vars):
    self.check(not self.definiendum.symbol.is_intentional(),
                f"No support for intentional objects in the head of a rule: "
                f"{self}")
    # create head variables
    q_v = {**q_vars}  # copy
    for q in self.quantees:
        q.annotate(voc, q_vars)
        for vars in q.vars:
            for var in vars:
                var.sort = q.sub_exprs[0] if q.sub_exprs else None
                q_v[var.name] = var

    self.definiendum = self.definiendum.annotate(voc, q_v)
    self.body = self.body.annotate(voc, q_v)
    if self.out:
        self.out = self.out.annotate(voc, q_v)

    return self
Rule.annotate = annotate

def rename_args(self, new_vars):
    """ for Clark's completion
        input : '!v: f(args) <- body(args)'
        output: '!nv: f(nv) <- nv=args & body(args)'
    """
    self.check(len(self.definiendum.sub_exprs) == len(new_vars), "Internal error")
    vars = [var.name for q in self.quantees for vars in q.vars for var in vars]
    for i in range(len(self.definiendum.sub_exprs)):
        arg, nv = self.definiendum.sub_exprs[i], list(new_vars.values())[i]
        if type(arg) == Variable \
        and arg.name in vars and arg.name not in new_vars:
            self.body = self.body.instantiate([arg], [nv])
            self.out = (self.out.instantiate([arg], [nv]) if self.out else
                        self.out)
            for j in range(i, len(self.definiendum.sub_exprs)):
                self.definiendum.sub_exprs[j] = \
                    self.definiendum.sub_exprs[j].instantiate([arg], [nv])
        else:
            eq = AComparison.make('=', [nv, arg])
            self.body = AConjunction.make('∧', [eq, self.body])

    self.definiendum.sub_exprs = list(new_vars.values())
    self.quantees = [Quantee.make(v, v.sort) for v in new_vars.values()]
    return self
Rule.rename_args = rename_args


# Class Structure  #######################################################

def annotate(self, idp):
    """
    Annotates the structure with the enumerations found in it.
    Every enumeration is converted into an assignment, which is added to
    `self.assignments`.

    :arg idp: a `Parse.IDP` object.
    :returns None:
    """
    if self.vocab_name not in idp.vocabularies:
        raise IDPZ3Error(f"Unknown vocabulary: {self.vocab_name}")
    self.voc = idp.vocabularies[self.vocab_name]
    for i in self.interpretations.values():
        i.annotate(self)
    self.voc.add_voc_to_block(self)
Structure.annotate = annotate


# Class SymbolInterpretation  #######################################################

def annotate(self, block):
    """
    Annotate the symbol.

    :arg block: a Structure object
    :returns None:
    """
    voc = block.voc
    self.block = block
    self.symbol = Symbol(name=self.name).annotate(voc, {})

    # create constructors if it is a type enumeration
    self.is_type_enumeration = (type(self.symbol.decl) != SymbolDeclaration)
    if self.is_type_enumeration and self.enumeration.constructors:
        # create Constructors before annotating the tuples
        for c in self.enumeration.constructors:
            c.type = self.name
            self.check(c.name not in voc.symbol_decls,
                    f"duplicate '{c.name}' constructor for '{self.name}' symbol")
            voc.symbol_decls[c.name] = c  #TODO risk of side-effects => use local decls ? issue #81

    self.enumeration.annotate(voc)

    # predicate enumeration have FALSE default
    if type(self.enumeration) != FunctionEnum and self.default is None:
        self.default = FALSE
    self.check(self.is_type_enumeration
                or all(s.name not in [INT, REAL, DATE]  # finite domain
                        for s in self.symbol.decl.sorts)
                or self.default is None,
        f"Can't use default value for '{self.name}' on infinite domain nor for type enumeration.")
    if self.default is not None:
        self.default = self.default.annotate(voc, {})
        self.check(self.default.value is not None,
            f"Default value for '{self.name}' must be ground: {self.default}")
SymbolInterpretation.annotate = annotate


# Class Enumeration  #######################################################

def annotate(self, voc):
    for t in self.tuples:
        t.annotate(voc)
Enumeration.annotate = annotate


# Class Tuple  #######################################################

def annotate(self, voc):
    self.args = [arg.annotate(voc, {}) for arg in self.args]
    self.check(all(a.value is not None for a in self.args),
                f"Tuple must be ground : ({self})")
Tuple.annotate = annotate


# Class ConstructedFrom  #######################################################

def annotate(self, voc):
    for c in self.constructors:
        for i, ts in enumerate(c.sorts):
            if ts.accessor is None:
                ts.accessor = Symbol(name=f"{c.name}_{i}")
            if ts.accessor.name in self.accessors:
                self.check(self.accessors[ts.accessor.name] == i,
                           "Accessors used at incompatible indices")
            else:
                self.accessors[ts.accessor.name] = i
        c.annotate(voc)
ConstructedFrom.annotate = annotate


# Class Constructor  #######################################################

def annotate(self, voc):
    for a in self.sorts:
        self.check(a.type in voc.symbol_decls,
                   f"Unknown type: {a.type}" )
        a.decl = SymbolDeclaration(annotations='', name=a.accessor,
                                   sorts=[Symbol(name=self.type)],
                                   out=Symbol(name=a.type))
        a.decl.annotate(voc)
    self.tester = SymbolDeclaration(annotations='',
                                    name=Symbol(name=f"is_{self.name}"),
                                    sorts=[Symbol(name=self.type)],
                                    out=Symbol(name=BOOL))
    self.tester.annotate(voc)
Constructor.annotate = annotate


# Class Display  #######################################################

def annotate(self, idp):
    self.voc = idp.vocabulary

    # add display predicates

    viewType = TypeDeclaration(name='_ViewType',
        constructors=[Constructor(name='normal'),
                        Constructor(name='expanded')])
    viewType.annotate(self.voc)

    # Check the AST for any constructors that belong to open types.
    # For now, the only open types are `unit` and `heading`.
    open_constructors = {'unit': [], 'heading': []}
    for constraint in self.constraints:
        constraint.generate_constructors(open_constructors)

    # Next, we convert the list of constructors to actual types.
    open_types = {}
    for name, constructors in open_constructors.items():
        # If no constructors were found, then the type is not used.
        if not constructors:
            open_types[name] = None
            continue

        type_name = name.capitalize()  # e.g. type Unit (not unit)
        open_type = TypeDeclaration(name=type_name,
                                    constructors=constructors)
        open_type.annotate(self.voc)
        open_types[name] = Symbol(name=type_name)

    for name, out in [
        ('goal', Symbol(name=BOOL)),
        ('expand', Symbol(name=BOOL)),
        ('relevant', Symbol(name=BOOL)),
        ('hide', Symbol(name=BOOL)),
        ('view', Symbol(name='_ViewType')),
        ('moveSymbols', Symbol(name=BOOL)),
        ('optionalPropagation', Symbol(name=BOOL)),
        ('manualPropagation', Symbol(name=BOOL)),
        ('unit', open_types['unit']),
        ('heading', open_types['heading'])
    ]:
        symbol_decl = SymbolDeclaration(annotations='',
                                        name=Symbol(name=name),
                                        sorts=[], out=out)
        symbol_decl.annotate(self.voc)

    # annotate constraints
    for constraint in self.constraints:
        constraint.annotate(self.voc, {})
Display.annotate = annotate


# Class Expression  #######################################################

def annotate(self, voc, q_vars):
    " annotate tree after parsing "
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    return self.annotate1()
Expression.annotate = annotate


def annotate1(self):
    " annotations that are common to __init__ and make() "
    self.fresh_vars = set()
    if self.value is not None:
        pass
    if self.simpler is not None:
        self.fresh_vars = self.simpler.fresh_vars
    else:
        for e in self.sub_exprs:
            self.fresh_vars.update(e.fresh_vars)
    return self
Expression.annotate1 = annotate1


# Class IfExpr  #######################################################

def annotate1(self):
    self.type = self.sub_exprs[IfExpr.THEN].type
    return Expression.annotate1(self)
IfExpr.annotate1 = annotate1


# Class AQuantification  #######################################################

def annotate(self, voc, q_vars):
    # also called by AAgregate.annotate
    q_v = {**q_vars}  # copy
    for q in self.quantees:
        q.annotate(voc, q_vars)
        for vars in q.vars:
            for var in vars:
                self.check(var.name not in voc.symbol_decls,
                    f"the quantified variable '{var.name}' cannot have"
                    f" the same name as another symbol")
                var.sort = q.sub_exprs[0] if q.sub_exprs else None
                q_v[var.name] = var
    self.sub_exprs = [e.annotate(voc, q_v) for e in self.sub_exprs]
    return self.annotate1()
AQuantification.annotate = annotate

def annotate1(self):
    Expression.annotate1(self)
    for q in self.quantees:  # remove declared variables
        for vs in q.vars:
            for v in vs:
                self.fresh_vars.discard(v.name)
    for q in self.quantees:  # add variables in sort expression
        for sort in q.sub_exprs:
            self.fresh_vars.update(sort.fresh_vars)
    return self
AQuantification.annotate1 = annotate1


# Class Operator  #######################################################

def annotate1(self):
    if self.type is None:
        self.type = REAL if any(e.type == REAL for e in self.sub_exprs) \
                else INT if any(e.type == INT for e in self.sub_exprs) \
                else self.sub_exprs[0].type  # constructed type, without arithmetic
    return Expression.annotate1(self)
Operator.annotate1 = annotate1


# Class AImplication  #######################################################

def annotate1(self):
    self.check(len(self.sub_exprs) == 2,
               "Implication is not associative.  Please use parenthesis.")
    self.type = BOOL
    return Expression.annotate1(self)
AImplication.annotate1 = annotate1


# Class AImplication, AEquivalence  #######################################################

def annotate1(self):
    self.check(len(self.sub_exprs) == 2,
               "Equivalence is not associative.  Please use parenthesis.")
    self.type = BOOL
    return Expression.annotate1(self)
AEquivalence.annotate1 = annotate1

# Class ARImplication  #######################################################

def annotate(self, voc, q_vars):
    # reverse the implication
    self.sub_exprs.reverse()
    out = AImplication(sub_exprs=self.sub_exprs,
                        operator=['⇒']*len(self.operator))
    if hasattr(self, "block"):
        out.block = self.block
    return out.annotate(voc, q_vars)
ARImplication.annotate = annotate


# Class AComparison  #######################################################

def annotate(self, voc, q_vars):
    out = Operator.annotate(self, voc, q_vars)
    out.type = BOOL
    # a≠b --> Not(a=b)
    if len(self.sub_exprs) == 2 and self.operator == ['≠']:
        out = AUnary.make('¬', AComparison.make('=', self.sub_exprs))
    return out
AComparison.annotate = annotate


# Class AUnary  #######################################################

def annotate1(self):
    if len(self.operators) % 2 == 0: # negation of negation
        return self.sub_exprs[0]
    self.type = self.sub_exprs[0].type
    return Expression.annotate1(self)
AUnary.annotate1 = annotate1


# Class AAggregate  #######################################################

def annotate(self, voc, q_vars):
    self = AQuantification.annotate(self, voc, q_vars)
    self.type = self.sub_exprs[AAggregate.OUT].type if self.out else INT

    assert not self.using_if, f"Internal error in Aggregate: {self}"
    self.sub_exprs = [IfExpr.make(if_f=self.sub_exprs[AAggregate.CONDITION],
            then_f=Number(number='1') if self.out is None else
                    self.sub_exprs[AAggregate.OUT],
            else_f=Number(number='0'))]
    self.using_if = True
    return self
AAggregate.annotate = annotate
AAggregate.annotate1 = AQuantification.annotate1


# Class AppliedSymbol  #######################################################

def annotate(self, voc, q_vars):
    self.symbol = self.symbol.annotate(voc, q_vars)
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    if self.in_enumeration:
        self.in_enumeration.annotate(voc)
    out = self.annotate1()

    # move the negation out
    if 'not' in self.is_enumerated:
        out = AppliedSymbol.make(out.symbol, out.sub_exprs,
                                 is_enumerated='is enumerated')
        out = AUnary.make('¬', out)
    elif 'not' in self.is_enumeration:
        out = AppliedSymbol.make(out.symbol, out.sub_exprs,
                                 is_enumeration='in',
                                 in_enumeration=out.in_enumeration)
        out = AUnary.make('¬', out)
    return out
AppliedSymbol.annotate = annotate

def annotate1(self):
    out = Expression.annotate1(self)
    out.symbol = out.symbol.annotate1()
    out.fresh_vars.update(out.symbol.fresh_vars)
    return out.simplify1()
AppliedSymbol.annotate1 = annotate1


# Class SymbolExpr  #######################################################

def annotate(self, voc, q_vars):
    out = Expression.annotate(self, voc, q_vars)
    return out.simplify1()
SymbolExpr.annotate = annotate


# Class Variable  #######################################################

def annotate(self, voc, q_vars):
    self.type = self.sort.decl.name if self.sort and self.sort.decl else ''
    return self
Variable.annotate = annotate


# Class UnappliedSymbol  #######################################################

def annotate(self, voc, q_vars):
    if self.name in voc.symbol_decls:
        self.decl = voc.symbol_decls[self.name]
        self.fresh_vars = {}
        self.check(type(self.decl) == Constructor,
                   f"{self} should be applied to arguments (or prefixed with a back-tick)")
        return self
    if self.name in q_vars:
        return q_vars[self.name]
    # elif self.name in voc.symbol_decls:  # in symbol_decls
    #     out = AppliedSymbol.make(self.s, self.sub_exprs)
    #     return out.annotate(voc, q_vars)
    # If this code is reached, an undefined symbol was present.
    self.check(False, f"Symbol not in vocabulary: {self}")
UnappliedSymbol.annotate = annotate


# Class Brackets  #######################################################

def annotate1(self):
    if not self.annotations:
        return self.sub_exprs[0]  # remove the bracket
    self.type = self.sub_exprs[0].type
    if self.annotations['reading']:
        self.sub_exprs[0].annotations = self.annotations
    self.fresh_vars = self.sub_exprs[0].fresh_vars
    return self
Brackets.annotate1 = annotate1


Done = True
