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

Classes to parse an IDP-Z3 theory.

"""
from __future__ import annotations

from copy import copy, deepcopy
from datetime import date
from enum import Enum
from itertools import groupby
from os import path
from sys import intern
from textx import metamodel_from_file
from typing import Tuple, List, Union, Optional, TYPE_CHECKING



from .Assignments import Assignments
from .Expression import (Annotations, Annotation, ASTNode, Constructor, CONSTRUCTOR,
                         Accessor, NextAppliedSymbol, NowAppliedSymbol, StartAppliedSymbol, SymbolExpr, Expression,
                         AIfExpr, IF, AQuantification, split_quantees, SetName,
                         SETNAME, Quantee, ARImplication, AEquivalence,
                         AImplication, ADisjunction, AConjunction, AComparison,
                         ASumMinus, AMultDiv, APower, AUnary, AAggregate,
                         AppliedSymbol, UnappliedSymbol, Number, Brackets,
                         Date, Extension, Identifier, Variable, TRUEC, FALSEC,
                         TRUE, FALSE, EQUALS, AND, OR,
                         BOOL_SETNAME, INT_SETNAME, REAL_SETNAME, DATE_SETNAME, EMPTY_SETNAME)
from .utils import (RESERVED_SYMBOLS, OrderedSet, NEWL, BOOL, INT, REAL, DATE,
                    CONCEPT, GOAL_SYMBOL, EXPAND, RELEVANT, ABS, IDPZ3Error,
                    MAX_QUANTIFIER_EXPANSION, Semantics as S, flatten)

if TYPE_CHECKING:
    from .Theory import Theory


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

        vocabularies (dict[str, Vocabulary]): list of vocabulary blocks, by name

        theories (dict[str, TheoryBlock]): list of theory blocks, by name

        structures (dict[str, Structure]): list of structure blocks, by name

        procedures (dict[str, Procedure]): list of procedure blocks, by name

        display (Display, Optional): display block, if any

        warnings (Exceptions): list of warnings
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
        self.now_voc = {}
        self.next_voc = {}
        init_thrs ={}
        init_strcs ={}
        for voc in self.vocabularies.values():
            now_voc:Vocabulary = voc.generate_now_voc()
            self.now_voc[now_voc.name]=now_voc
            now_voc.annotate_block(self)
            #print("voc now")
            next_voc = voc.generate_next_voc()
            self.next_voc[next_voc.name]=next_voc
            next_voc.annotate_block(self)
            #print("voc next")

            voc.annotate_block(self)
            #print("voc annot")
        for t in self.theories.values():
            if t.ltc:
                t.initialize_theory()
                #print("theories init")
                t.bst_theory()
                #print("theories bis")
                t.trs_theory()
                #print("theories trs")
                #if len(t.bistate_theory.definitions) > 1:
                #    print(t.bistate_theory.definitions[1].rules)

                #init_thrs[t.init_theory.name] = t.init_theory
                #init_thrs[t.bistate_theory.name] = t.bistate_theory
            #t.annotate(self)
        self.warnings = flatten(t.annotate_block(self)
                                for t in self.theories.values())
        #print("annotated theory")
        for struct in self.structures.values():
            struct.annotate_block(self)
            #init_strcs[struct.init_struct.name] = struct.init_struct
        #print("struc annotated..")
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

    def get_blocks(self, blocks: List[str] | str) -> List[ASTNode]:
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
        raise IDPZ3Error("Internal error") # monkey-patched


################################ Vocabulary  ##############################


class Vocabulary(ASTNode):
    """The class of AST nodes representing a vocabulary block.
    """
    def __init__(self, parent: ASTNode,
                 name: str,
                 declarations: List[Union[Declaration, VarDeclaration, Import]],
                 tempdcl:TemporalDeclaration|None):
        self.name = name
        self.tempdcl = tempdcl
        self.idp : Optional[IDP] = None  # parent object
        self.symbol_decls: dict[str, Union[Declaration, VarDeclaration, Constructor]] = {}
        self.contains_temporal = False

        self.name = 'V' if not self.name else self.name
        self.voc = self

        # expand multi-symbol declarations
        temp = []
        for decl in declarations:
            if isinstance(decl, SymbolDeclaration):
                for symbol in decl.symbols:
                    new = copy(decl)  # shallow copy !
                    new.name = intern(symbol)
                    new.private = new.name.startswith('_')
                    new.symbols = None
                    temp.append(new)
            else:
                temp.append(decl)
        self.declarations = temp
        self.original_decl =temp

        # define built-in types: Bool, Int, Real, Symbols
        self.declarations = [
            TypeDeclaration(self,
                name=BOOL, constructors=[TRUEC, FALSEC]),
            TypeDeclaration(self, name=INT, enumeration=IntRange()),
            TypeDeclaration(self, name=REAL, enumeration=RealRange()),
            TypeDeclaration(self, name=DATE, enumeration=DateRange()),
            TypeDeclaration(self, name='Tijd', enumeration=IntRange()),
            TypeDeclaration(self, name=CONCEPT, constructors=[]),
            SymbolDeclaration.make(self, name=GOAL_SYMBOL,
                            sorts=[SETNAME(CONCEPT, ins=[], out=SETNAME(BOOL))],
                            out=SETNAME(BOOL)),
            SymbolDeclaration.make(self, name=RELEVANT,
                            sorts=[SETNAME(CONCEPT, ins=[], out=SETNAME(BOOL))],
                            out=SETNAME(BOOL)),
            SymbolDeclaration.make(self, name=ABS,
                            sorts=[INT_SETNAME], out=INT_SETNAME),
            ] + self.declarations

    def __str__(self):
        return (f"vocabulary {{{NEWL}"
                f"    {f'{NEWL}    '.join(str(i) for i in self.declarations)}"
                f"{NEWL}}}{NEWL}").replace("    \n", "")

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

    #Has to be called before self is annotated
    def generate_now_voc(self):
        nowvoc = Vocabulary(parent=None,name=self.name+'_now',tempdcl=[],declarations=[])
        for d in self.original_decl:
            changed = False
            for t in self.tempdcl:
                if isinstance(d,SymbolDeclaration):
                    if d.name == t.symbol.name:
                        changed = True
                        sr = [s.init_copy() for s in d.sorts]
                        id = SymbolDeclaration(parent=None,name=(d.name),sorts=sr,out=d.out,annotations=Annotations(None,[]))
                        #id.arity -=1
                        #id.sorts.pop()
                        nowvoc.declarations.append(id)
                        break
            if not changed:
                if isinstance(d,VarDeclaration):
                    nowvoc.declarations.append(VarDeclaration(parent=None,name=(d.name),subtype=d.subtype))
                elif isinstance(d,SymbolDeclaration):
                    nowvoc.declarations.append(SymbolDeclaration(parent=None,name=(d.name),sorts=d.sorts,out=d.out,annotations=Annotations(None,[])))
                elif isinstance(d,TypeDeclaration):
                    enum =None
                    if d.interpretation:
                        #if isinstance(d.interpretation.enumeration,Ranges):
                        #    enum = Ranges(elements=d.interpretation.enumeration.elements)
                        #else:
                        #    enum = d.interpretation.enumeration.init_copy()
                        enum = d.interpretation.enumeration.init_copy()
                    cnstr = [c.init_copy() for c in d.constructors]
                    if len(cnstr) ==0:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,enumeration=enum))
                    else:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,constructors=cnstr,enumeration=enum))
                elif isinstance(d,Import):
                    #Not adding import
                    d
                else:
                    #without deepcopy
                    nowvoc.declarations.append(d.init_copy())
        return nowvoc
    
    def generate_next_voc(self):
        nowvoc = Vocabulary(parent=None,name=self.name+'_next',tempdcl=[],declarations=[])
        nowvoc.idp = self.idp
        for d in self.original_decl:
            changed = False
            for t in self.tempdcl:
                if isinstance(d,SymbolDeclaration):
                    if str(d.name) == str(t.symbol):
                        changed = True
                        sr = [s.init_copy() for s in d.sorts]
                        id = SymbolDeclaration(parent=None,name=d.name,sorts=sr,out=d.out,annotations=Annotations(None,[]))
                        #id.arity -=1
                        #id.sorts.pop()
                        nowvoc.declarations.append(id)
                        srn = [s.init_copy() for s in d.sorts]
                        next_d = SymbolDeclaration(parent=None,name=(d.name),sorts=srn,out=d.out,annotations=Annotations(None,[]))
                        next_d.name = d.name + "_next"
                        next_d.is_next= True
                        nowvoc.declarations.append(next_d)
                        #nowvoc.symbol_decls[next_d.name] = next_d
                        break
            if not changed:
                if isinstance(d,VarDeclaration):
                    nowvoc.declarations.append(VarDeclaration(parent=None,name=(d.name),subtype=d.subtype))
                elif isinstance(d,SymbolDeclaration):
                    nowvoc.declarations.append(SymbolDeclaration(parent=None,name=(d.name),sorts=d.sorts,out=d.out,annotations=Annotations(None,[])))
                elif isinstance(d,TypeDeclaration):
                    enum =None
                    if d.interpretation:
                        #if isinstance(d.interpretation.enumeration,Ranges):
                        #    enum = Ranges(elements=d.interpretation.enumeration.elements)
                        #else:
                        #    enum = d.interpretation.enumeration.init_copy()
                        enum = d.interpretation.enumeration.init_copy()
                    cnstr = [c.init_copy() for c in d.constructors]
                    if len(cnstr) ==0:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,enumeration=enum))
                    else:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,constructors=cnstr,enumeration=enum))
                elif isinstance(d,Import):
                    d
                else:
                    #without deepcopy
                    nowvoc.declarations.append(d.init_copy())
        return nowvoc

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

        domains (List[SetName]): a singleton list with a set having the type's name

        codomain (SetName): the Boolean type

        constructors ([Constructor]): list of constructors in the enumeration

        interpretation (SymbolInterpretation): the symbol interpretation

        map (dict[string, Expression]): a mapping from code to Expression in range

        block (Vocabulary): the vocabulary block that contains it
    """

    def __init__(self, parent,
                 name: str,
                 constructors: Optional[List[Constructor]] = None,
                 enumeration: Optional[Enumeration] = None):
        self.name = name
        self.constructors = constructors if constructors else []
        enumeration = enumeration

        self.arity : int = 1
        self.domains : List[SetName] = [SetName(None, self.name)]
        self.codomain : SetName = BOOL_SETNAME
        self.block: Optional[Block] = None

        self.map : dict[str, Expression]= {}

        self.interpretation : Optional[SymbolInterpretation] = None
        if enumeration:
            self.interpretation = SymbolInterpretation(parent=None,
                                 name=UnappliedSymbol(None, self.name),
                                 sign='≜',
                                 enumeration=enumeration, default=FALSE)
            self.interpretation.block = parent

    def init_copy(self,parent=None):
        enum =None
        if self.interpretation:
            enum = self.interpretation.enumeration.init_copy()
        cnstr = [c.init_copy() for c in self.constructors]
        return TypeDeclaration(parent=parent,name=self.name,constructors=cnstr,enumeration=enum)

    def __str__(self):
        if self.name in RESERVED_SYMBOLS:
            return ''
        enumeration = self.enumeration if hasattr(self, 'enumeration') and self.enumeration else ""
        constructors = enumeration.constructors if enumeration else None
        constructed = ("" if not bool(constructors) or all(0 == len(c.domains) for c in constructors)
                       else "constructed from ")
        enumeration = (f"{constructed}{{{', '.join(str(c) for c in constructors)}}}" if constructors else
                       f"{self.interpretation}" if self.interpretation else
                       f"{enumeration}")
        return (f"type {self.name} {'' if not enumeration else ':= ' + enumeration}")

    def contains_element(self, term: Expression,
                     extensions: dict[str, Extension]
                     ) -> Expression:
        """returns an Expression that is TRUE when `term` is in the type
        """
        if self.name == CONCEPT:
            comparisons = [EQUALS([term, UnappliedSymbol.construct(c)])
                          for c in self.constructors]
            return OR(comparisons)
        else:
            (superset, filter) = extensions[self.name]
            if superset is not None:
                # superset.sort(key=lambda t: str(t))
                if term.is_value():
                    comparisons = (TRUE if any(term.same_as(t[0]) for t in superset) else
                                   FALSE)
                else:
                    comparisons = OR([EQUALS([term, t[0]]) for t in superset])
                out = (comparisons if filter is None else
                       AND([filter([term]), comparisons]))
            elif filter is not None:
                out = filter([term])
            else:
                out = TRUE
            return out

    def translate(self, problem: Theory):
        pass

class SymbolDeclaration(ASTNode):
    """The class of AST nodes representing an entry in the vocabulary,
    declaring one or more symbols.
    Multi-symbols declaration are replaced by single-symbol declarations
    before the annotate() stage.

    Attributes:
        annotations : the annotations given by the expert.

            `annotations['reading']` is the annotation
            giving the intended meaning of the expression (in English).

        symbols ([str]): the symbols being defined, before expansion

        name (string): the identifier of the symbol, after expansion of the node

        arity (int): the number of arguments

        domains (List[SetName]): the types of the arguments

        codomain (SetName): the type of the symbol

        symbol_expr (SymbolExpr, Optional): symbol expression of the same name

        symbol_expr (SymbolExpr, Optional): a SymbolExpr of the same name

        instances (dict[string, Expression]):
            a mapping from the code of a symbol applied to a tuple of
            arguments to its parsed AST

        range (List[Expression]): the list of possible values

        private (Bool): True if the symbol name starts with '_' (for use in IC)

        block: the vocabulary where it is defined

        unit (str):
            the unit of the symbol, such as m (meters)

        heading (str):
            the heading that the symbol should belong to

        optimizable (bool):
            whether this symbol should get optimize buttons in the IC

        by_z3 (Bool): True if the symbol is created by z3 (testers and accessors of constructors)
    """

    def __init__(self,
                 parent,
                 annotations: Optional[Annotations],
                 sorts: List[SetName],
                 out: SetName,
                 symbols: Optional[List[str]] = None,
                 name: Optional[str] = None):
        #temp_symbol  = kwargs.pop('temporal')
        self.annotations : Annotation = annotations.annotations if annotations else {}
        self.temp= False
        self.symbols : Optional[List[str]]
        self.name : Optional[str]
        self.is_next = False
        #self.temp= False
        if symbols:
            self.symbols = symbols
            self.name = None
        else:
            self.symbols = None
            self.name = name
        self.domains : List[SetName] = sorts
        self.codomain : SetName = out
        if self.codomain is None:
            self.codomain = SETNAME(BOOL)

        self.symbol_expr : Optional[SymbolExpr]= None
        self.arity = None
        self.private = None
        self.unit: Optional[str] = None
        self.heading: Optional[str] = None
        self.optimizable: bool = True

        self.range : Optional[List[AppliedSymbol]]= None  # all possible terms.  Used in get_range and IO.py
        self.instances : Optional[dict[str, AppliedSymbol]]= None  # not starting with '_'
        self.block: Optional[ASTNode] = None  # vocabulary where it is declared
        self.view = ViewType.NORMAL  # "hidden" | "normal" | "expanded" whether the symbol box should show atoms that contain that symbol, by default
        self.by_z3 = False

    @classmethod
    def make(cls, parent, name, sorts, out):
        o = cls(parent=parent, name=name, sorts=sorts, out=out, annotations=None)
        o.arity = len([d for d in o.domains if d.root_set is not EMPTY_SETNAME])
        return o
    
    def init_copy(self,parent=None):
        sr = [s.init_copy() for s in self.sorts]
        return SymbolDeclaration(parent=parent,name=self.name,sorts=sr,out=self.out.init_copy(),annotations=self.annotations.init_copy())


    def __str__(self):
        if self.name in RESERVED_SYMBOLS:
            return ''
        args = '⨯'.join(map(str, self.domains)) if 0 < len(self.domains) else ''
        return (f"{self.name}: "
                f"{ '('+args+')' if args else '()'}"
                f" → {self.codomain.name}")

    def __repr__(self):
        return str(self)

    def has_in_domain(self, args: List[Expression],
                      interpretations: dict[str, "SymbolInterpretation"],
                      extensions: dict[str, Extension]
                      ) -> Expression:
        """Returns an expression that is TRUE when `args` are in the domain of the symbol.

        Arguments:
            args (List[Expression]): the list of arguments to be checked, e.g. `[1, 2]`

        Returns:
            Expression: whether `(1,2)` is in the domain of the symbol
        """
        assert self.arity == len(args), \
            f"Incorrect arity of {str(args)} for {self.name}"
        return AND([typ.has_element(term, extensions)
                   for typ, term in zip(self.domains, args)])

    def has_in_range(self, value: Expression,
                     interpretations: dict[str, "SymbolInterpretation"],
                     extensions: dict[str, Extension]
                     ) -> Expression:
        """Returns an expression that says whether `value` is in the range of the symbol.
        """
        return self.codomain.has_element(value, extensions)

    def contains_element(self, term: Expression,
                     extensions: dict[str, Extension]
                     ) -> Expression:
        """returns an Expression that is TRUE when `term` satisfies the predicate
        """
        assert self.codomain == BOOL_SETNAME and self.name is not None, "Internal error"
        (superset, filter) = extensions[self.name]
        if superset is not None:
            # superset.sort(key=lambda t: str(t))
            comparisons = [EQUALS([term, t[0]]) for t in superset]
            out = (OR(comparisons) if filter is None else
                    AND([filter([term]), OR(comparisons)]))
        elif filter is not None:
            out = filter([term])
        else:
            out = TRUE
        return out

    def translate(self, problem: Theory):
        raise IDPZ3Error("Internal error") # monkey-patched

class VarDeclaration(ASTNode):
    """ represents a declaration of variable (IEP 24)

    Attributes:
        name (str): name of the variable

        subtype (SetName): type of the variable
    """

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.subtype = kwargs.pop('subtype')

    def __str__(self):
        return f"var {self.name} ∈ {self.subtype}"
    
class TemporalDeclaration(ASTNode):
    """ represents a declaration of Temporal predicate (IEP 24)

    Attributes:
        symbol (SymbolExpr): symbol of the variable

    """

    def __init__(self, **kwargs):
        self.symbol = kwargs.pop('name')

    def __str__(self):
        return f"Temporal {self.symbol} "

Declaration = Union[TypeDeclaration, SymbolDeclaration]


################################ TheoryBlock  ###############################


class TheoryBlock(ASTNode):
    """ The class of AST nodes representing a theory block.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.vocab_name = kwargs.pop('vocab_name')
        constraints: List[Expression] = kwargs.pop('constraints')
        self.definitions = kwargs.pop('definitions')
        self.interpretations = self.dedup_nodes(kwargs, 'interpretations')
        self.ltc = True if kwargs.pop('ltc') else False
        self.inv = True if kwargs.pop('inv') else False
        self.idp =None
        #self.ltc = False

        self.name = "T" if not self.name else self.name
        self.vocab_name = 'V' if not self.vocab_name else self.vocab_name

        self.declarations = {}
        self.def_constraints = {}  # {(Declaration, Definition): List[Expression]}
        self.assignments = Assignments()

        self.constraints = OrderedSet()
        for c in constraints:
            if c.annotations is not None:
                c.expr.annotations = c.annotations.annotations
            self.constraints.append(c.expr)
        for definition in self.definitions:
            for rule in definition.rules:
                rule.block = self
        self.voc = None
        # For storing the initialized theory for ltc progression
        self.init_theory : TheoryBlock = None
        self.bistate_theory : TheoryBlock = None
        self.transition_theory : TheoryBlock = None
        #self.init_constraints = []
        #self.init_defs = []
        #self.init_interp = []

    def __str__(self):
        return self.name
    
    def contains_next(self,e:Expression):
        if isinstance(e,NextAppliedSymbol):
            return True
        if isinstance(e,(AppliedSymbol,NowAppliedSymbol,StartAppliedSymbol,UnappliedSymbol)):
            return False
        for s in e.sub_exprs:
            r = self.contains_next(s)
            if r:
                return True
        return False
    
    def contains_now(self,e:Expression):
        if isinstance(e,NowAppliedSymbol):
            return True
        if isinstance(e,(AppliedSymbol,NextAppliedSymbol,StartAppliedSymbol,UnappliedSymbol)):
            return False
        for s in e.sub_exprs:
            r = self.contains_next(s)
            if r:
                return True
        return False
    
    def trs_theory(self):
        self.transition_theory = TheoryBlock(name=self.name+'_transition',vocab_name=self.vocab_name+'_next',ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
        cnstrs = []
        for c in self.constraints:
            n = self.contains_next(c)
            if n:
                r = self.bis_subexpr(c.init_copy())
                if r != False:
                    cnstrs.append(r)
            else:
                r = self.sis_subexpr(c.init_copy())
                r2 = self.bis_subexpr(c.init_copy())
                if r != False:
                    cnstrs.append(r)
                    cnstrs.append(r2)
        defs = []
        for definition in self.definitions:
            defs.append(Definition(None,Annotations(None,[]),definition.mode_str,[]))
            for rule in definition.rules:
                rl = rule.init_copy()
                if isinstance(rule.definiendum,NextAppliedSymbol):
                    r = self.bis_rule(rl)
                    if r != False:
                        defs[-1].rules.append(r)
                elif isinstance(rule.definiendum,NowAppliedSymbol):
                    rl2 = rl.init_copy()
                    rl.definiendum = self.bis_subexpr(rl.definiendum)
                    rl.body = self.bis_subexpr(rl.definiendum)
                    if rl.body != False:
                        defs[-1].rules.append(rl)
                    rl2.definiendum = self.sis_subexpr(rl2.definiendum)
                    rl2.body = self.sis_subexpr(rl2.definiendum)
                    if rl2.body != False:
                        defs[-1].rules.append(rl2)
                elif not isinstance(rule.definiendum,StartAppliedSymbol):
                    if self.contains_now(rl.body):
                        rl2 = rl.init_copy()
                        rl.body = self.bis_subexpr(rl.definiendum)
                        if rl.body != False:
                            defs[-1].rules.append(rl)
                        rl2.body = self.sis_subexpr(rl2.definiendum)
                        if rl2.body != False:
                            defs[-1].rules.append(rl2)
                    else:
                        rl.body = self.sis_subexpr(rl.definiendum)
                        if rl.body != False:
                            defs[-1].rules.append(rl)
        self.transition_theory.constraints = cnstrs
        self.transition_theory.definitions = defs
        for d in defs:
            for r in d.rules:
                r.block = self.transition_theory
        for i in self.interpretations.values():
            r = i.initialize_temporal_interpretation([])
            self.transition_theory.interpretations[r.name] = r
        

    def bst_theory(self):
        self.bistate_theory = TheoryBlock(name=self.name+'_next',vocab_name=self.vocab_name+'_next',ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
        cnstrs = []
        for c in self.constraints:
            #would this be used before start/now are removed or after ?\
            # look how this is done?
            n = self.contains_next(c)
            if n:
                r = self.bis_subexpr(c.init_copy())
                if r != False:
                    cnstrs.append(r)
            else:
                r = self.sis_subexpr(c.init_copy())
                if r != False:
                    cnstrs.append(r)
        defs = []
        for definition in self.definitions:
            defs.append(Definition(None,Annotations(None,[]),definition.mode_str,[]))
            for rule in definition.rules:
                defs[-1].rules.append(self.bis_rule(rule.init_copy()))
                if defs[-1].rules[-1] == False:
                    defs[-1].rules.pop()
            #self.init_theory.definitions.append(idef)
        #self.init_theory.constraints = cnstrs
        self.bistate_theory.constraints = cnstrs
        self.bistate_theory.definitions = defs
        for d in defs:
            for r in d.rules:
                r.block = self.bistate_theory
        
            
    
    def initialize_theory(self):
        self.init_theory = TheoryBlock(name=self.name+'_now',vocab_name=self.vocab_name+'_now',ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
        cnstrs = []
        for c in self.constraints:
            #would this be used before start/now are removed or after ?\
            # look how this is done?
            r = self.init_subexpr(c.init_copy())
            if r != False:
                self.init_theory.constraints.append(r)
        for definition in self.definitions:
            self.init_theory.definitions.append(Definition(None,Annotations(None,[]),definition.mode_str,[]))
            for rule in definition.rules:
                self.init_theory.definitions[-1].rules.append(self.init_rule(rule.init_copy()))
                if self.init_theory.definitions[-1].rules[-1] == False:
                    self.init_theory.definitions[-1].rules.pop()

    def sis_subexpr(self, expression:Expression):
        if isinstance(expression, (StartAppliedSymbol,NextAppliedSymbol)):
            return False
        if isinstance(expression, NowAppliedSymbol):
            e = expression.sub_expr
            symb = SymbolExpr(None,(str(e.symbol)+'_next'),None,None)
            return AppliedSymbol(None,symb,e.sub_exprs,None,e.is_enumerated,e.is_enumeration,e.in_enumeration)
        if isinstance(expression,(AppliedSymbol,UnappliedSymbol)):
            return expression
        #sbex : List[Expression] = []
        i = 0
        for e in expression.sub_exprs:
            expression.sub_exprs[i] = self.sis_subexpr(e)
            if expression.sub_exprs[i] == False:
                return False
            i+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
        #expression.sub_exprs = sbex
        return expression


    def bis_subexpr(self, expression:Expression):
        if isinstance(expression, StartAppliedSymbol):
            return False
        if isinstance(expression, NowAppliedSymbol):
            return expression.sub_expr
        if isinstance(expression, NextAppliedSymbol):
            e = expression.sub_expr
            symb = SymbolExpr(None,(str(e.symbol)+'_next'),None,None)
            return AppliedSymbol(None,symb,e.sub_exprs,None,e.is_enumerated,e.is_enumeration,e.in_enumeration)
        if isinstance(expression,(AppliedSymbol,UnappliedSymbol)):
            return expression
        #sbex : List[Expression] = []
        i = 0
        for e in expression.sub_exprs:
            expression.sub_exprs[i] = self.bis_subexpr(e)
            if expression.sub_exprs[i] == False:
                return False
            i+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
        #expression.sub_exprs = sbex
        return expression

    def init_subexpr(self, expression:Expression):
        if isinstance(expression, StartAppliedSymbol):
            return expression.sub_expr
        if isinstance(expression, NowAppliedSymbol):
            return expression.sub_expr
        if isinstance(expression, NextAppliedSymbol):
            return False
        if isinstance(expression,(AppliedSymbol,UnappliedSymbol)):
            return expression
        #sbex : List[Expression] = []
        i = 0
        for e in expression.sub_exprs:
            expression.sub_exprs[i] = self.init_subexpr(e)
            if expression.sub_exprs[i] == False:
                return False
            i+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
        #expression.sub_exprs = sbex
        return expression
    
    def init_subexpr2(self, expression:Expression):
        i = 0
        for e in expression.sub_exprs:
            if isinstance(e, (StartAppliedSymbol,NowAppliedSymbol) ):
                expression.sub_exprs[i] = e.sub_expr
            elif isinstance(e, NextAppliedSymbol):
                return False
            elif isinstance(e,(AppliedSymbol,UnappliedSymbol)):
                return 
            else:
                r = self.init_subexpr2(e)
                if r == False:
                    return False
            i+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
    
    def bis_rule(self, rule: Rule):
        next = False
        now = False
        if isinstance(rule.definiendum,StartAppliedSymbol):
            return False
        if isinstance(rule.definiendum,(NextAppliedSymbol,NowAppliedSymbol)):
            if isinstance(rule.definiendum,(NowAppliedSymbol)):
                now = True
            else:
                next = True
            e = rule.definiendum.sub_expr
            symb = SymbolExpr(None,(str(e.symbol)+'_next'),None,None)
            rule.definiendum = AppliedSymbol(None,symb,e.sub_exprs,None,e.is_enumerated,e.is_enumeration,e.in_enumeration)
            
        if next:
            rule.body = self.bis_subexpr(rule.body)
        elif now:
            rule.body = self.sis_subexpr(rule.body)
        else:
            rule.body = self.sis_subexpr(rule.body)
        if rule.body == False:
                return False
        return rule
    

    def init_rule(self, rule: Rule):
        if isinstance(rule.definiendum,NextAppliedSymbol):
            return False
        if isinstance(rule.definiendum,(NowAppliedSymbol,StartAppliedSymbol)):
            rule.definiendum = rule.definiendum.sub_expr
        #using init_subexpr for the subexpressions of body 
        if isinstance(rule.body,NextAppliedSymbol):
            return False
        if isinstance(rule.body,(NowAppliedSymbol,StartAppliedSymbol)):
            rule.body = rule.body.sub_expr
        elif isinstance(rule.body,(AppliedSymbol,UnappliedSymbol)): 
            rule.body
        else:
            r = self.init_subexpr2(rule.body)
            if r == False:
                return False
        #rule.body = self.init_subexpr(rule.body)
        return rule

class Definition(Expression):
    """ The class of AST nodes representing an inductive definition.

    Attributes:
        id (num): unique identifier for each definition

        rules ([Rule]):
            set of rules for the definition, e.g., `!x: p(x) <- q(x)`

        renamed (dict[Declaration, List[Rule]]):
            rules with normalized body for each defined symbol,
            e.g., `!x: p(x) <- q(p1_)`
            (quantees and head are unchanged)

        canonicals (dict[Declaration, List[Rule]]):
            normalized rule for each defined symbol,
            e.g., `! p1_: p(p1_) <- q(p1_)`

        clarks (dict[Declaration, Transformed Rule]):
            normalized rule for each defined symbol (used to be Clark completion)
            e.g., `! p1_: p(p1_) <=> q(p1_)`

        def_vars (dict[String, dict[String, Variable]]):
            Fresh variables for arguments and result

        inductive (set[SymbolDeclaration])
            set of SymbolDeclaration with an inductive definition

        cache (dict[SymbolDeclaration, str, Expression]):
            cache of instantiation of the definition

        inst_def_level (int): depth of recursion during instantiation

    """
    definition_id = 0  # intentional static variable so that no two definitions get the same ID

    def __init__(self, parent, annotations: Optional[Annotations], mode, rules):
        Definition.definition_id += 1
        self.id = Definition.definition_id
        self.mode_str = mode
        self.mode = (S.WELLFOUNDED if mode is None or 'well-founded' in mode else
                     S.COMPLETION if 'completion' in mode else
                     S.KRIPKEKLEENE if 'Kripke-Kleene' in mode else
                     S.COINDUCTION if 'co-induction' in mode else
                     S.STABLE if 'stable' in mode else
                     S.RECDATA if 'recursive' in mode else
                     mode)
        assert type(self.mode) == S, f"Unsupported mode: {mode}"
        self.annotations : Annotation = annotations.annotations if annotations else {}
        self.rules: List[Rule] = rules
        self.renamed: dict[SymbolDeclaration, List[Rule]] = {}
        self.clarks: dict[SymbolDeclaration, Rule] = {}
        self.canonicals: dict[SymbolDeclaration, List[Rule]] = {}
        self.def_vars: dict[str, Variable] = {}
        self.inductive: set[SymbolDeclaration] = set()
        self.cache: dict[Tuple[Declaration, str], Expression] = {}  # {decl, str: Expression}
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

    def get_def_constraints(self,
                            problem,
                            for_explain: bool = False
                            ) -> dict[Tuple[SymbolDeclaration, Definition], List[Expression]]:
        raise IDPZ3Error("Internal error") # monkey-patched

    def instantiate_definition(self, decl, new_args, theory):
        raise IDPZ3Error("Internal error") # monkey-patched


class Rule(Expression):
    def __init__(self, parent,
                 annotations: Annotations,
                 quantees: List[Quantee],
                 definiendum: AppliedSymbol,
                 out: Expression,
                 body: Expression):
        self.annotations: Annotation = (annotations.annotations if annotations else
                            {'reading': str(self)})
        self.quantees = quantees
        self.definiendum = definiendum
        self.out = out
        self.body = body
        self.has_finite_domain = None  # Bool
        self.block = None  # theory where it occurs

        split_quantees(self)

        if self.body is None:
            self.body = TRUE
        self.original = None

    def __repr__(self):
        quant = ('' if not self.quantees else
                 f"∀ {','.join(str(q) for q in self.quantees)}: ")
        return (f"{quant}{self.definiendum} "
                f"{(' = ' + str(self.out)) if self.out else ''}"
                f"← {str(self.body)}")

    def __str__(self): return repr(self)

    def __deepcopy__(self, memo):
        cls = self.__class__ # Extract the class of the object
        out = cls.__new__(cls) # Create a new instance of the object based on extracted class
        memo[id(self)] = out
        out.__dict__.update(self.__dict__)

        out.definiendum = deepcopy(self.definiendum)
        out.definiendum.sub_exprs = [deepcopy(e) for e in self.definiendum.sub_exprs]
        out.out = deepcopy(self.out)
        out.body = deepcopy(self.body)
        return out
    
    def init_copy(self,parent=None):
        definiendum =None
        body =None
        quantees =[]
        out=None
        if self.definiendum:
            definiendum = self.definiendum.init_copy()
        if self.out:
            out = self.out.init_copy()
        if self.body:
            body = self.body.init_copy()
        if self.quantees:
            quantees = [q.init_copy() for q in self.quantees]

        return Rule(parent=parent,definiendum=definiendum,out=out,body=body,quantees=quantees,annotations=Annotations(None,[]))

    def instantiate_definition(self, new_args, theory):
        raise IDPZ3Error("Internal error") # monkey-patched


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
        self.init_struct : Structure= None

    def __str__(self):
        return self.name


class SymbolInterpretation(Expression):
    """
    AST node representing `<symbol> := { <identifiers*> } else <default>.`

    Attributes:
        name (string): name of the symbol being enumerated.

        symbol_decl (SymbolDeclaration): symbol being enumerated

        enumeration ([Enumeration]): enumeration.

        default (Expression): default value (for function enumeration).

        is_type_enumeration (Bool): True if the enumeration is for a type symbol.

    """
    def __init__(self, parent,
                 name: UnappliedSymbol,
                 sign: str,
                 enumeration: Enumeration,
                 default: Optional[Expression]):
        self.name = name.name
        self.sign = sign
        self.enumeration = enumeration
        self.default = default
        self.no_enum = False
        if not self.enumeration:
            self.no_enum = True
            self.enumeration = Enumeration(parent=self, tuples=[])

        self.sign = ('⊇' if self.sign == '>>' else
                     '≜' if self.sign == ':=' else self.sign)
        self.check(self.sign == '≜' or
                   (type(self.enumeration) == FunctionEnum and self.default is None),
                   "'⊇' can only be used with a functional enumeration ('→') without else clause")

        self.symbol_decl: Optional[SymbolDeclaration] = None
        self.is_type_enumeration = None
        self.block = None

    def __repr__(self):
        return f"{self.name} {self.sign} {self.enumeration}"

    def __str__(self) -> str:
        return f"{self.name} {self.sign} {self.enumeration}"

    def interpret_application(self, rank, applied, args, tuples=None):
        """returns an expression equivalent to `self.symbol` applied to `args`,
        simplified by the interpretation of `self.symbol`.

        This is a recursive function.

        Example: assume `f>>{(1,2)->A, (1, 3)->B, (2,1)->C}` and `args=[g(1),2)]`.
        The returned expression is:
        ```
        if g(1) = 1 then A
        else if g(1)=2 then f(g(1),2)
        else f(g(1),2)
        ```

        Args:
            rank (Int): iteration number (from 0)

            applied (AppliedSymbol): template to create new AppliedSymbol
                (ex: `g(1),a()`, before interpretation)

            args (List(Expression)): interpreted arguments applied to the symbol (ex: `g(1),2`)

            tuples (OrderedSet[TupleIDP], optional): relevant tuples for this iteration.
                Initialized with `[[1,2,A], [1,3,B], [2,1,C]]`

        Returns:
            Expression: Grounded interpretation of self.symbol applied to args
        """
        if tuples == None:
            tuples = self.enumeration.sorted_tuples
            if all(a.is_value() for a in args):  # use lookup
                key = ",".join(a.code for a in args)
                if key in self.enumeration.lookup:
                    return self.enumeration.lookup[key]
                elif self.sign == '≜':  # can use default
                    return self.default

        if rank == self.symbol_decl.arity:  # valid tuple -> return a value
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

            if args[rank].is_value():
                for val, tuples2 in groups:  # try to resolve
                    if str(args[rank]) == val:
                        out = self.interpret_application(rank+1,
                                        applied, args, list(tuples2))
            else:
                for val, tuples2 in groups:
                    tuples = list(tuples2)
                    out = IF(
                        EQUALS([args[rank], tuples[0].args[rank]]),
                        self.interpret_application(rank+1,
                                                   applied, args, tuples),
                        out)
            return out
        

    def initialize_temporal_interpretation(self,tempdc) -> SymbolInterpretation:
        enum = None
        if not self.no_enum:
            enum = self.enumeration.init_copy()
        #tempdc : List[TemporalDeclaration] = self.block.voc.tempdcl
        changed = False
        for t in tempdc:
            if (t.symbol.name == self.name) and enum:
                tp = []
                for e in enum.tuples.values():
                    if isinstance(e,FunctionTuple):
                        t_arg = e.args[-2]
                        self.check( type(t_arg) == Number, f"Last argument should be a number for temporal predicates")
                        if t_arg.number == '0':
                            #2 pop to remove the value and time from arg list
                            e.args.pop()
                            e.args.pop()
                            tp.append(FunctionTuple(args=e.args,value=e.value))
                            #initialized_interp.enumeration.tuples.pop(str(e))
                    else:
                        t_arg = e.args[-1]
                        self.check( type(t_arg) == Number, f"Last argument should be a number for temporal predicates")
                        if t_arg.number == '0':
                            e.args.pop()
                            tp.append((type(e))(args=e.args))
                            if len(e.args) == 0:
                                changed =True
                          #initialized_interp.enumeration.tuples.pop(str(e))
                #TO DO : ADD ELSE CASE
                if not isinstance(enum,ConstructedFrom):
                    if isinstance(enum,Ranges):
                        #TO DO how is it possible to return Range type
                        enum = Enumeration(None,tuples=tp)
                    else:
                        enum = (type(enum))(None,tuples=tp)
                break
        default = None
        if self.default:
            default = self.default.init_copy()
        initialized_interp = SymbolInterpretation(parent=None,name= UnappliedSymbol(None,(self.name)),sign = self.sign,
                             enumeration=enum, default=default)
        if changed:
            initialized_interp.enumeration = Enumeration(None,tuples=[])
            initialized_interp.default = TRUE
            #if not changed:

        return initialized_interp
                    

class Enumeration(Expression):
    """Represents an enumeration of tuples of expressions.
    Used for predicates, or types without n-ary constructors.

    Attributes:
        tuples (OrderedSet[TupleIDP]): OrderedSet of TupleIDP of Expression

        sorted_tuples: a sorted list of tuples

        lookup: dictionary from arguments to values

        constructors (List[Constructor], optional): List of Constructor
    """
    def __init__(self, parent:ASTNode|None, tuples: List[TupleIDP]):
        self.sorted_tuples = sorted(tuples, key=lambda t: t.code)  # do not change dropdown order
        self.tuples: Optional[OrderedSet] = OrderedSet(tuples)

        self.lookup: dict[str, Expression] = {}
        self.constructors: Optional[List[Constructor]]
        if all(len(c.args) == 1 and type(c.args[0]) == UnappliedSymbol
               for c in self.tuples):
            self.constructors = [CONSTRUCTOR(c.args[0].name)
                                 for c in self.tuples]
        else:
            self.constructors = None

    def init_copy(self,parent=None):
        tp = [t.init_copy(None) for t in self.tuples.values()]
        return Enumeration(parent=parent,tuples=tp)

    def __repr__(self):
        return (f'{{{", ".join([repr(t) for t in self.tuples])}}}' if self.tuples else
                f'{{{", ".join([repr(t) for t in self.constructors])}}}')

    def __str__(self) -> str:
        return repr(self)
    
    def contains(self, args,
                 arity: Optional[int] = None,
                 rank: int = 0,
                 tuples: Optional[List[TupleIDP]] = None,
                 theory: Optional[Theory] = None
                 ) -> Expression:
        """ returns an Expression that says whether Tuple args is in the enumeration """

        if arity is None:
            arity = len(args)
        if rank == arity:  # valid tuple
            return TRUE
        if tuples is None:
            tuples = self.sorted_tuples

        # constructs If-then-else recursively
        groups = groupby(tuples, key=lambda t: str(t.args[rank]))
        if args[rank].is_value():
            for val, tuples2 in groups:  # try to resolve
                if str(args[rank]) == val:
                    return self.contains(args, arity, rank+1, list(tuples2),
                                theory=theory)
            return FALSE
        else:
            if rank + 1 == arity:  # use OR
                equalities = [ EQUALS([args[rank], t.args[rank]])
                        for t in tuples]
                out = OR(equalities)
                out.enumerated = ', '.join(str(c) for c in tuples)
                return out
            out = FALSE
            for val, tuples2 in groups:
                tuples = list(tuples2)
                out = IF(EQUALS([args[rank], tuples[0].args[rank]]),
                    self.contains(args, arity, rank+1, tuples, theory),
                    out)
            return out

    def extensionE(self,
                   extensions: Optional[dict[str, Extension]]=None
                  ) -> Extension:
        """computes the extension of an enumeration, i.e., a set of tuples and a filter

        Args:
            interpretations (dict[str, &quot;SymbolInterpretation&quot;], optional): _description_. Defaults to None.
            extensions (dict[str, Extension], optional): _description_. Defaults to None.

        Returns:
            Extension: _description_
        """
        # assert all(c.range is not None for c in self.constructors)
        ranges = [c.range for c in self.constructors]
        return ([[t] for r in ranges for t in r], None)


class FunctionEnum(Enumeration):
    def extensionE(self,
                   extensions: Optional[dict[str, Extension]] = None
                  ) -> Extension:
        self.check(False,
                   f"Can't use function enumeration for type declaration or quantification")
        return (None, None)  # dead code
    
    def init_copy(self,parent=None):
        tp = [t.init_copy(None) for t in self.tuples.values()]
        return FunctionEnum(parent=parent,tuples=tp)

class CSVEnumeration(Enumeration):
    def init_copy(self,parent=None):
        tp = [t.init_copy(None) for t in self.tuples.values()]
        return CSVEnumeration(parent=parent,tuples=tp)
    pass


class ConstructedFrom(Enumeration):
    """Represents a 'constructed from' enumeration of constructors

    Attributes:
        tuples (OrderedSet[TupleIDP], Optional): OrderedSet of tuples of Expression

        constructors (List[Constructor]): List of Constructor

        accessors (dict[str, int]): index of the accessor in the constructors
    """
    def __init__(self, parent: Optional[ASTNode],
                 constructed: str,
                 constructors: List[Constructor]):
        self.constructed = constructed
        self.constructors = constructors
        self.tuples: Optional[OrderedSet] = None
        self.accessors: dict[str, int] = dict()

    def init_copy(self,parent=None):
        cnstr = [c.init_copy() for c in self.constructors]
        return ConstructedFrom(parent=parent,constructed=self.constructed,constructors=cnstr)
    
    def contains(self, args,
                 arity: Optional[int] = None,
                 rank: int = 0,
                 tuples: Optional[List[TupleIDP]] = None,
                 theory: Optional[Theory] = None
                 ) -> Expression:
        """returns True if args belong to the type enumeration"""
        # args must satisfy the tester of one of the constructors
        #TODO add tests
        assert len(args) == 1, f"Incorrect arity in {self.parent.name}{args}"
        if type(args[0].decl) == Constructor:  # try to simplify it
            self.check(self.parent.name == args[0].decl.codomain,
                       f"Incorrect type of {args[0]} for {self.parent.name}")
            self.check(len(args[0].sub_exprs) == len(args[0].decl.domains),
                       f"Incorrect arity")
            return AND([t.decl.codomain.has_element(e, theory.extensions)
                        for e,t in zip(args[0].sub_exprs, args[0].decl.domains)])
        out = [AppliedSymbol.construct(constructor.tester, args)
                for constructor in self.constructors]
        return OR(out)

    def extensionE(self,
                   extensions: Optional[dict[str, Extension]] = None
                  ) -> Extension:
        def filter(args):
            if type(args[0]) != Variable and type(args[0].decl) == Constructor:  # try to simplify it
                #TODO add tests
                self.check(self.parent.name == args[0].decl.codomain,
                        f"Incorrect type of {args[0]} for {self.parent.name}")
                self.check(len(args[0].sub_exprs) == len(args[0].decl.domains),
                        f"Incorrect arity")
                return AND([t.decl.codomain.has_element(e, extensions)
                            for e,t in zip(args[0].sub_exprs, args[0].decl.domains)])
            out = [AppliedSymbol.construct(constructor.tester, args)
                    for constructor in self.constructors]
            return OR(out)  # return of filter()
        return (([t.args for t in self.tuples], None) if self.tuples else
                (None, filter))


class TupleIDP(Expression):
    def __init__(self, **kwargs):
        self.args: List[Identifier] = kwargs.pop('args')
        self.code = intern(",".join([str(a) for a in self.args]))

    def __str__(self):
        return self.code
    
    def init_copy(self,parent=None):
        a = [i.init_copy() for i in self.args]
        return TupleIDP(args=a)

    def __repr__(self):
        return f"({self.code})" if 1 < len(self.args) else self.code


class FunctionTuple(TupleIDP):
    def __init__(self, **kwargs):
        self.args = kwargs.pop('args')
        if not isinstance(self.args, list):
            self.args = [self.args]
        self.value = kwargs.pop('value')
        self.args.append(self.value)
        self.code = intern(",".join([str(a) for a in self.args]))

    def init_copy(self,parent=None):
        a = [i.init_copy() for i in self.args]
        a.pop()
        return FunctionTuple(args=a,value=self.value.init_copy())

class CSVTuple(TupleIDP):
    def init_copy(self,parent=None):
        a = [i.init_copy() for i in self.args]
        return CSVTuple(args=a)
    pass


class Ranges(Enumeration):
    def __init__(self, parent:ASTNode, **kwargs):
        self.elements = kwargs.pop('elements')

        tuples: List[TupleIDP] = []
        self.type: Optional[SetName] = None
        if self.elements:
            self.type = self.elements[0].fromI.type
            for x in self.elements:
                if x.fromI.type != self.type:
                    if self.type in [INT_SETNAME, REAL_SETNAME] and x.fromI.type in [INT_SETNAME, REAL_SETNAME]:
                        self.type = REAL_SETNAME  # convert to REAL
                        tuples = [TupleIDP(args=[n.args[0].real()])
                                  for n in tuples]
                    else:
                        self.check(False,
                            f"incorrect value {x.fromI} for {self.type}")

                if x.toI is None:
                    tuples.append(TupleIDP(args=[x.fromI]))
                elif self.type == INT_SETNAME and x.fromI.type == INT_SETNAME and x.toI.type == INT_SETNAME:
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        tuples.append(TupleIDP(args=[Number(number=str(i))]))
                elif self.type == REAL_SETNAME and x.fromI.type == INT_SETNAME and x.toI.type == INT_SETNAME:
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        tuples.append(TupleIDP(args=[Number(number=str(float(i)))]))
                elif self.type == REAL_SETNAME:
                    self.check(False, f"Can't have a range over real: {x.fromI}..{x.toI}")
                elif self.type == DATE_SETNAME and x.fromI.type == DATE_SETNAME and x.toI.type == DATE_SETNAME:
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        d = Date(iso=f"#{date.fromordinal(i).isoformat()}")
                        tuples.append(TupleIDP(args=[d]))
                else:
                    self.check(False, f"Incorrect value {x.toI} for {self.type}")
        Enumeration.__init__(self, parent=parent, tuples=tuples)

    def init_copy(self,parent=None):
        el = [copy(e) for e in self.elements]
        return Ranges(parent=parent,elements=el)

    def contains(self, args,
                 arity: Optional[int] = None,
                 rank: int = 0,
                 tuples: Optional[List[TupleIDP]] = None,
                 theory: Optional[Theory] = None
                 ) -> Expression:
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

    def extensionE(self,
                   extensions: Optional[dict[str, Extension]] = None
                  ) -> Extension:
        if not self.elements:
            return(None, None)
        if self.tuples is not None: # and len(self.tuples) < MAX_QUANTIFIER_EXPANSION:
            return ([t.args for t in self.tuples], None)
        def filter(args):
            sub_exprs = []
            for x in self.elements:
                if x.toI is None:
                    e = EQUALS([args[0], x.fromI])
                else:
                    e = AComparison.make('≤', [x.fromI, args[0], x.toI])
                sub_exprs.append(e)
            return OR(sub_exprs)
        return(None, filter)


class RangeElement(Expression):
    def __init__(self, **kwargs):
        self.fromI = kwargs.pop('fromI')
        self.toI = kwargs.pop('toI')


class IntRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, parent=self, elements=[])
        self.type = INT_SETNAME
        self.tuples = None

    def init_copy(self,parent=None):
        r = super().init_copy(parent)
        r.type= INT_SETNAME
        r.tuples =None
        return r

    def extensionE(self,
                   extensions: Optional[dict[str, Extension]] = None
                  ) -> Extension:
        return (None, None)

#For natural numbers  
class NatRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, fromI =0 , toI=5,elements=[])
        self.type = ABS
        self.tuples = None

    def init_copy(self,parent=None):
        r = super().init_copy(parent)
        r.type= INT
        r.tuples =None
        return r

    def extensionE(self,
                   extensions: Optional[dict[str, Extension]] = None
                  ) -> Extension:
        return (None, None)



class RealRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, parent=self, elements=[])
        self.type = REAL_SETNAME
        self.tuples = None
    def init_copy(self,parent=None):
        r = super().init_copy(parent)
        r.type= REAL
        r.tuples =None
        return r

    def extensionE(self,
                   extensions: Optional[dict[str, Extension]] = None
                  ) -> Extension:
        return (None, None)


class DateRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, parent=self, elements=[])
        self.type = DATE_SETNAME
        self.tuples = None
    
    def init_copy(self,parent=None):
        r = super().init_copy(parent)
        r.type= DATE
        r.tuples =None
        return r

    def extensionE(self,
                   extensions: Optional[dict[str, Extension]] = None
                  ) -> Extension:
        return (None, None)


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
        self.voc = None

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
                self.check(constraint.symbol.name,
                           f"Invalid syntax: {constraint}")  # SymbolExpr $()
                name = constraint.symbol.name
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
                self.check(constraint.sub_exprs[0].symbol.name,
                           f"Invalid syntax: {constraint}")
                if constraint.sub_exprs[0].symbol.name == 'view':
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

                                         Vocabulary, Import, VarDeclaration,
                                         TypeDeclaration, Accessor, SetName,
                                         SymbolDeclaration,TemporalDeclaration,
                                         SymbolExpr,

                                         TheoryBlock, Definition, Rule, AIfExpr,
                                         AQuantification, Quantee, ARImplication,
                                         AEquivalence, AImplication,
                                         ADisjunction, AConjunction,
                                         AComparison, ASumMinus, AMultDiv,
                                         APower, AUnary, AAggregate,
                                         AppliedSymbol, UnappliedSymbol,StartAppliedSymbol,NowAppliedSymbol,NextAppliedSymbol,
                                         Number, Brackets, Date, Variable,

                                         Structure, SymbolInterpretation,
                                         Enumeration, FunctionEnum, CSVEnumeration,
                                         TupleIDP, FunctionTuple, CSVTuple,
                                         ConstructedFrom, Constructor, Ranges,
                                         RangeElement, Display,

                                         Procedure, Call1, String,
                                         PyList, PyAssignment])
