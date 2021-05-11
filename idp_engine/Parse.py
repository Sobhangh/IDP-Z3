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

Classes to parse an IDP-Z3 theory.

"""
__all__ = ["IDP", "Vocabulary", "Annotations", "Extern",
           "TypeDeclaration",
           "SymbolDeclaration", "Symbol", "Theory", "Definition",
           "Rule", "Structure", "Enumeration", "Tuple",
           "Display", "Procedure", ]

from copy import copy
from datetime import date
from enum import Enum
from itertools import groupby
from os import path
from re import findall
from sys import intern
from textx import metamodel_from_file
from typing import Dict, Union, Optional


from .Assignments import Assignments
from .Expression import (ASTNode, Constructor, Accessor, Symbol, SymbolExpr,
                         IfExpr, AQuantification, Quantee,
                         ARImplication, AEquivalence,
                         AImplication, ADisjunction, AConjunction,
                         AComparison, ASumMinus, AMultDiv, APower, AUnary,
                         AAggregate, AppliedSymbol, UnappliedSymbol,
                         Number, Brackets, Date,
                         Variable, TRUEC, FALSEC, TRUE, FALSE)
from .utils import (OrderedSet, NEWL, BOOL, INT, REAL, DATE, SYMBOL,
                    RELEVANT, ARITY, INPUT_DOMAIN, OUTPUT_DOMAIN, IDPZ3Error,
                    CO_CONSTR_RECURSION_DEPTH, MAX_QUANTIFIER_EXPANSION)


def str_to_IDP(atom, val_string):
    assert atom.type, "Internal error"
    if atom.type == BOOL:
        if val_string not in ['True', 'False']:
            raise IDPZ3Error(
                f"{atom.annotations['reading']} is not defined, and assumed false")
        out = (TRUE if val_string == 'True' else
               FALSE)
    elif atom.type == DATE:
        d = (date.fromordinal(eval(val_string)) if not val_string.startswith('#') else
             date.fromisoformat(val_string[1:]))
        out = Date(iso=f"#{d.isoformat()}")
    elif (hasattr(atom.decl.out.decl, 'map')
          and val_string in atom.decl.out.decl.map):  # constructor
        out = atom.decl.out.decl.map[val_string]
    else:  # could be fraction
        out = Number(number=str(eval(val_string.replace('?', ''))))
    return out


class ViewType(Enum):
    HIDDEN = "hidden"
    NORMAL = "normal"
    EXPANDED = "expanded"


class IDP(ASTNode):
    """The class of AST nodes representing an IDP-Z3 program.
    """
    def __init__(self, **kwargs):
        # log("parsing done")
        self.vocabularies = self.dedup_nodes(kwargs, 'vocabularies')
        self.theories = self.dedup_nodes(kwargs, 'theories')
        self.structures = self.dedup_nodes(kwargs, 'structures')
        self.display = kwargs.pop('display')
        self.procedures = self.dedup_nodes(kwargs, 'procedures')

        for voc in self.vocabularies.values():
            voc.annotate(self)
        for t in self.theories.values():
            t.annotate(self)
        for struct in self.structures.values():
            struct.annotate(self)

        # determine default vocabulary, theory, before annotating display
        self.vocabulary = next(iter(self.vocabularies.values()))
        self.theory = next(iter(self.theories    .values()))
        if self.display is None:
            self.display = Display(constraints=[])

    @classmethod
    def parse(cls, file_or_string):
        if path.exists(file_or_string):
            return idpparser.model_from_file(file_or_string)
        else:
            return idpparser.model_from_str(file_or_string)

    def get_blocks(self, blocks):
        names = blocks.split(",") if type(blocks) is str else blocks
        out = []
        for name in names:
            name = name.strip()  # remove spaces
            out.append(self.vocabularies[name] if name in self.vocabularies else
                       self.theories[name] if name in self.theories else
                       self.structures[name] if name in self.structures else
                       self.procedures[name] if name in self.procedures else
                       self.display if name == "Display" else
                       "")
        return out


################################ Vocabulary  ##############################


class Annotations(ASTNode):
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
                    arg = findall(pat, p[1])
                    l_symb = arg[0][1]
                    u_symb = arg[0][2]
                    l_bound = arg[1][1]
                    u_bound = arg[1][2]
                    slider_arg = {'lower_symbol': l_symb,
                                  'upper_symbol': u_symb,
                                  'lower_bound': l_bound,
                                  'upper_bound': u_bound}
                    return(p[0], slider_arg)
                except:  # could not parse the slider data
                    return (p[0], p[1])
            else:
                return ('reading', p[0])

        self.annotations = dict((pair(t) for t in self.annotations))


class Vocabulary(ASTNode):
    """The class of AST nodes representing a vocabulary block.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.declarations = kwargs.pop('declarations')
        self.idp = None  # parent object
        self.symbol_decls: Dict[str, Type] = {}

        self.name = 'V' if not self.name else self.name
        self.voc = self

        # expand multi-symbol declarations
        temp = []
        for decl in self.declarations:
            if not isinstance(decl, SymbolDeclaration):
                temp.append(decl)
            else:
                for symbol in decl.symbols:
                    new = copy(decl)  # shallow copy !
                    new.name = intern(symbol.name)
                    new.symbols = None
                    temp.append(new)
        self.declarations = temp

        # define built-in types: Bool, Int, Real, Symbols
        self.declarations = [
            TypeDeclaration(
                name=BOOL, constructors=[TRUEC, FALSEC]),
            TypeDeclaration(name=INT, enumeration=IntRange()),
            TypeDeclaration(name=REAL, enumeration=RealRange()),
            TypeDeclaration(name=DATE, enumeration=DateRange()),
            TypeDeclaration(
                name=SYMBOL,
                constructors=([Constructor(name=f"`{s}")
                               for s in [DATE,]]  # TODO '𝔹', 'ℤ', 'ℝ',
                             +[Constructor(name=f"`{s.name}")
                                for s in self.declarations
                                if type(s) == SymbolDeclaration
                                or type(s) in Type.__args__])),
            SymbolDeclaration(annotations='', name=Symbol(name=RELEVANT),
                                sorts=[], out=Symbol(name=BOOL)),
            SymbolDeclaration(annotations='', name=Symbol(name=ARITY),
                                sorts=[Symbol(name=SYMBOL)],
                                out=Symbol(name=INT)),
            SymbolDeclaration(annotations='', name=Symbol(name=INPUT_DOMAIN),
                                sorts=[Symbol(name=SYMBOL), Symbol(name=INT)],
                                out=Symbol(name=SYMBOL)),
            SymbolDeclaration(annotations='', name=Symbol(name=OUTPUT_DOMAIN),
                                sorts=[Symbol(name=SYMBOL)],
                                out=Symbol(name=SYMBOL))
            ] + self.declarations

    def __str__(self):
        return (f"vocabulary {{{NEWL}"
                f"{NEWL.join(str(i) for i in self.declarations)}"
                f"{NEWL}}}{NEWL}")

    def add_voc_to_block(self, block):
        """adds the enumerations in a vocabulary to a theory or structure block

        Args:
            block (Problem): the block to be updated
        """
        for s in self.declarations:
            block.check(s.name not in block.declarations,
                        f"Duplicate declaration of {self.name} "
                        f"in vocabulary and block {block.name}")
            block.declarations[s.name] = s
            if (type(s) == TypeDeclaration
                and s.interpretation
                and self.name != BOOL):
                block.check(s.name not in block.interpretations,
                            f"Duplicate enumeration of {self.name} "
                            f"in vocabulary and block {block.name}")
                block.interpretations[s.name] = s.interpretation


class Extern(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def __str__(self):
        return f"extern vocabulary {self.name}"


class TypeDeclaration(ASTNode):
    """AST node to represent `type <symbol> := <enumeration>`

    Args:
        name (string): name of the type

        arity (int): the number of arguments

        sorts (List[Symbol]): the types of the arguments

        out (Symbol): the Boolean Symbol

        type (string): Z3 type of an element of the type; same as `name`

        constructors ([Constructor]): list of constructors in the enumeration

        range ([Expression]): list of expressions of that type

        interpretation (SymbolInterpretation): the symbol interpretation

        translated (Z3): the translation of the type in Z3

        map (Dict[string, Expression]): a mapping from code to Expression in range
    """

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.constructors = ([] if 'constructors' not in kwargs else
                             kwargs.pop('constructors'))
        enumeration = (None if 'enumeration' not in kwargs else
                            kwargs.pop('enumeration'))

        self.arity = 1
        self.sorts = [Symbol(name=self.name)]
        self.out = Symbol(name=BOOL)
        self.type = (self.name if type(enumeration) != Ranges else
                     enumeration.type)  # INT or REAL or DATE

        self.translated = None
        self.range = None
        self.map = {}  # {String: constructor}

        self.interpretation = (None if enumeration is None else
            SymbolInterpretation(name=Symbol(name=self.name),
                                 enumeration=enumeration, default=None))

    def __str__(self):
        return (f"type {self.name} := "
                f"{{{','.join(map(str, self.constructors))}}}")

    def check_bounds(self, var):
        return self.interpretation.enumeration.contains([var], False)

    def is_subset_of(self, other):
        return self == other


class SymbolDeclaration(ASTNode):
    """The class of AST nodes representing an entry in the vocabulary,
    declaring one or more symbols.
    Multi-symbols declaration are replaced by single-symbol declarations
    before the annotate() stage.

    Attributes:
        annotations : the annotations given by the expert.

            `annotations['reading']` is the annotation
            giving the intended meaning of the expression (in English).

        symbols ([Symbol]): the symbols beind defined, before expansion

        name (string): the identifier of the symbol, after expansion of the node

        arity (int): the number of arguments

        sorts (List[Symbol]): the types of the arguments

        out (Symbol): the type of the symbol

        type (string): name of the Z3 type of an instance of the symbol

        domain (List): the list of possible tuples of arguments

        instances (Dict[string, Expression]):
            a mapping from the code of a symbol applied to a tuple of
            arguments to its parsed AST

        range (List[Expression]): the list of possible values

        unit (str):
            the unit of the symbol, such as m (meters)

        heading (str):
            the heading that the symbol should belong to
    """

    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')
        if 'symbols' in kwargs:
            self.symbols = kwargs.pop('symbols')
            self.name = None
        else:
            self.name = intern(kwargs.pop('name').name)
            self.symbols = None
        self.sorts = kwargs.pop('sorts')
        self.out = kwargs.pop('out')
        if self.out is None:
            self.out = Symbol(name=BOOL)

        self.arity = len(self.sorts)
        self.annotations = self.annotations.annotations if self.annotations else {}
        self.unit: str = None
        self.heading: str = None

        self.translated = None

        self.type = None  # a string
        self.domain = None  # all possible arguments
        self.range = None  # all possible values
        self.instances = None  # {string: AppliedSymbol} not starting with '_'
        self.block: Optional[Block] = None  # vocabulary where it is declared
        self.view = ViewType.NORMAL  # "hidden" | "normal" | "expanded" whether the symbol box should show atoms that contain that symbol, by default

    def __str__(self):
        args = ','.join(map(str, self.sorts)) if 0 < len(self.sorts) else ''
        return (f"{self.name}"
                f"{ '('+args+')' if args else ''}"
                f"{'' if self.out.name == BOOL else f' : {self.out.name}'}")

    def is_subset_of(self, other):
        return (self.arity == 1 and self.type == BOOL
                and self.sorts[0].decl == other)


Type = Union[TypeDeclaration, SymbolDeclaration]


################################ Theory  ###############################


class Theory(ASTNode):
    """ The class of AST nodes representing a theory block.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.vocab_name = kwargs.pop('vocab_name')
        self.constraints = OrderedSet(kwargs.pop('constraints'))
        self.definitions = kwargs.pop('definitions')
        self.interpretations = self.dedup_nodes(kwargs, 'interpretations')
        self.goals = {}

        self.name = "T" if not self.name else self.name
        self.vocab_name = 'V' if not self.vocab_name else self.vocab_name

        self.declarations = {}
        self.clark = {}  # {(Declaration, Definition): Rule}
        self.def_constraints = {}  # {Declaration: Expression}
        self.assignments = Assignments()

        for constraint in self.constraints:
            constraint.block = self
        for definition in self.definitions:
            for rule in definition.rules:
                rule.block = self

    def __str__(self):
        return self.name


class Definition(ASTNode):
    """ The class of AST nodes representing an inductive definition.
        id (num): unique identifier for each definition

        rules ([Rule]): set of rules for the definition

        clarks ({Declaration: Transformed Rule}): normalized rule for each defined symbol (used to be Clark completion)

        def_vars ({String: {String: Variable}}): Fresh variables for arguments and result
    """
    definition_id = 0  # intentional static variable so that no two definitions get the same ID

    def __init__(self, **kwargs):
        Definition.definition_id += 1
        self.id = Definition.definition_id
        self.rules = kwargs.pop('rules')
        self.clarks = {}  # {Declaration: Transformed Rule}
        self.def_vars = {}  # {String: {String: Variable}}

    def __str__(self):
        return "Definition(s) of " + ",".join([k.name for k in self.clarks.keys()])

    def __repr__(self):
        out = []
        for rule in self.clarks.values():
            out.append(repr(rule))
        return NEWL.join(out)

    def __eq__(self, another):
        return self.id == another.id

    def __hash__(self):
        return hash(self.id)

class Rule(ASTNode):
    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')
        self.quantees = kwargs.pop('quantees')
        self.definiendum = kwargs.pop('definiendum')
        self.out = kwargs.pop('out')
        self.body = kwargs.pop('body')
        self.is_whole_domain = None  # Bool
        self.whole_domain = None  # Expression
        self.block = None  # theory where it occurs
        self.cache = {}
        self.inst_def_level = 0

        self.annotations = self.annotations.annotations if self.annotations else {}

        if self.out is not None:
            self.definiendum.sub_exprs.append(self.out)
        if self.body is None:
            self.body = TRUE

    def __repr__(self):
        return (f"Rule:∀{','.join(str(q) for q in self.quantees)}: "
                f"{self.definiendum} "
                f"⇔{str(self.body)}")

    def rename_args(self, new_vars):
        """ for Clark's completion
            input : '!v: f(args) <- body(args)'
            output: '!nv: f(nv) <- nv=args & body(args)' """

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

    def instantiate_definition(self, new_args, theory):
        """Create an instance of the definition for new_args, and interpret it for theory.

        Args:
            new_args ([Expression]): tuple of arguments to be applied to the defined symbol
            theory (Problem): the context for the interpretation

        Returns:
            Expression: a boolean expression
        """
        key = str(new_args)
        if key in self.cache:
            return self.cache[key]

        self.inst_def_level += 1
        if self.inst_def_level > CO_CONSTR_RECURSION_DEPTH:
            return None

        self.cache[key] = None  # avoid recursive loops
        # assert self.is_whole_domain == False
        out = self.body.copy()  # in case there are no arguments
        instance = AppliedSymbol.make(self.definiendum.symbol, new_args)
        instance.in_head = True
        if self.definiendum.decl.type == BOOL:  # a predicate
            self.check(len(self.definiendum.sub_exprs) == len(new_args),
                       "Internal error")
            out = out.instantiate(self.definiendum.sub_exprs, new_args, theory)
            out = AEquivalence.make('⇔', [instance, out])
        else:
            self.check(len(self.definiendum.sub_exprs) == len(new_args)+1 ,
                       "Internal error")
            out = out.instantiate(self.definiendum.sub_exprs,
                                  new_args+[instance], theory)
        out.block = self.block
        out = out.interpret(theory)
        self.cache[key] = out
        self.inst_def_level -= 1
        return out


# Expressions : see Expression.py

################################ Structure  ###############################

class Structure(ASTNode):
    """
    The class of AST nodes representing an structure block.
    """
    def __init__(self, **kwargs):
        """
        The textx parser creates the Structure object. All information used in
        this method directly comes from text.
        """
        self.name = kwargs.pop('name')
        self.vocab_name = kwargs.pop('vocab_name')
        self.interpretations = self.dedup_nodes(kwargs, 'interpretations')
        self.goals = {}

        self.name = 'S' if not self.name else self.name
        self.vocab_name = 'V' if not self.vocab_name else self.vocab_name

        self.voc = None
        self.declarations = {}
        self.assignments = Assignments()

    def __str__(self):
        return self.name


class SymbolInterpretation(ASTNode):
    """
    AST node representing `<symbol> := { <identifiers*> } else <default>`

    Attributes:
        name (string): name of the symbol being enumerated.

        symbol (Symbol): symbol being enumerated

        enumeration ([Enumeration]): enumeration.

        default (Expression): default value (for function enumeration).

        is_type_enumeration (Bool): True if the enumeration is for a type symbol.

    """
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name').name
        self.enumeration = kwargs.pop('enumeration')
        self.default = kwargs.pop('default')

        if not self.enumeration:
            self.enumeration = Enumeration(tuples=[])

        self.symbol = None
        self.is_type_enumeration = None

    def interpret_application(self, theory, rank, applied, args, tuples=None):
        """ returns the interpretation of self applied to args """
        tuples = list(self.enumeration.tuples) if tuples == None else tuples
        if rank == self.symbol.decl.arity:  # valid tuple -> return a value
            if not type(self.enumeration) == FunctionEnum:
                return TRUE if tuples else self.default
            else:
                self.check(len(tuples) <= 1,
                           f"Duplicate values in structure "
                           f"for {str(self.name)}{str(tuples[0])}")
                return (self.default if not tuples else  # enumeration of constant
                        tuples[0].args[rank])
        else:  # constructs If-then-else recursively
            out = (self.default if self.default is not None else
                   applied._change(sub_exprs=args))
            groups = groupby(tuples, key=lambda t: str(t.args[rank]))

            if args[rank].value is not None:
                for val, tuples2 in groups:  # try to resolve
                    if str(args[rank]) == val:
                        out = self.interpret_application(theory, rank+1,
                                        applied, args, list(tuples2))
            else:
                for val, tuples2 in groups:
                    tuples = list(tuples2)
                    out = IfExpr.make(
                        AComparison.make('=', [args[rank], tuples[0].args[rank]]),
                        self.interpret_application(theory, rank+1,
                                                   applied, args, tuples),
                        out)
            return out


class Enumeration(ASTNode):
    """Represents an enumeration of tuples of expressions.
    Used for predicates, or types without n-ary constructors.

    Attributes:
        tuples (OrderedSet[Tuple]): OrderedSet of Tuple of Expression

        constructors (List[Constructor], optional): List of Constructor
    """
    def __init__(self, **kwargs):
        self.tuples = kwargs.pop('tuples')
        if not isinstance(self.tuples, OrderedSet):
            # self.tuples.sort(key=lambda t: t.code)
            self.tuples = OrderedSet(self.tuples)
        if all(len(c.args) == 1 and type(c.args[0]) == UnappliedSymbol
               for c in self.tuples):
            self.constructors = [Constructor(name=c.args[0].name)
                                 for c in self.tuples]
        else:
            self.constructors = None

    def __repr__(self):
        return ", ".join([repr(t) for t in self.tuples])

    def contains(self, args, function, arity=None, rank=0, tuples=None):
        """ returns an Expression that says whether Tuple args is in the enumeration """

        if arity is None:
            arity = len(args)
        if rank == arity:  # valid tuple
            return TRUE
        if tuples is None:
            tuples = self.tuples
            self.check(all(len(t.args)==arity+(1 if function else 0)
                           for t in tuples),
                "Incorrect arity of tuples in Enumeration.  Please check use of ',' and ';'.")

        # constructs If-then-else recursively
        groups = groupby(tuples, key=lambda t: str(t.args[rank]))
        if args[rank].value is not None:
            for val, tuples2 in groups:  # try to resolve
                if str(args[rank]) == val:
                    return self.contains(args, function, arity, rank+1, list(tuples2))
            return FALSE
        else:
            if rank + 1 == arity:  # use OR
                out = [ AComparison.make('=', [args[rank], t.args[rank]])
                        for t in tuples]
                out = ADisjunction.make('∨', out)
                out.enumerated = ', '.join(str(c) for c in tuples)
                return out
            out = FALSE
            for val, tuples2 in groups:
                tuples = list(tuples2)
                out = IfExpr.make(
                    AComparison.make('=', [args[rank], tuples[0].args[rank]]),
                    self.contains(args, function, arity, rank+1, tuples),
                    out)
            return out

class FunctionEnum(Enumeration):
    pass

class CSVEnumeration(Enumeration):
    pass

class ConstructedFrom(Enumeration):
    """Represents a 'constructed from' enumeration of constructors

    Attributes:
        tuples (OrderedSet[Tuple]): OrderedSet of tuples of Expression

        constructors (List[Constructor]): List of Constructor
    """
    def __init__(self, **kwargs):
        self.constructed = kwargs.pop('constructed')
        self.constructors = kwargs.pop('constructors')
        self.tuples = None

class Tuple(ASTNode):
    def __init__(self, **kwargs):
        self.args = kwargs.pop('args')
        self.code = intern(",".join([str(a) for a in self.args]))

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code

    def translate(self):
        return [arg.translate() for arg in self.args]

class FunctionTuple(Tuple):
    def __init__(self, **kwargs):
        self.args = kwargs.pop('args')
        if not isinstance(self.args, list):
            self.args = [self.args]
        self.value = kwargs.pop('value')
        self.args.append(self.value)
        self.code = intern(",".join([str(a) for a in self.args]))

class CSVTuple(Tuple):
    pass

class Ranges(Enumeration):
    def __init__(self, **kwargs):
        self.elements = kwargs.pop('elements')

        tuples = []
        self.type = None
        for x in self.elements:
            if self.type == None:
                self.type = x.fromI.type
            if x.toI is None:
                tuples.append(Tuple(args=[x.fromI]))
            elif x.fromI.type == INT and x.toI.type == INT:
                for i in range(x.fromI.py_value, x.toI.py_value + 1):
                    tuples.append(Tuple(args=[Number(number=str(i))]))
            elif x.fromI.type == DATE and x.toI.type == DATE:
                for i in range(x.fromI.py_value, x.toI.py_value + 1):
                    tuples.append(Tuple(args=[Number(number=str(i))])) #TODO1
            else:
                self.check(False, f"Can't have a range over reals")
        Enumeration.__init__(self, tuples=tuples)

    def contains(self, args, function, arity=None, rank=0, tuples=None):
        var = args[0]
        if not self.elements:
            return None
        if self.tuples and len(self.tuples) < MAX_QUANTIFIER_EXPANSION:
            es = [AComparison.make('=', [var, c.args[0]]) for c in self.tuples]
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

class IntRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, elements=[])
        self.type = INT

class RealRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, elements=[])
        self.type = REAL

class DateRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, elements=[])
        self.type = DATE

################################ Display  ###############################

class Display(ASTNode):
    def __init__(self, **kwargs):
        self.constraints = kwargs.pop('constraints')
        self.moveSymbols = False
        self.optionalPropagation = False
        self.manualPropagation = False
        self.name = "display"

    def run(self, idp):
        for constraint in self.constraints:
            if type(constraint) == AppliedSymbol:
                self.check(type(constraint.symbol.sub_exprs[0]) == Symbol,
                           f"Invalid syntax: {constraint}")
                name = constraint.symbol.sub_exprs[0].name
                symbols = []
                # All arguments should be symbols, except for the first
                # argument of 'unit' and 'heading'.
                for i, symbol in enumerate(constraint.sub_exprs):
                    if name in ['unit', 'heading'] and i == 0:
                        continue
                    self.check(symbol.name.startswith('`'),
                        f"arg '{symbol.name}' of {name}'"
                        f" must begin with a tick '`'")
                    self.check(symbol.name[1:] in self.voc.symbol_decls,
                        f"argument '{symbol.name}' of '{name}'"
                        f" must be a symbol")
                    symbols.append(self.voc.symbol_decls[symbol.name[1:]])

                if name == 'goal':  # e.g.,  goal(Prime)
                    for s in symbols:
                        idp.theory.goals[s.name] = s
                        s.view = ViewType.EXPANDED  # the goal is always expanded
                elif name == 'expand':  # e.g. expand(Length, Angle)
                    for symbol in symbols:
                        self.voc.symbol_decls[symbol.name].view = ViewType.EXPANDED
                elif name == 'hide':  # e.g. hide(Length, Angle)
                    for symbol in symbols:
                        self.voc.symbol_decls[symbol.name].view = ViewType.HIDDEN
                elif name == 'relevant':  # e.g. relevant(Tax)
                    for s in symbols:
                        idp.theory.goals[s.name] = s
                elif name == 'unit':  # e.g. unit('m', `length):
                    for symbol in symbols:
                        symbol.unit = str(constraint.sub_exprs[0])
                elif name == 'heading':
                    # e.g. heading('Shape', `type).
                    for symbol in symbols:
                        symbol.heading = str(constraint.sub_exprs[0])
                elif name == "moveSymbols":
                    self.moveSymbols = True
                elif name == "optionalPropagation":
                    self.optionalPropagation = True
                elif name == "manualPropagation":
                    self.manualPropagation = True
                else:
                    raise IDPZ3Error(f"unknown display constraint:"
                                     f" {constraint}")
            elif type(constraint) == AComparison:  # e.g. view = normal
                self.check(constraint.is_assignment(), "Internal error")
                self.check(type(constraint.sub_exprs[0].symbol.sub_exprs[0]) == Symbol,
                           f"Invalid syntax: {constraint}")
                if constraint.sub_exprs[0].symbol.sub_exprs[0].name == 'view':
                    if constraint.sub_exprs[1].name == 'expanded':
                        for s in self.voc.symbol_decls.values():
                            if type(s) == SymbolDeclaration and s.view == ViewType.NORMAL:
                                s.view = ViewType.EXPANDED  # don't change hidden symbols
                    else:
                        self.check(constraint.sub_exprs[1].name == 'normal',
                                   f"unknown display constraint: {constraint}")
            else:
                raise IDPZ3Error(f"unknown display contraint: {constraint}")


################################ Main  ##################################

class Procedure(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.args = kwargs.pop('args')
        self.pystatements = kwargs.pop('pystatements')

    def __str__(self):
        return f"{NEWL.join(str(s) for s in self.pystatements)}"


class Call1(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.args = kwargs.pop('args')
        self.kwargs = kwargs.pop('kwargs')
        self.post = kwargs.pop('post')

    def __str__(self):
        kwargs = ("" if len(self.kwargs)==0 else
                  f"{',' if self.args else ''}{','.join(str(a) for a in self.kwargs)}")
        return ( f"{self.name}({','.join(str(a) for a in self.args)}{kwargs})"
                 f"{'' if self.post is None else '.'+str(self.post)}")


class Call0(ASTNode):
    def __init__(self, **kwargs):
        self.pyExpr = kwargs.pop('pyExpr')

    def __str__(self):
        return str(self.pyExpr)


class String(ASTNode):
    def __init__(self, **kwargs):
        self.literal = kwargs.pop('literal')

    def __str__(self):
        return f'{self.literal}'


class PyList(ASTNode):
    def __init__(self, **kwargs):
        self.elements = kwargs.pop('elements')

    def __str__(self):
        return f"[{','.join(str(e) for e in self.elements)}]"


class PyAssignment(ASTNode):
    def __init__(self, **kwargs):
        self.var = kwargs.pop('var')
        self.val = kwargs.pop('val')

    def __str__(self):
        return f'{self.var} = {self.val}'


########################################################################

Block = Union[Vocabulary, Theory, Structure, Display]

dslFile = path.join(path.dirname(__file__), 'Idp.tx')

idpparser = metamodel_from_file(dslFile, memoization=True,
                                classes=[IDP, Annotations,

                                         Vocabulary, Extern,
                                         TypeDeclaration, Accessor,
                                         SymbolDeclaration, Symbol,
                                         SymbolExpr,

                                         Theory, Definition, Rule, IfExpr,
                                         AQuantification, Quantee, ARImplication,
                                         AEquivalence, AImplication,
                                         ADisjunction, AConjunction,
                                         AComparison, ASumMinus, AMultDiv,
                                         APower, AUnary, AAggregate,
                                         AppliedSymbol, UnappliedSymbol,
                                         Number, Brackets, Date, Variable,

                                         Structure, SymbolInterpretation,
                                         Enumeration, FunctionEnum, CSVEnumeration,
                                         Tuple, FunctionTuple, CSVTuple,
                                         ConstructedFrom, Constructor, Ranges,
                                         Display,

                                         Procedure, Call1, Call0, String,
                                         PyList, PyAssignment])
