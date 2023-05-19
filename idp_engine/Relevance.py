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
from copy import copy

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

    # determine goals
    goals = OrderedSet()
    for constraint in self.constraints:  # not simplified
        if (type(constraint) == AppliedSymbol
           and constraint.decl.name == RELEVANT):
            goals.extend(constraint.sub_exprs)  # all instances of the goal symbol

    out = self.simplify(except_numeric=True)  # creates a copy

    # set given information to relevant
    for q in self.assignments.values():
        q.relevant = (q.status in [S.GIVEN, S.DEFAULT, S.EXPANDED])

    constraints = OrderedSet()

    # collect constraints in the simplified theory (except type constraints)
    for constraint in out.constraints:
        if constraint.is_type_constraint_for is None:
            constraints.append(constraint)

    constraints = split_constraints(constraints)

    # determine the starting set of relevant questions, and initialize the ending set
    # start with goal_symbol
    to_add, _relevant = OrderedSet(), OrderedSet()  # set of questions and constraints

    if goals:
        to_add = goals

        # append constraints (indirectly) related to q (for goal_symbol)
        done = False
        while not done:
            done = True
            for constraint in constraints:
                if constraint.questions is None:
                    constraint.questions = OrderedSet()
                    constraint.collect(constraint.questions,
                                    all_=True, co_constraints=False)
                if any(q in to_add for q in constraint.questions):  # if constraint is related
                    for q in constraint.questions:
                        if q not in to_add:
                            to_add.extend(constraint.questions)
                            done = False
    else:
        to_add = copy(constraints)

    # need to add the propagated assignments used for simplifications
    for q in out.assignments.values():  # out => exclude numeric expressions
        if q.value is not None:
            to_add.append(q.sentence)  # issue #252, #277

    # no constraints --> make every question in def_constraints relevant
    if all(e.is_type_constraint_for is not None for e in self.constraints):
        _relevant = to_add
        for def_constraints in out.def_constraints.values():
            for def_constraint in def_constraints:
                q = def_constraint.simplify_with(out.assignments, co_constraints_too=False)
                questions = OrderedSet()
                q.collect(questions, all_=True, co_constraints=True)
                for q in questions:
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

                # append questions in co_constraints to next too
                if type(q) == AppliedSymbol:
                    inst = [defin.instantiate_definition(q.decl, q.sub_exprs, self)
                            for defin in self.definitions]
                    inst = [x.simplify_with(out.assignments, co_constraints_too=False)
                            for x in inst if x]
                    if inst:
                        next.extend(inst)

            to_add = OrderedSet(e for e in next if e not in _relevant)

    for q in _relevant:
        ass = self.assignments.get(q.code, None)
        if (ass and not ass.is_certainly_undefined
        and ass.status != S.UNIVERSAL):  #TODO
            ass.relevant = True
    return self
Theory.determine_relevance = determine_relevance


Done = True