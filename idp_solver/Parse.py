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
__all__ = ["Idp", "Vocabulary", "Annotations", "Extern",
           "ConstructedTypeDeclaration", "RangeDeclaration",
           "SymbolDeclaration", "Sort", "Symbol", "Theory", "Definition",
           "Rule", "Structure", "Enumeration", "Tuple",
           "Display", "Procedure", "idpparser", ]

from copy import copy
from enum import Enum
from itertools import groupby
from os import path
from re import findall
from sys import intern
from textx import metamodel_from_file
from typing import Dict, Union, Optional


from .Assignments import Assignments
from .Expression import (ASTNode, Constructor, IfExpr, AQuantification,
                         ARImplication, AEquivalence,
                         AImplication, ADisjunction, AConjunction,
                         AComparison, ASumMinus, AMultDiv, APower, AUnary,
                         AAggregate, AppliedSymbol, UnappliedSymbol,
                         Number, Brackets, Arguments,
                         Variable, TRUE, FALSE)
from .utils import (unquote, OrderedSet, NEWL, BOOL, INT, REAL, SYMBOL, IDPZ3Error)


def str_to_IDP(atom, val_string):
    if atom.type == BOOL:
        if val_string not in ['True', 'False']:
            raise IDPZ3Error(
                f"{atom.annotations['reading']} is not defined, and assumed false")
        out = (TRUE if val_string == 'True' else
               FALSE)
    elif (atom.type in [REAL, INT] or
            type(atom.decl.out.decl) == RangeDeclaration):  # could be fraction
        out = Number(number=str(eval(val_string.replace('?', ''))))
    else:  # constructor
        out = atom.decl.out.decl.map[val_string]
    return out


class ViewType(Enum):
    HIDDEN = "hidden"
    NORMAL = "normal"
    EXPANDED = "expanded"


class Idp(ASTNode):
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
            ConstructedTypeDeclaration(
                name=BOOL, constructors=[TRUE, FALSE]),
            RangeDeclaration(name=INT, elements=[]),
            RangeDeclaration(name=REAL, elements=[]),
            ConstructedTypeDeclaration(
                name=SYMBOL,
                constructors=[Constructor(name=f"`{s.name}")
                              for s in self.declarations
                              if type(s) == SymbolDeclaration]),
            SymbolDeclaration(annotations='', name=Symbol(name='__relevant'),
                                    sorts=[], out=Sort(name=BOOL)),
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
            if (type(s) == ConstructedTypeDeclaration
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


class ConstructedTypeDeclaration(ASTNode):
    """AST node to represent `type <symbol> := <enumeration>`

    Args:
        name (string): name of the type

        constructors ([Constructor]): list of constructors in the enumeration

        interpretation (SymbolInterpretation): the symbol interpretation

        translated (Z3): the translation of the type in Z3

        map (Dict[string, Constructor]): a mapping from code to Expression
    """

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.constructors = ([] if 'constructors' not in kwargs else
                             kwargs.pop('constructors'))
        enumeration = (None if 'enumeration' not in kwargs else
                            kwargs.pop('enumeration'))
        self.translated = None
        self.map = {}  # {String: constructor}
        self.type = None

        self.interpretation = (None if not enumeration else
            SymbolInterpretation(name=Symbol(name=self.name),
                                 enumeration=enumeration, default=None))

    def __str__(self):
        return (f"type {self.name} := "
                f"{{{','.join(map(str, self.constructors))}}}")

    def check_bounds(self, var):
        if self.name == BOOL:
            out = [var, AUnary.make('¬', var)]
        else:
            out = [AComparison.make('=', [var, c]) for c in self.constructors]
        out = ADisjunction.make('∨', out)
        return out


class RangeDeclaration(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')  # maybe INT, REAL
        self.elements = kwargs.pop('elements')
        self.translated = None
        self.constructors = None  # not used

        self.type = REAL if self.name == REAL else INT
        self.range = []
        for x in self.elements:
            if x.toI is None:
                self.range.append(x.fromI)
                if x.fromI.type != INT:
                    self.type = REAL
            elif x.fromI.type == INT and x.toI.type == INT:
                for i in range(x.fromI.py_value, x.toI.py_value + 1):
                    self.range.append(Number(number=str(i)))
            else:
                self.check(False, f"Can't have a range over reals: {self.name}")

    def __str__(self):
        elements = ";".join([str(x.fromI) + ("" if x.toI is None else ".." +
                                             str(x.toI)) for x in self.elements])
        return f"type {self.name} = {{{elements}}}"

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

        sorts (List[Sort]): the types of the arguments

        out : the type of the symbol

        type (string): the name of the type of the symbol

        arity (int): the number of arguments

        domain (List): the list of possible tuples of arguments

        instances (Dict[string, Expression]):
            a mapping from the code of a symbol applied to a tuple of
            arguments to its parsed AST

        range (List[Expression]): the list of possible values

        unit (str):
            the unit of the symbol, such as m (meters)

        category (str):
            the category that the symbol should belong to
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
            self.out = Sort(name=BOOL)

        self.arity = len(self.sorts)
        self.annotations = self.annotations.annotations if self.annotations else {}
        self.unit: str = None
        self.category: str = None

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


class Sort(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.name = (BOOL if self.name == '𝔹' else
                     INT if self.name == 'ℤ' else
                     REAL if self.name == 'ℝ' else
                     self.name
        )
        self.code = intern(self.name)
        self.decl = None

    def __str__(self):
        return ('𝔹' if self.name == BOOL else
                'ℤ' if self.name == INT else
                'ℝ' if self.name == REAL else
                self.name
        )

    def translate(self):
        return self.decl.translate()


class Symbol(ASTNode):
    def __init__(self, **kwargs):
        self.name = unquote(kwargs.pop('name'))

    def __str__(self): return self.name


Type = Union[RangeDeclaration, ConstructedTypeDeclaration, SymbolDeclaration]


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
        self.clark = {}  # {Declaration: Rule}
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
    def __init__(self, **kwargs):
        self.rules = kwargs.pop('rules')
        self.clarks = None  # {Declaration: Transformed Rule}
        self.def_vars = {}  # {String: {String: Variable}} Fresh variables for arguments & result

    def __str__(self):
        return "Definition(s) of " + ",".join([k.name for k in self.clark.keys()])

    def __repr__(self):
        out = []
        for rule in self.clarks.values():
            out.append(repr(rule))
        return NEWL.join(out)


class Rule(ASTNode):
    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')
        self.quantees = kwargs.pop('quantees')
        self.symbol = kwargs.pop('symbol')
        self.args = kwargs.pop('args')  # later augmented with self.out, if any
        self.out = kwargs.pop('out')
        self.body = kwargs.pop('body')
        self.expanded = None  # Expression
        self.block = None  # theory where it occurs

        self.vars, self.sorts = [], []
        for q in self.quantees:
            self.vars.append(q.var)
            self.sorts.append(q.sort)
        self.annotations = self.annotations.annotations if self.annotations else {}

        self.check(len(self.vars) == len(self.sorts), "Internal error")
        self.q_vars = {}  # {string: Variable}
        self.args = [] if self.args is None else self.args.sub_exprs
        if self.out is not None:
            self.args.append(self.out)
        if self.body is None:
            self.body = TRUE

    def __repr__(self):
        return (f"Rule:∀{','.join(f'{str(v)}[{str(s)}]' for v, s in zip(self.vars,self.sorts))}: "
                f"{self.symbol}({','.join(str(e) for e in self.args)}) "
                f"⇔{str(self.body)}")

    def rename_args(self, new_vars):
        """ for Clark's completion
            input : '!v: f(args) <- body(args)'
            output: '!nv: f(nv) <- nv=args & body(args)' """

        self.check(len(self.args) == len(new_vars), "Internal error")
        for i in range(len(self.args)):
            arg, nv = self.args[i],  list(new_vars.values())[i]
            if type(arg) == Variable \
            and arg.name in self.vars and arg.name not in new_vars:
                self.body = self.body.instantiate(arg, nv)
                self.out = self.out.instantiate(arg, nv) if self.out else self.out
                for j in range(i, len(self.args)):
                    self.args[j] = self.args[j].instantiate(arg, nv)
            else:
                eq = AComparison.make('=', [nv, arg])
                self.body = AConjunction.make('∧', [eq, self.body])

        self.args = list(new_vars.values())
        self.vars = list(new_vars.keys())
        self.sorts = [v.sort for v in new_vars.values()]
        self.q_vars = new_vars
        return self

    def instantiate_definition(self, new_args, theory):
        out = self.body.copy() # in case there is no arguments
        self.check(len(new_args) == len(self.args)
                   or len(new_args)+1 == len(self.args), "Internal error")
        for old, new in zip(self.args, new_args):
            out = out.instantiate(old, new)
        out = out.interpret(theory)  # add justification recursively
        instance = AppliedSymbol.make(self.symbol, new_args)
        if self.symbol.decl.type != BOOL:  # a function
            out = out.instantiate(self.args[-1], instance)
        else:
            out = AEquivalence.make('⇔', [instance, out])
        out.block = self.block
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
        tuples = self.enumeration.tuples if tuples == None else list(tuples)
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

            if type(args[rank]) in [Constructor, Number]:
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
    def __init__(self, **kwargs):
        self.tuples = kwargs.pop('tuples')
        if not isinstance(self.tuples, OrderedSet):
            # self.tuples.sort(key=lambda t: t.code)
            self.tuples = OrderedSet(self.tuples)

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
        if args[rank].as_rigid() is not None:
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


################################ Display  ###############################

class Display(ASTNode):
    def __init__(self, **kwargs):
        self.constraints = kwargs.pop('constraints')
        self.moveSymbols = False
        self.optionalPropagation = False
        self.name = "display"

    def run(self, idp):
        for constraint in self.constraints:
            if type(constraint) == AppliedSymbol:
                symbols = []
                # All arguments should be symbols, except for the first
                # argument of 'unit' and 'category'.
                for i, symbol in enumerate(constraint.sub_exprs):
                    if constraint.name in ['unit', 'category'] and i == 0:
                        continue
                    self.check(symbol.name.startswith('`'),
                        f"arg '{symbol.name}' of {constraint.name}'"
                        f" must begin with a tick '`'")
                    self.check(symbol.name[1:] in self.voc.symbol_decls,
                        f"argument '{symbol.name}' of '{constraint.name}'"
                        f" must be a symbol")
                    symbols.append(self.voc.symbol_decls[symbol.name[1:]])

                if constraint.name == 'goal':  # e.g.,  goal(Prime)
                    for s in symbols:
                        idp.theory.goals[s.name] = s
                        s.view = ViewType.EXPANDED  # the goal is always expanded
                elif constraint.name == 'expand':  # e.g. expand(Length, Angle)
                    for symbol in symbols:
                        self.voc.symbol_decls[symbol.name].view = ViewType.EXPANDED
                elif constraint.name == 'hide':  # e.g. hide(Length, Angle)
                    for symbol in symbols:
                        self.voc.symbol_decls[symbol.name].view = ViewType.HIDDEN
                elif constraint.name == 'relevant':  # e.g. relevant(Tax)
                    for s in symbols:
                        idp.theory.goals[s.name] = s
                elif constraint.name == 'unit':  # e.g. unit('m', `length):
                    for symbol in symbols:
                        symbol.unit = str(constraint.sub_exprs[0])
                elif constraint.name == 'category':
                    # e.g. category('Shape', `type).
                    for symbol in symbols:
                        symbol.category = str(constraint.sub_exprs[0])
            elif type(constraint) == AComparison:  # e.g. view = normal
                self.check(constraint.is_assignment(), "Internal error")
                if constraint.sub_exprs[0].name == 'view':
                    if constraint.sub_exprs[1].name == 'expanded':
                        for s in self.voc.symbol_decls.values():
                            if type(s) == SymbolDeclaration and s.view == ViewType.NORMAL:
                                s.view = ViewType.EXPANDED  # don't change hidden symbols
                    else:
                        self.check(constraint.sub_exprs[1].name == 'normal',
                                   f"unknown display constraint: {constraint}")
                else:
                    raise IDPZ3Error(f"unknown display constraint: {constraint}")
            elif type(constraint) == UnappliedSymbol:
                if constraint.name == "moveSymbols":
                    self.moveSymbols = True
                elif constraint.name == "optionalPropagation":
                    self.optionalPropagation = True
                else:
                    raise IDPZ3Error(f"unknown display contraint:"
                                     f"{constraint}")
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
        kwargs = "" if len(self.kwargs)==0 else f",{','.join(str(a) for a in self.kwargs)}"
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
                                classes=[Idp, Annotations,

                                         Vocabulary, Extern,
                                         ConstructedTypeDeclaration,
                                         RangeDeclaration,
                                         SymbolDeclaration, Symbol, Sort,

                                         Theory, Definition, Rule, IfExpr,
                                         AQuantification, ARImplication,
                                         AEquivalence, AImplication,
                                         ADisjunction, AConjunction,
                                         AComparison, ASumMinus, AMultDiv,
                                         APower, AUnary, AAggregate,
                                         AppliedSymbol, UnappliedSymbol,
                                         Number, Brackets, Arguments,

                                         Structure, SymbolInterpretation,
                                         Enumeration, FunctionEnum, CSVEnumeration,
                                         Tuple, FunctionTuple, CSVTuple,
                                         Display,

                                         Procedure, Call1, Call0, String, PyList, PyAssignment])
