# Copyright 2019-2023 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of IDP-Z3.
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


from idp_engine.Assignments import Status as S
from idp_engine.Run import Theory
from idp_engine.utils import OrderedSet, NEWL, indented, DEFAULT
from .IO import load_json
import json

# Types
from idp_engine import IDP
from typing import Dict, Tuple, Union


class State(Theory):
    """ Contains a state of problem solving """
    cache: dict[str, 'State'] = {}

    @classmethod
    def make(cls, idp: IDP, previous_active: str, active: str, ignore: str = None) -> "State":
        """Manage the cache of State

        Args:
            idp (IDP): idp source code
            previous_active (str): assignments due to previous full propagation
            active (str): assignment choices from client
            ignore (str): user-disabled laws to ignore

        Returns:
            State: a State
        """
        ignored_laws = set(json.loads(ignore)) if ignore else set()
        if active != "{}" and idp.code in State.cache:
            state = State.cache[idp.code]
            state.ignored_laws = ignored_laws
            state.add_given(active, previous_active)
        else:
            if 100 < len(State.cache):
                # remove oldest entry, to prevent memory overflow
                State.cache.pop(list(State.cache.keys())[-1])
            state = State(idp)
            State.cache[idp.code] = state
            state.ignored_laws = ignored_laws
            state.add_given(active, previous_active, True)
        return state

    def __init__(self, idp: IDP):
        # determine default vocabulary, theory, before annotating display
        if len(idp.theories) != 1:
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

        super().__init__(extended=True)

        if len(idp.theories) == 2:
            blocks = ([idp.theories['environment']]
                      + [struct for struct in idp.structures.values()
                         if struct.voc.name == 'environment'])
            self.environment = Theory(* blocks, extended=True)

            blocks = [self.environment, idp.theories['decision']]
        else:  # take the first theory
            self.environment = None
            blocks = [next(iter(idp.theories.values()))]

        blocks += [struct for struct in idp.structures.values()
                   if struct.voc.name != 'environment']
        self.add(*blocks)

        # sentences in decision theory may be environmental (issue 147)
        if self.environment:
            for a in self.assignments.values():
                if (a.sentence not in self.environment.assignments
                        and not a.sentence.has_decision()):
                    self.environment.assignments.assert__(a.sentence, a.value, a.status)

    def add_given(self, jsonstr: str, previous: str, keep_defaults: bool = False):
        """
        Add the assignments that the user gave through the interface.
        These are in the form of a json string.

        :arg jsonstr: the user's assignment in json
        :arg previous: the assignments from the last propagation
        :arg keep_default: whether default assignments should not be reset
        :post: the state has the jsonstr and previous added
        """

        if self.environment:
            load_json(self.environment.assignments, jsonstr, keep_defaults)
            load_json(self.environment.previous_assignments, previous, False)
        load_json(self.assignments, jsonstr, keep_defaults)
        load_json(self.previous_assignments, previous, False)

        # perform propagation
        if self.environment is not None:  # if there is a decision vocabulary
            self.environment.ignored_laws = self.ignored_laws
            self.environment.propagate(tag=S.ENV_CONSQ)
            self.assignments.update(self.environment.assignments)
            self._formula = None
        self.propagate(tag=S.CONSEQUENCE)

    def __str__(self) -> str:
        self.co_constraints = OrderedSet()
        for c in self.constraints:
            c.collect_co_constraints(self.co_constraints)
        return (f"Universals:  {indented}{indented.join(repr(c) for c in self.assignments.values() if c.status == S.UNIVERSAL)}{NEWL}"
                f"Consequences:{indented}{indented.join(repr(c) for c in self.assignments.values() if c.status in [S.CONSEQUENCE, S.ENV_CONSQ])}{NEWL}"
                f"Simplified:  {indented}{indented.join(c.__str__()  for c in self.constraints)}{NEWL}"
                f"Irrelevant:  {indented}{indented.join(repr(c) for c in self.assignments.values() if not c.relevant)}{NEWL}"
                f"Co-constraints:{indented}{indented.join(c.__str__() for c in self.co_constraints)}{NEWL}"
                )

