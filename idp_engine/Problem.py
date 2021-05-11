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

import time
from copy import copy
from itertools import chain
from typing import Any, Iterable, List
from z3 import Solver, sat, unsat, unknown, Optimize, Not, And, Or, Implies

from .Assignments import Status, Assignment, Assignments
from .Expression import (TRUE, AConjunction, Expression, FALSE, AppliedSymbol,
                         AComparison, AUnary)
from .Parse import (TypeDeclaration, Symbol, SymbolDeclaration,
                    Theory, str_to_IDP)
from .Simplify import join_set_conditions
from .utils import (OrderedSet, NEWL, BOOL, INT, REAL, DATE,
                    RESERVED_SYMBOLS, SYMBOL, RELEVANT)

class Problem(object):
    """A collection of theory and structure blocks.

    Attributes:
        declarations (dict[str, Type]): the list of type and symbol declarations

        constraints (OrderedSet): a set of assertions.

        assignments (Assignment): the set of assignments.
            The assignments are updated by the different steps of the problem
            resolution.

        clark (dict[(SymbolDeclaration, Definition), Rule]):
            A mapping of defined symbol to the rule that defines it.

        def_constraints (dict[SymbolDeclaration], Expression):
            A mapping of defined symbol to the whole-domain constraint
            equivalent to its definition.

        interpretations (dict[string, SymbolInterpretation]):
            A mapping of enumerated symbols to their interpretation.

        goals (dict[string, SymbolDeclaration]):
            A set of goal symbols

        _formula (Expression, optional): the logic formula that represents
            the problem.

        questions (OrderedSet): the set of questions in the problem.
            Questions include predicates and functions applied to arguments,
            comparisons, and variable-free quantified expressions.

        co_constraints (OrderedSet): the set of co_constraints in the problem.
    """
    def __init__(self, *blocks):
        self.declarations = {}
        self.clark = {}  # {(Declaration, Definition): Rule}
        self.constraints = OrderedSet()
        self.assignments = Assignments()
        self.def_constraints = {}
        self.interpretations = {}
        self.goals = {}
        self.name = ''

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
        out.constraints = OrderedSet(c.copy() for c in self.constraints)
        out.def_constraints = self.def_constraints.copy()
        # copy() is called before making substitutions => invalidate derived fields
        out._formula = None
        return out

    def add(self, block):
        self._formula = None  # need to reapply the definitions

        for name, decl in block.declarations.items():
            assert (name not in self.declarations
                    or self.declarations[name] == block.declarations[name]
                    or name in [BOOL, INT, REAL, DATE, SYMBOL]
                    or name in RESERVED_SYMBOLS), \
                    f"Can't add declaration for {name} in {block.name}: duplicate"
            self.declarations[name] = decl
        for decl in self.declarations.values():
            if type(decl) == TypeDeclaration:
                decl.translated = None  # reset the translation of declarations
                decl.interpretation = (  #TODO side-effects ? issue #81
                    None if decl.name not in [INT, REAL, DATE, SYMBOL] else
                    decl.interpretation)

        # process block.interpretations
        for name, interpret in block.interpretations.items():
            assert (name not in self.interpretations
                    or name in [INT, REAL, DATE, SYMBOL]
                    or self.interpretations[name] == block.interpretations[name]), \
                     f"Can't add enumeration for {name} in {block.name}: duplicate"
            self.interpretations[name] = interpret

        if isinstance(block, Theory) or isinstance(block, Problem):
            self.co_constraints, self.questions = None, None
            for (decl, defin), rule in block.clark.items():
                if not (decl, defin) in self.clark:
                    self.clark[(decl, defin)] = rule
            self.constraints.extend(v.copy() for v in block.constraints)
            self.def_constraints.update(
                {k:v.copy() for k,v in block.def_constraints.items()})

        for name, s in block.goals.items():
            self.goals[name] = s
        return self

    def assert_(self, code: str, value: Any, status: Status = Status.GIVEN):
        """asserts that an expression has a value

        Args:
            code (str): the code of the expression, e.g., "p()"
            value (Any): a Python value, e.g., "True"
            status (Status, Optional): how the value was obtained.  Default: Status.GIVEN
        """
        self._interpret()
        code = str(code)
        atom = self.assignments[code].sentence
        if value is None:
            self.assignments.assert_(atom, value, Status.UNKNOWN, False)
        else:
            val = str_to_IDP(atom, str(value))
            self.assignments.assert_(atom, val, status, False)
        # reset any consequences
        for v in self.assignments.values():
            if v.status in [Status.CONSEQUENCE, Status.ENV_CONSQ, Status.EXPANDED]:
                v.status = Status.UNKNOWN
                v.value = None
        self._formula = None

    def _interpret(self):
        """ apply the enumerations and definitions """
        if self.questions is None:
            self.assignments = Assignments()

            for decl in self.declarations.values():
                decl.interpret(self)

            for symbol_interpretation in self.interpretations.values():
                if not symbol_interpretation.is_type_enumeration:
                    symbol_interpretation.interpret(self)

            # expand goals
            for s in self.goals.values():
                assert s.instances, "goals must be instantiable."
                relevant = Symbol(name=RELEVANT)
                relevant.decl = self.declarations[RELEVANT]
                constraint = AppliedSymbol.make(relevant, s.instances.values())
                self.constraints.append(constraint)

            # expand whole-domain definitions
            for (decl, _), rule in self.clark.items():
                if rule.is_whole_domain:
                    self.def_constraints[decl] = rule.interpret(self).whole_domain

            self.co_constraints, self.questions = OrderedSet(), OrderedSet()
            for c in self.constraints:
                c.interpret(self)
                c.co_constraints(self.co_constraints)
                c.collect(self.questions, all_=False)
            for s in list(self.questions.values()):
                if s.is_reified():
                    self.assignments.assert_(s, None, Status.UNKNOWN, False)

            for ass in self.assignments.values():
                ass.sentence = ass.sentence
                ass.sentence.original = ass.sentence.copy()

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
        solver = Optimize()
        solver.add(self.formula().translate())
        assert term in self.assignments, "Internal error"
        s = self.assignments[term].sentence.translate()
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

    def explain(self, consequence):
        """returns the facts and laws that justify 'consequence in the 'self Problem

        Args:
            self (Problem): the problem state
            consequence (string): the code of the sentence to be explained.  Must be a key in self.assignments

        Returns:
            (facts, laws) (List[Assignment], List[Expression])]: list of facts and laws that explain the consequence
        """
        facts, laws = [], []
        reasons = [Status.GIVEN, Status.STRUCTURE]

        negated = consequence.replace('~', '¬').startswith('¬')
        consequence = consequence[1:] if negated else consequence
        assert consequence in self.assignments, \
            f"Can't find this sentence: {consequence}"

        to_explain = self.assignments[consequence].sentence

        # rules used in justification
        if to_explain.type != BOOL:  # determine numeric value
            val = self.assignments[consequence].value
            if val is None:  # can't explain an expanded value
                return ([], [])
            to_explain = AComparison.make("=", [to_explain, val])
        if negated:
            to_explain = AUnary.make('¬', to_explain)

        s = Solver()
        s.set(':core.minimize', True)
        ps = {}  # {reified: constraint}

        for ass in self.assignments.values():
            if ass.status in reasons:
                p = ass.translate()
                ps[p] = ass
                #TODO use assert_and_track ?
                s.add(Implies(p, p))
        todo = chain(self.constraints, self.def_constraints.values())
        for constraint in todo:
            p = constraint.reified()
            ps[p] = constraint.original.interpret(self).translate()
            s.add(Implies(p, ps[p]))

        s.add(Not(to_explain.translate()))
        s.check(list(ps.keys()))
        unsatcore = s.unsat_core()

        if unsatcore:
            for k, a1 in self.assignments.items():
                if a1.status in reasons:
                    for a2 in unsatcore:
                        if type(ps[a2]) == Assignment \
                        and a1.sentence.same_as(ps[a2].sentence):  #TODO we might miss some equality
                            if a1.status == Status.GIVEN:
                                facts.append(a1)
                            else:
                                laws.append(a1.formula())

            for a1 in chain(self.def_constraints.values(), self.constraints):
                #TODO find the rule
                for a2 in unsatcore:
                    if str(a1.original.interpret(self).translate()) == str(ps[a2]):
                        laws.append(a1)
        return (facts, laws)

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

    def _generalize(self,
                    conjuncts: List[Assignment],
                    known, z3_formula=None
    ) -> List[Assignment]:
        """finds a subset of `conjuncts`
            that is still a minimum satisfying assignment for `self`, given `known`.

        Args:
            conjuncts (List[Assignment]): a list of assignments
                The last element of conjuncts is the goal or TRUE
            known: a z3 formula describing what is known (e.g. reification axioms)
            z3_formula: the z3 formula of the problem.
                Can be supplied for better performance

        Returns:
            [List[Assignment]]: A subset of `conjuncts`
                that is a minimum satisfying assignment for `self`, given `known`
        """
        if z3_formula is None:
            z3_formula = self.formula().translate()

        conditions, goal = conjuncts[:-1], conjuncts[-1]
        # verify satisfiability
        solver = Solver()
        z3_conditions = And([l.translate() for l in conditions])
        solver.add(And(z3_formula, known, z3_conditions))
        if solver.check() != sat:
            return []
        else:
            for i, c in (list(enumerate(conditions))): # optional: reverse the list
                conditions_i = And([l.translate()
                        for j, l in enumerate(conditions)
                        if j != i])
                solver = Solver()
                if goal.sentence == TRUE or goal.value is None:  # find an abstract model
                    # z3_formula & known & conditions => conditions_i is always true
                    solver.add(Not(Implies(And(known, conditions_i), z3_conditions)))
                else:  # decision table
                    # z3_formula & known & conditions => goal is always true
                    hypothesis = And(z3_formula, known, conditions_i)
                    solver.add(Not(Implies(hypothesis, goal.translate())))
                if solver.check() == unsat:
                    conditions[i] = Assignment(TRUE, TRUE, Status.UNKNOWN)
            conditions = join_set_conditions(conditions)
            return [c for c in conditions if c.sentence != TRUE]+[goal]

    def decision_table(self, goal_string="", timeout=20, max_rows=50,
                       first_hit=True, verify=False):
        """returns a decision table for `goal_string`, given `self`.

        Args:
            goal_string (str, optional): the last column of the table.
            timeout (int, optional): maximum duration in seconds. Defaults to 20.
            max_rows (int, optional): maximum number of rows. Defaults to 50.
            first_hit (bool, optional): requested hit-policy. Defaults to True.
            verify (bool, optional): request verification of table completeness.  Defaults to False

        Returns:
            list(list(Assignment)): the non-empty cells of the decision table
        """
        max_time = time.time()+timeout  # 20 seconds max

        if goal_string:
            goal_pred = goal_string.split("(")[0]
            assert goal_pred in self.declarations, (
                f"Unrecognized goal string: {goal_string}")
            self.goals[goal_pred] = self.declarations[goal_pred]
            self._formula = None
        formula = self.formula()
        theory = formula.translate()

        # ignore type constraints
        questions = OrderedSet()
        for c in self.constraints:
            if not c.is_type_constraint_for:
                c.collect(questions, all_=False)
        # ignore questions about defined symbols (except goal)
        symbols = {decl for (decl, defin) in self.clark.keys()}
        qs = OrderedSet()
        for q in questions.values():
            if (goal_string == q.code
            or any(s not in symbols for s in q.unknown_symbols(co_constraints=False).values())):
                qs.append(q)
        questions = qs
        assert not goal_string or goal_string in [a.code for a in questions], \
            f"Internal error"

        known = And([ass.translate() for ass in self.assignments.values()
                        if ass.status != Status.UNKNOWN]
                    + [q.reified()==q.translate() for q in questions
                        if q.is_reified()])

        solver = Solver()
        solver.add(theory)
        solver.add(known)

        models, count = [], 0
        while (solver.check() == sat  # for each parametric model
               and count < max_rows and time.time() < max_time):
            # find the interpretation of all atoms in the model
            assignments = []  # [Assignment]
            model = solver.model()
            goal = None
            for atom in questions.values():
                assignment = self.assignments.get(atom.code, None)
                if assignment and assignment.value is None and atom.type == BOOL:
                    if not atom.is_reified():
                        val1 = model.eval(atom.translate())
                    else:
                        val1 = model.eval(atom.reified())
                    if val1 == True:
                        ass = Assignment(atom, TRUE , Status.UNKNOWN)
                    elif val1 == False:
                        ass = Assignment(atom, FALSE, Status.UNKNOWN)
                    else:
                        ass = Assignment(atom, None, Status.UNKNOWN)
                    if atom.code == goal_string:
                        goal = ass
                    elif ass.value is not None:
                        assignments.append(ass)
            if verify:
                assert not goal_string or goal.value is not None, \
                    "The goal is not always determined by the theory"
            # start with negations !
            assignments.sort(key=lambda l: (l.value==TRUE, str(l.sentence)))
            assignments.append(goal if goal_string else
                                Assignment(TRUE, TRUE, Status.UNKNOWN))

            assignments = self._generalize(assignments, known, theory)
            models.append(assignments)

            # add constraint to eliminate this model
            modelZ3 = Not(And( [l.translate() for l in assignments
                if l.value is not None] ))
            solver.add(modelZ3)

            count +=1

        if verify:
            def verify_models(known, models, goal_string):
                """verify that the models cover the universe

                Args:
                    known ([type]): [description]
                    models ([type]): [description]
                    goal_string ([type]): [description]
                """
                known2 = known
                for model in models:
                    condition = [l.translate() for l in model
                                    if l.value is not None
                                    and l.sentence.code != goal_string]
                    known2 = And(known2, Not(And(condition)))
                solver = Solver()
                solver.add(known2)
                assert solver.check() == unsat, \
                    "The DMN table does not cover the full domain"
            verify_models(known, models, goal_string)

        models.sort(key=len)

        if first_hit:
            known2 = known
            models1, last_model = [], []
            while models and time.time() < max_time:
                if len(models) == 1:
                    models1.append(models[0])
                    break
                model = models.pop(0).copy()
                condition = [l.translate() for l in model
                                if l.value is not None
                                and l.sentence.code != goal_string]
                if condition:
                    possible = Not(And(condition))
                    if verify:
                        solver = Solver()
                        solver.add(known2)
                        solver.add(possible)
                        result = solver.check()
                        assert result == sat, \
                            "A row has become impossible to trigger"
                    known2 = And(known2, possible)
                    models1.append(model)
                    models = [self._generalize(m, known2, theory)
                        for m in models]
                    models = [m for m in models if m] # ignore impossible models
                    models = list(dict([(",".join([str(c) for c in m]), m)
                                        for m in models]).values())
                    models.sort(key=len)
                else: # when not deterministic
                    last_model += [model]
            models = models1 + last_model
            # post process if last model is just the goal
            # replace [p=>~G, G] by [~p=>G]
            if (len(models[-1]) == 1
            and models[-1][0].sentence.code == goal_string
            and models[-1][0].value is not None):
                last_model = models.pop()
                hypothesis, consequent = [], last_model[0].negate()
                while models:
                    last = models.pop()
                    if (len(last) == 2
                    and last[-1].sentence.code == goal_string
                    and last[-1].value.same_as(consequent.value)):
                        hypothesis.append(last[0].negate())
                    else:
                        models.append(last)
                        break
                hypothesis.sort(key=lambda l: (l.value==TRUE, str(l.sentence)))
                model = hypothesis + [last_model[0]]
                model = self._generalize(model, known, theory)
                models.append(model)
                if hypothesis:
                    models.append([consequent])

            # post process to merge similar successive models
            # {x in c1 => g. x in c2 => g.} becomes {x in c1 U c2 => g.}
            # must be done after first-hit transformation
            for i in range(len(models)-1, 0, -1):  # reverse order
                m, prev = models[i], models[i-1]
                if (len(m) == 2 and len(prev) == 2
                    and m[1].same_as(prev[1])):  # same goals
                    # p | (~p & q) = ~(~p & ~q)
                    new = join_set_conditions([prev[0].negate(), m[0].negate()])
                    if len(new) == 1:
                        new = new[0].negate()
                        models[i-1] = [new, models[i-1][1]]
                        del models[i]
            if verify:
                verify_models(known, models, goal_string)

        return models

Done = True
