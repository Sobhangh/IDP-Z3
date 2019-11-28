"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""
from copy import copy
from z3 import And

from Idp.Expression import Brackets, AUnary
from Structure_ import json_to_literals, Equality, LiteralQ
from utils import *

class Case:
    """
    Contains a state of problem solving
    """
    cache = {}

    def __init__(self, idp, jsonstr):

        self.idp = idp # Idp vocabulary and theory
        self.given = json_to_literals(idp, jsonstr) # {LiteralQ : atomZ3} from the user interface

        # initialisation
        self.atoms = self.idp.atoms # {atom_string: Expression} atoms + numeric terms !
        self.typeConstraints = self.idp.vocabulary
        self.definitions = self.idp.theory.definitions # Definitions

        self.universals = [] # [LiteralQ]
        self.consequences = [] # [LiteralQ]
        self.irrelevant = [] # [Expression] subtences
        self.simplified = self.idp.theory.constraints # [Expression]

        if DEBUG: invariant = ".".join(str(e) for e in self.idp.theory.constraints)

        # find immediate universals
        self.universals, l1 = [], []
        for i, c in enumerate(self.simplified):
            u = self.expr_to_literal(c)
            if u:
                self.universals.append(u[0])
            else:
                l1.append(c)
        self.simplified = l1
        
        # simplify self.simplified using given
        todo = list(self.given.keys()) + self.universals
        while todo:
            lit = todo.pop(0)
            old, new = lit.as_substitution(self)

            if new is not None:
                l1 = []
                for c in self.simplified:
                    c1 = c.substitute(old, new)
                    # find immediate consequences
                    u = self.expr_to_literal(c1)
                    if u:
                        self.consequences.append(u[0])
                        todo.append(u[0])
                    else:
                        l1.append(c1)
                self.simplified = l1

        # update consequences using propagation
        # simplify self.simplified using all consequences
        # simplify universal, using all consequences
        # find irrelevant

        if DEBUG: assert invariant == ".".join(str(e) for e in self.idp.theory.constraints)

    def __str__(self):
        return (# f"Type: {self.typeConstraints}"
                f"Definitions:{indented}{indented.join(repr(d) for d in self.definitions)}{nl}"
                f"Universals:{indented}{indented.join(repr(c) for c in self.universals)}{nl}"
                f"Consequences:{indented}{indented.join(repr(c) for c in self.consequences)}{nl}"
                f"Simplified:{indented}{indented.join(str(c) for c in self.simplified)}{nl}"
        )

    def expr_to_literal(self, expr, truth=True):
        if expr.code in self.atoms: # found it !
            return [LiteralQ(truth, expr)]
        if isinstance(expr, Brackets):
            return self.expr_to_literal(expr.sub_exprs[0], truth)
        if isinstance(expr, AUnary) and expr.operator == '~':
            return self.expr_to_literal(expr.sub_exprs[0], not truth)
        return []

    def translate(self):
        self.translated = And(
            self.typeConstraints.translated
            + sum((d.translate(self.idp) for d in self.definitions), [])
            + [c.subtence.translate() for c in self.universals]
            + [c.translate() for c in self.simplified]
            + (list(self.given.values())) )
        return self.translated

def make_case(idp, jsonstr):
        if (idp, jsonstr) in Case.cache:
            return Case.cache[(idp, jsonstr)]

        case = Case(idp, jsonstr)

        if 20<len(Case.cache):
            del Case.cache[0] # remove oldest entry, to prevent memory overflow
        Case.cache[(idp, jsonstr)] = case
        return case