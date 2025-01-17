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

This module contains the ASTNode classes for expressions.

(Many methods are monkey-patched by other modules)

"""
from __future__ import annotations

from copy import copy, deepcopy
from collections import ChainMap
from datetime import date
from dateutil.relativedelta import *
from fractions import Fraction
from re import findall
from sys import intern
from textx import get_location
from typing import (Optional, List, Union, Tuple, Set, Callable, TYPE_CHECKING,
                    Generator, Any, Dict)
if TYPE_CHECKING:
    from .Theory import Theory
    from .Assignments import Assignments, Status
    from .Parse import IDP, Vocabulary, Declaration, SymbolDeclaration, SymbolInterpretation, Enumeration
    from .Annotate import Annotated, Exceptions

from .utils import (unquote, OrderedSet, BOOL, INT, REAL, DATE, CONCEPT, EMPTY,
                    RESERVED_SYMBOLS, IDPZ3Error, Semantics)


class ASTNode(object):
    """superclass of all AST nodes
    """

    def location(self):
        try:
            location = get_location(self)
            location['end'] = (location['col'] +
                (len(self.code) if hasattr(self, "code") else 0))
            return location
        except:
            return {'line': 1, 'col': 1, 'end': 1}

    def check(self, condition: bool, msg: str):
        """raises an exception if `condition` is not True

        Args:
            condition (Bool): condition to be satisfied
            msg (str): error message

        Raises:
            IDPZ3Error: when `condition` is not met
        """
        if not condition:
            raise IDPZ3Error(msg, self)

    def SCA_Check(self,detections):
        raise IDPZ3Error("Internal error") # monkey-patched

    def dedup_nodes(self,
                    kwargs: dict[str, List[ASTNode]],
                    arg_name:str
                    ) -> dict[str, ASTNode]:
        """pops `arg_name` from kwargs as a list of named items
        and returns a mapping from name to items

        Args:
            kwargs: dictionary mapping named arguments to list of ASTNodes

            arg_name: name of the kwargs argument, e.g. "interpretations"

        Returns:
            dict[str, ASTNode]: mapping from `name` to AST nodes

        Raises:
            AssertionError: in case of duplicate name
        """
        ast_nodes = kwargs.pop(arg_name)
        
        out = {}
        for i in ast_nodes:
            # can't get location here
            assert hasattr(i, "name"), "internal error"
            assert i.name not in out, f"Duplicate '{i.name}' in {arg_name}"
            out[i.name] = i
        return out

    def annotate_block(self,
                       idp: IDP,
                       ) -> Exceptions:
        raise IDPZ3Error("Internal error") # monkey-patched

    def annotate_declaration(self,
                             voc: Vocabulary,
                             ) -> ASTNode:
        raise IDPZ3Error("Internal error") # monkey-patched

    def interpret(self, problem: Optional[Theory]) -> ASTNode:
        return self

    def EN(self):
        raise IDPZ3Error("Internal error") # monkey-patched

Annotation = Dict[str, Union[str, Dict[str, Any]]]

class Annotations(ASTNode):
    def __init__(self, parent, annotations: List[str]):
        self.original_ant = []
        for s in annotations:
            self.original_ant.append(s) 
        self.annotations : Annotation = {}
        v: Union[str, dict[str, Any]]
        for s in annotations:
            p = s.split(':', 1)
            if len(p) == 2:
                if p[0] != 'slider':
                    k, v = (p[0], p[1])
                else:
                    # slider:(lower_sym, upper_sym) in (lower_bound, upper_bound)
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
                    k, v = ('slider', slider_arg)
            else:
                k, v = ('reading', p[0])
            self.check(k not in self.annotations,
                       f"Duplicate annotation: [{k}: {v}]")
            self.annotations[k] = v

    def init_copy(self,parent=None):
        return Annotations(parent,self.original_ant)

class Constructor(ASTNode):
    """Constructor declaration

    Attributes:
        name (string): name of the constructor

        args (List[Accessor])

        sorts (List[SetName]): types of the arguments of the constructor

        out (SetName): type that contains this constructor

        arity (Int): number of arguments of the constructor

        tester (SymbolDeclaration, Optional): function to test if the constructor
        has been applied to some arguments (e.g., is_rgb)

        concept_decl (SymbolDeclaration, Optional): declaration with name[1:],
        only for Concept constructors.

        range: the list of identifiers
    """

    def __init__(self, parent: Optional[ASTNode],
                 name: str,
                 args: Optional[List[Accessor]] = None):
        self.name : str = name
        self.args = args if args else []  #TODO avoid self.args by defining Accessor as subclass of SetName
        self.domains = [a.codomain for a in self.args]

        self.arity = len(self.domains)

        self.codomain: Optional[SetName] = None
        self.concept_decl: Optional[SymbolDeclaration] = None
        self.tester: Optional[SymbolDeclaration] = None
        self.range: Optional[List[Expression]] = None

    def __str__(self):
        return (self.name if not self.args else
                f"{self.name}({', '.join((str(a) for a in self.args))})" )
    
    def init_copy(self,parent=None):
        sr = None
        if self.args:
            sr = [s.init_copy() for s in self.args]
        return Constructor(parent,self.name,sr)
    
def CONSTRUCTOR(name: str, args=None) -> Constructor:
    return Constructor(None, name, args)

class Accessor(ASTNode):
    """represents an accessor and a type

    Attributes:
        accessor (str, Optional): name of accessor function

        codomain (SetName): name of the output type of the accessor

        decl (SymbolDeclaration): declaration of the accessor function
    """
    def __init__(self, parent,
                 out: SetName,
                 accessor: Optional[str] = None):
        self.accessor = accessor
        self.codomain = out
        self.decl: Optional[SymbolDeclaration] = None

    def __str__(self):
        return (self.codomain.name if not self.accessor else
                f"{self.accessor}: {self.codomain.name}" )

    def init_copy(self,parent=None):
        acc = None
        if self.accessor:
            acc = self.accessor
        return Accessor(parent,self.codomain.init_copy(),acc)

class Expression(ASTNode):
    """The abstract class of AST nodes representing (sub-)expressions.

    Attributes:
        code (string):
            Textual representation of the expression.  Often used as a key.

            It is generated from the sub-tree.

        str (string)
            Textual representation of the simplified expression.

        sub_exprs (List[Expression]):
            The children of the AST node.

            The list may be reduced by simplification.

        type (SetName, Optional):
            The type of the expression, e.g., ``bool``.

        co_constraint (Expression, optional):
            A constraint attached to the node.

            For example, the co_constraint of ``square(length(top()))`` is
            ``square(length(top())) = length(top())*length(top()).``,
            assuming ``square`` is appropriately defined.

            The co_constraint of a defined symbol applied to arguments
            is the instantiation of the definition for those arguments.
            This is useful for definitions over infinite domains,
            as well as to compute relevant questions.

        annotations (dict[str, str]):
            The set of annotations given by the expert in the IDP-Z3 program.

            ``annotations['reading']`` is the annotation
            giving the intended meaning of the expression (in English).

        original (Expression):
            The original expression, before propagation and simplification.

        variables (Set(string)):
            The set of names of the variables in the expression, before interpretation.

        is_type_constraint_for (string):
            name of the symbol for which the expression is a type constraint

    """



    def __init__(self, parent: Optional[ASTNode]=None,
                 annotations: Optional[Annotations]=None):
        if parent:
            self.parent = parent
        self.sub_exprs: List[Expression]

        self.code: str = intern(str(self))
        self.annotations: Annotation = (
            annotations.annotations if annotations else {'reading': self.code})
        self.original: Optional[Expression] = self

        self.str: str = self.code
        self.variables: Optional[Set[str]] = None
        self.type: Optional[SetName] = None
        self.is_type_constraint_for: Optional[str] = None
        self.co_constraint: Optional[Expression] = None

        # attributes of the top node of a (co-)constraint
        self.questions: Optional[OrderedSet] = None
        self.relevant: Optional[bool] = None

    def __deepcopy__(self, memo):
        cls = self.__class__ # Extract the class of the object
        out = cls.__new__(cls) # Create a new instance of the object based on extracted class
        memo[id(self)] = out
        out.__dict__.update(self.__dict__)

        out.sub_exprs = [deepcopy(e, memo) for e in self.sub_exprs]
        out.variables = deepcopy(self.variables, memo)
        out.co_constraint = deepcopy(self.co_constraint, memo)
        out.questions = deepcopy(self.questions, memo)
        return out
    
    def init_copy(self,parent=None):
        sub_exprs = [e.init_copy() for e in self.sub_exprs] 
        expr = Expression(parent)
        expr.sub_exprs = sub_exprs
        return expr       


    def same_as(self, other: Expression):
        # symmetric
        if self.str == other.str: # and type(self) == type(other):
            return True

        if (type(self) in [Number, Date]
        and type(other) in [Number, Date]):
            return float(self.py_value) == float(other.py_value)

        return False

    def __repr__(self): return str(self)

    def __log__(self):  # for debugWithYamlLog
        return {'class': type(self).__name__,
                'code': self.code,
                'str': self.str,
                'co_constraint': self.co_constraint}

    def annotate(self,
                 voc: Vocabulary,
                 q_vars: dict[str, Variable],
                 ltc=False,
                 temporal_head=0
                 ) -> Annotated:
        raise IDPZ3Error("Internal error") # monkey-patched

    def annotate_quantee(self,
                 voc: Vocabulary,
                 q_vars: dict[str, Variable],
                 inferred: dict[str, SetName],
                 ltc:bool,
                 temporal_head:int=0
                 ) -> Annotated:
        raise IDPZ3Error("Internal error") # monkey-patched

    def fill_attributes_and_check(self: Expression) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def has_variables(self) -> bool:
        return any(e.has_variables() for e in self.sub_exprs)

    def collect(self,
                questions: OrderedSet,
                all_: bool=True,
                co_constraints: bool=True
                ):
        """collects the questions in self.

        `questions` is an OrderedSet of Expression
        Questions are the terms and the simplest sub-formula that
        can be evaluated.

        all_=False : ignore expanded formulas
        and AppliedSymbol interpreted in a structure

        co_constraints=False : ignore co_constraints

        default implementation for UnappliedSymbol, AIfExpr, AUnary, Variable,
        Number_constant, Brackets
        """
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)

    def collect_symbols(self,
                        symbols: Optional[dict[str, SymbolDeclaration]] = None,
                        co_constraints: bool=True
                        ) -> dict[str, SymbolDeclaration]:
        """ returns the list of symbols occurring in self,
        ignoring type constraints and symbols created by aggregates
        """
        symbols = {} if symbols == None else symbols
        assert symbols is not None, "Internal error"
        if self.is_type_constraint_for is None:  # ignore type constraints
            if (hasattr(self, 'decl') and self.decl
                and self.decl.__class__.__name__ == "SymbolDeclaration"
                and not self.decl.name in RESERVED_SYMBOLS
                and not self.decl.name.startswith('__')):  # min/max aggregates
                symbols[self.decl.name] = self.decl
            for e in self.sub_exprs:
                e.collect_symbols(symbols, co_constraints)
        return symbols

    def collect_nested_symbols(self,
                               symbols: Set[SymbolDeclaration],
                               is_nested: bool
                               ) -> Set[SymbolDeclaration]:
        raise IDPZ3Error("Internal error") # monkey-patched

    def generate_constructors(self, constructors: dict[str, List[Constructor]]):
        """ fills the list `constructors` with all constructors belonging to
        open types.
        """
        for e in self.sub_exprs:
            e.generate_constructors(constructors)

    def collect_co_constraints(self, co_constraints: OrderedSet, recursive=True):
        """ collects the constraints attached to AST nodes, e.g. instantiated
        definitions

        Args:
            recursive: if True, collect co_constraints of co_constraints too
        """
        if self.co_constraint is not None and self.co_constraint not in co_constraints:
            co_constraints.append(self.co_constraint)
            if recursive:
                self.co_constraint.collect_co_constraints(co_constraints, recursive)
        for e in self.sub_exprs:
            e.collect_co_constraints(co_constraints, recursive)

    def is_value(self) -> bool:
        """True for numerals, date, identifiers,
        and constructors applied to values.

        Synomym: "is ground", "is rigid"

        Returns:
            bool: True if `self` represents a value.
        """
        return False

    def is_reified(self) -> bool:
        """False for values and for symbols applied to values.

        Returns:
            bool: True if `self` has to be reified to obtain its value in a Z3 model.
        """
        return True

    def is_assignment(self) -> bool:
        """

        Returns:
            bool: True if `self` assigns a rigid term to a rigid function application
        """
        return False

    def has_decision(self) -> bool:
        # returns true if it contains a variable declared in decision
        # vocabulary
        return any(e.has_decision() for e in self.sub_exprs)

    def type_inference(self, voc: Vocabulary) -> dict[str, SetName]:
        if isinstance(self,(NowAppliedSymbol,NextAppliedSymbol,StartAppliedSymbol,CauseTrueAppliedSymbol,CauseFalseAppliedSymbol)):
            return {}
        try:
            return dict(ChainMap(*(e.type_inference(voc) for e in self.sub_exprs)))
        except AttributeError as e:
            if "has no attribute 'sorts'" in str(e):
                msg = f"Incorrect arity for {self}"
            else:
                msg = f"Unknown error for {self}"
            self.check(False, msg)
            return {}  # dead code

    def __str__(self) -> str:
        raise IDPZ3Error("Internal error")  # monkey-patched

    def _change(self: Expression,
                sub_exprs: Optional[List[Expression]] = None,
                ops : Optional[List[str]] = None,
                simpler : Optional[Expression] = None,
                co_constraint : Optional[Expression] = None
                ) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def update_exprs(self, new_exprs: Generator[Expression, None, None]) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def simplify1(self) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def interpret(self,
                  problem: Optional[Theory],
                  subs: dict[str, Expression]
                  ) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def _interpret(self,
                    problem: Optional[Theory],
                    subs: dict[str, Expression]
                    ) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def substitute(self,
                   e0: Expression,
                   e1: Expression,
                   assignments: Assignments,
                   tag=None) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def simplify_with(self, assignments: Assignments, co_constraints_too=True) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def symbolic_propagate(self,
                           assignments: Assignments,
                           tag: Status,
                           truth: Optional[Expression] = None
                           ):
        raise IDPZ3Error("Internal error") # monkey-patched

    def propagate1(self,
                   assignments: Assignments,
                   tag: Status,
                   truth: Optional[Expression] = None
                   ):
        raise IDPZ3Error("Internal error") # monkey-patched

    def translate(self, problem: Theory, vars={}):
        raise IDPZ3Error("Internal error") # monkey-patched

    def reified(self, problem: Theory):
        raise IDPZ3Error("Internal error") # monkey-patched

    def translate1(self, problem: Theory, vars={}):
        raise IDPZ3Error("Internal error") # monkey-patched

    def as_set_condition(self) -> Tuple[Optional[AppliedSymbol], Optional[bool], Optional[Enumeration]]:
        """Returns an equivalent expression of the type "x in y", or None

        Returns:
            Tuple[Optional[AppliedSymbol], Optional[bool], Optional[Enumeration]]: meaning "expr is (not) in enumeration"
        """
        return (None, None, None)

    def split_equivalences(self) -> Expression:
        """Returns an equivalent expression where equivalences are replaced by
        implications

        Returns:
            Expression
        """
        out = self.update_exprs(e.split_equivalences() for e in self.sub_exprs)
        return out

    def add_level_mapping(self,
                          level_symbols: dict[SymbolDeclaration, SetName],
                          head: AppliedSymbol,
                          pos_justification: bool,
                          polarity: bool,
                          mode: Semantics
                          ) -> Expression:
        raise IDPZ3Error("Internal error") # monkey-patched

    def get_type(self):
        return self.type



class SetName(Expression):
    """ASTNode representing a (sub-)type or a `Concept[aSignature]`, e.g., `Concept[T*T->Bool]`

    Inherits from Expression

    Args:
        name (str): name of the concept

        concept_domains (List[SetName], Optional): domain of the Concept signature, e.g., `[T, T]`

        codomain (SetName, Optional): range of the Concept signature, e.g., `Bool`

        decl (Declaration, Optional): declaration of the type

        root_set (SetName, Optional): a Type or a Concept with signature (Concept[T->T])
    """

    def __init__(self, parent,
                 name:str,
                 ins: Optional[List[SetName]] = None,
                 out: Optional[SetName] = None):
        self.name = unquote(name)
        self.concept_domains = ins
        self.codomain = out
        self.sub_exprs = []
        self.decl: Declaration = None
        self.root_set: SetName = None
        super().__init__(parent)

    def init_copy(self,parent=None):
        insa = []
        if self.concept_domains:
            for i in self.concept_domains:
                insa.append(i.init_copy())
        else:
            insa =None
        outa = None
        if self.codomain:
            outa =self.codomain.init_copy()
        return SetName(parent,self.name,insa,outa)

    def __str__(self):
        return self.name + ("" if not self.codomain else
                            f"[{'*'.join(str(s) for s in self.concept_domains)}->{self.codomain}]")

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        self.check(self.name != CONCEPT or self.codomain,
                   f"`Concept` must be qualified with a type signature")
        return (other and self.name == other.name and
                (not self.codomain or (
                    self.codomain == other.codomain and
                    len(self.concept_domains) == len(other.concept_domains) and
                    all(s==o for s, o in zip(self.concept_domains, other.concept_domains)))))

    def extension(self, extensions: dict[str, Extension]) -> Extension:
        raise IDPZ3Error("Internal error") # monkey-patched

    def is_value(self): return True

    def has_element(self,
                    term: Expression,
                    extensions: dict[str, Extension]
                    ) -> Expression:
        """Returns an Expression that says whether `term` is in the type/predicate denoted by `self`.

        Args:
            term (Expression): the argument to be checked

        Returns:
            Expression: whether `term` `term` is in the type denoted by `self`.
        """
        if self.name == CONCEPT:
            extension = self.extension(extensions)[0]
            assert extension is not None, "Internal error"
            comparisons = [EQUALS([term, c[0]]) for c in extension]
            return OR(comparisons)
        else:
            assert self.decl is not None, "Internal error"
            self.check(self.decl.codomain == BOOL_SETNAME, "internal error")
            return self.decl.contains_element(term, extensions)

def SETNAME(name: str, ins=None, out=None) -> SetName:
    return SetName(None, name, ins, out)

BOOL_SETNAME = SETNAME(BOOL)
INT_SETNAME = SETNAME(INT)
REAL_SETNAME = SETNAME(REAL)
DATE_SETNAME = SETNAME(DATE)
EMPTY_SETNAME = SETNAME(EMPTY)

class AIfExpr(Expression):
    PRECEDENCE = 10
    IF = 0
    THEN = 1
    ELSE = 2

    def __init__(self, parent,
                 if_f: Expression,
                 then_f: Expression,
                 else_f: Expression
                 ):
        self.if_f = if_f
        self.then_f = then_f
        self.else_f = else_f

        self.sub_exprs = [self.if_f, self.then_f, self.else_f]
        super().__init__()

    @classmethod
    def make(cls,
             if_f: Expression,
             then_f: Expression,
             else_f: Expression
             ) -> 'AIfExpr':
        out = (cls)(None, if_f=if_f, then_f=then_f, else_f=else_f)
        return out.fill_attributes_and_check().simplify1()

    def init_copy(self,parent=None):
        return AIfExpr(parent,self.if_f.init_copy(),self.then_f.init_copy(),self.else_f.init_copy())

    def __str__(self):
        return (f"if {self.sub_exprs[AIfExpr.IF  ].str}"
                f" then {self.sub_exprs[AIfExpr.THEN].str}"
                f" else {self.sub_exprs[AIfExpr.ELSE].str}")

def IF(IF: Expression,
       THEN: Expression,
       ELSE: Expression,
       annotations=None
       ) -> AIfExpr:
    return AIfExpr.make(IF, THEN, ELSE)


class Quantee(Expression):
    """represents the description of quantification, e.g., `x in T` or `(x,y) in P`
    The `Concept` type may be qualified, e.g. `Concept[Color->Bool]`

    Attributes:
        vars (List[List[Variable]]): the (tuples of) variables being quantified

        subtype (SetName, Optional): a literal SetName to quantify over, e.g., `Color` or `Concept[Color->Bool]`.

        sort (SymbolExpr, Optional): a dereferencing expression, e.g.,. `$(i)`.

        sub_exprs (List[SymbolExpr], Optional): the (unqualified) type or predicate to quantify over,
        e.g., `[Color], [Concept] or [$(i)]`.

        arity (int): the length of the tuple of variables

        decl (SymbolDeclaration, Optional): the (unqualified) Declaration to quantify over, after resolution of `$(i)`.
        e.g., the declaration of `Color`
    """
    def __init__(self, parent,
                 vars: Union[List[Variable], List[List[Variable]]],
                 subtype: Optional[SetName] = None,
                 sort: Optional[SymbolExpr] = None):
        self.subtype = subtype
        self.sort_orig = sort
        sort = sort
        if self.subtype:
            self.check(self.subtype.name == CONCEPT or self.subtype.codomain is None,
                   f"Can't use signature after predicate {self.subtype.name}")

        self.sub_exprs = ([sort] if sort else
                          [self.subtype] if self.subtype else
                          [])
        self.arity = None
        self.var_org = vars
        self.vars : List[List[Variable]] = []
        for i, v in enumerate(vars):
            if hasattr(v, 'vars'):  # varTuple
                self.check(1 < len(v.vars), f"Can't have singleton in binary quantification")
                self.vars.append(v.vars)
                self.arity = len(v.vars) if self.arity == None else self.arity
            else:
                assert isinstance(v, Variable), "Internal error1"
                self.vars.append([v])
                self.arity = 1 if self.arity == None else self.arity

        super().__init__()
        self.decl = None

        self.check(all(len(v) == self.arity for v in self.vars),
                    f"Inconsistent tuples in {self}")

    def init_copy(self,parent=None):
        vars  = []
        for lv in self.var_org:
            if isinstance(lv,Variable):
                vars.append(lv.init_copy()) 
            else:
                vars.append([])
                for v in lv:
                    vars[-1].append(v.init_copy()) 
        sbtyp = None
        if self.subtype:
            sbtyp = self.subtype.init_copy()
        srt_org = None
        if self.sort_orig:
            srt_org = self.sort_orig.init_copy()
        return Quantee(parent,vars,sbtyp,srt_org)

    @classmethod
    def make(cls,
             var: List[Variable],
             subtype: Optional[SetName] = None,
             sort: Optional[SymbolExpr] = None
             ) -> 'Quantee':
        out = (cls) (None, [var], subtype=subtype, sort=sort)
        return out.fill_attributes_and_check()

    def __str__(self):
        signature = ("" if len(self.sub_exprs) <= 1 else
                     f"[{','.join(t.str for t in self.sub_exprs[1:-1])}->{self.sub_exprs[-1]}]"
        )
        return (f"{','.join(str(v) for vs in self.vars for v in vs)}"
                f"{f' ∈ {self.sub_exprs[0]}' if self.sub_exprs else ''}"
                f"{signature}")


def split_quantees(self):
    """replaces an untyped quantee `x,y,z` into 3 quantees,
    so that each variable can have its own sort

    Args:
        self: either a AQuantification, AAggregate or Rule"""
    if len(self.quantees)==1 and not self.quantees[0].sub_exprs:
        # separate untyped variables, so that they can be typed separately
        q = self.quantees.pop()
        for vars in q.vars:
            for var in vars:
                self.quantees.append(Quantee.make(var, sort=None))


class AQuantification(Expression):
    """ASTNode representing a quantified formula

    Args:
        annotations (dict[str, str]):
            The set of annotations given by the expert in the IDP-Z3 program.

            ``annotations['reading']`` is the annotation
            giving the intended meaning of the expression (in English).

        q (str): either '∀' or '∃'

        quantees (List[Quantee]): list of variable declarations

        f (Expression): the formula being quantified

        supersets, new_quantees, vars1: attributes used in `interpret`
    """
    PRECEDENCE = 20

    def __init__(self, parent: Optional[ASTNode],
                 annotations: Optional[Annotations],
                 q: str,
                 quantees: List[Quantee],
                 f: Expression):
        self.q = q
        self.quantees = quantees
        self.f = f
        self.wrapper = False

        self.q = ('∀' if self.q in ['!', 'forall'] else
                  '∃' if self.q in ["?", "thereisa"] else
                  self.q)
        split_quantees(self)

        self.sub_exprs = [self.f]
        super().__init__(annotations=annotations)

        self.type = BOOL_SETNAME
        self.supersets: Optional[List[List[List[Union[Identifier, Variable]]]]] = None
        self.new_quantees: Optional[List[Quantee]] = None
        self.vars1 : Optional[List[Variable]] = None

    @classmethod
    def make(cls,
             q: str,
             quantees: List[Quantee],
             f: Expression,
             annotations: Optional[Annotation]=None
             ) -> 'AQuantification':
        "make and annotate a quantified formula"
        out = cls(None, None, q, quantees, f)
        if annotations:
            out.annotations = annotations
        return out.fill_attributes_and_check()

    def __str__(self):
        if len(self.sub_exprs) == 0:
            body = TRUE.str if self.q == '∀' else FALSE.str
        elif len(self.sub_exprs) == 1:
            body = self.sub_exprs[0].str
        else:
            connective = '∧' if self.q == '∀' else '∨'
            body = connective.join("("+e.str+")" for e in self.sub_exprs)

        if self.quantees:
            vars = ','.join([f"{q}" for q in self.quantees])
            return f"{self.q} {vars}: {body}"
        else:
            return body

    def __deecopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.quantees = [deepcopy(q, memo) for q in self.quantees]
        return out
    
    def init_copy(self,parent=None):
        quantees = [q.init_copy() for q in self.quantees]
        q =None
        if self.q:
            q =self.q
        f= None
        if self.f:
            f = self.f.init_copy()
        ex : AQuantification = AQuantification(parent,None,q,quantees,f)
        return ex

    def collect(self, questions, all_=True, co_constraints=True):
        questions.append(self)
        if all_:
            Expression.collect(self, questions, all_, co_constraints)
            for q in self.quantees:
                q.collect(questions, all_, co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        for q in self.quantees:
            q.collect_symbols(symbols, co_constraints)
        return symbols
    
    def propagate_changes(self):
        self.f = self.sub_exprs[0]
        return super().propagate_changes()

def FORALL(qs, expr, annotations=None):
    return AQuantification.make('∀', qs, expr, annotations)
def EXISTS(qs, expr, annotations=None):
    return AQuantification.make('∃', qs, expr, annotations)


class ForNext(Expression):
    """Represents a Start symbol applied to  another applied symbol 

    Args:
        arg (AppliedSymbol): the applied symbol 

        in_head (Bool): True if the AppliedSymbol occurs in the head of a rule
    """
    PRECEDENCE = 20

    def __init__(self, parent,
                 exp:Expression,number:Number,var:SymbolExpr):
        self.symbol  = SymbolExpr(self,'ForNext',None,None)
        self.exp = exp
        self.num = number
        self.var = var
        self.sub_exprs = [exp,number,var]
        super().__init__()

        #self.as_disjunction = None
        #self.decl = None
        self.in_head = False

    @classmethod
    def make(cls,
             symbol: SymbolExpr,
             exp:Expression,number:Number,variable:SymbolExpr
             ) -> ForNext:
        out = cls(None, symbol, exp,number,variable)
        out.sub_exprs = [exp,number]
        # annotate
        out.decl = symbol.decl
        return out.annotate1()

    #@classmethod
    #def construct(cls, constructor, args):

    def __str__(self):
        out = f"{self.symbol}[{self.sub_exprs[0].str} , {self.num.str} , {self.var.str}]"
        return (f"{out}")

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.symbol = deepcopy(out.symbol)
        #out.as_disjunction = deepcopy(out.as_disjunction)
        return out
    def init_copy(self,parent=None):
        return ForNext(parent,self.exp.init_copy(),self.num.init_copy(),self.var.init_copy())

    def collect(self, questions, all_=True, co_constraints=True):
        self.exp.collect(questions,all,co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        self.symbol.collect_symbols(symbols, co_constraints)
        return symbols

    def has_decision(self):
        return self.exp.has_decision()


    def is_value(self) -> bool:
        # independent of is_enumeration and in_enumeration !
        return self.exp.is_value()

    def is_reified(self):
        # independent of is_enumeration and in_enumeration !
        return self.exp.is_reified()

    def generate_constructors(self, constructors: dict):
        self.exp.generate_constructors(constructors,dict)


class Operator(Expression):
    PRECEDENCE = 0  # monkey-patched
    MAP: dict[str, Callable] = dict()  # monkey-patched
    NORMAL = {
        "is strictly less than": "<",
        "is less than": "≤",
        "=<": "≤",
        "is greater than": "≥",
        "is strictly greater than": ">",
        ">=" : "≥",
        "is not": "≠",
        "~=": "≠",
        "<=>": "⇔",
        "is the same as": "⇔",
        "are necessary and sufficient conditions for": "⇔",
        "<=": "⇐",
        "are necessary conditions for": "⇐",
        "=>": "⇒",
        "then": "⇒",
        "are sufficient conditions for": "⇒",
        "|": "∨",
        "or": "∨",
        "&": "∧",
        "and": "∧",
        "*": "⨯",
        "is": "=",
    }
    EN_map: Optional[dict[str, str]] = None

    def __init__(self, parent, operator, sub_exprs,
                 annotations:Optional[Annotations]=None):
        self.operator = operator
        self.sub_exprs = sub_exprs

        self.operator = list(map(
            lambda op: Operator.NORMAL.get(op, op)
            , self.operator))

        super().__init__(parent, annotations=annotations)

        self.type = BOOL_SETNAME if self.operator[0] in '&|∧∨⇒⇐⇔' \
               else BOOL_SETNAME if self.operator[0] in '=<>≤≥≠' \
               else None

    @classmethod
    def make(cls,
             ops: Union[str, List[str]],
             operands: List[Expression],
             annotations: Optional[Annotation] =None,
             parent=None
             ) -> Expression:
        """ creates a BinaryOp
            beware: cls must be specific for ops !
        """
        if len(operands) == 0:
            if cls == AConjunction:
                out = copy(TRUE)
            elif cls == ADisjunction:
                out = copy(FALSE)
            else:
                assert False, "Internal error"
        elif len(operands) == 1:
            return operands[0]
        else:
            if isinstance(ops, str):
                ops = [ops] * (len(operands)-1)
            out = (cls)(parent, ops, operands)
        if annotations:
            out.annotations = annotations

        if parent:  # for error messages
            out._tx_position = parent. _tx_position
            out._tx_position_end = parent. _tx_position_end
        return out.fill_attributes_and_check().simplify1()

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return Operator(parent,self.operator.copy(),sub_ex)

    def __str__(self):
        def parenthesis(precedence, x):
            return f"({x.str})" if type(x).PRECEDENCE <= precedence else f"{x.str}"
        precedence = type(self).PRECEDENCE
        temp = parenthesis(precedence, self.sub_exprs[0])
        for i in range(1, len(self.sub_exprs)):
            temp += f" {self.operator[i-1]} {parenthesis(precedence, self.sub_exprs[i])}"
        return temp

    def collect(self, questions, all_=True, co_constraints=True):
        if self.operator[0] in '=<>≤≥≠':
            questions.append(self)
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)

class AImplication(Operator):
    PRECEDENCE = 50

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return AImplication(parent,self.operator.copy(),sub_ex)

def IMPLIES(exprs, annotations=None):
    return AImplication.make('⇒', exprs, annotations)




class AEquivalence(Operator):
    PRECEDENCE = 40

    # NOTE: also used to split rules into positive implication and negative implication. Please don't change.
    def split(self):
        posimpl = IMPLIES([self.sub_exprs[0], self.sub_exprs[1]])
        negimpl = RIMPLIES(deepcopy([self.sub_exprs[0], self.sub_exprs[1]]))
        return AND([posimpl, negimpl])

    def split_equivalences(self):
        out = self.update_exprs(e.split_equivalences() for e in self.sub_exprs)
        return out.split()
    
    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return AEquivalence(parent,self.operator.copy(),sub_ex)

def EQUIV(exprs, annotations=None):
    return AEquivalence.make('⇔', exprs, annotations)

    

class ARImplication(Operator):
    PRECEDENCE = 30

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return ARImplication(parent,self.operator.copy(),sub_ex)

def RIMPLIES(exprs, annotations):
    return ARImplication.make('⇐', exprs, annotations)


class ADisjunction(Operator):
    PRECEDENCE = 60

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return ADisjunction(parent,self.operator.copy(),sub_ex)

    def __str__(self):
        if not hasattr(self, 'enumerated'):
            return super().__str__()
        return f"{self.sub_exprs[0].sub_exprs[0].code} in {{{self.enumerated}}}"

def OR(exprs):
    return ADisjunction.make('∨', exprs)


class AConjunction(Operator):
    PRECEDENCE = 70

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return AConjunction(parent,self.operator.copy(),sub_ex)

def AND(exprs):
    return AConjunction.make('∧', exprs)


class AComparison(Operator):
    PRECEDENCE = 80

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return AComparison(parent,self.operator.copy(),sub_ex)

    def is_assignment(self):
        # f(x)=y
        return (len(self.sub_exprs) == 2 and
                self.operator in [['='], ['≠']]
                and isinstance(self.sub_exprs[0], AppliedSymbol)
                and not self.sub_exprs[0].is_reified()
                and self.sub_exprs[1].is_value())

def EQUALS(exprs):
    return AComparison.make('=',exprs)


class ASumMinus(Operator):
    PRECEDENCE = 90

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return ASumMinus(parent,self.operator.copy(),sub_ex)


class AMultDiv(Operator):
    PRECEDENCE = 100

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return AMultDiv(parent,self.operator.copy(),sub_ex)


class APower(Operator):
    PRECEDENCE = 110

    def init_copy(self,parent=None):
        sub_ex = [q.init_copy() for q in self.sub_exprs]
        return APower(parent,self.operator.copy(),sub_ex)


class AUnary(Expression):
    PRECEDENCE = 120
    MAP : dict[str, Callable] = dict()  # monkey-patched

    def __init__(self, parent,
                 operators: List[str],
                 f: Expression):
        self.operators = operators
        self.f = f
        self.operators = ['¬' if c in ['~', 'not'] else c for c in self.operators]
        self.operator = self.operators[0]
        self.check(all([c == self.operator for c in self.operators]),
                   "Incorrect mix of unary operators")

        self.sub_exprs = [self.f]
        super().__init__()

    @classmethod
    def make(cls, op: str, expr: Expression) -> AUnary:
        out = AUnary(None, operators=[op], f=expr)
        return out.fill_attributes_and_check().simplify1()

    def init_copy(self,parent=None):
        return AUnary(parent,self.operators.copy(),self.f.init_copy())

    def __str__(self):
        return f"{self.operator}({self.sub_exprs[0].str})"
    
    def propagate_changes(self):
        self.f = self.sub_exprs[0]
        return super().propagate_changes()

def NOT(expr):
    return AUnary.make('¬', expr)


class AAggregate(Expression):
    PRECEDENCE = 130

    def __init__(self, parent,
                 aggtype: str,
                 quantees: List[Quantee],
                 lambda_: Optional[str] = None,
                 f: Optional[Expression] = None,
                 if_: Optional[Expression] = None):
        self.aggtype = aggtype
        self.quantees: List[Quantee] = quantees
        self.lambda_ = lambda_
        self.if_orig = if_
        self.aggtype = ("#" if self.aggtype == "card" else
                        "min" if self.aggtype == "minimum" else
                        "max" if self.aggtype == "maximum" else
                        self.aggtype)
        split_quantees(self)
        self.f = TRUE if f is None and self.aggtype == "#" else f
        self.sub_exprs = [self.f]  # later: expressions to be summed
        if if_:
            self.sub_exprs.append(if_)
        self.annotated = False  # cannot test q_vars, because aggregate may not have quantee
        self.q = ''
        self.supersets, self.new_quantees, self.vars1 = None, None, None
        super().__init__()

    def init_copy(self,parent=None):
        f = None
        if_ = None
        if self.f != TRUE:
            f = self.f.init_copy()
        if self.if_orig:
            if_ = self.if_orig.init_copy()
        quantees = [q.init_copy() for q in self.quantees]
        return AAggregate(parent,self.aggtype,quantees,self.lambda_,f,if_)

    def __str__(self):
        # aggregates are over finite domains, and cannot have partial expansion
        if not self.annotated:
            assert len(self.sub_exprs) <= 2, "Internal error"
            vars = ",".join([f"{q}" for q in self.quantees])
            if self.aggtype in ["sum", "min", "max"]:
                out = (f"{self.aggtype}(lambda {vars} : "
                        f"{self.sub_exprs[0].str}"
                        f"{f' if {self.sub_exprs[1]}' if len(self.sub_exprs) == 2 else ''}"
                        f")" )
            else:
                out = (f"{self.aggtype}{{{vars} : "
                       f"{self.sub_exprs[0].str}"
                       f"}}")
        else:
            out = (f"{self.aggtype}{{"
                   f"{','.join(e.str for e in self.sub_exprs)}"
                   f"}}")
        return out

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.quantees = [deepcopy(q, memo) for q in self.quantees]
        return out

    def collect(self, questions, all_=True, co_constraints=True):
        if all_ or len(self.quantees) == 0:
            Expression.collect(self, questions, all_, co_constraints)
            for q in self.quantees:
                q.collect(questions, all_, co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        return AQuantification.collect_symbols(self, symbols, co_constraints)
    
    def propagate_changes(self):
        self.f = self.sub_exprs[0]
        return super().propagate_changes()


class AppliedSymbol(Expression):
    """Represents a symbol applied to arguments

    Args:
        symbol (SymbolExpr): the symbol to be applied to arguments

        is_enumerated (string): '' or 'is enumerated'

        is_enumeration (string): '' or 'in'

        in_enumeration (Enumeration): the enumeration following 'in'

        as_disjunction (Optional[Expression]):
            the translation of 'is_enumerated' and 'in_enumeration' as a disjunction

        decl (Declaration): the declaration of the symbol, if known

        in_head (Bool): True if the AppliedSymbol occurs in the head of a rule

        in_temp (Bool): whether it is used inside second order temporal predicate
    """
    PRECEDENCE = 200

    def __init__(self, parent,
                 symbol,
                 sub_exprs,
                 annotations: Optional[Annotations] =None,
                 is_enumerated='',
                 is_enumeration='',
                 in_enumeration=''):
        self.symbol : SymbolExpr = symbol
        self.sub_exprs = sub_exprs
        self.is_enumerated = is_enumerated
        self.is_enumeration = is_enumeration
        if self.is_enumeration == '∉':
            self.is_enumeration = 'not'
        self.in_enumeration = in_enumeration

        super().__init__(annotations=annotations)

        self.as_disjunction = None
        self.decl: Optional[Declaration] = None
        self.in_head = False
        self.in_temp = False

    @classmethod
    def make(cls,
             symbol: SymbolExpr,
             args: List[Expression],
             type_: Optional[SetName] = None,
             annotations: Optional[Annotations] =None,
             is_enumerated='',
             is_enumeration='',
             in_enumeration='',
             type_check=True
             ) -> AppliedSymbol:
        out = cls(None, symbol, args, annotations,
                  is_enumerated, is_enumeration, in_enumeration)
        out.sub_exprs = args
        # annotate
        out.decl = symbol.decl
        out.type = type_
        return out.fill_attributes_and_check(type_check)

    @classmethod
    def construct(cls, constructor, args):
        out= cls.make(SymbolExpr.make(constructor.name), args)
        out.decl = constructor
        out.type = constructor.codomain
        out.variables = set()
        return out

    def __str__(self):
        out = f"{self.symbol}({', '.join([x.str for x in self.sub_exprs])})"
        if self.in_enumeration:
            enum = f"{', '.join(str(e) for e in self.in_enumeration.tuples)}"
        return (f"{out}"
                f"{ ' '+self.is_enumerated if self.is_enumerated else ''}"
                f"{ f' {self.is_enumeration} {{{enum}}}' if self.in_enumeration else ''}")

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.symbol = deepcopy(self.symbol, memo)
        out.as_disjunction = deepcopy(self.as_disjunction, memo)
        return out

    def init_copy(self,parent=None):
        #print("sfas")
        #print(self.sub_exprs)
        sub_ex = [e.init_copy() for e in self.sub_exprs]
        return AppliedSymbol(parent,self.symbol.init_copy(),sub_ex,None,self.is_enumerated,self.is_enumeration,self.in_enumeration)

    def collect(self, questions, all_=True, co_constraints=True):
        if self.decl and self.decl.name not in RESERVED_SYMBOLS:
            questions.append(self)
            if self.is_enumerated or self.in_enumeration:
                app = AppliedSymbol.make(self.symbol, self.sub_exprs)
                questions.append(app)
        self.symbol.collect(questions, all_, co_constraints)
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)
        if co_constraints and self.co_constraint is not None:
            self.co_constraint.collect(questions, all_, co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        self.symbol.collect_symbols(symbols, co_constraints)
        return symbols

    def has_decision(self):
        return ((self.decl.block is not None and not self.decl.block.name == 'environment')
            or any(e.has_decision() for e in self.sub_exprs))

    def type_inference(self, voc: Vocabulary):
        decl = (voc.symbol_decls.get(self.symbol.name, None)
                 if voc and hasattr(voc, "symbol_decls")
                 else None)
        if decl:
            self.check(decl.arity == len(self.sub_exprs),
                f"Incorrect number of arguments in {self}: "
                f"should be {decl.arity}")
        # try:
        out = {}
        for i, e in enumerate(self.sub_exprs):
            if decl and type(e) in [Variable, UnappliedSymbol]:
                out[e.name] = decl.domains[i]
            else:
                out.update(e.type_inference(voc))
        return out

    def is_value(self) -> bool:
        # independent of is_enumeration and in_enumeration !
        return (type(self.decl) == Constructor
                and all(e.is_value() for e in self.sub_exprs))

    def is_reified(self):
        # independent of is_enumeration and in_enumeration !
        return (not all (e.is_value() for e in self.sub_exprs))

    def generate_constructors(self, constructors: dict):
        assert self.symbol.name, "Can't use concepts here"
        symbol = self.symbol.name
        if symbol in ['unit', 'heading']:
            assert type(self.sub_exprs[0]) == UnappliedSymbol, "Internal error"
            constructor = CONSTRUCTOR(self.sub_exprs[0].name)
            constructors[symbol].append(constructor)

class StartAppliedSymbol(Expression):
    """Represents a Start symbol applied to  another applied symbol 

    Args:
        arg (AppliedSymbol): the applied symbol 

        in_head (Bool): True if the AppliedSymbol occurs in the head of a rule
    """
    PRECEDENCE = 200

    def __init__(self, parent,
                 arg):
        self.symbol  = SymbolExpr(self,'Start',None,None)
        self.sub_expr: AppliedSymbol  = arg
        self.sub_exprs = [arg]
        super().__init__()

        #self.as_disjunction = None
        #self.decl = None
        self.in_head = False

    @classmethod
    def make(cls,
             symbol: SymbolExpr,
             arg: AppliedSymbol,
             ) -> StartAppliedSymbol:
        out = cls(None, symbol, arg)
        out.sub_exprs = [arg]
        # annotate
        out.decl = symbol.decl
        return out.annotate1()

    #@classmethod
    #def construct(cls, constructor, args):

    def __str__(self):
        out = f"{self.symbol}({self.sub_expr.str})"
        return (f"{out}")

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.symbol = deepcopy(out.symbol)
        #out.as_disjunction = deepcopy(out.as_disjunction)
        return out
    def init_copy(self,parent=None):
        return StartAppliedSymbol(parent,self.sub_expr.init_copy())

    def collect(self, questions, all_=True, co_constraints=True):
        self.sub_expr.collect(questions,all,co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        self.symbol.collect_symbols(symbols, co_constraints)
        return symbols

    def has_decision(self):
        return self.sub_expr.has_decision()


    def is_value(self) -> bool:
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_value()

    def is_reified(self):
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_reified()

    def generate_constructors(self, constructors: dict):
        self.sub_expr.generate_constructors(constructors,dict)

class NowAppliedSymbol(Expression):
    """Represents a Start symbol applied to  another applied symbol 

    Args:
        arg (AppliedSymbol): the applied symbol 

        in_head (Bool): True if the AppliedSymbol occurs in the head of a rule
    """
    PRECEDENCE = 200

    def __init__(self, parent,
                 arg):
        self.symbol  = SymbolExpr(self,'Now',None,None)
        self.sub_expr: AppliedSymbol  = arg
        self.sub_exprs = [arg]
        super().__init__()

        #self.as_disjunction = None
        #self.decl = None
        self.in_head = False

    @classmethod
    def make(cls,
             symbol: SymbolExpr,
             arg: AppliedSymbol,
             ) -> StartAppliedSymbol:
        out = cls(None, symbol, arg)
        out.sub_exprs = [arg]
        # annotate
        out.decl = symbol.decl
        return out.annotate1()

    #@classmethod
    #def construct(cls, constructor, args):

    def __str__(self):
        out = f"{self.symbol}({self.sub_expr.str})"
        return (f"{out}")

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.symbol = deepcopy(out.symbol)
        #out.as_disjunction = deepcopy(out.as_disjunction)
        return out
    def init_copy(self,parent=None):
        return NowAppliedSymbol(parent,self.sub_expr.init_copy())

    def collect(self, questions, all_=True, co_constraints=True):
        self.sub_expr.collect(questions,all,co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        self.symbol.collect_symbols(symbols, co_constraints)
        return symbols

    def has_decision(self):
        return self.sub_expr.has_decision()
        
    def is_value(self) -> bool:
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_value()

    def is_reified(self):
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_reified()

    def generate_constructors(self, constructors: dict):
        self.sub_expr.generate_constructors(constructors,dict)

class NextAppliedSymbol(Expression):
    """Represents a Start symbol applied to  another applied symbol 

    Args:
        arg (AppliedSymbol): the applied symbol 

        in_head (Bool): True if the AppliedSymbol occurs in the head of a rule
    """
    PRECEDENCE = 200

    def __init__(self, parent,
                 arg):
        self.symbol  = SymbolExpr(self,'Next',None,None)
        self.sub_expr: AppliedSymbol  = arg
        self.sub_exprs = [arg]

        super().__init__()

        #self.as_disjunction = None
        #self.decl = None
        self.in_head = False

    @classmethod
    def make(cls,
             symbol: SymbolExpr,
             arg: AppliedSymbol,
             ) -> NextAppliedSymbol:
        out = cls(None, symbol, arg)
        out.sub_exprs = [arg]
        # annotate
        out.decl = symbol.decl
        return out.annotate1()

    #@classmethod
    #def construct(cls, constructor, args):

    def __str__(self):
        out = f"{self.symbol}({self.sub_expr.str})"
        return (f"{out}")

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.symbol = deepcopy(out.symbol)
        #out.as_disjunction = deepcopy(out.as_disjunction)
        return out
    def init_copy(self,parent=None):
        return NextAppliedSymbol(parent,self.sub_expr.init_copy())

    def collect(self, questions, all_=True, co_constraints=True):
        self.sub_expr.collect(questions,all,co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        self.symbol.collect_symbols(symbols, co_constraints)
        return symbols

    def has_decision(self):
        return self.sub_expr.has_decision()

    def is_value(self) -> bool:
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_value()

    def is_reified(self):
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_reified()

    def generate_constructors(self, constructors: dict):
        self.sub_expr.generate_constructors(constructors,dict)

class CauseTrueAppliedSymbol(Expression):
    """Represents a Positive Causality symbol applied to  another applied symbol 
    """
    PRECEDENCE = 200

    def __init__(self, parent,
                 arg):
        self.symbol  = SymbolExpr(self,'+',None,None)
        self.sub_expr: AppliedSymbol  = arg
        self.sub_exprs = [arg]
        super().__init__()
        self.in_head = False

    @classmethod
    def make(cls,
             symbol: SymbolExpr,
             arg: AppliedSymbol,
             ) -> CauseTrueAppliedSymbol:
        out = cls(None, symbol, arg)
        out.sub_exprs = [arg]
        # annotate
        out.decl = symbol.decl
        return out.annotate1()

    #@classmethod
    #def construct(cls, constructor, args):

    def __str__(self):
        out = f"{self.symbol}({self.sub_expr.str})"
        return (f"{out}")

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.symbol = deepcopy(out.symbol)
        #out.as_disjunction = deepcopy(out.as_disjunction)
        return out
    def init_copy(self,parent=None):
        return CauseTrueAppliedSymbol(parent,self.sub_expr.init_copy())

    def collect(self, questions, all_=True, co_constraints=True):
        self.sub_expr.collect(questions,all,co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        self.symbol.collect_symbols(symbols, co_constraints)
        return symbols

    def has_decision(self):
        return self.sub_expr.has_decision()

    def is_value(self) -> bool:
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_value()

    def is_reified(self):
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_reified()

    def generate_constructors(self, constructors: dict):
        self.sub_expr.generate_constructors(constructors,dict)

class CauseFalseAppliedSymbol(Expression):
    """Represents a Positive Causality symbol applied to  another applied symbol 
    """
    PRECEDENCE = 200

    def __init__(self, parent,
                 arg):
        self.symbol  = SymbolExpr(self,'-',None,None)
        self.sub_expr: AppliedSymbol  = arg
        self.sub_exprs = [arg]
        super().__init__()
        self.in_head = False

    @classmethod
    def make(cls,
             symbol: SymbolExpr,
             arg: AppliedSymbol,
             ) -> CauseFalseAppliedSymbol:
        out = cls(None, symbol, arg)
        out.sub_exprs = [arg]
        # annotate
        out.decl = symbol.decl
        return out.annotate1()

    #@classmethod
    #def construct(cls, constructor, args):

    def __str__(self):
        out = f"{self.symbol}({self.sub_expr.str})"
        return (f"{out}")

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.symbol = deepcopy(out.symbol)
        return out
    def init_copy(self,parent=None):
        return CauseFalseAppliedSymbol(parent,self.sub_expr.init_copy())

    def collect(self, questions, all_=True, co_constraints=True):
        self.sub_expr.collect(questions,all,co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        self.symbol.collect_symbols(symbols, co_constraints)
        return symbols

    def has_decision(self):
        return self.sub_expr.has_decision()

    def is_value(self) -> bool:
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_value()

    def is_reified(self):
        # independent of is_enumeration and in_enumeration !
        return self.sub_expr.is_reified()

    def generate_constructors(self, constructors: dict):
        self.sub_expr.generate_constructors(constructors,dict)

class GLFormula(Expression):
    """
        Repressents the following LTL formula: G p 
    """
    def __init__(self,parent,expr:LFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "G " + str(self.expr) 

class XLFormula(Expression):
    """
        Repressents the following LTL formula: X p 
    """
    def __init__(self,parent,expr:LFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "X " + str(self.expr) 

class FLFormula(Expression):
    """
        Repressents the following LTL formula: F p 
    """
    def __init__(self,parent,expr:LFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "F " + str(self.expr) 

class NLFormula(Expression):
    """
        Repressents the following LTL formula: not p 
    """
    def __init__(self,parent,expr:LFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "not " + str(self.expr) 

class ULFormula(Expression):
    """
        Repressents the following LTL formula: q U p 
    """
    def __init__(self,parent,expr1:LFormula,expr2:LFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]
    def __str__(self) -> str:
        return str(self.expr1) + " U " + str(self.expr2)

class WLFormula(Expression):
    """
        Repressents the following LTL formula: q W p 
    """
    def __init__(self,parent,expr1:LFormula,expr2:LFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return str(self.expr1) + " W " + str(self.expr2)

class RLFormula(Expression):
    """
        Repressents the following LTL formula: q R p 
    """
    def __init__(self,parent,expr1:LFormula,expr2:LFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return str(self.expr1) + " R " + str(self.expr2)

class CLFormula(Expression):
    """
        Repressents the following LTL formula: q and p 
    """
    def __init__(self,parent,expr1:LFormula,expr2:LFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return str(self.expr1) + " & " + str(self.expr2)

class DLFormula(Expression):
    """
        Repressents the following LTL formula: q or p 
    """
    def __init__(self,parent,expr1:LFormula,expr2:LFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return str(self.expr1) + " or " + str(self.expr2)

class ILFormula(Expression):
    """
        Repressents the following LTL formula: q => p 
    """
    def __init__(self,parent,expr1:LFormula,expr2:LFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return str(self.expr1) + " => " + str(self.expr2)

LFormula = Union[Expression,ILFormula,DLFormula,CLFormula,NLFormula,XLFormula,FLFormula,GLFormula,ULFormula,WLFormula,RLFormula]



class ICFormula(Expression):
    """
        Repressents the following CTL formula: q => p 
    """
    def __init__(self,parent,expr1:CTLFormula,expr2:CTLFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return str(self.expr1) + " => " + str(self.expr2)
    
class DCFormula(Expression):
    """
        Repressents the following CTL formula: q or p 
    """
    def __init__(self,parent,expr1:CTLFormula,expr2:CTLFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return str(self.expr1) + " or " + str(self.expr2)
    
class CCFormula(Expression):
    """
        Repressents the following CTL formula: q AND p 
    """
    def __init__(self,parent,expr1:CTLFormula,expr2:CTLFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return str(self.expr1) + " and " + str(self.expr2)

class NCFormula(Expression):
    """
        Repressents the following CTL formula: not q  
    """
    def __init__(self,parent,expr:CTLFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "not " + str(self.expr) 

class AXFormula(Expression):
    """
        Repressents the following CTL formula: AX q  
    """
    def __init__(self,parent,expr:CTLFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "AX " + str(self.expr) 
    
class EXFormula(Expression):
    """
        Repressents the following CTL formula: EX q  
    """
    def __init__(self,parent,expr:CTLFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "EX " + str(self.expr) 
    
class AFFormula(Expression):
    """
        Repressents the following CTL formula: AF q  
    """
    def __init__(self,parent,expr:CTLFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "AF " + str(self.expr) 

class EFFormula(Expression):
    """
        Repressents the following CTL formula: EF q  
    """
    def __init__(self,parent,expr:CTLFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "EF " + str(self.expr) 
    
class AGFormula(Expression):
    """
        Repressents the following CTL formula: AG q  
    """
    def __init__(self,parent,expr:CTLFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "AG " + str(self.expr) 
    
class EGFormula(Expression):
    """
        Repressents the following CTL formula: EG q  
    """
    def __init__(self,parent,expr:CTLFormula):
        self.expr = expr
        self.sub_exprs = [expr]

    def __str__(self) -> str:
        return "EG " + str(self.expr) 
    
class AUFormula(Expression):
    """
        Repressents the following CTL formula: A q U p 
    """
    def __init__(self,parent,expr1:CTLFormula,expr2:CTLFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return "A " + str(self.expr1) + " U " + str(self.expr2)
    
class EUFormula(Expression):
    """
        Repressents the following CTL formula: E q U p 
    """
    def __init__(self,parent,expr1:CTLFormula,expr2:CTLFormula):
        self.expr1 = expr1
        self.expr2 = expr2
        self.sub_exprs = [expr1,expr2]

    def __str__(self) -> str:
        return "E " + str(self.expr1) + " U " + str(self.expr2)
    
CTLFormula = Union[Expression , NCFormula , CCFormula , DCFormula , ICFormula , AXFormula , EXFormula  , AFFormula , EFFormula , AGFormula , EGFormula , AUFormula , EUFormula]


class SymbolExpr(Expression):
    """ represents either a type name, a symbol name
    or a `$(..)` expression evaluating to a type or symbol name

    Attributes:

        name (Optional[str]): name of the type or symbol, or None

        eval (Optional[str]): `$` or None

        s (Optional[Expression]): argument of the `$`.

        decl (Optional[Declaration]): the declaration of the symbol

    Either `name` and `decl`are not None, or `eval` and `s` are not None.
    When `eval` is None, `s` is None too.
    """
    def __init__(self, parent,
                 name: Optional[str],
                 eval: Optional[str],
                 s: Optional[Expression]):
        self.name = unquote(name) if name else name
        self.eval = eval
        self.s = s
        self.sub_exprs = [s] if s is not None else []
        self.decl: Optional[Declaration] = None
        super().__init__()

    def init_copy(self,parent=None):
        s = None
        if self.s:
            s = self.s.init_copy()
        return SymbolExpr(parent,self.name,self.eval,s)

    @classmethod
    def make(cls, name: str) -> SymbolExpr:
        return (cls)(None, name, None, None)

    def __str__(self):
        return (f"$({self.sub_exprs[0]})" if self.eval else
                f"{self.name}")

class UnappliedSymbol(Expression):
    """The result of parsing a symbol not applied to arguments.
    Can be a constructor or a quantified variable.

    Variables are converted to Variable() by annotate().
    """
    PRECEDENCE = 200

    def __init__(self, parent: Optional[ASTNode], name: str):
        self.name = unquote(name)

        Expression.__init__(self)

        self.sub_exprs = []
        self.decl = None
        self.is_enumerated = None
        self.is_enumeration = None
        self.in_enumeration = None

    def init_copy(self,parent=None):
        return UnappliedSymbol(parent,self.name)

    @classmethod
    def construct(cls, constructor: Constructor):
        """Create an UnappliedSymbol from a constructor
        """
        out = (cls)(None, name=constructor.name)
        out.decl = constructor
        out.type = constructor.codomain
        out.variables = set()
        return out

    def is_value(self): return True

    def is_reified(self): return False

    def __str__(self): return self.name

TRUEC = CONSTRUCTOR('true')
FALSEC = CONSTRUCTOR('false')

TRUE = UnappliedSymbol.construct(TRUEC)
TRUE.type = BOOL_SETNAME
FALSE = UnappliedSymbol.construct(FALSEC)
FALSE.type = BOOL_SETNAME


class Variable(Expression):
    """AST node for a variable in a quantification or aggregate

    Args:
        name (str): name of the variable

        type (Optional[Union[SetName]]): sort of the variable, if known
    """
    PRECEDENCE = 200

    def __init__(self, parent,
                 name:str,
                 type: Optional[SetName]=None):
        self.name = name
        assert type is None or isinstance(type, SetName), \
            f"Internal error: {self}"

        super().__init__()

        self.type = type
        self.sub_exprs = []
        self.variables = set([self.name])

    def __str__(self): return self.name

    def __deepcopy__(self, memo):
        return self
    
    def init_copy(self,parent=None):
        s = None
        if self.type:
            s = self.type.init_copy()
        return Variable(parent,self.name,s)

    def fill_attributes_and_check(self: Expression) -> Expression: return self

    def has_variables(self) -> bool: return True

def VARIABLE(name: str, type: SetName):
    return Variable(None, name, type)


class Number(Expression):
    PRECEDENCE = 200

    def __init__(self, **kwargs):
        self.number = kwargs.pop('number')

        super().__init__()

        self.sub_exprs = []
        self.variables = set()
        self.py_value = 0 # to get the type

        ops = self.number.split("/")
        if len(ops) == 2:  # possible with z3_to_idp for rational value
            self.py_value = Fraction(self.number)
            self.type = REAL_SETNAME
        elif '.' in self.number:
            self.py_value = Fraction(self.number if not self.number.endswith('?') else
                                     self.number[:-1])
            self.type = REAL_SETNAME
        else:
            self.py_value = int(self.number)
            self.type = INT_SETNAME
        self.decl = None

    def __str__(self): return self.number

    def init_copy(self,parent=None):
        return Number(number=self.number)

    def real(self):
        """converts the INT number to REAL"""
        self.check(self.type in [INT_SETNAME, REAL_SETNAME], f"Can't convert {self} to {REAL}")
        return Number(number=str(float(self.py_value)))

    def is_value(self): return True

    def is_reified(self): return False

ZERO = Number(number='0')
ONE = Number(number='1')


class Date(Expression):
    PRECEDENCE = 200

    def __init__(self, **kwargs):
        self.iso = kwargs.pop('iso')

        dt = (date.today() if self.iso == '#TODAY' else
                     date.fromisoformat(self.iso[1:]))
        if 'y' in kwargs:
            y = int(kwargs.pop('y'))
            m = int(kwargs.pop('m'))
            d = int(kwargs.pop('d'))
            dt = dt + relativedelta(years=y, months=m, days=d)
        self.date = dt

        super().__init__()

        self.sub_exprs = []
        self.variables = set()

        self.py_value = int(self.date.toordinal())
        self.type = DATE_SETNAME

    @classmethod
    def make(cls, value: int) -> Date:
        return cls(iso=f"#{date.fromordinal(value).isoformat()}")

    def __str__(self): return f"#{self.date.isoformat()}"

    def init_copy(self,parent=None):
        return Date(iso=self.iso)

    def is_value(self): return True

    def is_reified(self): return False


class Brackets(Expression):
    PRECEDENCE = 200

    def __init__(self, parent, f, annotations: Optional[Annotations]=None):
        self.f = f
        self.sub_exprs = [self.f]

        super().__init__()
        self.annotations = (annotations.annotations if annotations else
            {'reading': self.f.annotations['reading']})

    def init_copy(self,parent=None):
        return Brackets(parent=parent,f=self.f.init_copy(),annotations=Annotations(None,[]))
    
    # don't @use_value, to have parenthesis
    def __str__(self): return f"({self.sub_exprs[0].str})"

    def propagate_changes(self):
        self.f = self.sub_exprs[0]
        return super().propagate_changes()


class RecDef(Expression):
    """represents a recursive definition
    """
    def __init__(self, parent, name, vars, expr):
        self.parent = parent
        self.name = name
        self.vars = vars
        self.sub_exprs = [expr]

        Expression.__init__(self)

        if parent:  # for error messages
            self._tx_position = parent. _tx_position
            self._tx_position_end = parent. _tx_position_end
   
    def init_copy(self,parent=None):
        return RecDef(parent,self.name,self.vars.init_copy(),self.sub_exprs[0].init_copy())
   
    def __str__(self):
        return (f"{self.name}("
                f"{', '.join(str(v) for v in self.vars)}"
                f") = {self.sub_exprs[0]}.")

Identifier = Union[AppliedSymbol, UnappliedSymbol, Number, Date]
Extension = Tuple[Optional[List[List[Identifier]]],  # None if the extension is infinite (e.g., Int)
                  Optional[Callable]]  # None if filtering is not required
