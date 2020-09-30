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

"""

Classes to execute the main block of an IDP program

"""


from .Parse import *

class Problem(object):
    """ A combination of theories and structures
    """
    def __init__(self, theories):
        self.definitions = []
        self.clark = {} # {Declaration: Rule}
        self.constraints = OrderedSet()
        self.assignments = Assignments()

        for t in theories:
            t.addTo(self)

def addTo(self, problem):
    problem.definitions.append(self.definitions)
    for symbol, rule in self.clark.items():
        if symbol not in problem.clark:
            problem.clark[symbol] = rule
        else:
            new_rule = copy(rule)  # not elegant, but rare
            new_rule.body = AConjunction.make('∧', [problem.clark[symbol].body, rule.body])
            problem.clark[symbol] = new_rule
    
Theory.addTo = addTo

def addTo(self, problem):
    pass
Structure.addTo = addTo




def execute(self):
    """ 
    Execute the IDP program
    """

    mybuiltins = {'print': print}
    mylocals = {**self.vocabularies, **self.theories, **self.structures}
    exec(str(self.procedures['main']), mybuiltins, mylocals)
Idp.execute = execute





Done = True