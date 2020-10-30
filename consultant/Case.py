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
    """ Contains a state of problem solving """
    cache: Dict[Tuple[Idp, str, List[str]], 'Case'] = {}

    def __init__(self, idp: Idp):
        super().__init__([])

        if len(idp.theories) == 2:
            self.environment = Problem([idp.theories['environment']])
            if 'environment' in idp.structures: 
                self.environment.add(idp.structures['environment'])
            self.environment.symbolic_propagate(tag=Status.ENV_UNIV)

            self.add(self.environment)
            self.add(idp.theories['decision'])
            if 'decision' in idp.structures: 
                self.add(idp.structures['decision'])
        else: # take the first theory and structure
            self.add(next(iter(idp.theories.values())))
            if len(idp.structures)==1:
                self.add(next(iter(idp.structures.values())))
        self.symbolic_propagate(tag=Status.UNIVERSAL)

        self.idp = idp # Idp vocabulary and theory

        self._finalize()

    def add_given(self, jsonstr: str):
        out = self.copy()

        out.given = json_to_literals(out.idp, jsonstr) # {atom.code : assignment} from the user interface

        if len(out.idp.theories) == 2:
            out.environment = self.environment.copy()
            out.environment.assignments.update(out.given)
        else:
            out.assignments.update(out.given)
        return out._finalize()

    def _finalize(self):
        # propagate universals
        if len(self.idp.vocabularies)==2: # if there is a decision vocabulary
            self.environment.propagate(tag=Status.ENV_CONSQ, extended=True)
            self.assignments.update(self.environment.assignments)
            self._formula = None
        self.propagate(tag=Status.CONSEQUENCE, extended=True)
        self.simplify()
        
        self.get_relevant_subtences()
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

def make_case(idp: Idp, jsonstr: str) -> Case:
    """ manages the cache of Cases """
    if (idp, jsonstr) in Case.cache:
        return Case.cache[(idp, jsonstr)]

    case = Case.cache.get((idp, "{}"), Case(idp))
    case = case.add_given(jsonstr)

    if 100<len(Case.cache):
        # remove oldest entry, to prevent memory overflow
        Case.cache = {k:v for k,v in list(Case.cache.items())[1:]}
    Case.cache[(idp, jsonstr)] = case
    return case
