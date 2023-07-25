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

routines to analyze Z3 expressions, e.g., the definition of a function in a model

"""

from __future__ import annotations
import re
from typing import List, TYPE_CHECKING, Optional
from z3 import ModelRef, FuncInterp, is_and, is_or, is_eq, is_not, AstRef, DatatypeRef, BoolRef, IntNumRef

from .Assignments import Assignments
from .Expression import Expression, SYMBOL, AppliedSymbol
from .Parse import str_to_IDP2, SymbolDeclaration
from .utils import RESERVED_SYMBOLS
if TYPE_CHECKING:
    from .Theory import Theory

TRUEFALSE = re.compile(r"\b(True|False)\b")

def get_interpretations(theory: Theory, model: ModelRef
                        ) -> dict[str, dict[str, Optional[Expression]]]:
    """analyze the Z3 function interpretations in the model

    A Z3 interpretation maps some tuples of arguments to the value of the symbol applied to those tuples,
    and uses a default (else) value for the value of the symbol applied to other tuples.

    The function returns a mapping from symbol names
    to a mapping from some applied symbols to their value in the model
    and with "" mapped to the default value (or None if undetermined in the model).
    """
    out : dict[str, dict[str, Optional[Expression]]] = {}
    for decl in theory.declarations.values():
        if (type(decl) == SymbolDeclaration
        and decl.name is not None
        and not decl.name in RESERVED_SYMBOLS):
            out.setdefault(decl.name, {})
            map = out[decl.name]
            if decl.name not in theory.z3:  # declared but not used in theory
                map[""] = None
            else:
                interp = model[theory.z3[decl.name]]
                if interp is None:
                    map[""] = None # can be any value
                elif type(interp) == FuncInterp:
                    try:
                        a_list = interp.as_list()
                    except:  # ast is null
                        map[""] = None
                        continue
                    for args in a_list[:-1]:
                        _args = (str(a) for a in args[:-1])
                        applied = f"{decl.name}({', '.join(_args)})"
                        # Replace True by true, False by false
                        applied = re.sub(TRUEFALSE, lambda m: m.group(1).lower(), applied)
                        val = args[-1]
                        map[applied] = str_to_IDP2("", decl.out.decl, str(val))
                    try:
                        map[""] = str_to_IDP2("", decl.out.decl, str(a_list[-1])) # else
                    except:
                        map[""] = None  # Var(0) => can be any value
                elif type(interp) in [DatatypeRef, BoolRef, IntNumRef]:
                    map[""] = str_to_IDP2("", decl.out.decl, str(interp))
                else:
                    assert False, "Internal error"
    return out

def collect_questions(z3_expr: AstRef,
                      decl: SymbolDeclaration,
                      ass: Assignments,
                      out: List[Expression]):
    """ determines the function applications that should be evaluated/propagated
    based on the function interpretation in `z3_expr` (obtained from a Z3 model).

    i.e., add `<decl>(<value>)` to `out`
       for each occurrence of `var(0) = value`
       in the else clause of a Z3 function interpretation.

    example: the interpretation of opgenomen is `z3_expr`, i.e. `
            [else ->
                Or(Var(0) == 12,
                    And(Not(Var(0) == 12), Not(Var(0) == 11), Var(0) == 13),
                    And(Not(Var(0) == 12), Var(0) == 11))]`

    result: `[opgenomen(11), opgenomen(12), opgenomen(13)]` is added to `out`

    Args:
        z3_expr (AstRef): the function interpretation in a model of Z3
        decl (SymbolDeclaration): the declaration of the function
        ass (Assignments): teh list of assignments already planned for evaluation/propagation
        out (List[Expression]): the resulting list
    """
    if type(z3_expr) == FuncInterp:
        try:
            else_ = z3_expr.else_value()
        except:
            return
        collect_questions(else_, decl, ass, out)
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
    return
