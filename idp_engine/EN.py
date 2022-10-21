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

Methods to show a Theory in plain English.

"""

from copy import copy

from .Parse import IDP
from .Parse import Definition, Rule
from .Expression import (ASTNode, AQuantification, AAggregate, Operator,
                         AComparison, AUnary, AppliedSymbol, Brackets)
from .Theory import Theory


def EN(self):
    out = "\nTheory: \n".join(Theory(th).EN() for th in self.theories.values())
    return "Theory: \n" + out
IDP.EN = EN


def EN(self):
    return str(self)
ASTNode.EN = EN


def EN(self):
    rules = '\n'.join(f"    {r.original.EN()}." for r in self.rules)
    return "Definition:\n" + rules
Definition.EN = EN


def EN(self):
    #TODO len(self.quantees) > self.definiendum.symbol.decl.arity
    vars = ','.join([f"{q}" for q in self.quantees])
    quant = f"for each {','.join(str(q) for q in self.quantees)}, " if vars else ""
    return (f"{quant}"
            f"{self.definiendum.EN()} "
            f"{(' is ' + str(self.out.EN())) if self.out else ''}"
            f" if {str(self.body.EN())}").replace("  ", " ")
Rule.EN = EN


def EN(self):
    self = self.original
    vars = ','.join([f"{q}" for q in self.quantees])
    if self.q == '∀':
        return f"for every {vars}, it is true that {self.sub_exprs[0].EN()}"
    else:
        return f"there is a {vars} such that {self.sub_exprs[0].EN()}"
AQuantification.EN = EN


def EN(self):
    self = self.original
    vars = ",".join([f"{q}" for q in self.quantees])
    if self.aggtype in ['sum', 'min', 'max']:
        return (f"the {self.aggtype} of "
                f"{self.sub_exprs[0].EN()} "
                f"for all {vars}")
    else: #  #
        return (f"the number of {vars} satisfying "
                f"{self.sub_exprs[0].EN()}")
AAggregate.EN = EN


Operator.EN_map =  {'∧': " and ",
                    '∨': " or ",
                    '⇒': " is a sufficient condition for ",
                    '⇐': " is a necessary condition for ",
                    '⇔': " iff ",
                    "=": " is ",
                    "≠": " is not ",
                    }

def EN(self):
    def parenthesis(precedence, x):
        return f"({x.EN()})" if type(x).PRECEDENCE <= precedence else f"{x.EN()}"
    precedence = type(self).PRECEDENCE
    temp = parenthesis(precedence, self.sub_exprs[0])
    for i in range(1, len(self.sub_exprs)):
        op = Operator.EN_map.get(self.operator[i-1], self.operator[i-1])
        temp += f" {op} {parenthesis(precedence, self.sub_exprs[i])}"
    return temp
Operator.EN = EN


def EN(self):
    if (type(self.sub_exprs[0]) == AComparison
        and len(self.sub_exprs[0].sub_exprs) == 2
        and self.sub_exprs[0].operator[0] == "="):
        # ~(a=b)
        new_expr = copy(self.sub_exprs[0])
        new_expr.operator[0] = "≠"
        return new_expr.EN()
    return f"{self.operator}({self.sub_exprs[0].EN()})"
AUnary.EN = EN


def EN(self):
    en = self.symbol.decl.annotations.get('EN', None)
    if en:
        out = en.format("", *(e.EN() for e in self.sub_exprs))
    else:
        out = f"{self.symbol}({', '.join([x.EN() for x in self.sub_exprs])})"
    if self.in_enumeration:
        enum = f"{', '.join(str(e) for e in self.in_enumeration.tuples)}"
    return (f"{out}"
            f"{ ' '+self.is_enumerated if self.is_enumerated else ''}"
            f"{ f' {self.is_enumeration} {{{enum}}}' if self.in_enumeration else ''}")
AppliedSymbol.EN = EN


def EN(self):
    return f"({self.sub_exprs[0].EN()})"
Brackets.EN = EN


def EN(self) -> str:
    """returns a string containing the Theory in controlled English
    """
    constraints = '\n'.join(f"- {c.original.EN()}." for c in self.constraints.values()
                            if not c.is_type_constraint_for
                            and (not type(c)==AppliedSymbol or c.symbol.name != "relevant")).replace("  ", " ")
    definitions = '\n'.join(f"- {d.EN()}" for d in self.definitions)
    return (constraints + "\n" + definitions)
Theory.EN = EN


Done = True