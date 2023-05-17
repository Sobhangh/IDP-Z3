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
This module contains the logic for the computation of relevance.
"""
from __future__ import annotations

from .Assignments import Status as S
from .Expression import (AppliedSymbol, TRUE, Expression, AQuantification,
                                   AConjunction, Brackets)
from .Theory import Theory
from .utils import OrderedSet, RELEVANT


def split_constraints(constraints: OrderedSet) -> OrderedSet:
    """replace [.., a ∧ b, ..] by [.., a, b, ..]

    This is to avoid dependencies between a and b (see issue #95).

    Args:
        constraints (OrderedSet): set of constraints that may contain conjunctions

    Returns:
        OrderedSet: set of constraints without top-level conjunctions
    """

    def split(c: Expression, cs: OrderedSet):
        """split constraint c and adds it to cs"""
        if type(c) in [AConjunction, Brackets]:
            for e in c.sub_exprs:
                split(e, cs)
        elif type(c) == AQuantification and c.q == '∀':
            conj = OrderedSet()
            for e in c.sub_exprs:
                split(e, conj)
            for e in conj:
                out = AQuantification.make(c.q, c.quantees, e)
                # out.code = c.code
                out.annotations = c.annotations
                cs.append(out)
        else:
            cs.append(c)

    new_constraints = OrderedSet()
    for c in constraints:
        split(c, new_constraints)
    return new_constraints


def determine_relevance(self: Theory) -> Theory:
    """Determines the questions that are relevant in a model,
    or that can appear in a justification of a ``goal_symbol``.

    When an *irrelevant* value is changed in a model M of the theory,
    the resulting M' structure is still a model.
    Relevant questions are those that are not irrelevant.

    Call must be made after a propagation, on a Theory created with ``extended=True``.
    The result is found in the ``relevant`` attribute of the assignments in ``self.assignments``.

    If ``goal_symbol`` has an enumeration in the theory
    (e.g., ``goal_symbol := {`tax_amount}.``),
    relevance is computed relative to those goals.

    Definitions in the theory are ignored,
    unless they influence axioms in the theory or goals in ``goal_symbol``.

    Returns:
        Theory: the Theory with relevant information in ``self.assignments``.
    """
    assert self.extended == True,\
        "The theory must be created with 'extended=True' for relevance computations."

    out = self.simplify(except_numeric=True)  # creates a copy

    # set given information to relevant
    for q in self.assignments.values():
        q.relevant = (q.status in [S.GIVEN, S.DEFAULT, S.EXPANDED])

    constraints = OrderedSet()

    # collect constraints in the simplified theory (except type constraints)
    for constraint in out.constraints:
        if constraint.is_type_constraint_for is None:
            constraints.append(constraint)

    # also collect propagated assignments used for simplifications
    for q in out.assignments.values():  # out => exclude numeric expressions
        if q.value is not None:
            constraints.append(q.sentence)  # issue #252, #277

    constraints = split_constraints(constraints)

    # determine the starting set of relevant questions, and initialize the ending set
    # start with goal_symbol
    to_add, _relevant = OrderedSet(), OrderedSet()  # set of questions and constraints
    for constraint in self.constraints:  # not simplified !
        if (type(constraint) == AppliedSymbol
           and constraint.decl.name == RELEVANT):
            to_add.extend(constraint.sub_exprs)  # all instances of the goal symbol

    # no goal_symbol --> make every simplified constraint relevant
    if len(to_add) == 0:
        to_add = constraints

    # still nothing relevant --> make every question in def_constraints relevant
    if len(to_add) == 0:
        for def_constraints in out.def_constraints.values():
            for def_constraint in def_constraints:
                def_constraint.questions = OrderedSet()
                def_constraint.collect(def_constraint.questions,
                                    all_=True, co_constraints=True)
                for q in def_constraint.questions:
                    _relevant.append(q)
    else:
        # find relevant symbols by breadth-first diffusion
        # input: to_add, constraints
        # output: _relevant
        while to_add:
            next = OrderedSet()
            for q in to_add:
                _relevant.append(q)

                # append questions in q to next
                q.collect(next, all_=True, co_constraints=False)

                # append constraints related to q (for goal_symbol)
                for constraint in constraints:
                    if constraint.questions is None:
                        constraint.questions = OrderedSet()
                        constraint.collect(constraint.questions, all_=True, co_constraints=False)
                    if q in constraint.questions:
                        next.extend(constraint.questions)

                # append questions in co_constraints to next too
                co_constraints = OrderedSet()
                q.collect_co_constraints(co_constraints, recursive=False)
                for constraint in co_constraints:
                    next.append(constraint)

            to_add = OrderedSet(e for e in next if e not in _relevant)

    for q in _relevant:
        ass = self.assignments.get(q.code, None)
        if (ass and not ass.is_certainly_undefined):  #TODO
            ass.relevant = True
    return self
Theory.determine_relevance = determine_relevance


Done = True