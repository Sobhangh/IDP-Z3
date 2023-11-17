# Copyright 2019-2023 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of IDP-Z3.
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
from __future__ import annotations

from copy import copy, deepcopy
from itertools import chain
from typing import Union, List, NamedTuple, Optional
import string  # .digits

from .Parse import (IDP, Vocabulary, Import, TypeDeclaration, Declaration,
                    SymbolDeclaration, VarDeclaration, TheoryBlock, Definition,
                    Rule, Structure, SymbolInterpretation, Enumeration, Ranges,
                    FunctionEnum, TupleIDP, ConstructedFrom, Display)
from .Expression import (ASTNode, Expression, TYPE, Set_, BOOLT, INTT, REALT, DATET,
                         Constructor, CONSTRUCTOR, AIfExpr, IF,
                         AQuantification, Quantee, ARImplication, AImplication,
                         AEquivalence, Operator, AComparison, AUnary,
                         AAggregate, AppliedSymbol, UnappliedSymbol, Variable,
                         VARIABLE, Brackets, SymbolExpr, Number, NOT,
                         EQUALS, AND, OR, FALSE, ZERO, IMPLIES, FORALL, EXISTS)

from .utils import (BOOL, INT, REAL, DATE, CONCEPT, RESERVED_SYMBOLS,
                    OrderedSet, Semantics)

Exceptions = Union[Exception, List["Exceptions"]]  # nested list of Exceptions

Annotated = Expression
# class Annotated(NamedTuple):
#     node: Expression
#     wdf: Expression
#     warnings: Exceptions


# Class Vocabulary  #######################################################

def annotate_block(self: ASTNode,
                   idp: IDP,
                   ) -> Exceptions:
    assert isinstance(self, Vocabulary), "Internal error"
    self.idp = idp

    # process Import and determine the constructors of CONCEPT
    temp: dict[str, Declaration] = {}  # contains the new self.declarations
    for s in self.declarations:
        if isinstance(s, Import):
            other = self.idp.vocabularies[s.name]
            for s1 in other.declarations:
                if s1.name in temp:
                    s.check(str(temp[s1.name]) == str(s1),
                            f"Inconsistent declaration for {s1.name}")
                temp[s1.name] = s1
        else:
            s.block = self
            s.check(s.name not in temp or s.name in RESERVED_SYMBOLS,
                    f"Duplicate declaration of {s.name}")
            temp[s.name] = s
    temp[CONCEPT].constructors=([CONSTRUCTOR(f"`{s}")
                                 for s in [BOOL, INT, REAL, DATE, CONCEPT]]
                               +[CONSTRUCTOR(f"`{s.name}")
                                 for s in temp.values()
                                 if s.name not in RESERVED_SYMBOLS
                                 and type(s) in Declaration.__args__])
    self.declarations = list(temp.values())

    # annotate declarations
    for s in self.declarations:
        s.annotate_declaration(self)  # updates self.symbol_decls

    BOOLT.annotate(self, {})
    INTT.annotate(self, {})
    REALT.annotate(self, {})
    DATET.annotate(self, {})

    concepts = self.symbol_decls[CONCEPT]
    for constructor in concepts.constructors:
        constructor.symbol = (TYPE(constructor.name[1:])
                                .annotate(self, {}))

    # populate .map of CONCEPT
    for c in concepts.constructors:
        assert not c.sorts, "Internal error"
        concepts.map[str(c)] = UnappliedSymbol.construct(c)
    return []
Vocabulary.annotate_block = annotate_block


# Class TypeDeclaration  #######################################################

def annotate_declaration(self: ASTNode,
                         voc: Vocabulary,
                         ) -> ASTNode:
    assert isinstance(self, TypeDeclaration), "Internal error"
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc, {})
    self.out.annotate(voc, {})
    for c in self.constructors:
        c.type = self
        self.check(c.name not in voc.symbol_decls or self.name == CONCEPT,
                    f"duplicate '{c.name}' constructor for '{self.name}' type")
        voc.symbol_decls[c.name] = c
    if self.interpretation:
        self.interpretation.annotate(voc, {})
        base_decl = (self.name if type(self.interpretation.enumeration) != Ranges else
                        self.interpretation.enumeration.type.name)  # INT or REAL or DATE
        self.base_decl = voc.symbol_decls[base_decl]
    else:
        self.base_decl = self
    return self
TypeDeclaration.annotate_declaration = annotate_declaration


# Class SymbolDeclaration  #######################################################

def annotate_declaration(self: SymbolDeclaration,
                         voc: Vocabulary,
                         ) -> ASTNode:
    self.check(self.name is not None, "Internal error")
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc, {})
    self.out.annotate(voc, {})
    self.type = self.out

    for s in chain(self.sorts, [self.out]):
        self.check(s.name != CONCEPT or s == s, # use equality to check nested concepts
                   f"`Concept` must be qualified with a type signature in {self}")
    self.base_decl = (None if self.out != BOOLT or self.arity != 1 else
                      self.sorts[0].decl.base_decl)
    return self
SymbolDeclaration.annotate_declaration = annotate_declaration


# Class VarDeclaration  #######################################################

def annotate_declaration(self: ASTNode,
                         voc: Vocabulary,
                         ) -> ASTNode:
    assert isinstance(self, VarDeclaration), "Internal error"
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    self.check(self.name == self.name.rstrip(string.digits),
                f"Variable {self.name} cannot be declared with a digital suffix.")
    voc.symbol_decls[self.name] = self
    self.subtype.annotate(voc, {})
    return self
VarDeclaration.annotate_declaration = annotate_declaration


# Class Set_  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Set_), "Internal error"
    if self.name in q_vars:
        return q_vars[self.name]

    self.check(self.name in voc.symbol_decls,
               f'Undeclared symbol name: "{self.name}"')

    self.decl = voc.symbol_decls[self.name]
    self.variables = set()
    self.type = self.decl.type
    if self.out:
        self.ins = [s.annotate(voc, q_vars) for s in self.ins]
        self.out = self.out.annotate(voc, q_vars)
    return self
Set_.annotate = annotate


# Class TheoryBlock  #######################################################

def annotate_block(self: ASTNode,
                   idp: IDP,
                   ) -> Exceptions:
    out = []
    assert isinstance(self, TheoryBlock), "Internal error"
    self.check(self.vocab_name in idp.vocabularies,
                f"Unknown vocabulary: {self.vocab_name}")
    self.voc = idp.vocabularies[self.vocab_name]

    for i in self.interpretations.values():
        i.block = self
        i.annotate(self.voc, {})
    self.voc.add_voc_to_block(self)

    self.definitions = [e.annotate(self.voc, {}) for e in self.definitions]

    constraints = OrderedSet()
    for c in self.constraints:
        c1 = c.annotate(self.voc, {})
        c1.check(c1.type is None or c1.type == BOOLT,
                    f"{c.code} must be boolean")
        constraints.append(c1)
    self.constraints = constraints
    return out
TheoryBlock.annotate_block = annotate_block


# Class Definition  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Definition), "Internal error"
    self.rules = [r.annotate(voc, q_vars) for r in self.rules]

    # create level-mapping symbols, as needed
    # self.level_symbols: dict[SymbolDeclaration, Set_]
    dependencies = set()
    for r in self.rules:
        symbs: dict[str, SymbolDeclaration] = {}
        r.body.collect_symbols(symbs)
        for s in symbs.values():
            dependencies.add((r.definiendum.symbol.decl, s))

    while True:
        new_relations = set((x, w) for x, y in dependencies
                            for q, w in dependencies if q == y)
        closure_until_now = dependencies | new_relations
        if len(closure_until_now) == len(dependencies):
            break
        dependencies = closure_until_now

    # check for nested recursive symbols
    symbs = {s for (s, ss) in dependencies if s == ss}
    nested: set[SymbolDeclaration] = set()
    for r in self.rules:
        decl = r.definiendum.symbol.decl
        r.body.collect_nested_symbols(nested, False)
        if decl in symbs and decl not in self.inductive:
            self.inductive.add(decl)

    if self.mode == Semantics.RECDATA:
        # check that the variables in r.out are in the arguments of definiendum
        for r in self.rules:
            if r.out:
                args = set()
                for e in r.definiendum.sub_exprs:
                    for v in e.variables:
                        args.add(v)
                error = list(set(r.out.variables) - args)
                self.check(len(error) == 0,
                        f"Eliminate variable {error} in the head of : {r}")

    # check for nested recursive symbols
    nested = set()
    for r in self.rules:
        r.body.collect_nested_symbols(nested, False)
    for decl in self.inductive:
        self.check(decl not in nested,
                    f"Inductively defined nested symbols are not supported yet: "
                    f"{decl.name}.")
        if self.mode != Semantics.RECDATA:
            self.check(decl.out == BOOLT,
                        f"Inductively defined functions are not supported yet: "
                        f"{decl.name}.")

    # create common variables, and rename vars in rule
    self.canonicals = {}
    for r in self.rules:
        # create common variables
        decl = voc.symbol_decls[r.definiendum.decl.name]
        if decl.name not in self.def_vars:
            name = f"{decl.name}_"
            q_v = {f"{decl.name}{str(i)}_":
                    VARIABLE(f"{decl.name}{str(i)}_", sort)
                    for i, sort in enumerate(decl.sorts)}
            if decl.out != BOOLT:
                q_v[name] = VARIABLE(name, decl.out)
            self.def_vars[decl.name] = q_v

        # rename the variables in the arguments of the definiendum
        new_vars_dict = self.def_vars[decl.name]
        new_vars = list(new_vars_dict.values())
        renamed = deepcopy(r)

        vars = {var.name : var for q in renamed.quantees for vars in q.vars for var in vars}
        args = renamed.definiendum.sub_exprs + ([renamed.out] if r.out else [])
        r.check(len(args) == len(new_vars), "Internal error")

        for i in range(len(args)- (1 if r.out else 0)):  # without rule.out
            arg, nv = renamed.definiendum.sub_exprs[i], new_vars[i]
            if type(arg) == Variable \
            and arg.name in vars and arg.name not in new_vars_dict:  # a variable, but not repeated (and not a new variable name, by chance)
                del vars[arg.name]
                rename_args(renamed, {arg.name: nv})
            else:
                eq = EQUALS([nv, arg])
                renamed.body = AND([eq, renamed.body])

        canonical = deepcopy(renamed)

        inferred = renamed.body.type_inference(voc)
        for v in vars.values():
            renamed.body = EXISTS([Quantee.make(v, sort=v.type)
                                   .annotate_quantee(voc, {}, inferred)],
                                  renamed.body)
        self.renamed.setdefault(decl, []).append(renamed)

        # rename the variable for the value of the definiendum
        if r.out:  # now process r.out
            arg, nv = canonical.out, new_vars[-1]
            if type(arg) == Variable \
            and arg.name in vars and arg.name not in new_vars:  # a variable, but not repeated (and not a new variable name, by chance)
                del vars[arg.name]
                rename_args(canonical, {arg.name: nv})
            else:
                eq = EQUALS([nv, arg])
                canonical.body = AND([eq, canonical.body])

        inferred = canonical.body.type_inference(voc)
        for v in vars.values():
            canonical.body = EXISTS([Quantee.make(v, sort=v.type)
                                     .annotate_quantee(voc, {}, inferred)],
                                    canonical.body)

        canonical.definiendum.sub_exprs = new_vars[:-1] if r.out else new_vars
        canonical.out = new_vars[-1] if r.out else None
        canonical.quantees = [Quantee.make(v, sort=v.type) for v in new_vars]

        self.canonicals.setdefault(decl, []).append(canonical)

    # join the bodies of rules
    for decl, rules in self.canonicals.items():
        new_rule = copy(rules[0])
        exprs = [rule.body for rule in rules]
        new_rule.body = OR(exprs)
        self.clarks[decl] = new_rule
    return self
Definition.annotate = annotate


# Class Rule  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Rule), "Internal error"
    self.original = copy(self)
    self.check(self.definiendum.symbol.name,
                f"No support for intentional objects in the head of a rule: "
                f"{self}")
    # create head variables
    q_v = copy(q_vars)
    inferred = self.definiendum.type_inference(voc)
    inferred.update(self.body.type_inference(voc))
    for q in self.quantees:
        q.annotate_quantee(voc, q_vars, inferred)
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

def rename_args(self: Rule, subs: dict[str, Expression]):
    """replace old variables by new variables
        (ignoring arguments in the head before the it
    """
    self.body = self.body.interpret(None, subs)
    self.out = (self.out.interpret(None, subs) if self.out else
                self.out)
    args = self.definiendum.sub_exprs
    for j in range(0, len(args)):
        args[j] = args[j].interpret(None, subs)


# Class Structure  #######################################################

def annotate_block(self: ASTNode,
                   idp: IDP,
                   ) -> Exceptions:
    """
    Annotates the structure with the enumerations found in it.
    Every enumeration is converted into an assignment, which is added to
    `self.assignments`.

    :arg idp: a `Parse.IDP` object.
    :returns None:
    """
    assert isinstance(self, Structure), "Internal error"
    self.check(self.vocab_name in idp.vocabularies,
               f"Unknown vocabulary: {self.vocab_name}")
    self.voc = idp.vocabularies[self.vocab_name]
    for i in self.interpretations.values():
        i.block = self
        i.annotate(self.voc, {})
    self.voc.add_voc_to_block(self)
    return []
Structure.annotate_block = annotate_block


# Class SymbolInterpretation  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    """
    Annotate the symbol.

    :arg block: a Structure object
    :returns None:
    """
    assert isinstance(self, SymbolInterpretation), "Internal error"
    self.symbol = TYPE(self.name).annotate(voc, {})
    enumeration = self.enumeration  # shorthand

    # create constructors if it is a type enumeration
    self.is_type_enumeration = (type(self.symbol.decl) != SymbolDeclaration)
    if self.is_type_enumeration and enumeration.constructors:
        # create Constructors before annotating the tuples
        for c in enumeration.constructors:
            c.type = self.symbol
            self.check(c.name not in voc.symbol_decls,
                    f"duplicate '{c.name}' constructor for '{self.name}' symbol")
            voc.symbol_decls[c.name] = c  #TODO risk of side-effects => use local decls ? issue #81

    enumeration.annotate(voc, q_vars)

    self.check(self.is_type_enumeration
                or all(s not in [INTT, REALT, DATET]  # finite domain #TODO
                        for s in self.symbol.decl.sorts)
                or self.default is None,
        f"Can't use default value for '{self.name}' on infinite domain nor for type enumeration.")

    self.check(not(self.symbol.decl.out.decl.base_decl == BOOLT
                   and type(enumeration) == FunctionEnum),
        f"Can't use function enumeration for predicates '{self.name}' (yet)")

    # predicate enumeration have FALSE default
    if type(enumeration) != FunctionEnum and self.default is None:
        self.default = FALSE

    if self.default is not None:
        self.default = self.default.annotate(voc, {})
        self.check(self.default.is_value(),
                   f"Value for '{self.name}' may only use numerals,"
                   f" identifiers or constructors: '{self.default}'")
    return self
SymbolInterpretation.annotate = annotate


# Class Enumeration  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Enumeration), "Internal error"
    if self.tuples:
        for t in self.tuples:
            t.annotate(voc, q_vars)
    return self
Enumeration.annotate = annotate


# Class TupleIDP  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, TupleIDP), "Internal error"
    self.args = [arg.annotate(voc, q_vars) for arg in self.args]
    self.check(all(a.is_value() for a in self.args),
               f"Interpretation may only contain numerals,"
               f" identifiers or constructors: '{self}'")
    return self
TupleIDP.annotate = annotate


# Class ConstructedFrom  #######################################################

def annotate(self: ASTNode,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, ConstructedFrom), "Internal error"
    for c in self.constructors:
        for i, ts in enumerate(c.sorts):
            if not ts.accessor:
                ts.accessor = f"{c.name}_{i}"
            if ts.accessor in self.accessors:
                self.check(self.accessors[ts.accessor] == i,
                           "Accessors used at incompatible indices")
            else:
                self.accessors[ts.accessor] = i
        c.annotate(voc, q_vars)
    return self
ConstructedFrom.annotate = annotate


# Class Constructor  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Constructor), "Internal error"
    for a in self.sorts:
        self.check(a.out.name in voc.symbol_decls,
                   f"Unknown type: {a.out}" )
        a.decl = SymbolDeclaration.make(self,
            name=a.accessor, sorts=[self.type], out=a.out)
        a.decl.by_z3 = True
        a.decl.annotate_declaration(voc)
    self.tester = SymbolDeclaration.make(self,
            name=f"is_{self.name}", sorts=[self.type], out=BOOLT)
    self.tester.by_z3 = True
    self.tester.annotate_declaration(voc)
    return self
Constructor.annotate = annotate


# Class Display  #######################################################

def annotate_block(self: ASTNode,
                   idp: IDP,
                   ) -> Exceptions:
    assert isinstance(self, Display), "Internal error"
    self.voc = idp.vocabulary

    # add display predicates

    viewType = TypeDeclaration(self, name='_ViewType',
        constructors=[CONSTRUCTOR('normal'),
                        CONSTRUCTOR('expanded')])
    viewType.annotate_declaration(self.voc)

    # Check the AST for any constructors that belong to open types.
    # For now, the only open types are `unit` and `heading`.
    open_constructors = {'unit': [], 'heading': []}
    for constraint in self.constraints:
        constraint.generate_constructors(open_constructors)

    # Next, we convert the list of constructors to actual types.
    open_types: dict[str, Optional[Set_]] = {}
    for name, constructors in open_constructors.items():
        # If no constructors were found, then the type is not used.
        if not constructors:
            open_types[name] = None
            continue

        type_name = name.capitalize()  # e.g. type Unit (not unit)
        open_type = TypeDeclaration(self, name=type_name,
                                    constructors=constructors)
        open_type.annotate_declaration(self.voc)
        open_types[name] = TYPE(type_name)

    for name, out in [
        ('expand', BOOLT),
        ('hide', BOOLT),
        ('view', BOOLT),
        ('moveSymbols', BOOLT),
        ('optionalPropagation', BOOLT),
        ('manualPropagation', BOOLT),
        ('optionalRelevance', BOOLT),
        ('manualRelevance', BOOLT),
        ('unit', open_types['unit']),
        ('heading', open_types['heading']),
        ('noOptimization', BOOLT)
    ]:
        symbol_decl = SymbolDeclaration.make(self, name=name,
                                        sorts=[], out=out)
        symbol_decl.annotate_declaration(self.voc)

    # annotate constraints and interpretations
    for constraint in self.constraints:
        constraint.annotate(self.voc, {})
    for i in self.interpretations.values():
        i.block = self
        i.annotate(self.voc, {})
    return []
Display.annotate_block = annotate_block


# Class Expression  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    """annotate tree after parsing

    Resolve names and determine type as well as variables in the expression

    Args:
        voc (Vocabulary): the vocabulary
        q_vars (dict[str, Variable]): the quantifier variables that may appear in the expression

    Returns:
        Expression: an equivalent AST node, with updated type, .variables
    """
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    return self.set_variables()
Expression.annotate = annotate


def set_variables(self: Expression) -> Expression:
    " annotations that are common to __init__ and make() "
    self.variables = set()
    for e in self.sub_exprs:
        self.variables.update(e.variables)
    return self
Expression.set_variables = set_variables


# Class AIfExpr  #######################################################

def set_variables(self: AIfExpr) -> Expression:
    self.type = self.sub_exprs[AIfExpr.THEN].type
    if not self.type:
        self.type = self.sub_exprs[AIfExpr.ELSE].type
    return Expression.set_variables(self)
AIfExpr.set_variables = set_variables


# Class Quantee  #######################################################

def annotate_quantee(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable],
             inferred: dict[str, Set_]
             ) -> Annotated:
    assert isinstance(self, Quantee), "Internal error"
    Expression.annotate(self, voc, q_vars)
    for vars in self.vars:
        self.check(not self.sub_exprs
                   or not self.sub_exprs[0].decl
                   or len(vars)==len(self.sub_exprs[0].decl.sorts),
                    f"Incorrect arity for {self}")
        for i, var in enumerate(vars):
            self.check(var.name not in voc.symbol_decls
                        or type(voc.symbol_decls[var.name]) == VarDeclaration,
                f"the quantified variable '{var.name}' cannot have"
                f" the same name as another symbol")
            # 1. get variable sort from the quantee, if possible
            var.sort = (self.sub_exprs[0].decl.sorts[i]  # `!x in p` or `! (x,y) in p` or `!x in Concept[...]`
                        if self.sub_exprs and self.sub_exprs[0].decl
                        else None)
            # 2. compare with variable declaration, if any
            var_decl = voc.symbol_decls.get(var.name.rstrip(string.digits), None)
            if var_decl and type(var_decl) == VarDeclaration:
                subtype = var_decl.subtype
                if var.sort:
                    self.check(var.sort.name == subtype.name,
                        f"Can't use declared {var.name} as a "
                        f"{var.sort.name if var.sort else ''}")
                else:
                    self.sub_exprs = [subtype.annotate(voc, {})]
                    var.sort = self.sub_exprs[0]
            # 3. use type inference if still not found
            if var.sort is None:
                var.sort = inferred.get(var.name) if inferred else None
            var.type = var.sort
            q_vars[var.name] = var
    if not self.sub_exprs and var.sort:
        self.sub_exprs = [var.sort]
    return self
Quantee.annotate_quantee = annotate_quantee


# Class AQuantification  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    # also called by AAgregate.annotate
    assert isinstance(self, AQuantification) or isinstance(self, AAggregate), "Internal error"
    q_v = copy(q_vars)
    inferred = self.sub_exprs[0].type_inference(voc)
    for q in self.quantees:
        q.annotate_quantee(voc, q_v, inferred)  # adds inner variables to q_v
    self.sub_exprs = [e.annotate(voc, q_v) for e in self.sub_exprs]
    return self.set_variables()
AQuantification.annotate = annotate

def set_variables(self: AQuantification) -> Expression:
    Expression.set_variables(self)
    for q in self.quantees:  # remove declared variables
        for vs in q.vars:
            for v in vs:
                self.variables.discard(v.name)
    for q in self.quantees:  # add variables in sort expression
        for sort in q.sub_exprs:
            self.variables.update(sort.variables)
    return self
AQuantification.set_variables = set_variables


# Class Operator  #######################################################

def annotate(self: Operator,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self = Expression.annotate(self, voc, q_vars)

    for e in self.sub_exprs:
        if self.operator[0] in '&|∧∨⇒⇐⇔':
            self.check(e.type is None or e.type == BOOLT or e.str in ['true', 'false'],
                       f"Expected boolean formula, got {e.type}: {e}")
    return self
Operator.annotate = annotate

def set_variables(self: Operator) -> Expression:
    if self.type is None:  # not a BOOL operator
        self.type = REALT if any(e.type == REALT for e in self.sub_exprs) \
                else INTT if any(e.type == INTT for e in self.sub_exprs) \
                else DATET if any(e.type == DATET for e in self.sub_exprs) \
                else self.sub_exprs[0].type  # constructed type, without arithmetic
    return Expression.set_variables(self)
Operator.set_variables = set_variables


# Class AImplication  #######################################################

def set_variables(self: AImplication) -> Expression:
    self.check(len(self.sub_exprs) == 2,
               "Implication is not associative.  Please use parenthesis.")
    self.type = BOOLT
    return Expression.set_variables(self)
AImplication.set_variables = set_variables


# Class AEquivalence  #######################################################

def set_variables(self: AEquivalence) -> Expression:
    self.check(len(self.sub_exprs) == 2,
               "Equivalence is not associative.  Please use parenthesis.")
    self.type = BOOLT
    return Expression.set_variables(self)
AEquivalence.set_variables = set_variables

# Class ARImplication  #######################################################

def annotate(self: ARImplication,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    # reverse the implication
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    out = AImplication.make(ops=['⇒'], operands=list(reversed(list(self.sub_exprs))),
                        annotations=None, parent=self)
    out.original = self
    return out.annotate(voc, q_vars)
ARImplication.annotate = annotate


# Class AComparison  #######################################################

def annotate(self: AComparison,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    out = Operator.annotate(self, voc, q_vars)
    out.type = BOOLT

    for e in self.sub_exprs:
        if self.operator[0] in "<>≤≥" and e.type:
            decl = voc.symbol_decls.get(e.type.name, None)
            self.check(voc.symbol_decls[e.type.name].base_decl in [INTT, REALT, DATET]
                       or decl.type in [INTT, REALT, DATET]
                       or (hasattr(decl, 'interpretation')
                           and decl.interpretation is None)
                       or not hasattr(decl, 'enumeration')
                       or decl.enumeration is None,
                        f"Expected numeric formula, got {e.type}: {e}")

    # a≠b --> Not(a=b)
    if len(self.sub_exprs) == 2 and self.operator == ['≠']:
        out = NOT(EQUALS(self.sub_exprs))
    return out
AComparison.annotate = annotate


# Class AUnary  #######################################################

def set_variables(self: AUnary) -> Expression:
    if len(self.operators) % 2 == 0: # negation of negation
        return self.sub_exprs[0]
    self.type = self.sub_exprs[0].type
    return Expression.set_variables(self)
AUnary.set_variables = set_variables


# Class AAggregate  #######################################################

def annotate(self: AAggregate,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    if not self.annotated:

        self = AQuantification.annotate(self, voc, q_vars)

        if self.aggtype == "sum" and len(self.sub_exprs) == 2:
            self.original = copy(self)
            self.sub_exprs = [AIfExpr(self.parent, self.sub_exprs[1],
                                    self.sub_exprs[0], ZERO).set_variables()]

        if self.aggtype == "#":
            self.sub_exprs = [IF(self.sub_exprs[0], Number(number='1'),
                                 Number(number='0'))]
            self.type = INTT
        else:
            self.type = self.sub_exprs[0].type
            if self.aggtype in ["min", "max"]:
                # the `min` aggregate in `!y in T: min(lamda x in type: term(x,y) if cond(x,y))=0`
                # is replaced by `_*(y)` with the following co-constraint:
                #     !y in T: ( ?x in type: cond(x,y) & term(x) = _*(y)
                #                !x in type: cond(x,y) => term(x) =< _*(y).
                self.check(self.type, f"Can't infer type of {self}")
                name = "__" + self.str
                if name in voc.symbol_decls:
                    symbol_decl = voc.symbol_decls[name]
                    to_create = False
                else:
                    symbol_decl = SymbolDeclaration.make(self,
                        "__"+self.str, # name `__ *`
                        [TYPE(v.sort.code) for v in q_vars.values()],
                        self.type).annotate_declaration(voc)    # output_domain
                    to_create = True
                symbol = SymbolExpr.make(symbol_decl.name)
                applied = AppliedSymbol.make(symbol, q_vars.values())
                applied = applied.annotate(voc, q_vars)

                if to_create:
                    eq = EQUALS([deepcopy(applied), self.sub_exprs[0]])
                    if len(self.sub_exprs) == 2:
                        eq = AND([self.sub_exprs[1], eq])
                    coc1 = EXISTS(self.quantees, eq)

                    op = '≤' if self.aggtype == "min" else '≥'
                    comp = AComparison.make(op,
                                    deepcopy([applied, self.sub_exprs[0]]))
                    if len(self.sub_exprs) == 2:
                        comp = IMPLIES([self.sub_exprs[1], comp])
                    coc2 = FORALL(deepcopy(self.quantees), comp)

                    coc = AND([coc1, coc2])
                    inferred = coc.type_inference(voc)
                    quantees = [Quantee.make(v, sort=v.type)
                                .annotate_quantee(voc, {}, inferred)
                                for v in q_vars.values()]
                    applied.co_constraint = (
                        coc if not quantees else
                        FORALL(quantees, coc).annotate(voc, q_vars))
                    applied.co_constraint.annotations['reading'] = f"Calculation of {self.code}"
                return applied
        self.annotated = True
    return self
AAggregate.annotate = annotate
AAggregate.set_variables = AQuantification.set_variables


# Class AppliedSymbol  #######################################################

def annotate(self: AppliedSymbol,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.symbol = self.symbol.annotate(voc, q_vars)
    if self.symbol.decl:
        self.check(self.symbol.decl.arity == len(self.sub_exprs)
                   or self.symbol.decl.name in ['hide', 'unit', 'heading', 'noOptimization'],
            f"Incorrect number of arguments in {self}: "
            f"should be {self.symbol.decl.arity}")
    self.check((not self.symbol.decl or type(self.symbol.decl) != Constructor
                or 0 < self.symbol.decl.arity),
               f"Constructor `{self.symbol}` cannot be applied to argument(s)")
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    if self.in_enumeration:
        self.in_enumeration.annotate(voc, q_vars)
    out = self.set_variables()

    # move the negation out
    if 'not' in self.is_enumerated:
        out = AppliedSymbol.make(out.symbol, out.sub_exprs,
                                 is_enumerated='is enumerated')
        out = NOT(out)
    elif 'not' in self.is_enumeration:
        out = AppliedSymbol.make(out.symbol, out.sub_exprs,
                                 is_enumeration='in',
                                 in_enumeration=out.in_enumeration)
        out = NOT(out)
    return out
AppliedSymbol.annotate = annotate

def set_variables(self: AppliedSymbol) -> Expression:
    out = Expression.set_variables(self)
    out.symbol = out.symbol.set_variables()
    out.variables.update(out.symbol.variables)
    return out.simplify1()
AppliedSymbol.set_variables = set_variables


# Class SymbolExpr  #######################################################

def annotate(self: SymbolExpr,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.decl = voc.symbol_decls.get(self.name, None)
    out = Expression.annotate(self, voc, q_vars)
    return out.simplify1()
SymbolExpr.annotate = annotate


# Class Variable  #######################################################

def annotate(self: Variable,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.type = self.sort
    return self
Variable.annotate = annotate


# Class Number  #######################################################

def annotate(self: Number,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.decl = voc.symbol_decls[self.type.name]
    return self
Number.annotate = annotate


# Class UnappliedSymbol  #######################################################

def annotate(self: UnappliedSymbol,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    if self.name in q_vars:  # ignore VarDeclaration
        return q_vars[self.name]
    if self.name in voc.symbol_decls:
        self.decl = voc.symbol_decls[self.name]
        self.variables = set()
        self.check(type(self.decl) == Constructor,
                   f"{self} should be applied to arguments (or prefixed with a back-tick)")
        return self
    # elif self.name in voc.symbol_decls:  # in symbol_decls
    #     out = AppliedSymbol.make(self.s, self.sub_exprs)
    #     return out.annotate(voc, q_vars)
    # If this code is reached, an undefined symbol was present.
      # after considering it as a declared symbol
    self.check(self.name.rstrip(string.digits) in q_vars,
               f"Symbol not in vocabulary: {self}")
    return self
UnappliedSymbol.annotate = annotate


# Class Brackets  #######################################################

def set_variables(self: Brackets) -> Expression:
    if not self.annotations:
        return self.sub_exprs[0]  # remove the bracket
    self.type = self.sub_exprs[0].type
    if self.annotations['reading']:
        self.sub_exprs[0].annotations = self.annotations
    self.variables = self.sub_exprs[0].variables
    return self
Brackets.set_variables = set_variables


Done = True
