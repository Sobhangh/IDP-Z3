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

Class to represent a collection of theory and structure blocks.

"""

from copy import copy
from typing import Iterable, List
from z3 import Solver, sat, unsat, unknown, Optimize, Not, And, Or

from .Assignments import Status, Assignment, Assignments
from .Expression import TRUE, AConjunction, Expression
from .Parse import Structure, Theory, str_to_IDP
from .utils import OrderedSet, NEWL

class Problem(object):
    """A collection of theory and structure blocks.

    Attributes:
        constraints (OrderedSet): a set of assertions.

        assignments (Assignment): the set of assignments.
            The assignments are updated by the different steps of the problem
            resolution.

        clark (dict[SymbolDeclaration, Rule]):
            A mapping of defined symbol to the rule that defines it.

        def_constraints (dict[SymbolDeclaration], Expression):
            A mapping of defined symbol to the whole-domain constraint
            equivalent to its definition.

        interpretations (dict[string, SymbolInterpretation]):
            A mapping of enumerated symbols to their interpretation.

        _formula (Expression, optional): the logic formula that represents
            the problem.

        questions (OrderedSet): the set of questions in the problem.
            Questions include predicates and functions applied to arguments,
            comparisons, and variable-free quantified expressions.

        co_constraints (OrderedSet): the set of co_constraints in the problem.
    """
    def __init__(self, *blocks):
        self.clark = {}  # {Declaration: Rule}
        self.constraints = OrderedSet()
        self.assignments = Assignments()
        self.def_constraints = {}
        self.interpretations = {}

        self._formula = None  # the problem expressed in one logic formula
        self.co_constraints = None  # Constraints attached to subformula. (see also docs/zettlr/Glossary.md)
        self.questions = None

        for b in blocks:
            self.add(b)

    @classmethod
    def make(cls, theories, structures):
        """ polymorphic creation """
        problem = (theories if type(theories) == 'Problem' else
                   cls(*theories) if isinstance(theories, Iterable) else
                   cls(theories))

        structures = ([] if structures is None else
                      structures if isinstance(structures, Iterable) else
                      [structures])
        for s in structures:
            problem.add(s)

        return problem

    def copy(self):
        out = copy(self)
        out.assignments = self.assignments.copy()
        out.constraints = [c.copy() for c in self.constraints]
        out.def_constraints = self.def_constraints.copy()
        # copy() is called before making substitutions => invalidate derived fields
        out._formula = None
        out.co_constraints, out.questions = None, None
        return out

    def add(self, block):
        self._formula = None  # need to reapply the definitions
        self.interpretations.update(block.interpretations) #TODO detect conflicts
        if type(block) == Structure:
            self.assignments.extend(block.assignments)
        elif isinstance(block, Theory) or isinstance(block, Problem):
            self.co_constraints, self.questions = None, None
            for decl, rule in block.clark.items():
                new_rule = copy(rule)
                if decl in self.clark:
                    new_rule.body = AConjunction.make('∧',
                        [self.clark[decl].body, new_rule.body])
                self.clark[decl] = new_rule
            self.constraints.extend(v.copy() for v in block.constraints)
            self.def_constraints.update(
                {k:v.copy() for k,v in block.def_constraints.items()})
            self.assignments.extend(block.assignments)
        else:
            assert False, "Cannot add to Problem"
        return self

    def add_assignments(self, assignments):
        self.assignments.extend(assignments)

    def _interpret(self):
        """ re-apply the definitions to the constraints """
        if self.questions is None:
            self.co_constraints, self.questions = OrderedSet(), OrderedSet()
            for c in self.constraints:
                c.interpret(self)
                c.co_constraints(self.co_constraints)
                c.collect(self.questions, all_=False)
            for s in list(self.questions.values()):
                if s.is_reified():
                    self.assignments.assert_(s, None, Status.UNKNOWN, False)

    def formula(self):
        """ the formula encoding the knowledge base """
        if not self._formula:
            self._interpret()
            self._formula = AConjunction.make(
                '∧',
                [a.formula() for a in self.assignments.values()
                 if a.value is not None]
                + [s for s in self.constraints]
                + [c for c in self.co_constraints]
                + [s for s in self.def_constraints.values()]
                + [TRUE]  # so that it is not empty
                )
        return self._formula

    def _todo(self, extended):
        return OrderedSet(
            a.sentence for a in self.assignments.values()
            if a.value is None
            and a.symbol_decl is not None
            and (not a.sentence.is_reified() or extended))

    def _from_model(self, solver, todo, complete, extended):
        """ returns Assignments from model in solver """
        ass = self.assignments.copy()
        for q in todo:
            if not q.is_reified():
                val1 = solver.model().eval(
                    q.translate(),
                    model_completion=complete)
            elif extended:
                solver.push()  # in case todo contains complex formula
                solver.add(q.reified() == q.translate())
                res1 = solver.check()
                if res1 == sat:
                    val1 = solver.model().eval(
                        q.reified(),
                        model_completion=complete)
                else:
                    val1 = None  # dead code
                solver.pop()
            if val1 is not None and str(val1) != str(q.translate()):  # otherwise, unknown
                val = str_to_IDP(q, str(val1))
                ass.assert_(q, val, Status.EXPANDED, None)
        return ass

    def expand(self, max=10, complete=False, extended=False):
        """ output: a list of Assignments, ending with a string """
        z3_formula = self.formula().translate()
        todo = self._todo(extended)

        solver = Solver()
        solver.add(z3_formula)

        count = 0
        while count < max or max <= 0:

            if solver.check() == sat:
                count += 1
                model = solver.model()
                ass = self._from_model(solver, todo, complete, extended)
                yield ass

                # exclude this model
                different = []
                for a in ass.values():
                    if a.status == Status.EXPANDED:
                        q = a.sentence
                        different.append(q.translate() != a.value.translate())
                solver.add(Or(different))
            else:
                break

        if solver.check() == sat:
            yield f"{NEWL}More models are available."
        elif 0 < count:
            yield f"{NEWL}No more models."
        else:
            yield "No models."

    def optimize(self, term, minimize=True, complete=False, extended=False):
        assert term in self.assignments, "Internal error"
        s = self.assignments[term].sentence.translate()

        solver = Optimize()
        solver.add(self.formula().translate())
        if minimize:
            solver.minimize(s)
        else:
            solver.maximize(s)
        solver.check()

        # deal with strict inequalities, e.g. min(0<x)
        solver.push()
        for i in range(0, 10):
            val = solver.model().eval(s)
            if minimize:
                solver.add(s < val)
            else:
                solver.add(val < s)
            if solver.check() != sat:
                solver.pop()  # get the last good one
                solver.check()
                break
        self.assignments = self._from_model(solver, self._todo(extended),
            complete, extended)
        return self

    def symbolic_propagate(self, tag=Status.UNIVERSAL):
        """ determine the immediate consequences of the constraints """
        self._interpret()
        for c in self.constraints:
            # determine consequences, including from co-constraints
            consequences = []
            new_constraint = c.substitute(TRUE, TRUE,
                self.assignments, consequences)
            consequences.extend(new_constraint.symbolic_propagate(self.assignments))
            if consequences:
                for sentence, value in consequences:
                    self.assignments.assert_(sentence, value, tag, False)
        return self

    def _propagate(self, tag, extended):
        z3_formula = self.formula().translate()
        todo = self._todo(extended)

        solver = Solver()
        solver.add(z3_formula)
        result = solver.check()
        if result == sat:
            for q in todo:
                solver.push()  # in case todo contains complex formula
                solver.add(q.reified() == q.translate())
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

    def propagate(self, tag=Status.CONSEQUENCE, extended=False):
        """ determine all the consequences of the constraints """
        out = list(self._propagate(tag, extended))
        assert out[0] != "Not satisfiable.", "Not satisfiable."
        return self

    def simplify(self):
        """ simplify constraints using known assignments """
        self._interpret()

        # annotate self.constraints with questions
        for e in self.constraints:
            questions = OrderedSet()
            e.collect(questions, all_=True)
            e.questions = questions

        for ass in self.assignments.values():
            old, new = ass.sentence, ass.value
            if new is not None:
                # simplify constraints
                new_constraints: List[Expression] = []
                for constraint in self.constraints:
                    if old in constraint.questions:  # for performance
                        self._formula = None  # invalidates the formula
                        consequences = []
                        new_constraint = constraint.substitute(old, new,
                            self.assignments, consequences)
                        del constraint.questions[old.code]
                        new_constraint.questions = constraint.questions
                        new_constraints.append(new_constraint)
                    else:
                        new_constraints.append(constraint)
                self.constraints = new_constraints
        return self

    def _generalize(self, structure, known=None, z3_formula=None):
        """finds a subset of structure
            that is a minimum satisfying assignment for self

        Invariants 'known and 'z3_formula can be supplied for better
        performance
        """
        if known is None:
            known = And([ass.translate() for ass in self.assignments.values()
                            if ass.status != Status.UNKNOWN]
                        + [ass.sentence.reified() == ass.sentence.translate()
                            for ass in self.assignments.values()
                            if ass.sentence.is_reified()])
        if z3_formula is None:
            z3_formula = self.formula().translate()

        conjuncts = (structure if not isinstance(structure, Problem) else
                     [ass for ass in structure.assignments.values()
                     if ass.status == Status.UNKNOWN])
        for i, c in enumerate(conjuncts):
            conjunction2 = And([l.translate()
                               for j, l in enumerate(conjuncts)
                               if j != i])
            solver = Solver()
            solver.add(And(known, conjunction2, Not(z3_formula)))
            if solver.check() == unsat:
                conjuncts[i] = Assignment(TRUE, TRUE, Status.UNKNOWN)
        return conjuncts

Done = True
