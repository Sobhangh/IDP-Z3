

from copy import copy

from .Parse import (Vocabulary, Extern, ConstructedTypeDeclaration,
                    RangeDeclaration, SymbolDeclaration, Sort, Symbol,
                    Theory, Definition, Rule,
                    Structure, SymbolInterpretation, Enumeration, FunctionEnum,
                    Tuple, Display)
from .Expression import (Constructor, AConjunction, ADisjunction, Variable, TRUE, FALSE)

from .utils import BOOL, INT, REAL, SYMBOL, OrderedSet, IDPZ3Error


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
Vocabulary.annotate = annotate


# Class Extern  #######################################################

def annotate(self, voc):
    other = voc.idp.vocabularies[self.name]
    #TODO merge while respecting order
    voc.symbol_decls = {**other.symbol_decls, **voc.symbol_decls}
Extern.annotate = annotate


# Class ConstructedTypeDeclaration  #######################################################

def annotate(self, voc):
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for c in self.constructors:
        c.type = self.name
        self.check(c.name not in voc.symbol_decls or self.name == SYMBOL,
                    f"duplicate constructor in vocabulary: {c.name}")
        voc.symbol_decls[c.name] = c
    self.range = self.constructors  # TODO constructor functions
    if self.interpretation:
        self.interpretation.annotate(voc)
ConstructedTypeDeclaration.annotate = annotate


# Class RangeDeclaration  #######################################################

def annotate(self, voc):
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
RangeDeclaration.annotate = annotate


# Class SymbolDeclaration  #######################################################

def annotate(self, voc):
    self.voc = voc
    self.check(self.name is not None, "Internal error")
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc)
    self.out.annotate(voc)
    self.type = self.out.decl.name
    return self
SymbolDeclaration.annotate = annotate


# Class Sort  #######################################################

def annotate(self, voc):
    self.decl = voc.symbol_decls[self.name]
Sort.annotate = annotate


# Class Symbol  #######################################################

def annotate(self, voc, q_vars):
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
    # squash multiple definitions of same symbol declaration
    for d in self.definitions:
        for decl, rule in d.clarks.items():
            if decl in self.clark:
                new_rule = copy(rule)  # not elegant, but rare
                new_rule.body = AConjunction.make('∧', [self.clark[decl].body, rule.body])
                new_rule.block = rule.block
                self.clark[decl] = new_rule
            else:
                self.clark[decl] = rule

    self.constraints = OrderedSet([e.annotate(self.voc, {})
                                    for e in self.constraints])
    self.constraints = OrderedSet([e.interpret(self)
                                    for e in self.constraints])
Theory.annotate = annotate


# Class Definition  #######################################################

def annotate(self, theory, voc, q_vars):
    self.rules = [r.annotate(voc, q_vars) for r in self.rules]

    # create common variables, and rename vars in rule
    self.clarks = {}
    for r in self.rules:
        decl = voc.symbol_decls[r.symbol.name]
        if decl.name not in self.def_vars:
            name = f"${decl.name}$"
            q_v = {f"${decl.name}!{str(i)}$":
                    Variable(f"${decl.name}!{str(i)}$", sort)
                    for i, sort in enumerate(decl.sorts)}
            if decl.out.name != BOOL:
                q_v[name] = Variable(name, decl.out)
            self.def_vars[decl.name] = q_v
        new_rule = r.rename_args(self.def_vars[decl.name])
        self.clarks.setdefault(decl, []).append(new_rule)

    # join the bodies of rules
    for decl, rules in self.clarks.items():
        exprs = sum(([rule.body] for rule in rules), [])
        rules[0].body = ADisjunction.make('∨', exprs)
        self.clarks[decl] = rules[0]
    return self
Definition.annotate = annotate


# Class Rule  #######################################################

def annotate(self, voc, q_vars):
    # create head variables
    self.check(len(self.vars) == len(self.sorts), "Internal error")
    for v, s in zip(self.vars, self.sorts):
        if s:
            s.annotate(voc)
        self.q_vars[v] = Variable(v,s)
    q_v = {**q_vars, **self.q_vars}  # merge

    self.symbol = self.symbol.annotate(voc, q_v)
    self.args = [arg.annotate(voc, q_v) for arg in self.args]
    self.out = self.out.annotate(voc, q_v) if self.out else self.out
    self.body = self.body.annotate(voc, q_v)
    return self
Rule.annotate = annotate


# Class Structure  #######################################################

def annotate(self, idp):
    """
    Annotates the structure with the enumerations found in it.
    Every enumeration is converted into an assignment, which is added to
    `self.assignments`.

    :arg idp: a `Parse.Idp` object.
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
    if self.is_type_enumeration:
        for i, c in enumerate(self.enumeration.tuples):
            self.check(len(c.args) == 1,
                        f"incorrect arity in {self.name} type enumeration")
            constr = Constructor(name=c.args[0].name)
            constr.type = self.name
            if self.name != BOOL:
                constr.py_value = i  # to allow comparisons
            self.check(constr.name not in voc.symbol_decls,
                    f"duplicate constructor in vocabulary: {constr.name}")
            voc.symbol_decls[constr.name] = constr

    self.enumeration.annotate(voc)

    # predicate enumeration have FALSE default
    if type(self.enumeration) != FunctionEnum and self.default is None:
        self.default = FALSE
    self.check(self.is_type_enumeration
                or all(s.name not in [INT, REAL]  # finite domain
                        for s in self.symbol.decl.sorts)
                or self.default is None,
        f"Can't use default value for '{self.name}' on infinite domain.")
    if self.default is not None:
        self.default = self.default.annotate(voc, {})
        self.check(self.default.as_rigid() is not None,
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
    self.check(all(a.as_rigid() is not None for a in self.args),
                f"Tuple must be ground : ({self})")
Tuple.annotate = annotate


# Class Display  #######################################################

def annotate(self, idp):
    self.voc = idp.vocabulary

    # add display predicates

    viewType = ConstructedTypeDeclaration(name='View',
        constructors=[Constructor(name='normal'),
                        Constructor(name='expanded')])
    viewType.annotate(self.voc)

    # Check the AST for any constructors that belong to open types.
    # For now, the only open types are `unit` and `category`.
    open_constructors = {'unit': [], 'category': []}
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
        open_type = ConstructedTypeDeclaration(name=type_name,
                                                constructors=constructors)
        open_type.annotate(self.voc)
        open_types[name] = Sort(name=type_name)

    for name, out in [
        ('goal', Sort(name=BOOL)),
        ('expand', Sort(name=BOOL)),
        ('relevant', Sort(name=BOOL)),
        ('hide', Sort(name=BOOL)),
        ('view', Sort(name='View')),
        ('moveSymbols', Sort(name=BOOL)),
        ('optionalPropagation', Sort(name=BOOL)),
        ('unit', open_types['unit']),
        ('category', open_types['category'])
    ]:
        symbol_decl = SymbolDeclaration(annotations='',
                                        name=Symbol(name=name),
                                        sorts=[], out=out)
        symbol_decl.annotate(self.voc)

    # annotate constraints
    for constraint in self.constraints:
        constraint.annotate(self.voc, {})
Display.annotate = annotate


Done = True