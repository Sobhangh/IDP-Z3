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

from .Expression import (ASTNode, AQuantification, AAggregate, Operator,
                         AComparison, AUnary, AppliedSymbol, Brackets)
from .Theory import Theory


def EN(self):
    return str(self)
ASTNode.EN = EN


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
        print(self)
        new_expr = copy(self.sub_exprs[0])
        new_expr.operator[0] = "≠"
        return new_expr.EN()
    return f"{self.operator}({self.sub_exprs[0].EN()})"
AUnary.EN = EN


def EN(self):
    en = self.symbol.decl.annotations.get('EN', None)
    if en:
        for i in reversed(range(len(self.sub_exprs))):
            en = en.replace(f'${i}', "{self.sub_exprs[i].EN()}")
        out = en.format(*self.sub_exprs)
        return out
    return str(self)
AppliedSymbol.EN = EN

def EN(self):
    return f"({self.sub_exprs[0].EN()})"
Brackets.EN = EN


def EN(self) -> str:
    """returns a string containing the Theory in controlled English
    """
    constraints = '\n'.join(f"- {c.original.EN()}." for c in self.constraints.values()
                            if not c.is_type_constraint_for)
    return constraints.replace("  ", " ")
Theory.EN = EN


Done = True