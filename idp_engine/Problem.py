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
from enum import Enum, auto
from itertools import chain
from typing import Any, Iterable, List
from z3 import Solver, sat, unsat, Optimize, Not, And, Or, Implies, is_false

from .Assignments import Status as S, Assignment, Assignments
from .Expression import (TRUE, AConjunction, Expression, FALSE, AppliedSymbol,
                         AComparison, AUnary)
from .Parse import (TypeDeclaration, Symbol, Theory, str_to_IDP)
from .Simplify import join_set_conditions
from .utils import (OrderedSet, NEWL, BOOL, INT, REAL, DATE,
                    RESERVED_SYMBOLS, SYMBOL, RELEVANT)

class Propagation(Enum):
    """Describe propagation method    """
    DEFAULT = auto()  # checks each question to see if it can have only 1 value
    BATCH = auto()  # finds a list of questions that has only 1 value
    Z3 = auto()  # use Z3's consequences API (incomplete propagation)


class Problem(object):
    """A collection of theory and structure blocks.

    Attributes:
        extended (Bool): True when the truth value of inequalities
            and quantified formula is of interest (e.g. in the Interactive Consultant)

        declarations (dict[str, Type]): the list of type and symbol declarations

        constraints (OrderedSet): a set of assertions.

        assignments (Assignment): the set of assignments.
            The assignments are updated by the different steps of the problem
            resolution.  Assignments include inequalities and quantified formula
            when the problem is extended

        definitions ([Definition]): a list of definitions in this problem

        def_constraints (dict[SymbolDeclaration, Definition], list[Expression]):
            A mapping of defined symbol to the whole-domain constraints
            equivalent to its definition.

        interpretations (dict[string, SymbolInterpretation]):
            A mapping of enumerated symbols to their interpretation.

        goals (dict[string, SymbolDeclaration]):
            A set of goal symbols

        _formula (Expression, optional): the logic formula that represents
            the problem.

        co_constraints (OrderedSet): the set of co_constraints in the problem.

        propagated (Bool): true if a propagation has been done

        assigned (OrderedSet): set of questions asserted since last propagate

        cleared (OrderedSet): set of questions unassigned since last propagate

        propagate_success (Bool): whether the last propagate call failed or not
    """
    def __init__(self, *blocks, extended=False):
        self.extended = extended

        self.declarations = {}
        self.definitions = []
        self.constraints = OrderedSet()
        self.assignments = Assignments()
        self.def_constraints = {}  # {(Declaration, Definition): List[Expression]}
        self.interpretations = {}
        self.goals = {}
        self.name = ''

        self._formula = None  # the problem expressed in one logic formula
        self.co_constraints = None  # Constraints attached to subformula. (see also docs/zettlr/Glossary.md)

        self.add(*blocks)
        self.propagate_success = True

    @classmethod
    def make(cls, theories, structures, extended=False):
        """ polymorphic creation """
        structures = ([] if structures is None else
                      structures if isinstance(structures, Iterable) else
                      [structures])
        if type(theories) == 'Problem':
            theories.add(*structures)
            self = theories
        elif isinstance(theories, Iterable):
            self = cls(* theories + structures, extended= extended)
        else:
            self = cls(* [theories] + structures, extended=extended)
        return self

    def copy(self):
        out = copy(self)
        out.assignments = self.assignments.copy()
        out.constraints = OrderedSet(c.copy() for c in self.constraints)
        out.def_constraints = {k:[e for e in v]  #TODO e.copy()
                               for k,v in self.def_constraints.items()}
        # copy() is called before making substitutions => invalidate derived fields
        out._formula = None
        return out

    def add(self, *blocks):
        for block in blocks:
            self._formula = None  # need to reapply the definitions

            for name, decl in block.declarations.items():
                assert (name not in self.declarations
                        or self.declarations[name] == block.declarations[name]
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
                self.co_constraints = None
                self.definitions += block.definitions
                self.constraints.extend(v.copy() for v in block.constraints)
                self.def_constraints.update(
                    {k:v.copy() for k,v in block.def_constraints.items()})

            for name, s in block.goals.items():
                self.goals[name] = s

        # apply the enumerations and definitions

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
        for defin in self.definitions:
            defin.interpret(self)

        # initialize assignments, co_constraints, questions

        self.co_constraints, questions = OrderedSet(), OrderedSet()
        for c in self.constraints:
            c.interpret(self)
            c.co_constraints(self.co_constraints)
            # don't collect questions from type constraints
            if not c.is_type_constraint_for:
                c.collect(questions, all_=False)
        for es in self.def_constraints.values():
            for e in es:
                e.co_constraints(self.co_constraints)
        for s in list(questions.values()):
            if s.code not in self.assignments:
                self.assignments.assert__(s, None, S.UNKNOWN, False)

        for ass in self.assignments.values():
            ass.sentence = ass.sentence
            ass.sentence.original = ass.sentence.copy()

        self.propagated, self.assigned, self.cleared = False, None, None
        return self

    def assert_(self, code: str, value: Any, status: S = S.GIVEN):
        """asserts that an expression has a value (or not)

        Args:
            code (str): the code of the expression, e.g., "p()"
            value (Any): a Python value, e.g., True
            status (Status, Optional): how the value was obtained.  Default: S.GIVEN
        """
        code = str(code)
        atom = self.assignments[code].sentence
        old_value = self.assignments[code].value
        if value is None:
            if self.propagated and old_value is not None:
                self.cleared.append(atom)
                self.assigned.pop(atom, None)
            self.assignments.assert__(atom, value, S.UNKNOWN, False)
        else:
            val = str_to_IDP(atom, str(value))
            if self.propagated and not(old_value and old_value.same_as(val)):
                self.assigned.append(atom)
                if old_value:
                    self.cleared.append(atom)
            self.assignments.assert__(atom, val, status, False)
        self._formula = None

    def formula(self):
        """ the formula encoding the knowledge base """
        if not self._formula:
            self._formula = AConjunction.make(
                '∧',
                [a.formula() for a in self.assignments.values()
                 if a.value is not None
                 and (a.status not in [S.CONSEQUENCE, S.ENV_CONSQ]
                      or (self.propagated and not self.cleared))]
                + [s for s in self.constraints]  #perf could be pre-compiled
                + [c for c in self.co_constraints]
                + [s for s in chain(*self.def_constraints.values())]
                )
        return self._formula

    def _todo(self):
        return OrderedSet(
            a.sentence for a in self.assignments.values()
            if a.status not in [S.GIVEN, S.STRUCTURE, S.UNIVERSAL, S.ENV_UNIV]
            and (not a.sentence.is_reified() or self.extended))

    def _from_model(self, solver, todo, complete):
        """ returns Assignments from model in solver """
        ass = self.assignments.copy()
        for q in todo:
            if not q.is_reified() or self.extended:
                # evaluating q.translate() directly fails the pipeline on arithmetic/forall.idp
                solver.add(q.reified() == q.translate())
        res1 = solver.check()
        if res1 == sat:
            for q in todo:
                if not q.is_reified() or self.extended:
                    val1 = solver.model().eval(q.reified(),
                                               model_completion=complete)
                    val = str_to_IDP(q, str(val1))
                    if val is not None:
                        ass.assert__(q, val, S.EXPANDED, None)
        return ass

    def expand(self, max=10, complete=False):
        """ output: a list of Assignments, ending with a string """
        z3_formula = self.formula().translate()
        todo = self._todo()

        solver = Solver()
        solver.add(z3_formula)

        count = 0
        while count < max or max <= 0:

            if solver.check() == sat:
                count += 1
                _ = solver.model()
                ass = self._from_model(solver, todo, complete)
                yield ass

                # exclude this model
                different = []
                for a in ass.values():
                    if a.status == S.EXPANDED:
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

    def optimize(self, term, minimize=True, complete=False):
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
        self.assignments = self._from_model(solver, self._todo(), complete)
        return self

    def symbolic_propagate(self, tag=S.UNIVERSAL):
        """ determine the immediate consequences of the constraints """
        for c in self.constraints:
            # determine consequences, including from co-constraints
            new_constraint = c.substitute(TRUE, TRUE, self.assignments, tag)
            new_constraint.symbolic_propagate(self.assignments, tag)
        return self

    def propagate(self, tag=S.CONSEQUENCE, method=Propagation.DEFAULT):
        """ determine all the consequences of the constraints """
        if method == Propagation.BATCH:
            out = list(self._batch_propagate(tag))
        if method == Propagation.Z3:
            out = list(self._z3_propagate(tag))
        else:
            out = list(self._propagate(tag))
        self.propagate_success = (out[0] != "Not satisfiable.")
        return self

    def get_range(self, term: str):
        """ Returns a list of the possible values of the term.
        """
        assert term in self.assignments, f"Unknown term: {term}"
        termE : Expression = self.assignments[term].sentence
        assert type(termE) == AppliedSymbol, f"{term} is not a term"
        range = termE.decl.range
        assert range, f"Can't determine range on infinite domains"

        out = self.copy()
        #  remove current assignments to same term
        if out.assignments[term].value:
            for a in out.assignments.values():
                if a.sentence.is_assignment and a.sentence.code.startswith(term):
                    out.assert_(a.sentence, None, S.UNKNOWN)
        out.formula()  # to keep universals and given, except self

        # now consider every value in range
        out.assignments = Assignments()
        for e in range:
            sentence = Assignment(termE, e, S.UNKNOWN).formula()
            # use assignments.assert_ to create one if necessary
            out.assignments.assert__(sentence, None, S.UNKNOWN, False)
        out.assigned = True  # to force propagation of Unknowns
        _ = list(out._propagate(S.CONSEQUENCE))  # run the generator
        assert all(e.sentence.is_assignment()
                   for e in out.assignments.values())
        return [str(e.sentence.sub_exprs[1])
                for e in out.assignments.values()
                if e.value is None or e.value.same_as(TRUE)]

    def explain(self, consequence=None):
        """
        Pre: the problem is UNSAT (under the negation of the consequence if not None)

        Returns the facts and laws that make the problem UNSAT.

        Args:
            self (Problem): the problem state
            consequence (string | None): the code of the sentence to be explained.  Must be a key in self.assignments

        Returns:
            (facts, laws) (List[Assignment], List[Expression])]: list of facts and laws that explain the consequence
        """
        facts, laws = [], []
        reasons = [S.GIVEN, S.STRUCTURE]

        s = Solver()
        s.set(':core.minimize', True)
        ps = {}  # {reified: constraint}

        for ass in self.assignments.values():
            if ass.status in reasons:
                p = ass.translate()
                ps[p] = ass
                #TODO use assert_and_track ?
                s.add(Implies(p, p))

        # get expanded def_constraints
        def_constraints = {}
        for defin in self.definitions:
            instantiables = defin.get_instantiables(for_explain=True)
            defin.add_def_constraints(instantiables, self, def_constraints)

        todo = chain(self.constraints, chain(*def_constraints.values()))
        for constraint in todo:
            p = constraint.reified()
            ps[p] = constraint.original.interpret(self).translate()
            s.add(Implies(p, ps[p]))

        if consequence:
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

            s.add(Not(to_explain.translate()))

        s.check(list(ps.keys()))
        unsatcore = s.unsat_core()

        if unsatcore:
            for k, a1 in self.assignments.items():
                if a1.status in reasons:
                    for a2 in unsatcore:
                        if type(ps[a2]) == Assignment \
                        and a1.sentence.same_as(ps[a2].sentence):  #TODO we might miss some equality
                            if a1.status == S.GIVEN:
                                facts.append(a1)
                            else:
                                laws.append(a1.formula())

            for a1 in chain(chain(*def_constraints.values()), self.constraints):
                #TODO find the rule
                for a2 in unsatcore:
                    if str(a1.original.interpret(self).translate()) == str(ps[a2]):
                        laws.append(a1)
        return (facts, laws)

    def simplify(self):
        """ returns a simpler copy of the Problem, using known assignments

        Assignments obtained by propagation become fixed constraints.
        """
        out = self.copy()

        # convert consequences to Universal
        for ass in out.assignments.values():
            if ass.value:
                ass.status = (S.UNIVERSAL if ass.status == S.CONSEQUENCE else
                        S.ENV_UNIV if ass.status == S.ENV_CONSQ else
                        ass.status)

        new_constraints: List[Expression] = []
        for constraint in out.constraints:
            new_constraint = constraint.simplify_with(out.assignments)
            new_constraints.append(new_constraint)
        out.constraints = new_constraints
        out._formula = None
        return out

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
                    conditions[i] = Assignment(TRUE, TRUE, S.UNKNOWN)
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
        assert self.extended == True, \
            "The problem must be created with 'extended=True' for decision_table."

        # determine questions, using goal_string and self.constraints
        questions = OrderedSet()
        if goal_string:
            goal_pred = goal_string.split("(")[0]
            assert goal_pred in self.declarations, (
                f"Unrecognized goal string: {goal_string}")
            for (decl, _),es in self.def_constraints.items():
                if decl != self.declarations[goal_pred]: continue
                for e in es:
                    e.collect(questions, all_=True)
            for q in questions:  # update assignments for defined goals
                if q.code not in self.assignments:
                    self.assignments.assert__(q, None, S.UNKNOWN,False)
        for c in self.constraints:
            if not c.is_type_constraint_for:
                c.collect(questions, all_=False)
        # ignore questions about defined symbols (except goal)
        symbols = {decl for defin in self.definitions for decl in defin.canonicals.keys()}
        qs = OrderedSet()
        for q in questions.values():
            if (goal_string == q.code
            or any(s not in symbols for s in q.collect_symbols(co_constraints=False).values())):
                qs.append(q)
        questions = qs
        assert not goal_string or goal_string in [a.code for a in questions], \
            f"Internal error"

        known = And([ass.translate() for ass in self.assignments.values()
                        if ass.status != S.UNKNOWN]
                    + [q.reified()==q.translate() for q in questions
                        if q.is_reified()])

        formula = self.formula()
        theory = formula.translate()
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
                        ass = Assignment(atom, TRUE, S.UNKNOWN)
                    elif val1 == False:
                        ass = Assignment(atom, FALSE, S.UNKNOWN)
                    else:
                        ass = Assignment(atom, None, S.UNKNOWN)
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
                                Assignment(TRUE, TRUE, S.UNKNOWN))

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
