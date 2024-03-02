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
from itertools import groupby, product
from os import path
from sys import intern
from textx import metamodel_from_file
from typing import Any, Tuple, List, Union, Optional, TYPE_CHECKING



from .Assignments import Assignments
from .Expression import (Annotations, Annotation, ASTNode, CLFormula, Constructor, CONSTRUCTOR,
                         Accessor, DLFormula, FLFormula, GLFormula, ILFormula, LFormula, NLFormula, NextAppliedSymbol, NowAppliedSymbol, RLFormula, StartAppliedSymbol, SymbolExpr, Expression,
                         AIfExpr, IF, AQuantification, ULFormula, WLFormula, XLFormula, split_quantees, SetName,
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
        self.temporallogicformulas = self.dedup_nodes(kwargs, 'temporallogicformulas')
        displays = kwargs.pop('displays')
        self.procedures = self.dedup_nodes(kwargs, 'procedures')

        assert len(displays) <= 1, "Too many display blocks"
        self.display = displays[0] if len(displays) == 1 else None
        self.now_voc = {}
        self.next_voc = {}
        init_thrs ={}
        init_strcs ={}
        #print("annotating begins............")
        for voc in self.vocabularies.values():
            #Annotating vocabulary for current and next time point; useful for LTC theories
            #For v_now the time argument of temporal predicates would be dropped e.g p(x,time) becomes p(x)
            #For v_next in addition to above an other prdicate p_next(x) would be added
            now_voc:Vocabulary = voc.generate_now_voc()
            self.now_voc[now_voc.name]=now_voc
            now_voc.annotate_block(self)
            #print("voc now")
            next_voc = voc.generate_next_voc()
            self.next_voc[next_voc.name]=next_voc
            next_voc.annotate_block(self)
            #print("voc next")

            voc.annotate_block(self)
            #if len(voc.tempdcl) > 0:
                #voc.transitiongraph = TransiotionGraph(voc)
                #print("tandsition graph")
                #print(voc.transitiongraph.states)
            #print("voc annot")
        for t in self.theories.values():
            if t.ltc:
                #Adds initialized version of LTC theory: For more info check progression document of IDP.
                t.initialize_theory()
                #print("theories init")
                #Adds bistate theory
                t.bst_theory()
                #print("theories bis")
                #Adds transition theory which is used for invariants: For more info check the paper Simulating dynamic systems with LTC 
                t.trs_theory()
                #print("theories trs")
                t.original_theory()
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
        #for v in self.now_voc.values():
        #    self.vocabularies[v.name] = v
        #for v in self.next_voc.values():
        #    self.vocabularies[v.name] = v
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
                 tempdcl:List[TemporalDeclaration]|None):
        self.name = name
        #List of temporal predicates
        self.tempdcl = tempdcl
        if tempdcl is None:
            self.tempdcl = []
        self.idp : Optional[IDP] = None  # parent object
        self.symbol_decls: dict[str, Union[Declaration, VarDeclaration, Constructor]] = {}
        self.contains_temporal = False

        self.name = 'V' if not self.name else self.name
        self.voc = self
        self.actions : List[str] =[]
        self.fluents : List[str] =[]
        self.ftemproral : List[str] =[]
        self.transitiongraph : TransiotionGraph = None
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
                    if decl.temporal is not None:
                        self.tempdcl.append(TemporalDeclaration(symbol=SymbolExpr(None,name=new.name,eval=None,s=None)))
                    if decl.temporal == "Action":
                        self.actions.append(new.name)
                    elif decl.temporal == "Temporal":
                        self.fluents.append(new.name)
                    elif decl.temporal == "FTemporal":
                        self.ftemproral.append(new.name)
                    
            else:
                temp.append(decl)
        self.declarations = temp
        #Used in generation of now and next vocabularies
        self.original_decl = temp

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
    def fullstr(self):
        return (f"vocabulary {self.name} {{{NEWL}"
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

    #Used for forward chaining
    def generate_expanded_voc(self,n:int) -> Vocabulary:
        nowvoc = Vocabulary(parent=None,name=self.name+"_expanded",tempdcl=[],declarations=[])
        for d in self.original_decl:
            changed = False
            for t in self.tempdcl:
                if isinstance(d,SymbolDeclaration):
                    #The predicate is temporal
                    if d.name == t.symbol.name:
                        changed = True
                        sr = [s.init_copy() for s in d.sorts]
                        sr.pop()
                        id = SymbolDeclaration(parent=None,name=(d.name),sorts=sr,out=d.out.init_copy(),annotations=Annotations(None,[]))
                        nowvoc.declarations.append(id)
                        i = 1 
                        while i <= n:
                            srs = [s.init_copy() for s in d.sorts]
                            srs.pop()
                            #TO DO: There could be possible issues with naming
                            ids = SymbolDeclaration(parent=None,name=(d.name+"_"+str(i)),sorts=srs,out=d.out.init_copy(),annotations=Annotations(None,[]))
                            nowvoc.declarations.append(ids)
                            i+=1
                        break
            if not changed:
                if isinstance(d,VarDeclaration):
                    nowvoc.declarations.append(VarDeclaration(parent=None,name=(d.name),subtype=d.subtype.init_copy()))
                elif isinstance(d,SymbolDeclaration):
                    sr = [s.init_copy() for s in d.sorts]
                    nowvoc.declarations.append(SymbolDeclaration(parent=None,name=(d.name),sorts=sr,out=d.out,annotations=Annotations(None,[])))
                elif isinstance(d,TypeDeclaration):
                    enum =None
                    if d.interpretation:
                        enum = d.interpretation.enumeration.init_copy()
                    cnstr = [c.init_copy() for c in d.constructors]
                    if len(cnstr) ==0:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,enumeration=enum))
                    else:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,constructors=cnstr,enumeration=enum))
                elif isinstance(d,Import):
                    d
                else:
                    nowvoc.declarations.append(d.init_copy())
        return nowvoc

    #Used for generating the vocabulary of current time, used in the context of LTC theories
    #Has to be called before self is annotated
    #TO DO: Merge common parts of now and next voc methods            
    def generate_now_voc(self):
        nowvoc = Vocabulary(parent=None,name=self.name+'_now',tempdcl=[],declarations=[])
        for d in self.original_decl:
            changed = False
            for t in self.tempdcl:
                if isinstance(d,SymbolDeclaration):
                    #The predicate is temporal
                    if d.name == t.symbol.name:
                        changed = True
                        sr = [s.init_copy() for s in d.sorts]
                        id = SymbolDeclaration(parent=None,name=(d.name),sorts=sr,out=d.out,annotations=Annotations(None,[]))
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
                        enum = d.interpretation.enumeration.init_copy()
                    cnstr = [c.init_copy() for c in d.constructors]
                    if len(cnstr) ==0:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,enumeration=enum))
                    else:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,constructors=cnstr,enumeration=enum))
                elif isinstance(d,Import):
                    #Not adding import because the declarations there would then get their voc now or next which should not be the case
                    #TO DO: create new declarations for the improted vocabs in annotating now or next voc
                    #TO DO: create tests with import and LTC theories 
                    d
                else:
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
                        #Current time predicate
                        id = SymbolDeclaration(parent=None,name=d.name,sorts=sr,out=d.out,annotations=Annotations(None,[]))
                        nowvoc.declarations.append(id)
                        srn = [s.init_copy() for s in d.sorts]
                        #Next time predicate
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
                        enum = d.interpretation.enumeration.init_copy()
                    cnstr = [c.init_copy() for c in d.constructors]
                    if len(cnstr) ==0:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,enumeration=enum))
                    else:
                        nowvoc.declarations.append(TypeDeclaration(parent=None,name=d.name,constructors=cnstr,enumeration=enum))
                elif isinstance(d,Import):
                    d
                else:
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
        if not enumeration:
            return (f"type {self.name} {''}")
        else:
            return (f"type {enumeration}")
        #return (f"type {self.name} {'' if not enumeration else ':= ' + enumeration}")

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
                 name: Optional[str] = None,
                 temporal: Optional[str] = None):
        #temp_symbol  = kwargs.pop('temporal')
        self.annotations : Annotation = annotations.annotations if annotations else {}
        #Indicating if the predicate is a temporal one
        self.temp= False
        self.symbols : Optional[List[str]]
        self.name : Optional[str]
        self.is_next = False
        self.temporal = temporal
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
        self.symbol = kwargs.pop('symbol')

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
        #Indicating if it is an LTC theory
        self.ltc = True if kwargs.pop('ltc') else False
        #Indicating if it is an invariant
        self.inv = True if kwargs.pop('inv') else False
        self.idp =None

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
        # For storing the initialized, bistate and transition theory for ltc theories
        self.init_theory : TheoryBlock = None
        self.bistate_theory : TheoryBlock = None
        self.transition_theory : TheoryBlock = None
        self.org_theory : TheoryBlock = None

    def __str__(self):
        return self.name
    
    
    def replace_with_n(self,expression:Expression,i,n):
        if isinstance(expression,(StartAppliedSymbol)):
            return False
        if isinstance(expression,(NextAppliedSymbol)):
            if i+1 <= n:
                e = expression.sub_expr
                j = i +1
                symb = SymbolExpr(None,(str(e.symbol)+'_'+str(j)),None,None)
                return self.replace_with_n(AppliedSymbol(None,symb,e.sub_exprs,None,e.is_enumerated,e.is_enumeration,e.in_enumeration),i,n)
            return False
        if isinstance(expression,NowAppliedSymbol):
            e = expression.sub_expr
            symb = None
            if i == 0:
                symb = SymbolExpr(None,(str(e.symbol)),None,None)
            else:
                symb = SymbolExpr(None,(str(e.symbol)+'_'+str(i)),None,None)
            return self.replace_with_n(AppliedSymbol(None,symb,e.sub_exprs,None,e.is_enumerated,e.is_enumeration,e.in_enumeration),i,n)
        if isinstance(expression,(UnappliedSymbol)):
            return expression
        j = 0
        for e in expression.sub_exprs:
            expression.sub_exprs[j] = self.replace_with_n(e,i,n)
            if expression.sub_exprs[j] == False:
                return False
            expression.sub_exprs[j].code =intern(str(expression.sub_exprs[j]))
            expression.sub_exprs[j].str = expression.sub_exprs[j].code
            j+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
        return expression

    #Expand the theory to n next time points
    def expand_theory(self,n:int,vocab:Vocabulary):
        #voc = vocab.generate_expanded_voc(n)
        exp_theory = TheoryBlock(name=self.name+"_expanded",vocab_name=vocab.name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
        cnstrs = []
        for c in self.constraints:
            i = 0
            while i <= n:
                s = self.replace_with_n(c.init_copy(),i,n)
                if s != False:
                    cnstrs.append(s)
                    s.code = intern(str(s))
                    s.str = s.code
                i+=1
        defs = []
        for definition in self.definitions:
            defs.append(Definition(None,Annotations(None,[]),definition.mode_str,[]))
            for rule in definition.rules:
                i = 0 
                while i <= n:
                    r = rule.init_copy()
                    r.definiendum = self.replace_with_n(r.definiendum,i,n)
                    if r.definiendum == False:
                        break
                    if r.out:
                        r.out = self.replace_with_n(r.out,i,n)
                        if r.out == False:
                            break
                    r.body = self.replace_with_n(r.body,i,n)
                    if r.body != False:
                        defs[-1].rules.append(r)
                    i+=1
        exp_theory.constraints = cnstrs
        exp_theory.definitions = defs
        for d in defs:
            for r in d.rules:
                r.block = exp_theory
        for i in self.interpretations.values():
            enum = None
            if not i.no_enum:
                enum = i.enumeration.init_copy()
            default = None
            if i.default:
                default = i.default.init_copy()
            r = SymbolInterpretation(None,UnappliedSymbol(None,i.name),i.sign,enum,default)
            exp_theory.interpretations[r.name] = r
        return exp_theory
    

    #Copies the original theory; used for LTC theories
    def original_theory(self):
        self.org_theory = TheoryBlock(name=self.name,vocab_name=self.vocab_name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
        cnstrs = []
        for c in self.constraints:
            cnstrs.append(c.init_copy())
        defs = []
        for definition in self.definitions:
            defs.append(Definition(None,Annotations(None,[]),definition.mode_str,[]))
            for rule in definition.rules:
                #print("org rule sl k")
                #print(rule)
                r = rule.init_copy()
                defs[-1].rules.append(r)
        self.org_theory.constraints = cnstrs
        self.org_theory.definitions = defs
        for d in defs:
            for r in d.rules:
                r.block = self.org_theory
        for i in self.interpretations.values():
            enum = None
            if not i.no_enum:
                enum = i.enumeration.init_copy()
            default = None
            if i.default:
                default = i.default.init_copy()
            r = SymbolInterpretation(None,UnappliedSymbol(None,i.name),i.sign,enum,default)
            self.org_theory.interpretations[r.name] = r

    #checks if an expression contains NextAppliedSymbol
    def contains_next(self,e:Expression):
        if isinstance(e,NextAppliedSymbol):
            return True
        #if isinstance(e,(NowAppliedSymbol,StartAppliedSymbol,UnappliedSymbol)):
        if isinstance(e,(UnappliedSymbol)):
            return False
        for s in e.sub_exprs:
            r = self.contains_next(s)
            if r:
                return True
        return False
    
    #checks if an expression contains NowAppliedSymbol
    def contains_now(self,e:Expression):
        if isinstance(e,NowAppliedSymbol):
            return True
        #if isinstance(e,(NextAppliedSymbol,StartAppliedSymbol,UnappliedSymbol)):
        if isinstance(e,(UnappliedSymbol)):
            return False
        for s in e.sub_exprs:
            r = self.contains_now(s)
            if r:
                return True
        return False
    
    #Initializes the transition thoery; used for LTC theories
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
                    r.code = intern(str(r))
                    r.str = r.code
            else:
                r = self.sis_subexpr(c.init_copy())
                r2 = self.bis_subexpr(c.init_copy())
                if r != False:
                    cnstrs.append(r)
                    cnstrs.append(r2)
                    r.code = intern(str(r))
                    r2.code = intern(str(r2))
                    r.str = r.code
                    r2.str = r2.code
        defs = []
        for definition in self.definitions:
            defs.append(Definition(None,Annotations(None,[]),definition.mode_str,[]))
            for rule in definition.rules:
                rl = rule.init_copy()
                #if isinstance(rule.definiendum,NextAppliedSymbol):
                nx = self.contains_next(rule.definiendum)
                nw = self.contains_now(rule.definiendum)
                if nx:
                    r = self.bis_rule(rl)
                    if r != False:
                        defs[-1].rules.append(r)
                # TO DO: It is more accurate that it gets checked if next is in the body
                elif nw:
                    rl2 = rl.init_copy()
                    rl.definiendum = self.bis_subexpr(rl.definiendum)
                    rl.body = self.bis_subexpr(rl.body)
                    if rl.out:
                        rl.out = self.bis_subexpr(rl.out)
                    if rl.body != False and (rl.out is None or rl.out != False):
                        defs[-1].rules.append(rl)
                        rl.code = intern(str(rl))
                        rl.str = rl.code
                    rl2.definiendum = self.sis_subexpr(rl2.definiendum)
                    rl2.body = self.sis_subexpr(rl2.body)
                    if rl2.out:
                        rl2.out = self.sis_subexpr(rl2.out)
                    if rl2.body != False and (rl2.out is None or rl2.out != False):
                        defs[-1].rules.append(rl2)
                        rl2.code = intern(str(rl2))
                        rl2.str = rl2.code
                #rule definedum does not have start
                elif self.bis_subexpr(rl.definiendum) != False:
                    if self.contains_now(rl.body) and not self.contains_next(rl.body):
                        rl2 = rule.init_copy()
                        rl.body = self.bis_subexpr(rl.body)
                        if rl.out:
                            rl.out = self.bis_subexpr(rl.out)
                        if rl.body != False and (rl.out is None or rl.out != False):
                            defs[-1].rules.append(rl)
                            rl.code = intern(str(rl))
                            rl.str = rl.code
                        rl2.body = self.sis_subexpr(rl2.body)
                        if rl2.out:
                            rl2.out = self.sis_subexpr(rl2.out)
                        if rl2.body != False and (rl2.out is None or rl2.out != False):
                            defs[-1].rules.append(rl2)
                            rl2.code = intern(str(rl2))
                            rl2.str = rl2.code
                    else:
                        rl.body = self.bis_subexpr(rl.body)
                        if rl.out:
                            rl.out = self.bis_subexpr(rl.out)
                        if rl.body != False and (rl.out is None or rl.out != False):
                            defs[-1].rules.append(rl)
                            rl.code = intern(str(rl))
                            rl.str = rl.code
        self.transition_theory.constraints = cnstrs
        self.transition_theory.definitions = defs
        for d in defs:
            for r in d.rules:
                r.block = self.transition_theory
        for i in self.interpretations.values():
            r = i.initialize_temporal_interpretation([])
            self.transition_theory.interpretations[r.name] = r
        
    #Initializes the bistate thoery; used for LTC theories
    def bst_theory(self):
        self.bistate_theory = TheoryBlock(name=self.name+'_next',vocab_name=self.vocab_name+'_next',ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
        cnstrs = []
        for c in self.constraints:
            n = self.contains_next(c)
            if n:
                r = self.bis_subexpr(c.init_copy())
                if r != False:
                    cnstrs.append(r)
                    r.code = intern(str(r))
                    r.str = r.code
            else:
                r = self.sis_subexpr(c.init_copy())
                if r != False:
                    cnstrs.append(r)
                    r.code = intern(str(r))
                    r.str = r.code
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
        
            
    #Initializes the initial thoery; used for LTC theories
    def initialize_theory(self):
        self.init_theory = TheoryBlock(name=self.name+'_now',vocab_name=self.vocab_name+'_now',ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
        cnstrs = []
        for c in self.constraints:
            r = self.init_subexpr(c.init_copy())
            if r != False:
                r.code = intern(str(r))
                r.str = r.code
                self.init_theory.constraints.append(r)
        for definition in self.definitions:
            self.init_theory.definitions.append(Definition(None,Annotations(None,[]),definition.mode_str,[]))
            nextl = []
            nextlquantees = []
            nextlapplieds = []
            nextlout = []
            startnowl = []
            for rule in definition.rules:
                if isinstance(rule.definiendum,NextAppliedSymbol):
                    nextl.append(str(rule.definiendum.sub_expr.symbol))
                    nextlquantees.append(rule.quantees)
                    if rule.out:
                        nextlout.append(rule.out.init_copy())
                    else:
                        nextlout.append(None)
                    nextlapplieds.append(rule.definiendum.sub_expr.init_copy())
                elif isinstance(rule.definiendum,(NowAppliedSymbol,StartAppliedSymbol)):
                    startnowl.append(str(rule.definiendum.sub_expr.symbol))
                self.init_theory.definitions[-1].rules.append(self.init_rule(rule.init_copy()))
                if self.init_theory.definitions[-1].rules[-1] == False:
                    self.init_theory.definitions[-1].rules.pop()
            j = 0
            for nx in nextl:
                if nx in startnowl:
                    pass
                else:
                    qs = [q.init_copy() for q in nextlquantees[j]] 
                    out = None
                    if nextlout[j]:
                        out = self.init_subexpr(nextlout[j])
                        if out == False:
                            out = None
                    r = Rule(None,Annotations(None,[]),qs,nextlapplieds[j],out,FALSE.init_copy())
                    #TO DO; IF YOU UNCOMMENT THIS, THEN MAKE SURE THAT YOU CHECK WITH contains_next and contains_now
                    #self.init_theory.definitions[-1].rules.append(r)
                j += 1

    #Returns the Single state formula transformed to current vocabulary: Now[p(x)] -> p_next(x)
    #Returns false if the expression contains Start or Next
    def sis_subexpr(self, expression:Expression):
        if isinstance(expression, (StartAppliedSymbol,NextAppliedSymbol)):
            return False
        if isinstance(expression, NowAppliedSymbol):
            e = expression.sub_expr
            symb = SymbolExpr(None,(str(e.symbol)+'_next'),None,None)
            return self.sis_subexpr(AppliedSymbol(None,symb,e.sub_exprs,None,e.is_enumerated,e.is_enumeration,e.in_enumeration))
        if isinstance(expression,(UnappliedSymbol)):
            return expression
        #sbex : List[Expression] = []
        i = 0
        for e in expression.sub_exprs:
            expression.sub_exprs[i] = self.sis_subexpr(e)
            if expression.sub_exprs[i] == False:
                return False
            expression.sub_exprs[i].code = intern(str(expression.sub_exprs[i]))
            expression.sub_exprs[i].str = expression.sub_exprs[i].code
            i+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
        #expression.sub_exprs = sbex
        return expression

    #Returns the Bistate state formula transformed to next vocabulary: Now[p(x)] -> p(x) and Next[p(x)] -> p_next(x)
    #Returns false if the expression contains Start
    def bis_subexpr(self, expression:Expression):
        if isinstance(expression, StartAppliedSymbol):
            return False
        if isinstance(expression, NowAppliedSymbol):
            return self.bis_subexpr(expression.sub_expr)
        if isinstance(expression, NextAppliedSymbol):
            e = expression.sub_expr
            symb = SymbolExpr(None,(str(e.symbol)+'_next'),None,None)
            return self.bis_subexpr(AppliedSymbol(None,symb,e.sub_exprs,None,e.is_enumerated,e.is_enumeration,e.in_enumeration))
        if isinstance(expression,(UnappliedSymbol)):
            return expression
        #sbex : List[Expression] = []
        i = 0
        for e in expression.sub_exprs:
            expression.sub_exprs[i] = self.bis_subexpr(e)
            if expression.sub_exprs[i] == False:
                return False
            expression.sub_exprs[i].code = intern(str(expression.sub_exprs[i]))
            expression.sub_exprs[i].str = expression.sub_exprs[i].code
            i+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
        #expression.sub_exprs = sbex
        return expression
    
    #Returns the initial state formula transformed to current vocabulary: Now[p(x)] -> p(x) and Start[p(x)] -> p(x)
    #Returns false if the expression contains Next
    def init_subexpr(self, expression:Expression):
        if isinstance(expression, StartAppliedSymbol):
            return self.init_subexpr(expression.sub_expr)
        if isinstance(expression, NowAppliedSymbol):
            return self.init_subexpr(expression.sub_expr)
        if isinstance(expression, NextAppliedSymbol):
            return False
        if isinstance(expression,(UnappliedSymbol)):
            return expression
        #sbex : List[Expression] = []
        i = 0
        for e in expression.sub_exprs:
            expression.sub_exprs[i] = self.init_subexpr(e)
            if expression.sub_exprs[i] == False:
                return False
            expression.sub_exprs[i].code = intern(str(expression.sub_exprs[i]))
            expression.sub_exprs[i].str = expression.sub_exprs[i].code
            i+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
        #expression.sub_exprs = sbex
        return expression
    
    #TO DO: Use init_subexpr instead
    def init_subexpr2(self, expression:Expression):
        i = 0
        for e in expression.sub_exprs:
            if isinstance(e, (StartAppliedSymbol,NowAppliedSymbol) ):
                expression.sub_exprs[i] = e.sub_expr
                expression.code = intern(str(expression))
                expression.str = expression.code
            elif isinstance(e, NextAppliedSymbol):
                return False
            elif isinstance(e,(UnappliedSymbol)):
                return 
            #else:
            r = self.init_subexpr2(e)
            if r == False:
                return False
            i+=1
        if isinstance(expression,(AQuantification,AAggregate,AUnary,Brackets)):
            expression.f = expression.sub_exprs[0]
    #Transforms a possible bistate rule to next vocabulary
    #If the rule violates the format of bistate rule returns false
    def bis_rule(self, rule: Rule):
        next = False
        now = False
        if isinstance(rule.definiendum,StartAppliedSymbol):
            return False
        now = self.contains_now(rule.definiendum)
        next = self.contains_next(rule.definiendum)
        if next:
            rule.definiendum = self.bis_subexpr(rule.definiendum)
        else:
            rule.definiendum = self.sis_subexpr(rule.definiendum)
        if rule.definiendum == False:
            return False
        """if isinstance(rule.definiendum,(NextAppliedSymbol,NowAppliedSymbol)):
            sym = None
            e = rule.definiendum.sub_expr
            if isinstance(rule.definiendum,(NowAppliedSymbol)):
                now = True
                #symb = SymbolExpr(None,(str(e.symbol)),None,None)
            else:
                next = True
            symb = SymbolExpr(None,(str(e.symbol)+'_next'),None,None)
            rule.definiendum = AppliedSymbol(None,symb,e.sub_exprs,None,e.is_enumerated,e.is_enumeration,e.in_enumeration)"""
        if next:
            rule.body = self.bis_subexpr(rule.body)
            if rule.out:
                rule.out = self.bis_subexpr(rule.out)
                if rule.out == False:
                    return False
        elif now:
            rule.body = self.sis_subexpr(rule.body)
            if rule.out:
                rule.out = self.sis_subexpr(rule.out)
                if rule.out == False:
                    return False
        else:
            rule.body = self.sis_subexpr(rule.body)
            if rule.out:
                rule.out = self.sis_subexpr(rule.out)
                if rule.out == False:
                    return False
        if rule.body == False:
                return False
        rule.code = intern(str(rule))
        rule.str = rule.code
        return rule
    
    #Transforms a possible initial rule to current vocabulary
    #If the rule violates the format of initial rule returns false
    def init_rule(self, rule: Rule):
        if self.contains_next(rule.definiendum):
            return False
        #if isinstance(rule.definiendum,(NowAppliedSymbol,StartAppliedSymbol)):
            #rule.definiendum = rule.definiendum.sub_expr
        rule.definiendum = self.init_subexpr(rule.definiendum)
        #using init_subexpr for the subexpressions of body 
        if rule.out:
            rule.out = self.init_subexpr(rule.out)
            if rule.out == False:
                return False
        rule.body = self.init_subexpr(rule.body)
        if rule.body == False:
            return False
        """if isinstance(rule.body,NextAppliedSymbol):
            return False
        if isinstance(rule.body,(NowAppliedSymbol,StartAppliedSymbol)):
            #rule.body = rule.body.sub_expr
            rule.body = self.init_subexpr(rule.body)
        elif isinstance(rule.body,(UnappliedSymbol)): 
            rule.body
        else:
            r = self.init_subexpr2(rule.body)
            if r == False:
                return False"""
        #rule.body = self.init_subexpr(rule.body)
        rule.code = intern(str(rule))
        rule.str = rule.code
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
            #print("definedum coop")
            #print(self.definiendum)
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
    
################################ TempLogic  ###############################
    
class TempLogic(ASTNode):
    """
    The class of AST nodes representing a temporal logic block.
    """
    def __init__(self,parent,**kwargs):
        self.name= kwargs.pop('name')
        self.vocab_name = kwargs.pop('vocab_name')
        self.formula : LFormula = kwargs.pop('formula')

    def __str__(self):
        return self.name
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
        #Initial structure: Used in the context of LTC theories
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
        if self.no_enum:
            return f"{self.name} {self.sign} {self.default}"
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
        
    def init_copy(self,parent=None):
        enum = None
        if not self.no_enum:
            enum = self.enumeration.init_copy()
        default = None
        if self.default:
            default = self.default.init_copy()
        return SymbolInterpretation(parent=None,name= UnappliedSymbol(None,(self.name)),sign = self.sign,
                             enumeration=enum, default=default)
        
    #Projects the interpretation to time 0: Used in the context of LTC theories
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
                    else:
                        t_arg = e.args[-1]
                        self.check( type(t_arg) == Number, f"Last argument should be a number for temporal predicates")
                        if t_arg.number == '0':
                            e.args.pop()
                            tp.append((type(e))(args=e.args))
                            if len(e.args) == 0:
                                changed =True
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
    
class TransiotionGraph:
    def __init__(self,voc:Vocabulary,problem:Theory):
        self.voc = voc
        #Each state is a list where each element is a tuple where first element is if the predicate is part of the 
        #state, second the name of the fluent and third its arguments
        self.states : List[List[Tuple(bool,str,Identifier)]] = []
        self.transtions : dict[Tuple(int,int),List[AppliedSymbol]] = {}
        self.aextentions : dict[str,Extension] = {}
        self.fextentions : dict[str,Extension] = {}
        self.ffextentions : dict[str,Extension] = {}
        self.tempfunct : dict(str,set) = {}
        self.tempfunctarg : dict(str,set) = {}
        self.FillExtensions(problem.extensions)
        print("fucnt exte")
        print(self.tempfunct)
        print(self.tempfunctarg)
        #TO DO : WHAT ABOUT FUNCTIONS and add tests for functions
        self.SetStates()
        

    def SetStates(self):
        #first element of tuple is the name of pred , last is whether it is a ftemporal
        fluentstate :List[Tuple(str,Extension,bool)] = []
        for f , extensions in self.fextentions.items():
           fluentstate.append((f,extensions,False))
        for f , extensions in self.ffextentions.items():
           fluentstate.append((f,extensions,True))
        if len(fluentstate) > 0:
            self.states = self.crossstates(fluentstate)


    def crossstates(self,fluentstate :List[Tuple(str,Extension,bool)])->List[List[Tuple]]:
        #print("cross states")
        #print(fluentstate)
        current = fluentstate[0]
        extent = current[1][0]
        if len(fluentstate) == 1 :
            if fluentstate[0][2]:
                return self.flistperm(current[0],list(self.tempfunctarg.get(current[0],set())))
            return TransiotionGraph.perturbateExtens(fluentstate[0])
        out = []
        result = self.crossstates(fluentstate[1:])
        #print("2e phase")
        if extent == [[]]:
            for r in result:
                out.append([(True,current[0],None)]+r)
                out.append([(False,current[0],None)]+r)
        else:
            perms =[]
            if current[2]:
                perms = self.flistperm(current[0],list(self.tempfunctarg.get(current[0],set())))
            else:
                perms = TransiotionGraph.listpermutation(current[0],extent)
            for r in result:
                #tot2 = r
                for c in perms:
                    #print(r)
                    out.append(r+c)
                    #tot = [(True,current[0],c)] + r
                    #tot2 += [(False,current[0],c)] 
                    #for c2 in extent:
                    #    if c2 != c:
                    #        tot += [(False,current[0],c2)]
                    #out.append(tot)
                #out.append(tot2)
        return out
    
    def perturbateExtens(fluentstate :Tuple(str,Extension,bool)):
        extent = fluentstate[1][0]
        if extent == [[]]:
            return [[(False,fluentstate[0],None)],[(True,fluentstate[0],None)]]
        elif len(extent) > 0:
            #res = []
            #tot2 = []
            #for e in extent:
            #    tot = [(True,fluentstate[0],e)]
            #    tot2 += [(False,fluentstate[0],e)]
            #    for e2 in extent:
            #        if e2 != e:
            #            tot += [(False,fluentstate[0],e2)]
            #    res.append(tot)
            #res.append(tot2)
            #return res
            return TransiotionGraph.listpermutation(fluentstate[0],extent)

    def listpermutation(name,elements):
        if len(elements) == 0:
            return
        if len(elements) == 1:
            return [[(False,name,elements[0])],[(True,name,elements[0])]]
        restults = TransiotionGraph.listpermutation(name,elements[1:])
        out = []
        for r in restults:
            out.append(r+[(False,name,elements[0])])
            out.append(r+[(True,name,elements[0])])
        return out
    
    def flistperm(self,name,argl):
        #argl = self.tempfunctarg[name]
        outl = list(self.tempfunct[name])
        if len(argl) <= 1 :
            a = tuple()
            if len(argl) == 1 :
                a = argl[0]
            res =[]
            for o in outl:

                res.append([(True,name,a+tuple([o]))])
                for o2 in outl:
                    if o2 != o :
                        res[-1].append((False,name,a+tuple([o2])))
            return res
        results = self.flistperm(name,argl[1:])
        a = argl[0]
        res = []
        for r in results:
            for o in outl:
                tot = [(True,name,a+tuple([o]))]
                for o2 in outl:
                    if o2 != o:
                        tot.append((False,name,a+tuple([o2])))
                res.append(r+tot)
        return res


    
    
    def FillExtensions(self,extensions: dict[str, Extension]):
        for s , e in extensions.items():
            for a in self.voc.actions:
                if s == a:
                    self.aextentions[a] = e
                    #if self.symbol_decl.codomain == BOOL_SETNAME:  # predicate
                    #    extension = [t.args for t in self.enumeration.tuples]
                    #    problem.extensions[self.symbol_decl.name] = (extension, None)
                    #if len(d.domains) == 0:  # () -> ..
                    #    self.aextensions[a] = [ ([[]], None) ]
                    #elif d.arity == 0:  # subset of ()
                    #    self.aextensions[a] = [s.extension({}) for s in d.domains]
                    #else:
                    #    self.aextensions[a] = [s.extension({}) for s in d.domains]
        
        for s , e in extensions.items():
            for f in self.voc.fluents:
                if s == f:
                    self.fextentions[f] = e
            for f in self.voc.ftemproral:
                if s == f:
                    self.ffextentions[f] = e
                    outputl = []
                    argl =[]
                    if e[0] == [[]]:
                        #TO DO: THROW EXCEPTION IN annnote of vocabulary if it is not a function
                        print("Error: FTemporal should be a function")
                    for r in e[0]:
                        outputl.append(r[-1])
                        if len(r) > 1:
                            argl.append(r[:-1])
                    r1 = self.tempfunct.get(f,set())
                    self.tempfunct[f] = set(outputl).union(r1)
                    if len(argl) == 0:
                        pass
                    else:
                        r2 = self.tempfunctarg.get(f,{})
                        self.tempfunctarg[f] = set(argl).union(r2)

        

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
                                         TempLogic,ILFormula,DLFormula,
                                         CLFormula,NLFormula,XLFormula,FLFormula,GLFormula,ULFormula,WLFormula,RLFormula,

                                         Structure, SymbolInterpretation,
                                         Enumeration, FunctionEnum, CSVEnumeration,
                                         TupleIDP, FunctionTuple, CSVTuple,
                                         ConstructedFrom, Constructor, Ranges,
                                         RangeElement, Display,

                                         Procedure, Call1, String,
                                         PyList, PyAssignment])
