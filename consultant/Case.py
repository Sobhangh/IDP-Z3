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
from debugWithYamlLog import NEWL, indented

from Idp.Expression import AppliedSymbol
from Idp.utils import *
from Idp.Run import Problem
from .IO import json_to_literals, Status
from .Inferences import get_relevant_subtences

# Types
from Idp import Idp, SymbolDeclaration
from Idp.Expression import Expression
from typing import Any, Dict, List, Union, Tuple, cast


class Case(Problem):
    """ Contains a state of problem solving """
    cache: Dict[Tuple[Idp, str, List[str]], 'Case'] = {}

    def __init__(self, idp: Idp):

        # determine default vocabulary, theory, before annotating display
        if len(idp.theories)!=1 and 'main' not in idp.procedures: # (implicit) display block
            assert len(idp.vocabularies) == 2, \
                "Maximum 2 vocabularies are allowed in Interactive Consultant"
            assert len(idp.theories)     == 2, \
                "Maximum 2 theories are allowed in Interactive Consultant"
            assert 'environment' in idp.vocabularies and 'decision' in idp.vocabularies, \
                "The 2 vocabularies in Interactive Consultant must be 'environment' and 'decision'"
            assert 'environment' in idp.theories and 'decision' in idp.theories, \
                "The 2 theories in Interactive Consultant must be 'environment' and 'decision'"

            idp.vocabulary = idp.vocabularies['decision']
            idp.theory     = idp.theories    ['decision']
            idp.theory.constraints.extend(idp.theories['environment'].constraints)
            idp.theory.definitions.extend(idp.theories['environment'].definitions)
            idp.theory.def_constraints.update(idp.theories['environment'].def_constraints)
            idp.theory.assignments.extend(idp.theories['environment'].assignments)
        idp.goal.annotate(idp)
        idp.view.annotate(idp)
        idp.display.annotate(idp)
        idp.display.run(idp)

        super().__init__()
        self.given = None # Assignments from the user interface

        if len(idp.theories) == 2:
            self.environment = Problem(idp.theories['environment'])
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

        out.given = json_to_literals(out, jsonstr)

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
        
        get_relevant_subtences(self)
        return self

    def __str__(self) -> str:
        self.co_constraints = OrderedSet()
        for c in self.constraints:
            c.co_constraints(self.co_constraints)
        return (f"Universals:  {indented}{indented.join(repr(c) for c in self.assignments.values() if c.status in [Status.UNIVERSAL, Status.ENV_UNIV])}{NEWL}"
                f"Consequences:{indented}{indented.join(repr(c) for c in self.assignments.values() if c.status in [Status.CONSEQUENCE, Status.ENV_CONSQ])}{NEWL}"
                f"Simplified:  {indented}{indented.join(c.__str1__()  for c in self.constraints)}{NEWL}"
                f"Irrelevant:  {indented}{indented.join(repr(c) for c in self.assignments.values() if not c.relevant)}{NEWL}"
                f"Co-constraints:{indented}{indented.join(c.__str1__() for c in self.co_constraints)}{NEWL}"
        )
        

def make_case(idp: Idp, jsonstr: str) -> Case:
    """ manages the cache of Cases """
    if (idp, jsonstr) in Case.cache:
        return Case.cache[(idp, jsonstr)]

    if (idp, "{}") in Case.cache:
        case = Case.cache[(idp, "{}")]
    else:
        case = Case(idp)
    case = case.add_given(jsonstr)

    if 100<len(Case.cache):
        # remove oldest entry, to prevent memory overflow
        Case.cache = {k:v for k,v in list(Case.cache.items())[1:]}
    Case.cache[(idp, jsonstr)] = case
    return case
