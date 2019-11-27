"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""

from z3 import And

from Structure_ import json_to_literals

class Case:
    """
    Contains a state of problem solving
    """
    cache = {}

    def __init__(self, idp, jsonstr):

        self.idp = idp # Idp vocabulary and theory
        self.given = json_to_literals(idp, jsonstr) # {literalQ : atomZ3} from the user interface

        # initialisation
        self.atoms = self.idp.atoms # {atom_string: Expression} atoms + numeric terms !
        self.universal = []
        self.typeConstraints = self.idp.vocabulary
        self.definitions = self.idp.theory.definitions # Definitions
        self.consequences = [] # [literalQ]
        self.irrelevant = [] # [Expression] subtences
        self.simplified = self.idp.theory.constraints # [Expression]

        # find universals
        # simplify self.simplified using given
        # find immediate consequences
        # update consequences using propagation
        # simplify self.simplified using all consequences
        # find irrelevant

    def translate(self):
        self.translated = And(
            self.typeConstraints.translated
            + [d.translate(self.idp) for d in self.definitions]
            + [c.translate() for c in self.universal + self.simplified]
            + (list(self.given.values())))
        return self.translated

def make_case(idp, jsonstr):
        if (idp, jsonstr) in Case.cache:
            return Case.cache[(idp, jsonstr)]

        case = Case(idp, jsonstr)

        if 20<len(Case.cache):
            del Case.cache[0] # remove oldest entry, to prevent memory overflow
        Case.cache[(idp, jsonstr)] = case
        return case