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

routines to analyze Z3 expressions, e.g., the definition of a function in a model

"""

from __future__ import annotations
from typing import List
from z3 import FuncInterp, is_and, is_or, is_eq, is_not

from .Assignments import Assignment
from .Expression import Expression, SYMBOL, AppliedSymbol
from .Parse import str_to_IDP2

def collect_questions(z3_expr, decl, ass, out: List[Expression]):
    if type(z3_expr) == FuncInterp:
        collect_questions(z3_expr.else_value(), decl, ass, out)
    elif is_and(z3_expr) or is_or(z3_expr) or is_not(z3_expr):
        for e in z3_expr.children():
            collect_questions(e, decl, ass, out)
    elif is_eq(z3_expr):
        typ = decl.sorts[0].decl
        arg_string = str(z3_expr.children()[1])
        atom_string = f"{decl.name}({arg_string})"
        if atom_string not in ass:
            arg = str_to_IDP2(typ.name, typ, arg_string)
            symb = SYMBOL(decl.name)
            symb.decl = decl
            atom = AppliedSymbol.make(symb, [arg])
            out.append(atom)
        pass
    return
