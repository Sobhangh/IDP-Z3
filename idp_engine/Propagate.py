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

Computes the consequences of an expression,
i.e., the sub-expressions that are necessarily true (or false)
if the expression is true (or false)

It has 2 parts:
* symbolic propagation
* Z3 propagation

This module monkey-patches the Expression and Problem classes and sub-classes.
"""

from typing import List, Tuple, Optional
from z3 import (Solver, sat, unsat, unknown, Not, Or, is_false, is_true, is_not, is_eq)

from .Assignments import Status as S, Assignments
from .Expression import (Expression, AQuantification,
                    ADisjunction, AConjunction,
                    AComparison, AUnary, Brackets, TRUE, FALSE)
from .Parse import str_to_IDP
from .Problem import Problem
from .utils import OrderedSet

###############################################################################
#
#  Symbolic propagation
#
###############################################################################


def _not(truth):
    return FALSE if truth.same_as(TRUE) else TRUE

# class Expression  ###########################################################


def symbolic_propagate(self,
                       assignments: "Assignments",
                       truth: Optional[Expression] = TRUE
                       ) -> List[Tuple[Expression]]:
    """returns the consequences of `self=truth` that are in assignments.

    The consequences are obtained by symbolic processing (no calls to Z3).

    Args:
        assignments (Assignments):
            The set of questions to chose from. Their value is ignored.

        truth (Expression, optional):
            The truth value of the expression `self`. Defaults to TRUE.

    Returns:
        A list of pairs (Expression, bool), descring the literals that
        are implicant
    """
    if self.value is not None:
        return []
    out = [(self, truth)] if self.code in assignments else []
    if self.simpler is not None:
        out = self.simpler.symbolic_propagate(assignments, truth) + out
        return out
    out = self.propagate1(assignments, truth) + out
    return out


Expression.symbolic_propagate = symbolic_propagate


def propagate1(self, assignments, truth):
    " returns the list of symbolic_propagate of self (default implementation) "
    return []


Expression.propagate1 = propagate1


# class AQuantification  ######################################################

def symbolic_propagate(self, assignments, truth=TRUE):
    out = [(self, truth)] if self.code in assignments else []
    if not self.quantees:  # expanded
        return self.sub_exprs[0].symbolic_propagate(assignments, truth) + out
    return out
AQuantification.symbolic_propagate = symbolic_propagate


# class ADisjunction  #########################################################

def propagate1(self, assignments, truth=TRUE):
    if truth.same_as(FALSE):
        return sum( (e.symbolic_propagate(assignments, truth) for e in self.sub_exprs), [])
    return []
ADisjunction.propagate1 = propagate1


# class AConjunction  #########################################################

def propagate1(self, assignments, truth=TRUE):
    if truth.same_as(TRUE):
        return sum( (e.symbolic_propagate(assignments, truth) for e in self.sub_exprs), [])
    return []
AConjunction.propagate1 = propagate1


# class AUnary  ############################################################

def propagate1(self, assignments, truth=TRUE):
    return ( [] if self.operator != '¬' else
        self.sub_exprs[0].symbolic_propagate(assignments, _not(truth)) )
AUnary.propagate1 = propagate1


# class AComparison  ##########################################################

def propagate1(self, assignments, truth=TRUE):
    if truth.same_as(TRUE) and len(self.sub_exprs) == 2 and self.operator == ['=']:
        # generates both (x->0) and (x=0->True)
        # generating only one from universals would make the second one
        # a consequence, not a universal
        operands1 = [e.value for e in self.sub_exprs]
        if   operands1[1] is not None:
            return [(self.sub_exprs[0], operands1[1])]
        elif operands1[0] is not None:
            return [(self.sub_exprs[1], operands1[0])]
    return []
AComparison.propagate1 = propagate1


# class Brackets  ############################################################

def symbolic_propagate(self, assignments, truth=TRUE):
    out = [(self, truth)] if self.code in assignments else []
    return self.sub_exprs[0].symbolic_propagate(assignments, truth) + out
Brackets.symbolic_propagate = symbolic_propagate



###############################################################################
#
#  Z3 propagation
#
###############################################################################


def _directional_todo(self):
    """ computes the list of candidate atoms for a new propagation

    Takes into account assertions made via self.assert_ since the last propagation:
    * a new assignment forces the re-propagation of Unknowns
    * a clearing of assignment forces the re-propagation of previous consequences
    """
    statuses = []
    if self.propagated:
        if self.assigned:
            statuses.extend([S.UNKNOWN, S.EXPANDED])
        if self.cleared:
            statuses.extend([S.CONSEQUENCE, S.ENV_CONSQ])
    else:
        statuses = [S.UNKNOWN, S.EXPANDED, S.CONSEQUENCE, S.ENV_CONSQ]

    if statuses:
        todo = OrderedSet(
            a.sentence for a in self.assignments.values()
            if ((not a.sentence.is_reified() or self.extended)
                and a.status in statuses
                ))
    else:
        todo = OrderedSet()
    return todo
Problem._directional_todo = _directional_todo


def _batch_propagate(self, tag=S.CONSEQUENCE):
    """ generator of new propagated assignments.  Update self.assignments too.

    uses the method outlined in https://stackoverflow.com/questions/37061360/using-maxsat-queries-in-z3/37061846#37061846
    and in J. Wittocx paper : https://drive.google.com/file/d/19LT64T9oMoFKyuoZ_MWKMKf9tJwGVax-/view?usp=sharing

    This method is not faster than _propagate(), and falls back to it in some cases
    """
    todo = self._directional_todo()
    if todo:
        z3_formula = self.formula().translate()

        solver = Solver()
        solver.add(z3_formula)
        result = solver.check()
        if result == sat:
            lookup, tests = {}, []
            for q in todo:
                solver.add(q.reified() == q.translate())  # in case todo contains complex formula
                if solver.check() != sat:
                    # print("Falling back !")
                    yield from self._propagate(tag)
                test = Not(q.reified() == solver.model().eval(q.reified()))
                tests.append(test)
                lookup[str(test)] = q
            solver.push()
            while True:
                solver.add(Or(tests))
                result = solver.check()
                if result == sat:
                    tests = [t for t in tests if is_false(solver.model().eval(t))]
                    for t in tests:  # reset the other assignments
                        if is_true(solver.model().eval(t)):
                            q = lookup[str(test)]
                            self.assignments.assert_(q, None, S.UNKNOWN, False)
                elif result == unsat:
                    solver.pop()
                    solver.check()  # not sure why this is needed
                    for test in tests:
                        q = lookup[str(test)]
                        val1 = solver.model().eval(q.reified())
                        val = str_to_IDP(q, str(val1))
                        yield self.assignments.assert_(q, val, tag, True)
                    break
                else:  # unknown
                    # print("Falling back !!")
                    yield from self._propagate(tag)
                    break
            yield "No more consequences."
        elif result == unsat:
            yield "Not satisfiable."
            yield str(z3_formula)
        else:
            yield "Unknown satisfiability."
            yield str(z3_formula)
    else:
        yield "No more consequences."
    self.propagated, self.assigned, self.cleared = True, OrderedSet(), OrderedSet()
Problem._batch_propagate = _batch_propagate


def _propagate(self, tag=S.CONSEQUENCE):
    """generator of new propagated assignments.  Update self.assignments too.
    """
    todo = self._directional_todo()
    if todo:
        z3_formula = self.formula().translate()

        solver = Solver()
        solver.add(z3_formula)
        result = solver.check()
        if result == sat:
            for q in todo:
                solver.push()  #  faster (~3%) with push than without
                solver.add(q.reified() == q.translate())  # in case todo contains complex formula
                res1 = solver.check()
                if res1 == sat:
                    val1 = solver.model().eval(q.reified())
                    if str(val1) != str(q.reified()):  # if not irrelevant
                        solver.push()
                        solver.add(Not(q.reified() == val1))
                        res2 = solver.check()
                        solver.pop()

                        if res2 == unsat:
                            val = str_to_IDP(q, str(val1))
                            yield self.assignments.assert_(q, val, tag, True)
                        elif res2 == unknown:
                            res1 = unknown
                        else:  # reset the value
                            self.assignments.assert_(q, None, S.UNKNOWN, False)
                solver.pop()
                if res1 == unknown:
                    # yield(f"Unknown: {str(q)}")
                    solver = Solver()  # restart the solver
                    solver.add(z3_formula)
            yield "No more consequences."
        elif result == unsat:
            yield "Not satisfiable."
            yield str(z3_formula)
        else:
            yield "Unknown satisfiability."
            yield str(z3_formula)
    else:
        yield "No more consequences."
    self.propagated, self.assigned, self.cleared = True, OrderedSet(), OrderedSet()
Problem._propagate = _propagate


def _z3_propagate(self, tag=S.CONSEQUENCE):
    """generator of new propagated assignments.  Update self.assignments too.

    use z3's consequences API (incomplete propagation)
    """
    todo = self._directional_todo()
    if todo:
        z3_todo, unreify = [], {}
        for q in todo:
            z3_todo.append(q.reified())
            unreify[q.reified()] = q

        z3_formula = self.formula().translate()

        solver = Solver()
        solver.add(z3_formula)
        result, consqs = solver.consequences([], z3_todo)
        if result == sat:
            for consq in consqs:
                atom = consq.children()[1]
                if is_not(consq):
                    value, atom = FALSE, atom.arg(0)
                else:
                    value = TRUE
                # try to unreify it
                if atom in unreify:
                    yield self.assignments.assert_(unreify[atom], value, tag, True)
                elif is_eq(consq):
                    assert value == TRUE
                    term = consq.children()[0]
                    if term in unreify:
                        q = unreify[term]
                        val = str_to_IDP(q, consq.children()[1])
                        yield self.assignments.assert_(q, val, tag, True)
                    else:
                        print("???", str(consq))
                else:
                    print("???", str(consq))
            yield "No more consequences."
            #yield from self._propagate(tag)  # incomplete --> finish with normal propagation
        elif result == unsat:
            yield "Not satisfiable."
            yield str(z3_formula)
        else:
            yield "Unknown satisfiability."
            yield str(z3_formula)
    else:
        yield "No more consequences."
    self.propagated, self.assigned, self.cleared = True, OrderedSet(), OrderedSet()
Problem._z3_propagate = _z3_propagate


Done = True
