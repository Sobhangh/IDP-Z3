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
__all__ = ["IDP", "Vocabulary", "Annotations", "Import",
           "TypeDeclaration",
           "SymbolDeclaration", "Symbol", "TheoryBlock", "Definition",
           "Rule", "Structure", "Enumeration", "Tuple",
           "Display", "Procedure", ]

from copy import copy
from datetime import date
from enum import Enum
from itertools import groupby
from operator import truediv
from os import path
from re import match
from sys import intern
from click import IntRange
from textx import metamodel_from_file
from typing import Dict, List, Union, Optional


from .Assignments import Assignments
from .Expression import (Annotations, ASTNode, Constructor, Accessor, Symbol, SymbolExpr,
                         Expression, AIfExpr, AQuantification, Subtype, Quantee,
                         ARImplication, AEquivalence,
                         AImplication, ADisjunction, AConjunction,
                         AComparison, ASumMinus, AMultDiv, APower, AUnary,
                         AAggregate, AppliedSymbol, UnappliedSymbol,
                         Number, Brackets, Date,
                         Variable, TRUEC, FALSEC, TRUE, FALSE, EQUALS, AND, OR, EQUIV)
from .utils import (RESERVED_SYMBOLS, OrderedSet, NEWL, BOOL, INT, REAL, DATE, CONCEPT,
                    GOAL_SYMBOL, EXPAND, RELEVANT, ABS, IDPZ3Error,
                    CO_CONSTR_RECURSION_DEPTH, MAX_QUANTIFIER_EXPANSION)

###############
#help functies voor SCA
def builtIn_type(elem):     #kijkt of het meegegeven type builtIn type is (return true or false)
    listOfSbuildIn = ["ℤ" , "𝔹", "ℝ", "Concept", "Int", "Bool", "Real", "Date"]
    return elem in listOfSbuildIn
################

def str_to_IDP(atom, val_string):
    """cast a string value for 'atom into an Expr object, or None

    used to convert Z3 models or json data from GUI

    Args:
        atom (Expr): the atom whose value must be converted
        val_string (str): the string representation of the value

    Returns:
        Expr?: the value cast as Expr, or None if unknown
    """
    assert atom.type, "Internal error"
    if val_string == str(atom) or val_string+"()" == str(atom):
        out = None  # Z3 means the value is unknown
    elif atom.type == BOOL:
        if val_string not in ['True', 'False', 'true', 'false']:
            raise IDPZ3Error(
                f"{atom.annotations['reading']} has wrong value: {val_string}")
        out = (TRUE if val_string in ['True', 'true'] else
               FALSE)
    elif atom.type == DATE:
        d = (date.fromordinal(eval(val_string)) if not val_string.startswith('#') else
             date.fromisoformat(val_string[1:]))
        out = Date(iso=f"#{d.isoformat()}")
    elif (hasattr(atom.decl.out.decl, 'map')
          and val_string in atom.decl.out.decl.map):  # constructor
        out = atom.decl.out.decl.map[val_string]
    elif 1 < len(val_string.split('(')):  # e.g., pos(0,0)
        # deconstruct val_string
        m = match(r"(?P<function>\w+)\s?\((?P<args>(?P<arg>\w+(,\s?)?)+)\)",
                  val_string).groupdict()

        typ = atom.decl.out.decl
        assert hasattr(typ, 'interpretation'), "Internal error"
        constructor = next(c for c in typ.interpretation.enumeration.constructors
                           if c.name == m['function'])

        args = m['args'].split(',')
        args = [Number(number=str(eval(a.replace('?', ''))))  #TODO deal with any argument based on constructor signature
                for a in args]

        out = AppliedSymbol.construct(constructor, args)
    else:  # a fraction
        out = Number(number=str(eval(val_string.replace('?', ''))))
    return out


class ViewType(Enum):
    HIDDEN = "hidden"
    NORMAL = "normal"
    EXPANDED = "expanded"


class IDP(ASTNode):
    """The class of AST nodes representing an IDP-Z3 program.
    """
    """ do not display this info in the API
    Attributes:
        code (str): source code of the IDP program

        vocabularies (Dict[str, Vocabulary]): list of vocabulary blocks, by name

        theories (Dict[str, TheoryBlock]): list of theory blocks, by name

        structures (Dict[str, Structure]): list of structure blocks, by name

        procedures (Dict[str, Procedure]): list of procedure blocks, by name

        display (Display, Optional): display block, if any
    """
    def __init__(self, **kwargs):
        # log("parsing done")
        self.code = None
        self.vocabularies = self.dedup_nodes(kwargs, 'vocabularies')
        self.theories = self.dedup_nodes(kwargs, 'theories')
        self.structures = self.dedup_nodes(kwargs, 'structures')
        displays = kwargs.pop('displays')
        self.procedures = self.dedup_nodes(kwargs, 'procedures')

        assert len(displays) <= 1, "Too many display blocks"
        self.display = displays[0] if len(displays) == 1 else None

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
            self.display = Display(constraints=[], interpretations=[])

    @classmethod
    def from_file(cls, file:str) -> "IDP":
        """parse an IDP program from file

        Args:
            file (str): path to the source file

        Returns:
            IDP: the result of parsing the IDP program
        """
        assert path.exists(file), f"Can't find {file}"
        with open(file, "r") as source:
            code = source.read()
            return cls.from_str(code)

    @classmethod
    def from_str(cls, code:str) -> "IDP":
        """parse an IDP program

        Args:
            code (str): source code to be parsed

        Returns:
            IDP: the result of parsing the IDP program
        """
        out = idpparser.model_from_str(code)
        out.code = code
        return out

    @classmethod
    def parse(cls, file_or_string: str) -> "IDP":
        """DEPRECATED: parse an IDP program

        Args:
            file_or_string (str): path to the source file, or the source code itself

        Returns:
            IDP: the result of parsing the IDP program
        """
        print("IDP.parse() is deprecated. Use `from_file` or `from_str` instead")
        code = file_or_string
        if path.exists(file_or_string):
            with open(file_or_string, "r") as source:
                code = source.read()
        out = idpparser.model_from_str(code)
        out.code = code
        return out

    def get_blocks(self, blocks: List[str]) -> List[ASTNode]:
        """returns the AST nodes for the blocks whose names are given

        Args:
            blocks (List[str]): list of names of the blocks to retrieve

        Returns:
            List[Union[Vocabulary, TheoryBlock, Structure, Procedure, Display]]:
                list of AST nodes
        """
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

    def execute(self) -> None:
        pass  # monkey patched

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self)
        #get all vocabularies
        V = self.get_blocks(self.vocabularies)
        for v in V :
            v.printAST(spaties+3)
        #get all structures
        S = self.get_blocks(self.structures)
        for s in S :
            s.printAST(spaties+3)
        #get all theories
        T = self.get_blocks(self.theories)
        for t in T :
            t.printAST(spaties+3)
        #get all procedures
        P = self.get_blocks(self.procedures)
        for p in P :
            p.printAST(spaties+3)

    def blockNameCheck(self,a) :
        if hasattr(a,'name'):
            for t in self.theories :
                if a.name == t:
                    return True
            for s in self.structures :
                if a.name == s:
                    return True
        return False

################################ Vocabulary  ##############################


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
                decl.private = decl.name.startswith('_')
                temp.append(decl)
            else:
                for symbol in decl.symbols:
                    new = copy(decl)  # shallow copy !
                    new.name = intern(symbol.name)
                    new.private = new.name.startswith('_')
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
                name=CONCEPT,
                constructors=[]),
            SymbolDeclaration(annotations='', name=Symbol(name=GOAL_SYMBOL),
                              sorts=[Subtype(name=CONCEPT, ins=[],
                                             out=Subtype(name=BOOL))],
                              out=Subtype(name=BOOL)),
            SymbolDeclaration(annotations='', name=Symbol(name=RELEVANT),
                              sorts=[Subtype(name=CONCEPT, ins=[],
                                             out=Subtype(name=BOOL))],
                              out=Subtype(name=BOOL)),
            SymbolDeclaration(annotations='', name=Symbol(name=ABS),
                                sorts=[Subtype(name=INT)],
                                out=Subtype(name=INT)),
            ] + self.declarations

    def __str__(self):
        return (f"vocabulary {{{NEWL}"
                f"{NEWL.join(str(i) for i in self.declarations)}"
                f"{NEWL}}}{NEWL}")

    def add_voc_to_block(self, block):
        """adds the enumerations in a vocabulary to a theory or structure block

        Args:
            block (Theory): the block to be updated
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

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+":"+self.name)
        for i in self.declarations:
            i.printAST(spaties+5)

    def SCA_Check(self,fouten):
        for i in self.declarations:
            i.SCA_Check(fouten)


class Import(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')

    def __str__(self):
        return f"Import {self.name}"


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

        self.range = None
        self.map = {}  # {String: constructor}

        self.interpretation = (None if enumeration is None else
            SymbolInterpretation(name=Symbol(name=self.name),
                                 enumeration=enumeration, default=None))

    def __str__(self):
        if self.name in RESERVED_SYMBOLS:
            return ''
        enumeration = (f"{','.join(map(str, self.constructors))}" if self.constructors else
                       f"{self.enumeration}")
        return (f"type {self.name} := {{{enumeration}}}")

    def check_bounds(self, var):
        if self.name == CONCEPT:
            comparisons = [EQUALS([var, UnappliedSymbol.construct(c)])
                          for c in self.constructors]
            return OR(comparisons)
        else:
            return self.interpretation.enumeration.contains([var], False)

    def is_subset_of(self, other):
        return self == other

    def printAST(self,spaties):
        if str(self) > self.name:
            print(spaties*" "+type(self).__name__+":",self)
        else :
            print(spaties*" "+type(self).__name__+":",self.name)
        for i in self.sorts:
            i.printAST(spaties+5)
        if self.interpretation is not None:
            self.interpretation.printAST(spaties+5)

    def SCA_Check(self,fouten):
        # style guide check : capital letter for type
        if self.name[0].islower():
            fouten.append((self,f"Style guide check, type name should start with a capital letter ","Warning"))

        # check if type has interpretation, if not check if in structures the type has given an interpretation
        if (self.interpretation is None and not(builtIn_type(self.name))):
            structs = self.block.idp.get_blocks(self.block.idp.structures)
            list =[]
            for i in structs:
                list.append(i.name)
            for s in structs :
                if s.vocab_name == self.block.name:
                    if not(self.name in s.interpretations):
                        fouten.append((self,f"Expected an interpretation for type {self.name} in Vocabulary {self.block.name} or Structures {list} ","Error"))
                        break


class SymbolDeclaration(ASTNode):
    """The class of AST nodes representing an entry in the vocabulary,
    declaring one or more symbols.
    Multi-symbols declaration are replaced by single-symbol declarations
    before the annotate() stage.

    Attributes:
        annotations : the annotations given by the expert.

            `annotations['reading']` is the annotation
            giving the intended meaning of the expression (in English).

        symbols ([Symbol]): the symbols being defined, before expansion

        name (string): the identifier of the symbol, after expansion of the node

        arity (int): the number of arguments

        sorts (List[Subtype]): the types of the arguments

        out (Subtype): the type of the symbol

        type (string): name of the Z3 type of an instance of the symbol

        in_domain (List): the list of possible tuples of arguments

        instances (Dict[string, Expression]):
            a mapping from the code of a symbol applied to a tuple of
            arguments to its parsed AST

        range (List[Expression]): the list of possible values

        private (Bool): True if the symbol name starts with '_' (for use in IC)

        unit (str):
            the unit of the symbol, such as m (meters)

        heading (str):
            the heading that the symbol should belong to

        optimizable (bool):
            whether this symbol should get optimize buttons in the IC
    """

    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')
        if 'symbols' in kwargs:
            self.symbols = kwargs.pop('symbols')
            self.name = None
        else:
            self.symbols = None
            if 'name' in kwargs:
                self.name = intern(kwargs.pop('name').name)
            else:
                self.name = intern(kwargs.pop('strname'))
        self.sorts = kwargs.pop('sorts')
        self.out = kwargs.pop('out')
        if self.out is None:
            self.out = Symbol(name=BOOL)

        self.arity = len(self.sorts)
        self.annotations = self.annotations.annotations if self.annotations else {}
        self.private = None
        self.unit: str = None
        self.heading: str = None
        self.optimizable: bool = True

        self.type = None  # a string
        self.in_domain = None  # all possible arguments
        self.range = None  # all possible values
        self.instances = None  # {string: AppliedSymbol} not starting with '_'
        self.block: Optional[Block] = None  # vocabulary where it is declared
        self.view = ViewType.NORMAL  # "hidden" | "normal" | "expanded" whether the symbol box should show atoms that contain that symbol, by default

    @classmethod
    def make(cls, strname, arity, sorts, out):
        o = cls(strname=strname, arity=arity, sorts=sorts, out=out, annotations={})
        return o

    def __str__(self):
        if self.name in RESERVED_SYMBOLS:
            return ''
        args = '⨯'.join(map(str, self.sorts)) if 0 < len(self.sorts) else ''
        return (f"{self.name}: "
                f"{ '('+args+')' if args else '()'}"
                f" -> {self.out.name}")

    def __repr__(self):
        return str(self)

    def is_subset_of(self, other):
        return (self.arity == 1 and self.type == BOOL
                and self.sorts[0].decl == other)

    def has_in_domain(self, args: List[Expression]) -> Expression:
        """Returns an expression that says whether the `args` are in the domain of the symbol.

        Arguments:
            args (List[Expression]): the list of arguments to be checked, e.g. `[1, 2]`

        Returns:
            Expression: whether `(1,2)` is in the domain of the symbol
        """
        assert len(self.sorts) == len(args), \
            f"Incorrect arity of {str(args)} for {self.name}"
        return AND([typ.has_element(term)
                   for typ, term in zip(self.sorts, args)])


    def has_in_range(self, value: Expression) -> Expression:
        """Returns an expression that says whether `value` is in the range of the symbol.
        """
        return self.out.has_element(value)

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__,":",self)
        for i in self.sorts:
            i.printAST(spaties+5)
        self.out.printAST(spaties+5)

    def SCA_Check(self,fouten):
        # style regel: func/pred namen met een kleine letter
        if self.name[0].isupper():
            fouten.append((self,f"Style guide check, predicate/function name should start with a lower letter ","Warning"))


Type = Union[TypeDeclaration, SymbolDeclaration]


################################ TheoryBlock  ###############################


class TheoryBlock(ASTNode):
    """ The class of AST nodes representing a theory block.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.vocab_name = kwargs.pop('vocab_name')
        constraints = kwargs.pop('constraints')
        self.definitions = kwargs.pop('definitions')
        self.interpretations = self.dedup_nodes(kwargs, 'interpretations')

        self.name = "T" if not self.name else self.name
        self.vocab_name = 'V' if not self.vocab_name else self.vocab_name

        self.declarations = {}
        self.def_constraints = {}  # {(Declaration, Definition): list[Expression]}
        self.assignments = Assignments()

        self.constraints = OrderedSet()
        for c in constraints:
            c.block = self
            if c.annotations is not None:
                c.expr.annotations = c.annotations.annotations
            self.constraints.append(c.expr)
        for definition in self.definitions:
            for rule in definition.rules:
                rule.block = self

    def __str__(self):
        return self.name

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self)
        for c in self.constraints:
            c.printAST(spaties+5)
        for d in self.definitions:
            d.printAST(spaties+5)

    def SCA_Check(self,fouten):
        for c in self.constraints:
            c.SCA_Check(fouten)
        for d in self.definitions:
            d.SCA_Check(fouten)


class Definition(ASTNode):
    """ The class of AST nodes representing an inductive definition.
        id (num): unique identifier for each definition

        rules ([Rule]):
            set of rules for the definition, e.g., `!x: p(x) <- q(x)`

        canonicals (Dict[Declaration, list[Rule]]):
            normalized rule for each defined symbol,
            e.g., `!$p!1$: p($p!1$) <- q($p!1$)`

        instantiables (Dict[Declaration], list[Expression]):
            list of instantiable expressions for each symbol,
            e.g., `p($p!1$) <=> q($p!1$)`

        clarks (Dict[Declaration, Transformed Rule]):
            normalized rule for each defined symbol (used to be Clark completion)
            e.g., `!$p!1$: p($p!1$) <=> q($p!1$)`

        def_vars (Dict[String, Dict[String, Variable]]):
            Fresh variables for arguments and result

        level_symbols (Dict[SymbolDeclaration, Symbol]):
            map of recursively defined symbols to level mapping symbols

        cache (Dict[SymbolDeclaration, str, Expression]):
            cache of instantiation of the definition

        inst_def_level (int): depth of recursion during instantiation

    """
    definition_id = 0  # intentional static variable so that no two definitions get the same ID

    def __init__(self, **kwargs):
        Definition.definition_id += 1
        self.id = Definition.definition_id
        self.annotations = kwargs.pop('annotations')
        self.annotations = self.annotations.annotations if self.annotations else {}
        self.rules = kwargs.pop('rules')
        self.clarks = {}  # {SymbolDeclaration: Transformed Rule}
        self.canonicals = {}
        self.instantiables = {}
        self.def_vars = {}  # {String: {String: Variable}}
        self.level_symbols = {}  # {SymbolDeclaration: Symbol}
        self.cache = {}  # {decl, str: Expression}
        self.inst_def_level = 0

    def __str__(self):
        return "Definition " +str(self.id)+" of " + ",".join([k.name for k in self.canonicals.keys()])

    def __repr__(self):
        out = []
        for rule in self.clarks.values():
            out.append(repr(rule))
        return NEWL.join(out)

    def __eq__(self, another):
        return self.id == another.id

    def __hash__(self):
        return hash(self.id)

    def instantiate_definition(self, decl, new_args, theory):
        rule = self.clarks.get(decl, None)
        if rule:
            key = str(new_args)
            if (decl, key) in self.cache:
                return self.cache[decl, key]

            if self.inst_def_level + 1 > CO_CONSTR_RECURSION_DEPTH:
                return None
            self.inst_def_level += 1
            self.cache[decl, key] = None

            out = rule.instantiate_definition(new_args, theory)

            self.cache[decl, key] = out
            self.inst_def_level -= 1
            return out

    def set_level_symbols(self):
        """Calculates which symbols in the definition are recursively defined,
           creates a corresponding level mapping symbol,
           and stores these in self.level_symbols.
        """
        dependencies = set()
        for r in self.rules:
            symbs = {}
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

        symbs = {s for (s, ss) in dependencies if s == ss}
        for r in self.rules:
            key = r.definiendum.symbol.decl
            if key not in symbs or key in self.level_symbols:
                continue
            symbdec = SymbolDeclaration.make(
                "_"+str(self.id)+"lvl_"+key.name,
                key.arity, key.sorts, Subtype(name=REAL))
            self.level_symbols[key] = Symbol(name=symbdec.name)
            self.level_symbols[key].decl = symbdec

        for decl in self.level_symbols.keys():
            self.check(decl.out.name == BOOL,
                       f"Inductively defined functions are not supported yet: "
                       f"{decl.name}.")

        if len(self.level_symbols) > 0:  # check for nested recursive symbols
            nested = set()
            for r in self.rules:
                r.body.collect_nested_symbols(nested, False)
            for decl in self.level_symbols.keys():
                self.check(decl not in nested,
                           f"Inductively defined nested symbols are not supported yet: "
                           f"{decl.name}.")

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self)
        for r in self.rules:
            r.printAST(spaties+5)

    def SCA_Check(self,fouten):
        for r in self.rules:
            r.SCA_Check(fouten)

class Rule(ASTNode):
    def __init__(self, **kwargs):
        self.annotations = kwargs.pop('annotations')
        self.quantees = kwargs.pop('quantees')
        self.definiendum = kwargs.pop('definiendum')
        self.out = kwargs.pop('out')
        self.body = kwargs.pop('body')
        self.is_whole_domain = None  # Bool
        self.block = None  # theory where it occurs

        self.annotations = self.annotations.annotations if self.annotations else {}

        if self.out is not None:
            self.definiendum.sub_exprs.append(self.out)
        if self.body is None:
            self.body = TRUE

    def __repr__(self):
        return (f"Rule:∀{','.join(str(q) for q in self.quantees)}: "
                f"{self.definiendum} "
                f"⇔{str(self.body)}")

    def instantiate_definition(self, new_args, theory):
        """Create an instance of the definition for new_args, and interpret it for theory.

        Args:
            new_args ([Expression]): tuple of arguments to be applied to the defined symbol
            theory (Theory): the context for the interpretation

        Returns:
            Expression: a boolean expression
        """

        #TODO assert self.is_whole_domain == False
        out = self.body.copy()  # in case there are no arguments
        instance = AppliedSymbol.make(self.definiendum.symbol, new_args)
        instance.in_head = True
        if self.definiendum.decl.type == BOOL:  # a predicate
            self.check(len(self.definiendum.sub_exprs) == len(new_args),
                       "Internal error")
            out = out.instantiate(self.definiendum.sub_exprs, new_args, theory)
            out = EQUIV([instance, out])
        else:
            self.check(len(self.definiendum.sub_exprs) == len(new_args)+1 ,
                       "Internal error")
            out = out.instantiate(self.definiendum.sub_exprs,
                                  new_args+[instance], theory)
        out.block = self.block
        out = out.interpret(theory)
        return out

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self)
        for q in self.quantees:
            q.printAST(spaties+5)
        self.definiendum.printAST(spaties+5)
        self.body.printAST(spaties+5)

    def SCA_Check(self,fouten):
        for q in self.quantees:
            q.SCA_Check(fouten)
        self.definiendum.SCA_Check(fouten)
        self.body.SCA_Check(fouten)


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

        self.name = 'S' if not self.name else self.name
        self.vocab_name = 'V' if not self.vocab_name else self.vocab_name

        self.voc = None
        self.declarations = {}
        self.assignments = Assignments()

    def __str__(self):
        return self.name

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self)
        for i in self.interpretations:
            self.interpretations[i].printAST(spaties+5)

    def SCA_Check(self,fouten):
        for i in self.interpretations:
            self.interpretations[i].SCA_Check(fouten)


class SymbolInterpretation(ASTNode):
    """
    AST node representing `<symbol> := { <identifiers*> } else <default>.`

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
            tuples.sort(key=lambda t: str(t.args[rank]))
            groups = groupby(tuples, key=lambda t: str(t.args[rank]))

            if args[rank].value is not None:
                for val, tuples2 in groups:  # try to resolve
                    if str(args[rank]) == val:
                        out = self.interpret_application(theory, rank+1,
                                        applied, args, list(tuples2))
            else:
                for val, tuples2 in groups:
                    tuples = list(tuples2)
                    out = AIfExpr.make(
                        EQUALS([args[rank], tuples[0].args[rank]]),
                        self.interpret_application(theory, rank+1,
                                                   applied, args, tuples),
                        out)
            return out

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self.name)
        self.enumeration.printAST(spaties+5)

    def SCA_Check(self,fouten):
        #check de gedefinieerde functies, predicaten, constanten en proposities
        if (not(isinstance(self.enumeration,(Ranges,FunctionEnum))) and not(self.is_type_enumeration)):   #als predicaat, const of boolean
            if self.symbol.decl.arity==0: #const en boolean
                out_type = self.symbol.decl.out                                                 #out type functie
                if hasattr(out_type.decl,'enumeration'):      #als type geen built-in type is
                    out_type_waardes = str(out_type.decl.enumeration).replace(" ", "").split(',')   #waardes out type
                    if self.default.str not in out_type_waardes:
                        fouten.append((self.default,f"Element of wrong type","Error"))  # element of wrong type used for const
            else :
                opties = []
                for i in self.symbol.decl.sorts:    #get alle waarde van argument types
                    opties.append(str(i.decl.enumeration).replace(" ", "").split(','))
                for t in self.enumeration.tuples:
                    if len(t.args) > self.symbol.decl.arity:    #als te veel input elementen
                        fouten.append((t.args[0],f"To much input elements, expected {self.symbol.decl.arity}","Error"))
                    else :
                        for i in range(0,len(t.args),1):  #get elements
                            if str(t.args[i]) not in opties[i]:
                                fouten.append((t.args[i],f"Element of wrong type","Error"))  # element of wrong type used in predicate

        if isinstance(self.enumeration,FunctionEnum):     #als functie
            out_type = self.symbol.decl.out                                                 #out type functie
            out_type_waardes = str(out_type.decl.enumeration).replace(" ", "").split(',')   #waardes out type
            opties = []
            for i in self.symbol.decl.sorts:    #get alle waarde van argument types
                opties.append(str(i.decl.enumeration).replace(" ", "").split(','))

            # bereken alle mogelijke combinaties
            newlist = []
            oudlist = opties[0]
            for i in range(1,len(opties)):
                newlist = []
                for a in oudlist:
                    for b in opties[i]:
                        hulp_element = []
                        if isinstance(a,list):
                            for c in a:
                                hulp_element.append(c)
                        else :
                            hulp_element.append(a)
                        hulp_element.append(b)
                        newlist.append(hulp_element)
                oudlist = newlist

            mogelijkheden = oudlist
            duplicates = []
            for t in self.enumeration.tuples:
                if str(t.value) not in out_type_waardes:  # als output element van verkeerd type
                    fouten.append((t.value,f"Output element of wrong type, {str(t.value)}","Error"))
                elements = []
                for i in range(0,len(t.args)-1,1):  #get input elements
                    if (i < len(opties) and (str(t.args[i]) not in opties[i])) :
                        fouten.append((t.args[i],f"Element of wrong type, {str(t.args[i])}","Error"))  # element of wrong type used
                    elements.append(str(t.args[i]))
                if len(t.args) > self.symbol.decl.arity+1:    #als te veel input elementen
                    fouten.append((t.args[0],f"To much input elements, expected {self.symbol.decl.arity}","Error"))
                elif elements in mogelijkheden:   #als mogelijkheid geldig is
                    mogelijkheden.remove(elements) #verwijder uit lijst om duplicates te vermijden
                    duplicates.append(elements) #voeg de al gebruikt mogelijkheden toe
                elif (self.symbol.decl.arity == 1 and elements[0] in mogelijkheden): #als func met 1arg
                    mogelijkheden.remove(elements[0]) #verwijder uit lijst om duplicates te vermijden
                    duplicates.append(elements[0]) #voeg de al gebruikt mogelijkheden toe
                elif (elements in duplicates or elements[0] in duplicates): # als duplicates
                        fouten.append((t.args[0],f"Wrong input elements, duplicate","Error"))  #duplicate

            if (len(mogelijkheden) > 0 and self.symbol.decl.arity == 1): #als functie niet voledig
                    fouten.append((self,f"Function not total defined, missing {mogelijkheden}","Error"))
            elif len(mogelijkheden) > 0: #als functie niet volledig
                fouten.append((self,f"Function not total defined, missing elements","Error"))


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
            # self.tuples.sort(key=lambda t: t.code) # do not change dropdown order
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
        tuples = sorted(list(tuples), key=lambda t: str(t.args[rank]))
        groups = groupby(tuples, key=lambda t: str(t.args[rank]))
        if args[rank].value is not None:
            for val, tuples2 in groups:  # try to resolve
                if str(args[rank]) == val:
                    return self.contains(args, function, arity, rank+1, list(tuples2))
            return FALSE
        else:
            if rank + 1 == arity:  # use OR
                out = [ EQUALS([args[rank], t.args[rank]])
                        for t in tuples]
                out = OR(out)
                out.enumerated = ', '.join(str(c) for c in tuples)
                return out
            out = FALSE
            for val, tuples2 in groups:
                tuples = list(tuples2)
                out = AIfExpr.make(
                    EQUALS([args[rank], tuples[0].args[rank]]),
                    self.contains(args, function, arity, rank+1, tuples),
                    out)
            return out

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self)
        for t in self.tuples:
            t.printAST(spaties+5)

class FunctionEnum(Enumeration):
    pass

class CSVEnumeration(Enumeration):
    pass

class ConstructedFrom(Enumeration):
    """Represents a 'constructed from' enumeration of constructors

    Attributes:
        tuples (OrderedSet[Tuple]): OrderedSet of tuples of Expression

        constructors (List[Constructor]): List of Constructor

        accessors (Dict[str, Int]): index of the accessor in the constructors
    """
    def __init__(self, **kwargs):
        self.constructed = kwargs.pop('constructed')
        self.constructors = kwargs.pop('constructors')
        self.tuples = None
        self.accessors = dict()

    def contains(self, args, function, arity=None, rank=0, tuples=None):
        """returns True if args belong to the type enumeration"""
        # args must satisfy the tester of one of the constructors
        assert len(args) == 1, f"Incorrect arity in {self.parent.name}{args}"
        if type(args[0].decl) == Constructor:  # try to simplify it
            self.check(self.parent.name == args[0].decl.type,
                       f"Incorrect type of {args[0]} for {self.parent.name}")
            self.check(len(args[0].sub_exprs) == len(args[0].decl.sorts),
                       f"Incorrect arity")
            return AND([t.decl.out.has_element(e)
                        for e,t in zip(args[0].sub_exprs, args[0].decl.sorts)])
        out = [AppliedSymbol.construct(constructor.tester, args)
                for constructor in self.constructors]
        return OR(out)

class Tuple(ASTNode):
    def __init__(self, **kwargs):
        self.args = kwargs.pop('args')
        self.code = intern(",".join([str(a) for a in self.args]))

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self)
        for a in self.args:
            a.printAST(spaties+5)

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
        if self.elements:
            self.type = self.elements[0].fromI.type
            for x in self.elements:
                if x.fromI.type != self.type:
                    if self.type in [INT, REAL] and x.fromI.type in [INT, REAL]:
                        self.type = REAL  # convert to REAL
                        tuples = [Tuple(args=[n.args[0].real()])
                                  for n in tuples]
                    else:
                        self.check(False,
                            f"incorrect value {x.fromI} for {self.type}")

                if x.toI is None:
                    tuples.append(Tuple(args=[x.fromI]))
                elif self.type == INT and x.fromI.type == INT and x.toI.type == INT:
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        tuples.append(Tuple(args=[Number(number=str(i))]))
                elif self.type == REAL and x.fromI.type == INT and x.toI.type == INT:
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        tuples.append(Tuple(args=[Number(number=str(float(i)))]))
                elif self.type == REAL:
                    self.check(False, f"Can't have a range over real: {x.fromI}..{x.toI}")
                elif self.type == DATE and x.fromI.type == DATE and x.toI.type == DATE:
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        d = Date(iso=f"#{date.fromordinal(i).isoformat()}")
                        tuples.append(Tuple(args=[d]))
                else:
                    self.check(False, f"Incorrect value {x.toI} for {self.type}")
        Enumeration.__init__(self, tuples=tuples)

    def contains(self, args, function, arity=None, rank=0, tuples=None):
        var = args[0]
        if not self.elements:
            return TRUE
        if self.tuples and len(self.tuples) < MAX_QUANTIFIER_EXPANSION:
            es = [EQUALS([var, c.args[0]]) for c in self.tuples]
            e = OR(es)
            return e
        sub_exprs = []
        for x in self.elements:
            if x.toI is None:
                e = EQUALS([var, x.fromI])
            else:
                e = AComparison.make('≤', [x.fromI, var, x.toI])
            sub_exprs.append(e)
        return OR(sub_exprs)

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
        self.interpretations = self.dedup_nodes(kwargs, 'interpretations')
        self.moveSymbols = False
        self.optionalPropagation = False
        self.manualPropagation = False
        self.optionalRelevance = False
        self.manualRelevance = False
        self.name = "display"

    def run(self, idp):
        """apply the display block to the idp theory"""

        def base_symbols(name, concepts):
            """Verify that concepts is a list of concepts.  Returns the list of symbols"""
            symbols = []
            # All concepts should be concepts, except for the first
            # argument of 'unit' and 'heading'.
            for i, symbol in enumerate(concepts):
                if name in ['unit', 'heading'] and i == 0:
                    continue
                self.check(symbol.name.startswith('`'),
                    f"arg '{symbol.name}' of {name}'"
                    f" must begin with a tick '`'")
                self.check(symbol.name[1:] in self.voc.symbol_decls,
                    f"argument '{symbol.name}' of '{name}'"
                    f" must be a concept")
                symbols.append(self.voc.symbol_decls[symbol.name[1:]])
            return symbols

        for k, interpretation in self.interpretations.items():
            symbols = base_symbols(interpretation.name,
                [t.args[0] for t in interpretation.enumeration.tuples])
            if interpretation.name == EXPAND:
                for symbol in symbols:
                    self.voc.symbol_decls[symbol.name].view = ViewType.EXPANDED
            elif interpretation.name == GOAL_SYMBOL:
                idp.theory.interpretations[k] = interpretation
            else:
                raise IDPZ3Error(f"Unknown enumeration in display: {interpretation}")
        for constraint in self.constraints:
            if type(constraint) == AppliedSymbol:
                self.check(type(constraint.symbol.sub_exprs[0]) == Symbol,
                           f"Invalid syntax: {constraint}")
                name = constraint.symbol.sub_exprs[0].name
                symbols = base_symbols(name, constraint.sub_exprs)

                if name == 'hide':  # e.g. hide(Length, Angle)
                    for symbol in symbols:
                        self.voc.symbol_decls[symbol.name].view = ViewType.HIDDEN
                elif name in [GOAL_SYMBOL, EXPAND]:  # e.g. goal_symbol(`tax_amount`)
                    self.check(False, f"Please use an enumeration for {name}")
                elif name == 'unit':  # e.g. unit('m', `length):
                    for symbol in symbols:
                        symbol.unit = str(constraint.sub_exprs[0])
                elif name == 'heading':
                    # e.g. heading('Shape', `type).
                    for symbol in symbols:
                        symbol.heading = str(constraint.sub_exprs[0])
                elif name == 'noOptimization':  # e.g., noOptimization(`temp)
                    for symbol in symbols:
                        symbol.optimizable = False
                elif name == "moveSymbols":
                    self.moveSymbols = True
                elif name == "optionalPropagation":
                    self.optionalPropagation = True
                elif name == "manualPropagation":
                    self.manualPropagation = True
                elif name == "optionalRelevance":
                    self.optionalRelevance = True
                elif name == "manualRelevance":
                    self.manualRelevance = True
                else:
                    raise IDPZ3Error(f"Unknown display axiom:"
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
                                   f"Unknown display axiom: {constraint}")
            else:
                raise IDPZ3Error(f"Unknown display axiom: {constraint}")


################################ Main  ##################################

class Procedure(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.args = kwargs.pop('args')
        self.pystatements = kwargs.pop('pystatements')

    def __str__(self):
        return f"{NEWL.join(str(s) for s in self.pystatements)}"

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self.name)
        for a in self.pystatements:
            a.printAST(spaties+5)

    def SCA_Check(self,fouten):
        for a in self.pystatements:
            a.SCA_Check(fouten)


class Call1(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.par = kwargs.pop('par') if 'par' in kwargs else None
        self.args = kwargs.pop('args')
        self.kwargs = kwargs.pop('kwargs')
        self.post = kwargs.pop('post')

    def __str__(self):
        kwargs = ("" if len(self.kwargs)==0 else
                  f"{',' if self.args else ''}{','.join(str(a) for a in self.kwargs)}")
        args = ("" if not self.par else
                f"({','.join(str(a) for a in self.args)}{kwargs})")
        return ( f"{self.name}{args}"
                 f"{'' if self.post is None else '.'+str(self.post)}")

    def printAST(self,spaties):
        print(spaties*" "+type(self).__name__+": ",self)
        for a in self.args:
            a.printAST(spaties+5)

    def SCA_Check(self,fouten):
        lijst_inferenties = ["model_check","model_expand","model_propagate"]
        if self.name in lijst_inferenties:
            if self.parent.name != "pretty_print":    #check if pretty_print is used
                fouten.append((self,f"No pretty_print used!","Warning"))
        if self.name == "model_check":  #check if correct amount of arguments used by model_check
            if (len(self.args) > 2 or len(self.args) == 0):
                fouten.append((self,f"Wrong number of arguments for model_check: given {len(self.args)} <-> expected {1} or {2}","Error"))
            else :
                a = self.parent
                while not(isinstance(a,IDP)):   #zoek IDP node in parent
                    a = a.parent
                for i in self.args:
                    if not(a.blockNameCheck(i)):   #check of block naam bestaat
                        fouten.append((i,f"Block {i} does not exist!","Error"))

        for a in self.args:
            a.SCA_Check(fouten)

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

Block = Union[Vocabulary, TheoryBlock, Structure, Display]

dslFile = path.join(path.dirname(__file__), 'Idp.tx')

idpparser = metamodel_from_file(dslFile, memoization=True,
                                classes=[IDP, Annotations,

                                         Vocabulary, Import,
                                         TypeDeclaration, Accessor, Subtype,
                                         SymbolDeclaration, Symbol,
                                         SymbolExpr,

                                         TheoryBlock, Definition, Rule, AIfExpr,
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

                                         Procedure, Call1, String,
                                         PyList, PyAssignment])
