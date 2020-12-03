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

Classes to execute the main block of an IDP program

"""

import types
from z3 import Solver

from .Assignments import Assignment
from .Parse import *
from .Problem import Problem, str_to_IDP


def model_check(theories, structures=None):
    """ output: "sat", "unsat" or "unknown" """

    problem = Problem.make(theories, structures)
    z3_formula = problem.formula().translate()

    solver = Solver()
    solver.add(z3_formula)
    yield str(solver.check())


def model_expand(theories, structures=None, max=10, complete=False, 
        extended=False):
    """ output: a list of Assignments, ending with a string """
    problem = Problem.make(theories, structures)
    yield from problem.expand(max=max, complete=complete, extended=extended)

def model_propagate(theories, structures=None):
    """ output: a list of Assignment """
    problem = Problem.make(theories, structures)
    yield from problem._propagate(tag=Status.CONSEQUENCE, extended=False)

def myprint(x=""):
    if isinstance(x, types.GeneratorType):
        for i, xi in enumerate(x):
            if isinstance(xi, Assignments):
                print(f"{NEWL}Model {i+1}{NEWL}==========")
                print(xi)
            else:
                print(xi)
    else:
        print(x)

def execute(self):
    """ Execute the IDP program """
    main = str(self.procedures['main'])
    mybuiltins = {'print': myprint}
    mylocals = {**self.vocabularies, **self.theories, **self.structures}
    mylocals['model_check'] = model_check
    mylocals['model_expand'] = model_expand
    mylocals['model_propagate'] = model_propagate
    mylocals['Problem'] = Problem

    exec(main, mybuiltins, mylocals)
Idp.execute = execute





Done = True