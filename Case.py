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
from z3 import And, Not, sat, unsat, unknown, is_true

from Idp.Expression import Brackets, AUnary, TRUE, FALSE
from Solver import mk_solver
from Structure_ import json_to_literals, Equality, LiteralQ, Truth
from utils import *

class Case:
    """
    Contains a state of problem solving
    """
    cache = {}

    def __init__(self, idp, jsonstr, expanded):

        self.idp = idp # Idp vocabulary and theory
        self.given = json_to_literals(idp, jsonstr) # {LiteralQ : atomZ3} from the user interface
        self.expanded_symbols = set(expanded)

        # initialisation

        # Lines in the GUI
        self.GUILines = {**idp.vocabulary.terms, **idp.theory.subtences} # {atom_string: Expression}
        self.typeConstraints = self.idp.vocabulary
        self.definitions = self.idp.theory.definitions # [Definition]
        self.simplified =  [] # [Expression]

        self.literals = {} # {subtence.code: LiteralQ}, atoms + given, with simplified formula and truth value

        if DEBUG: invariant = ".".join(str(e) for e in self.idp.theory.constraints)

        for GuiLine in self.GUILines.values():
            GuiLine.is_visible = any(s in self.expanded_symbols for s in GuiLine.unknown_symbols().keys())

        # initialize .literals
        self.literals = {s.code: LiteralQ(Truth.IRRELEVANT, s) for s in self.idp.theory.subtences.values()}
        for l in self.given:
            self.literals[l.subtence.code] = l.mk_given()

        # find immediate universals
        for i, c in enumerate(self.idp.theory.constraints):
            u = self.expr_to_literal(c)
            if u:
                for l in u:
                    self.literals[l.subtence.code] = l.mk_universal()
            else:
                self.simplified.append(c)
        
        # simplify all using given and universals
        to_propagate = list(l for l in self.literals.values() if l.truth.is_known())
        self.propagate(to_propagate)

        solver, _, _ = mk_solver(self.translate(), {})
        result = solver.check()
        if result == sat:
            # determine consequences on expanded symbols only (for speed)
            for key, l in self.literals.items():
                if not l.truth.is_known() \
                and self.GUILines[l.subtence.code].is_visible \
                and key in self.get_relevant_subtences():
                    atom = l.subtence
                    solver.push()
                    solver.add(atom.reified()==atom.translate())
                    res1 = solver.check()
                    if res1 == sat:
                        val1 = solver.model().eval(atom.reified())
                        if str(val1) != str(atom.reified()): # if not irrelevant
                            solver.push()
                            solver.add(Not(atom.reified()==val1))
                            res2 = solver.check()
                            solver.pop()

                            if res2 == unsat:
                                lit = LiteralQ(Truth.TRUE if is_true(val1) else Truth.FALSE, atom)
                                self.literals[key] = lit.mk_consequence()
                                self.propagate([lit])
                            elif res2 == unknown:
                                res1 = unknown
                    solver.pop()
                    if res1 == unknown: # restart solver
                        solver, _, _ = mk_solver(self.translate(), {})
                        result = solver.check()


        # determine relevant symbols
        relevant_subtences = self.get_relevant_subtences()

        for k, l in self.literals.items():
            if k in relevant_subtences:
                self.literals[k] = l.mk_relevant()

        # find relevant subtences in definitions  #TODO
        def mark_relevant(expr):
            nonlocal self
            if expr.code in self.literals:
                self.literals[expr.code] = self.literals[expr.code].mk_relevant()
            if expr.str in self.literals:
                self.literals[expr.str] = self.literals[expr.str].mk_relevant()
            for e in expr.sub_exprs:
                mark_relevant(e)
        for d in self.definitions:
            for symb in d.partition.values():
                for r in symb:
                    mark_relevant(r.body)

        if DEBUG: assert invariant == ".".join(str(e) for e in self.idp.theory.constraints)

    def __str__(self):
        return (f"Type:        {indented}{indented.join(repr(d) for d in self.typeConstraints.translated)}{nl}"
                f"Definitions: {indented}{indented.join(repr(d) for d in self.definitions)}{nl}"
                f"Universals:  {indented}{indented.join(repr(c) for c in self.literals.values() if c.is_universal())}{nl}"
                f"Consequences:{indented}{indented.join(repr(c) for c in self.literals.values() if c.is_consequence())}{nl}"
                f"Simplified:  {indented}{indented.join(str(c)  for c in self.simplified)}{nl}"
                f"Irrelevant:  {indented}{indented.join(str(c.subtence) for c in self.literals.values() if c.is_irrelevant())}{nl}"
        )

    def get_relevant_subtences(self):
        # determine relevant symbols
        symbols = mergeDicts( e.unknown_symbols() for e in self.simplified )

        # remove irrelevant domain conditions
        self.simplified = list(e for e in self.simplified
                if e.if_symbol is None or e.if_symbol in symbols)

        # determine relevant subtences
        relevant_subtences = mergeDicts( e.subtences() for e in self.simplified )
        relevant_subtences.update(mergeDicts( r.body.subtences() #TODO
            for d in self.definitions for symb in d.partition.values() for r in symb))

        return relevant_subtences

    def propagate(self, to_propagate):
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
                        for l in u:
                            self.literals[l.subtence.code] = l.mk_consequence()
                            to_propagate.append(l)
                    elif not c1 == TRUE:
                        l1.append(c1)
                self.simplified = l1

                # now for literals
                for u in self.literals.values():
                    if u != lit:
                        simple_u = u.subtence.substitute(old, new)
                        if simple_u != u.subtence:
                            if simple_u == TRUE:
                                u.truth = Truth.TRUE
                            if simple_u == FALSE:
                                u.truth = Truth.FALSE
                            self.literals[u.subtence.code] = LiteralQ(u.truth, simple_u)
                            # find immediate consequences
                            if u.truth.is_known(): # you can't propagate otherwise
                                for l in self.expr_to_literal(simple_u):
                                    if l != u:
                                        l = l if u.truth.is_true() else l.Not()
                                        to_propagate.append(l)


    def expr_to_literal(self, expr, truth=Truth.TRUE):
        # returns a literal for the matching atom in self.GUILines, or []
        if expr.code in self.GUILines: # found it !
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

def make_case(idp, jsonstr, expanded):

        if (idp, jsonstr, expanded) in Case.cache:
            return Case.cache[(idp, jsonstr, expanded)]

        case = Case(idp, jsonstr, expanded)

        if 100<len(Case.cache):
            # remove oldest entry, to prevent memory overflow
            Case.cache = {k:v for k,v in list(Case.cache.items())[1:]}
        Case.cache[(idp, jsonstr, expanded)] = case
        return case