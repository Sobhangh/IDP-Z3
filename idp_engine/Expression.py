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


(They are monkey-patched by other modules)

"""
__all__ = ["ASTNode", "Expression", "Constructor", "IfExpr", "Quantee", "AQuantification",
           "BinaryOperator", "AImplication", "AEquivalence", "ARImplication",
           "ADisjunction", "AConjunction", "AComparison", "ASumMinus",
           "AMultDiv", "APower", "AUnary", "AAggregate", "AppliedSymbol",
           "Arguments", "UnappliedSymbol", "Variable",
           "Number", "Brackets", "TRUE", "FALSE", "ZERO", "ONE"]

import copy
from collections import ChainMap
import sys
from textx import get_location
from typing import Optional, List, Tuple, Dict, Set, Any

from .utils import unquote, OrderedSet, BOOL, SYMBOL, IDPZ3Error


class ASTNode(object):
    """superclass of all AST nodes
    """

    def check(self, condition, msg):
        """raises an exception if `condition` is not True

        Args:
            condition (Bool): condition to be satisfied
            msg (str): error message

        Raises:
            IDPZ3Error: when `condition` is not met
        """
        if not condition:
            location = get_location(self)
            line = location['line']
            col = location['col']
            raise IDPZ3Error(f"Error on line {line}, col {col}: {msg}")

    def dedup_nodes(self, kwargs, arg_name):
        """pops `arg_name` from kwargs as a list of named items
        and returns a mapping from name to items

        Args:
            kwargs (Dict[str, ASTNode])
            arg_name (str): name of the kwargs argument, e.g. "interpretations"

        Returns:
            Dict[str, ASTNode]: mapping from `name` to AST nodes

        Raises:
            AssertionError: in case of duplicate name
        """
        ast_nodes = kwargs.pop(arg_name)
        out = {}
        for i in ast_nodes:
            # can't get location here
            assert i.name not in out, f"Duplicate '{i.name}' in {arg_name}"
            out[i.name] = i
        return out

    def annotate(self, idp):
        return  # monkey-patched

    def annotate1(self, idp):
        return  # monkey-patched

    def interpret(self, problem: Any) -> "Expression":
        return self  # monkey-patched


class Expression(ASTNode):
    """The abstract class of AST nodes representing (sub-)expressions.

    Attributes:
        code (string):
            Textual representation of the expression.  Often used as a key.

            It is generated from the sub-tree.
            Some tree transformations change it (e.g., instantiate),
            others don't.

        sub_exprs (List[Expression]):
            The children of the AST node.

            The list may be reduced by simplification.

        type (string):
            The name of the type of the expression, e.g., ``bool``.

        co_constraint (Expression, optional):
            A constraint attached to the node.

            For example, the co_constraint of ``square(length(top()))`` is
            ``square(length(top())) = length(top())*length(top()).``,
            assuming ``square`` is appropriately defined.

            The co_constraint of a defined symbol applied to arguments
            is the instantiation of the definition for those arguments.
            This is useful for definitions over infinite domains,
            as well as to compute relevant questions.

        simpler (Expression, optional):
            A simpler, equivalent expression.

            Equivalence is computed in the context of the theory and structure.
            Simplifying an expression is useful for efficiency
            and to compute relevant questions.

        value (Optional[Expression]):
            A rigid term equivalent to the expression, obtained by
            transformation.

            Equivalence is computed in the context of the theory and structure.

        annotations (Dict):
            The set of annotations given by the expert in the IDP source code.

            ``annotations['reading']`` is the annotation
            giving the intended meaning of the expression (in English).

        original (Expression):
            The original expression, before propagation and simplification.

        fresh_vars (Set(string)):
            The set of names of the variables in the expression.

    """
    __slots__ = ('sub_exprs', 'simpler', 'value', 'status', 'code',
                 'annotations', 'original', 'str', 'fresh_vars', 'type',
                 '_reified', 'is_type_constraint_for', 'co_constraint',
                 'normal', 'questions', 'relevant')

    COUNT = 0

    def __init__(self):
        self.sub_exprs: List["Expression"]
        self.simpler: Optional["Expression"] = None
        self.value: Optional["Expression"] = None

        self.code: str = sys.intern(str(self))
        self.annotations: Dict[str, str] = {'reading': self.code}
        self.original: Expression = self

        self.str: str = self.code
        self.fresh_vars: Optional[Set[str]] = None
        self.type: Optional[str] = None
        self._reified: Optional["Expression"] = None
        self.is_type_constraint_for: Optional[str] = None
        self.co_constraint: Optional["Expression"] = None

        # attributes of the top node of a (co-)constraint
        self.questions: Optional[OrderedSet] = None
        self.relevant: Optional[bool] = None
        self.block: Any = None

    def copy(self):
        " create a deep copy (except for Constructor and Number) "
        if type(self) in [Constructor, Number, Variable]:
            return self
        out = copy.copy(self)
        out.sub_exprs = [e.copy() for e in out.sub_exprs]
        out.value = None if out.value is None else out.value.copy()
        out.simpler = None if out.simpler is None else out.simpler.copy()
        out.co_constraint = (None if out.co_constraint is None
                             else out.co_constraint.copy())
        if hasattr(self, 'questions'):
            out.questions = copy.copy(self.questions)
        return out

    def same_as(self, other):
        if self.value is not None:
            return self.value  .same_as(other)
        if self.simpler is not None:
            return self.simpler.same_as(other)
        if other.value is not None:
            return self.same_as(other.value)
        if other.simpler is not None:
            return self.same_as(other.simpler)

        if (isinstance(self, Brackets)
           or (isinstance(self, AQuantification) and len(self.q_vars) == 0)):
            return self.sub_exprs[0].same_as(other)
        if (isinstance(other, Brackets)
           or (isinstance(other, AQuantification) and len(other.q_vars) == 0)):
            return self.same_as(other.sub_exprs[0])

        return self.str == other.str and type(self) == type(other)

    def __repr__(self): return str(self)

    def __str__(self):
        self.check(self.value is not self, "Internal error")
        if self.value is not None:
            return str(self.value)
        if self.simpler is not None:
            return str(self.simpler)
        return self.__str1__()

    def __log__(self):  # for debugWithYamlLog
        return {'class': type(self).__name__,
                'code': self.code,
                'str': self.str,
                'co_constraint': self.co_constraint}

    def collect(self, questions, all_=True, co_constraints=True):
        """collects the questions in self.

        `questions` is an OrderedSet of Expression
        Questions are the terms and the simplest sub-formula that
        can be evaluated.
        `collect` uses the simplified version of the expression.

        all_=False : ignore expanded formulas
        and AppliedSymbol interpreted in a structure
        co_constraints=False : ignore co_constraints

        default implementation for Constructor, IfExpr, AUnary, Variable,
        Number_constant, Brackets
        """

        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)

    def _questions(self):  # for debugging
        questions = OrderedSet()
        self.collect(questions)
        return questions

    def generate_constructors(self, constructors: dict):
        """ fills the list `constructors` with all constructors belonging to
        open types.
        """
        for e in self.sub_exprs:
            e.generate_constructors(constructors)

    def unknown_symbols(self, co_constraints=True):
        """ returns the list of symbol declarations in self, ignoring type constraints

        returns Dict[name, Declaration]
        """
        if self.is_type_constraint_for is not None:  # ignore type constraints
            return {}
        questions = OrderedSet()
        self.collect(questions, all_=True, co_constraints=co_constraints)
        out = {e.decl.name: e.decl for e in questions.values()
               if hasattr(e, 'decl')}
        return out

    def co_constraints(self, co_constraints):
        """ collects the constraints attached to AST nodes, e.g. instantiated
        definitions

        `co_constraints is an OrderedSet of Expression
        """
        if self.co_constraint is not None:
            co_constraints.append(self.co_constraint)
            self.co_constraint.co_constraints(co_constraints)
        for e in self.sub_exprs:
            e.co_constraints(co_constraints)

    def as_rigid(self):
        " returns a Number or Constructor, or None "
        return self.value

    def is_reified(self): return True

    def is_assignment(self) -> bool:
        """

        Returns:
            bool: True if `self` assigns a rigid term to a rigid function application
        """
        return False

    def has_decision(self):
        # returns true if it contains a variable declared in decision
        # vocabulary
        return any(e.has_decision() for e in self.sub_exprs)

    def type_inference(self):
        # returns a dictionary {Variable : Sort}
        try:
            return dict(ChainMap(*(e.type_inference() for e in self.sub_exprs)))
        except AttributeError as e:
            if "has no attribute 'sorts'" in str(e):
                msg = f"Incorrect arity for {self}"
            else:
                msg = f"Unknown error for {self}"
            self.check(False, msg)

    def __str1__(self) -> str:
        return ''  # monkey-patched

    def update_exprs(self, new_exprs) -> "Expression":
        return self  # monkey-patched

    def simplify1(self) -> "Expression":
        return self  # monkey-patched

    def substitute(self,
                   e0: "Expression",
                   e1: "Expression",
                   assignments: "Assignments",
                   todo=None) -> "Expression":
        return self  # monkey-patched

    def instantiate(self,
                    e0: "Expression",
                    e1: "Expression",
                    problem: "Problem"=None
                    ) -> "Expression":
        return self  # monkey-patched

    def symbolic_propagate(self,
                           assignments: "Assignments",
                           truth: Optional["Constructor"] = None
                           ) -> List[Tuple["Expression", "Constructor"]]:
        return []  # monkey-patched

    def propagate1(self,
                   assignments: "Assignments",
                   truth: Optional["Expression"] = None
                   ) -> List[Tuple["Expression", bool]]:
        return []  # monkey-patched

    def translate(self):
        pass  # monkey-patched

    def reified(self):
        pass  # monkey-patched

    def translate1(self):
        pass  # monkey-patched

    def as_set_condition(self) -> Tuple[Optional["AppliedSymbol"], Optional[bool], Optional["Enumeration"]]:
        """Returns an equivalent expression of the type "x in y", or None

        Returns:
            Tuple[Optional[AppliedSymbol], Optional[bool], Optional[Enumeration]]: meaning "expr is (not) in enumeration"
        """
        return (None, None, None)

class Constructor(Expression):
    PRECEDENCE = 200

    def __init__(self, **kwargs):
        self.name = unquote(kwargs.pop('name'))
        self.sub_exprs = []

        super().__init__()
        self.fresh_vars = set()
        self.symbol = None  # set only for SYMBOL constructors
        self.translated: Any = None

    def __str1__(self): return self.name

    def as_rigid(self): return self

    def is_reified(self): return False


TRUE = Constructor(name='true')
FALSE = Constructor(name='false')


class IfExpr(Expression):
    PRECEDENCE = 10
    IF = 0
    THEN = 1
    ELSE = 2

    def __init__(self, **kwargs):
        self.if_f = kwargs.pop('if_f')
        self.then_f = kwargs.pop('then_f')
        self.else_f = kwargs.pop('else_f')

        self.sub_exprs = [self.if_f, self.then_f, self.else_f]
        super().__init__()

    @classmethod
    def make(cls, if_f, then_f, else_f):
        out = (cls)(if_f=if_f, then_f=then_f, else_f=else_f)
        return out.annotate1().simplify1()

    def __str1__(self):
        return (f" if   {self.sub_exprs[IfExpr.IF  ].str}"
                f" then {self.sub_exprs[IfExpr.THEN].str}"
                f" else {self.sub_exprs[IfExpr.ELSE].str}")


class Quantee(object):
    def __init__(self, var, sort):
        self.var = var
        self.sort = sort


class AQuantification(Expression):
    PRECEDENCE = 20

    def __init__(self, **kwargs):
        self.q = kwargs.pop('q')
        self.quantees = kwargs.pop('quantees')
        self.f = kwargs.pop('f')

        self.q = '∀' if self.q == '!' else '∃' if self.q == "?" else self.q
        self.vars, self.sorts = [], []
        for q in self.quantees:
            self.vars.append(q.var)
            self.sorts.append(q.sort)

        self.sub_exprs = [self.f]
        self.quantifier_is_expanded = False
        super().__init__()

        self.q_vars = {}  # dict[String, Variable]
        self.type = BOOL

    @classmethod
    def make(cls, q, q_vars, f):
        "make and annotate a quantified formula"
        quantees = [Quantee(v.name, v.sort) for v in q_vars.values()]
        out = cls(q=q, quantees=quantees, f=f)
        out.q_vars = q_vars
        return out.annotate1()

    def __str1__(self):
        if not self.quantifier_is_expanded:
            self.check(len(self.vars) == len(self.sorts), "Internal error")
            vars = ''.join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
            return f"{self.q}{vars} : {self.sub_exprs[0].str}"
        else:
            return self.sub_exprs[0].str

    def collect(self, questions, all_=True, co_constraints=True):
        questions.append(self)
        if all_:
            for e in self.sub_exprs:
                e.collect(questions, all_, co_constraints)


class BinaryOperator(Expression):
    PRECEDENDE = 0  # monkey-patched
    MAP = dict()  # monkey-patched

    def __init__(self, **kwargs):
        self.sub_exprs = kwargs.pop('sub_exprs')
        self.operator = kwargs.pop('operator')

        self.operator = list(map(
            lambda op: "≤" if op == "=<" else "≥" if op == ">=" else "≠" if op == "~=" else \
                "⇔" if op == "<=>" else "⇐" if op == "<=" else "⇒" if op == "=>" else \
                "∨" if op == "|" else "∧" if op == "&" else op
            , self.operator))

        super().__init__()

        self.type = BOOL if self.operator[0] in '&|∧∨⇒⇐⇔' \
               else BOOL if self.operator[0] in '=<>≤≥≠' \
               else None

    @classmethod
    def make(cls, ops, operands):
        """ creates a BinaryOp
            beware: cls must be specific for ops !"""
        if len(operands) == 1:
            return operands[0]
        if isinstance(ops, str):
            ops = [ops] * (len(operands)-1)
        out = (cls)(sub_exprs=operands, operator=ops)
        return out.annotate1().simplify1()

    def __str1__(self):
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


class AImplication(BinaryOperator):
    PRECEDENCE = 50


class AEquivalence(BinaryOperator):
    PRECEDENCE = 40


class ARImplication(BinaryOperator):
    PRECEDENCE = 30

class ADisjunction(BinaryOperator):
    PRECEDENCE = 60

    def __str1__(self):
        if not hasattr(self, 'enumerated'):
            return super().__str1__()
        return f"{self.sub_exprs[0].sub_exprs[0].code} in {{{self.enumerated}}}"


class AConjunction(BinaryOperator):
    PRECEDENCE = 70


class AComparison(BinaryOperator):
    PRECEDENCE = 80

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_assignment(self):
        # f(x)=y
        return len(self.sub_exprs) == 2 and \
                self.operator in [['='], ['≠']] \
                and isinstance(self.sub_exprs[0], AppliedSymbol) \
                and all(e.as_rigid() is not None
                        for e in self.sub_exprs[0].sub_exprs) \
                and self.sub_exprs[1].as_rigid() is not None


class ASumMinus(BinaryOperator):
    PRECEDENCE = 90


class AMultDiv(BinaryOperator):
    PRECEDENCE = 100


class APower(BinaryOperator):
    PRECEDENCE = 110


class AUnary(Expression):
    PRECEDENCE = 120
    MAP = dict()  # monkey-patched

    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        self.operators = kwargs.pop('operators')
        self.operators = ['¬' if c == '~' else c for c in self.operators]
        self.operator = self.operators[0]
        self.check(all([c == self.operator for c in self.operators]),
                   "Incorrect mix of unary operators")

        self.sub_exprs = [self.f]
        super().__init__()

    @classmethod
    def make(cls, op, expr):
        out = AUnary(operators=[op], f=expr)
        return out.annotate1().simplify1()

    def __str1__(self):
        return f"{self.operator}({self.sub_exprs[0].str})"


class AAggregate(Expression):
    PRECEDENCE = 130
    CONDITION = 0
    OUT = 1

    def __init__(self, **kwargs):
        self.aggtype = kwargs.pop('aggtype')
        self.quantees = kwargs.pop('quantees')
        self.f = kwargs.pop('f')
        self.out = kwargs.pop('out')

        self.vars, self.sorts = [], []
        for q in self.quantees:
            self.vars.append(q.var)
            self.sorts.append(q.sort)
        self.sub_exprs = [self.f, self.out] if self.out else [self.f]  # later: expressions to be summed
        self.quantifier_is_expanded = False  # cannot test q_vars, because aggregate may not have quantee
        super().__init__()

        self.q_vars = {}

        if self.aggtype == "sum" and self.out is None:
            raise Exception("Must have output variable for sum")
        if self.aggtype != "sum" and self.out is not None:
            raise Exception("Can't have output variable for  #")

    def __str1__(self):
        if not self.quantifier_is_expanded:
            self.check(len(self.vars) == len(self.sorts), "Internal error")
            vars = "".join([f"{v}[{s}]" for v, s in zip(self.vars, self.sorts)])
            output = f" : {self.sub_exprs[AAggregate.OUT].str}" if self.out else ""
            out = (f"{self.aggtype}{{{vars} : "
                   f"{self.sub_exprs[AAggregate.CONDITION].str}"
                   f"{output}}}")
        else:
            out = (f"{self.aggtype}{{"
                   f"{','.join(e.str for e in self.sub_exprs)}"
                   f"}}")
        return out


    def collect(self, questions, all_=True, co_constraints=True):
        if all_ or len(self.sorts) == 0:
            for e in self.sub_exprs:
                e.collect(questions, all_, co_constraints)


class AppliedSymbol(Expression):
    PRECEDENCE = 200

    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.args = kwargs.pop('args')
        if 'is_enumerated' in kwargs:
            self.is_enumerated = kwargs.pop('is_enumerated')
        else:
            self.is_enumerated = ''
        if 'is_enumeration' in kwargs:
            self.is_enumeration = kwargs.pop('is_enumeration')
        else:
            self.is_enumeration = ''
        if 'in_enumeration' in kwargs:
            self.in_enumeration = kwargs.pop('in_enumeration')
        else:
            self.in_enumeration = None

        self.sub_exprs = self.args.sub_exprs
        super().__init__()

        self.decl = None
        self.name = self.s.name
        self.in_head = False

    @classmethod
    def make(cls, symbol, args, **kwargs):
        out = cls(s=symbol, args=Arguments(sub_exprs=args), **kwargs)
        out.sub_exprs = args
        # annotate
        out.decl = symbol.decl
        return out.annotate1()

    def __str1__(self):
        if len(self.sub_exprs) == 0:
            out = f"{str(self.s)}"
        else:
            out = f"{str(self.s)}({','.join([x.str for x in self.sub_exprs])})"
        if self.in_enumeration:
            enum = f"{', '.join(str(e) for e in self.in_enumeration.tuples)}"
        return (f"{out}"
                f"{ ' '+self.is_enumerated if self.is_enumerated else ''}"
                f"{ f' {self.is_enumeration} {{{enum}}}' if self.in_enumeration else ''}")

    def collect(self, questions, all_=True, co_constraints=True):
        if self.decl.name != SYMBOL and self.name != '__relevant':
            questions.append(self)
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)
        if co_constraints and self.co_constraint is not None:
            self.co_constraint.collect(questions, all_, co_constraints)

    def has_decision(self):
        self.check(self.decl.block is not None, "Internal error")
        return not self.decl.block.name == 'environment' \
            or any(e.has_decision() for e in self.sub_exprs)

    def type_inference(self):
        try:
            out = {}
            for i, e in enumerate(self.sub_exprs):
                if self.decl.name != SYMBOL and isinstance(e, Variable):
                    out[e.name] = self.decl.sorts[i]
                else:
                    out.update(e.type_inference())
            return out
        except AttributeError as e:
            #
            if "object has no attribute 'sorts'" in str(e):
                msg = f"Unexpected arity for symbol {self}"
            else:
                msg = f"Unknown error for symbol {self}"
            self.check(False, msg)

    def is_reified(self):
        return (self.in_enumeration or self.is_enumerated
                or any(e.is_reified() for e in self.sub_exprs))

    def reified(self):
        if self._reified is None:
            self._reified = ( super().reified() if self.is_reified() else
                 self.translate() )
        return self._reified

    def generate_constructors(self, constructors: dict):
        if self.name == 'unit' or self.name == 'category':
            constructor = Constructor(name=self.sub_exprs[0].name)
            constructors[self.name].append(constructor)

class Arguments(object):
    def __init__(self, **kwargs):
        self.sub_exprs = kwargs.pop('sub_exprs')
        super().__init__()


class UnappliedSymbol(Expression):
    """The result of parsing a symbol not applied to arguments.
    Can be a constructor, a quantified variable,
    or a symbol application without arguments (by abuse of notation, e.g. 'p').
    (The parsing of numbers result directly in Number nodes)

    Converted to the proper AST class by annotate().
    """
    PRECEDENCE = 200

    def __init__(self, **kwargs):
        self.s = kwargs.pop('s')
        self.name = self.s.name

        Expression.__init__(self)

        self.sub_exprs = []
        self.decl = None
        self.translated = None
        self.is_enumerated = None
        self.is_enumeration = None
        self.in_enumeration = None

    def __str1__(self): return self.name

    def collect(self, questions, all_=True, co_constraints=True):
        self.check(False, f"Internal error: {self}")


class Variable(Expression):
    """AST node for a variable in a quantification or aggregate
    """
    PRECEDENCE = 200

    def __init__(self, name, sort):
        self.name = name
        self.sort = sort

        super().__init__()

        self.type = sort.name if sort else ''
        self.sub_exprs = []
        self.translated = None
        self.fresh_vars = set([self.name])

    def __str1__(self): return self.name


class Number(Expression):
    PRECEDENCE = 200

    def __init__(self, **kwargs):
        self.number = kwargs.pop('number')

        super().__init__()

        self.sub_exprs = []
        self.fresh_vars = set()

        self.translated = None
        self.translate()  # also sets self.type

    def __str__(self): return self.number

    def as_rigid(self): return self
    def is_reified(self): return False


ZERO = Number(number='0')
ONE = Number(number='1')


class Brackets(Expression):
    PRECEDENCE = 200

    def __init__(self, **kwargs):
        self.f = kwargs.pop('f')
        annotations = kwargs.pop('annotations')
        self.sub_exprs = [self.f]

        super().__init__()
        if type(annotations) == dict:
            self.annotations = annotations
        elif annotations is None:
            self.annotations['reading'] = ''
        else:  # Annotations instance
            self.annotations = annotations.annotations

    # don't @use_value, to have parenthesis
    def __str__(self): return f"({self.sub_exprs[0].str})"
    def __str1__(self): return str(self)

    def as_rigid(self):
        return self.sub_exprs[0].as_rigid()

