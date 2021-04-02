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
Management of the State of problem solving with the Interactive Consultant.
"""


from idp_engine.Run import Problem
from idp_engine.utils import OrderedSet, NEWL, indented
from .IO import json_to_literals, Status
from .Inferences import get_relevant_subtences

# Types
from idp_engine import IDP
from typing import Dict, Tuple


class State(Problem):
    """ Contains a state of problem solving """
    cache: Dict[Tuple[IDP, str], 'State'] = {}

    def __init__(self, idp: IDP, with_default = False):

        # determine default vocabulary, theory, before annotating display
        if len(idp.theories) != 1 and 'main' not in idp.procedures:  # (implicit) display block
            assert len(idp.vocabularies) == 2, \
                "Maximum 2 vocabularies are allowed in Interactive Consultant"
            assert len(idp.theories) == 2, \
                "Maximum 2 theories are allowed in Interactive Consultant"
            assert 'environment' in idp.vocabularies and 'decision' in idp.vocabularies, \
                "The 2 vocabularies in Interactive Consultant must be 'environment' and 'decision'"
            assert 'environment' in idp.theories and 'decision' in idp.theories, \
                "The 2 theories in Interactive Consultant must be 'environment' and 'decision'"

            idp.vocabulary = idp.vocabularies['decision']
            idp.theory     = idp.theories    ['decision']
        if "_ViewType" not in idp.vocabulary.symbol_decls:
            idp.display.annotate(idp)
            idp.display.run(idp)
        self.idp = idp  # IDP vocabulary and theory

        super().__init__()
        self.given = None  # Assignments from the user interface

        if len(idp.theories) == 2:
            self.environment = Problem(idp.theories['environment'])
            if 'environment' in idp.structures:
                self.environment.add(idp.structures['environment'])
            self.environment.symbolic_propagate(tag=Status.ENV_UNIV)

            self.add(self.environment)
            self.add(idp.theories['decision'])
            if 'decision' in idp.structures:
                self.add(idp.structures['decision'])
        else:  # take the first theory and structure
            self.environment = None
            self.add(next(iter(idp.theories.values())))
            for name, struct in idp.structures.items():
                if name != "default" or with_default:
                    self.add(struct)
        self._interpret()
        self.symbolic_propagate(tag=Status.UNIVERSAL)

        self._finalize()

    def add_given(self, jsonstr: str):
        """
        Add the assignments that the user gave through the interface.
        These are in the form of a json string.

        :arg jsonstr: the user's assignment in json
        :returns: the state with the jsonstr added
        :rtype: State
        """
        out = self.copy()
        if out.environment:
            out.environment = out.environment.copy()
            _ = json_to_literals(out.environment, jsonstr)
        out.given = json_to_literals(out, jsonstr)

        return out._finalize()

    def _finalize(self):
        # propagate universals
        if self.environment is not None:  # if there is a decision vocabulary
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


def make_state(idp: IDP, jsonstr: str) -> State:
    """Manage the cache of State

    Args:
        idp (IDP): idp source code
        jsonstr (str): input from client
        with_default (bool, optional): True if default structure must be loaded. Defaults to False.

    Returns:
        State: a State
    """

    if (idp, jsonstr) in State.cache:
        return State.cache[(idp, jsonstr)]

    if 100 < len(State.cache):
        # remove oldest entry, to prevent memory overflow
        State.cache = {k: v for k, v in list(State.cache.items())[1:]}

    state = State(idp, with_default=(jsonstr == "{}")).add_given(jsonstr)
    State.cache[(idp, jsonstr)] = state
    return state
