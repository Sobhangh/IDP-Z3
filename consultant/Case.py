"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from copy import copy
from z3 import And, Not, sat, unsat, unknown, is_true
from debugWithYamlLog import Log, NEWL, indented

from Idp.Parse import RangeDeclaration
from Idp.Expression import TRUE, FALSE, AppliedSymbol, Variable, AComparison, \
    NumberConstant
from Idp.utils import *
from Idp.Run import Problem, str_to_IDP
from .IO import json_to_literals, Assignment, Status

# Types
from Idp import Idp, SymbolDeclaration
from Idp.Expression import Expression
from typing import Any, Dict, List, Union, Tuple, cast
from z3.z3 import Solver, BoolRef

class Case(Problem):
    """
    Contains a state of problem solving
    """
    cache: Dict[Tuple[Idp, str, List[str]], 'Case'] = {}

    def __init__(self, idp: Idp, expanded: List[str]):
        super().__init__([])

        self.idp = idp # Idp vocabulary and theory
        self.goal = idp.goal
        self.expanded_symbols = set(expanded)

        # initialisation
        self.clark = self.idp.theory.clark
        self.constraints = OrderedSet(c.copy() for c in self.idp.theory.constraints)
        self.assignments = self.idp.theory.assignments # atoms + given, with simplified formula and value value
        self.def_constraints = self.idp.theory.def_constraints # {Declaration: Expression}
        self._formula = None

        for s in self.idp.structures.values():
            self.assignments.extend(s.assignments)

        if __debug__: self.invariant = ".".join(str(e) for e in self.idp.theory.constraints)

        # find immediate universals
        out = OrderedSet()
        for c in self.constraints:
            status = Status.ENV_UNIV if c.block.name=='environment' else Status.UNIVERSAL
            # determine consequences, including from co-constraints, e.g. definitions
            consequences = []
            new_constraint = c.substitute(TRUE, TRUE, self.assignments, consequences)
            consequences.extend(new_constraint.implicants(self.assignments))
            if consequences:
                for sentence, value in consequences:
                    self.assignments.assert_(sentence, value, status, False)
            out.append(new_constraint)
        self.constraints = out

        self._finalize()

    def add_given(self, jsonstr: str):

        out = copy(self)
        out.assignments = out.assignments.copy()
        out.constraints = [c.copy() for c in self.constraints]

        out.given = json_to_literals(out.idp, jsonstr) # {atom.code : assignment} from the user interface
        out.assignments.update(out.given) #TODO get implicants, but do not add to simplified (otherwise always relevant)
        self._formula = None

        return out._finalize()

    def _finalize(self):

        # propagate universals
        if len(self.idp.vocabularies)==2: # if there is a decision vocabulary
            # first, consider only environmental facts and theory (exclude any statement containing decisions)
            self.full_propagate(all_=False)
        self.propagate(tag=Status.CONSEQUENCE, extended=True) # now consider all facts and theories
        self.simplify()
        
        self.get_relevant_subtences()
        if __debug__: assert self.invariant == ".".join(str(e) for e in self.idp.theory.constraints)
        return self

    def __str__(self) -> str:
        self.get_co_constraints()
        return (f"Universals:  {indented}{indented.join(repr(c) for c in self.assignments.values() if c.status in [Status.UNIVERSAL, Status.ENV_UNIV])}{NEWL}"
                f"Consequences:{indented}{indented.join(repr(c) for c in self.assignments.values() if c.status in [Status.CONSEQUENCE, Status.ENV_CONSQ])}{NEWL}"
                f"Simplified:  {indented}{indented.join(c.__str1__()  for c in self.constraints)}{NEWL}"
                f"Irrelevant:  {indented}{indented.join(repr(c) for c in self.assignments.values() if not c.relevant)}{NEWL}"
                f"Co-constraints:{indented}{indented.join(c.__str1__() for c in self.co_constraints)}{NEWL}"
        )

    def get_co_constraints(self):
        self.co_constraints = OrderedSet()
        for c in self.constraints:
            c.co_constraints(self.co_constraints)
        
    # def get_relevant_subtences(self) -> Tuple[Dict[str, SymbolDeclaration], Dict[str, Expression]]:
    #     """ causal interpretation of relevance """
    #     #TODO performance.  This method is called many times !  use expr.contains(expr, symbols)
    #     constraints = ( self.constraints )

    #     # determine relevant symbols (including defined ones)
    #     relevant_symbols = mergeDicts( e.unknown_symbols() for e in constraints )

    #     # remove irrelevant domain conditions
    #     self.constraints = list(filter(lambda e: e.if_symbol is None or e.if_symbol in relevant_symbols
    #                                  , self.constraints))

    #     # determine relevant subtences
    #     relevant_subtences = mergeDicts( e.subtences() for e in constraints )
    #     relevant_subtences.update(mergeDicts(s.instances for s in relevant_symbols.values()))

    #     for k, l in self.assignments.items():
    #         symbols = list(l.sentence.unknown_symbols().keys())
    #         has_relevant_symbol = any(s in relevant_symbols for s in symbols)
    #         if k in relevant_subtences and symbols and has_relevant_symbol:
    #             l.relevant = True

    def get_relevant_subtences(self):
        """         
        sets 'relevant in self.assignments
        sets rank of symbols in self.relevant_symbols
        removes irrelevant constraints in self.constraints
        """
        for a in self.assignments.values():
            a.relevant = False

        # collect (co-)constraints
        constraints = OrderedSet()
        for constraint in self.constraints:
            constraints.append(constraint)
            constraint.co_constraints(constraints)


        # initialize reachable with relevant, if any
        reachable = OrderedSet()
        for constraint in constraints:
            if type(constraint)==AppliedSymbol and constraint.name=='__relevant':
                for e in constraint.sub_exprs:
                    assert e.code in self.assignments, f"Invalid expression in relevant: {e.code}" 
                    reachable.append(e)

        # analyse given information
        given, hasGiven = OrderedSet(), False
        for q in self.assignments.values():
            if q.status == Status.GIVEN:
                hasGiven = True
                if not q.sentence.has_decision():
                    given.append(q.sentence)


        # constraints have set of questions in self.assignments
        # set constraint.relevant, constraint.questions
        for constraint in constraints:
            constraint.relevant = False
            constraint.questions = OrderedSet()
            constraint.collect(constraint.questions, all_=True, co_constraints=False)

            # add goals in constraint.original to constraint.questions
            # only keep questions in self.assignments
            qs = OrderedSet()
            constraint.original.collect(qs, all_=True, co_constraints=False)
            for q in qs:
                if q in reachable: # a goal
                    constraint.questions.append(q)
            constraint.questions = OrderedSet([q for q in constraint.questions
                if q.code in self.assignments])


        # nothing relevant --> make every question in a constraint relevant
        if len(reachable) == 0: 
            for constraint in constraints:
                if constraint.if_symbol is None:
                    for q in constraint.questions:
                        reachable.append(q)

        # find relevant symbols by depth-first propagation
        # relevants, rank = {}, 1
        # def dfs(question):
        #     nonlocal relevants, rank
        #     for constraint in constraints:
        #         # consider constraint not yet considered
        #         if ( not constraint.relevant
        #         # containing the question
        #         and question in constraint.questions):
        #             constraint.relevant = True
        #             for q in constraint.questions:
        #                 self.assignments[q.code].relevant = True
        #                 for s in q.unknown_symbols(co_constraints=False):
        #                     if s not in relevants:
        #                         relevants[s] = rank
        #                         rank = rank+1
        #                 if q.code != question.code \
        #                 and q.type == 'bool'\
        #                 and not q in given:
        #                     print("==>", q)
        #                     reachable.add(q)
        #                     dfs(q)
        # for question in list(reachable.values()):
        #     dfs(question)

        # find relevant symbols by breadth-first propagation
        # input: reachable, given, constraints
        # output: self.assignments[].relevant, constraints[].relevant, relevants[].rank
        relevants = {}  # Dict[string: int]
        to_add, rank = reachable, 1
        while to_add:
            for q in to_add:
                self.assignments[q.code].relevant = True
                for s in q.unknown_symbols(co_constraints=False):
                    if s not in relevants:
                        relevants[s] = rank
                if not q in given:
                    reachable.append(q)

            to_add, rank = OrderedSet(), 2 # or rank+1
            for constraint in constraints:
                # consider constraint not yet considered
                if ( not constraint.relevant
                # and with a question that is reachable but not given
                and  any(q in reachable and not q in given for q in constraint.questions) ):
                    constraint.relevant = True
                    to_add.extend(constraint.questions)
        if not hasGiven or self.idp.display.moveSymbols:
            self.relevant_symbols = relevants

        # remove irrelevant domain conditions
        self.constraints = list(filter(lambda constraint: constraint.relevant, self.constraints))


    def full_propagate(self, all_: bool) -> None:
        CONSQ = Status.CONSEQUENCE if all_ else Status.ENV_CONSQ

        Log(f"{NEWL}Z3 propagation ********************************")

        theory = self.translate(all_)
        solver = Solver()
        solver.add(theory)
        result = solver.check()
        if result == sat:
            todo = self.assignments.keys()

            # determine consequences on expanded symbols only (for speed)
            for key in todo:
                l = self.assignments[key]
                if ( l.value is None
                and (all_ or not l.sentence.has_decision())):
                    atom = l.sentence
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
                                val = str_to_IDP(atom, str(val1))
                                ass = self.assignments.assert_(atom, val, CONSQ, True)
                            elif res2 == unknown:
                                res1 = unknown
                    solver.pop()
                    if res1 == unknown: # restart solver
                        solver = Solver()
                        solver.add(theory)
                        result = solver.check()
        elif result == unsat:
            print(self.translate(all_))
            raise Exception("Not satisfiable !")


    def translate(self, all_: bool = True) -> BoolRef:
        self.get_co_constraints()
        self.translated = And(
            [s.translate() for s in self.def_constraints.values()]
            + [l.translate() for k, l in self.assignments.items() 
                    if l.value is not None and (all_ or not l.sentence.has_decision())]
            + [s.translate() for s in self.constraints
                    if all_ or not s.block.name=='environment']
            + [c.translate() for c in self.co_constraints]
            )
        return self.translated

def make_case(idp: Idp, jsonstr: str, expanded: List[str]) -> Case:

        if (idp, jsonstr, expanded) in Case.cache:
            return Case.cache[(idp, jsonstr, expanded)]

        if (idp, "{}", expanded) in Case.cache:
            return Case.cache[(idp, "{}", expanded)].add_given(jsonstr)

        case = Case(idp, expanded).add_given(jsonstr)

        if 100<len(Case.cache):
            # remove oldest entry, to prevent memory overflow
            Case.cache = {k:v for k,v in list(Case.cache.items())[1:]}
        Case.cache[(idp, jsonstr, expanded)] = case
        return case
