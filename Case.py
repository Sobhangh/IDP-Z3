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
from Structure_ import json_to_literals, Equality, LiteralQ, Truth
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
        self.definitions = self.idp.theory.definitions # [Definition]
        self.simplified = self.idp.theory.constraints # [Expression]

        self.literals = {} # {subtence.code: LiteralQ}, with truth value

        if DEBUG: invariant = ".".join(str(e) for e in self.idp.theory.constraints)

        # initialize .literals
        self.literals = {s.code: LiteralQ(Truth.IRRELEVANT, s) for s in self.idp.theory.subtences.values()}
        for l in self.given:
            self.literals[l.subtence.code] = l.mk_given()

        # find immediate universals
        l1 = []
        for i, c in enumerate(self.simplified):
            u = self.expr_to_literal(c)
            if u:
                self.literals[u[0].subtence.code] = u[0].mk_universal()
            else:
                l1.append(c)
        self.simplified = l1
        
        # simplify all using given and universals
        to_propagate = list(l for l in self.literals.values() if l.truth.is_known())
        while to_propagate:
            lit = to_propagate.pop(0)
            old, new = lit.as_substitution(self)

            if new is not None:
                l1 = []
                for c in self.simplified:
                    c1 = c.substitute(old, new)
                    # find immediate consequences
                    u = self.expr_to_literal(c1)
                    if u:
                        self.literals[u[0].subtence.code] = u[0].mk_consequence()
                        to_propagate.append(u[0])
                    else:
                        l1.append(c1)
                self.simplified = l1

                # now for literals
                for u in self.literals.values():
                    if u != lit:
                        simple_u = u.subtence.substitute(old, new)
                        if simple_u != u.subtence:
                            self.literals[u.subtence.code] = LiteralQ(u.truth, simple_u)
                            # find immediate consequences
                            if u.truth.is_known(): # you can't propagate otherwise
                                ls = self.expr_to_literal(simple_u)
                                if ls and ls[0] != u:
                                    out = ls[0] if u.truth.is_true() else ls[0].Not()
                                    to_propagate.append(out)

                #TODO typeConstraints ?

        # update consequences using propagation
        # simplify self.simplified using all consequences
        # simplify universal, using all consequences

        # find irrelevant
        def mark_relevant(expr):
            nonlocal self
            if expr.code in self.literals:
                self.literals[expr.code] = self.literals[expr.code].mk_relevant()
            if expr.str in self.literals:
                self.literals[expr.str] = self.literals[expr.str].mk_relevant()
            for e in expr.sub_exprs:
                mark_relevant(e)
        for expr in self.simplified:
            mark_relevant(expr)
        for d in self.definitions:
            for symb in d.partition.values():
                for r in symb:
                    mark_relevant(r.body)

        if DEBUG: assert invariant == ".".join(str(e) for e in self.idp.theory.constraints)

    def __str__(self):
        return (# f"Type: {self.typeConstraints}"
                f"Definitions: {indented}{indented.join(repr(d) for d in self.definitions)}{nl}"
                f"Universals:  {indented}{indented.join(repr(c) for c in self.literals.values() if c.is_universal())}{nl}"
                f"Consequences:{indented}{indented.join(repr(c) for c in self.literals.values() if c.is_consequence())}{nl}"
                f"Simplified:  {indented}{indented.join(str(c)  for c in self.simplified)}{nl}"
                f"Irrelevant:  {indented}{indented.join(str(c.subtence) for c in self.literals.values() if c.is_irrelevant())}{nl}"
        )

    def expr_to_literal(self, expr, truth=Truth.TRUE):
        if expr.code in self.atoms: # found it !
            return [LiteralQ(truth, expr)]
        if isinstance(expr, Brackets):
            return self.expr_to_literal(expr.sub_exprs[0], truth)
        if isinstance(expr, AUnary) and expr.operator == '~':
            return self.expr_to_literal(expr.sub_exprs[0], truth.Not() )
        return []

    def translate(self):
        self.translated = And(
            self.typeConstraints.translated
            + sum((d.translate(self.idp) for d in self.definitions), [])
            + [l.translate() for l in self.literals.values() if l.truth.is_known()]
            + [c.translate() for c in self.simplified]
            )
        return self.translated

def make_case(idp, jsonstr):
        if (idp, jsonstr) in Case.cache:
            return Case.cache[(idp, jsonstr)]

        case = Case(idp, jsonstr)

        if 100<len(Case.cache):
            # remove oldest entry, to prevent memory overflow
            Case.cache = {k:v for k,v in list(Case.cache.items())[1:]}
        Case.cache[(idp, jsonstr)] = case
        return case