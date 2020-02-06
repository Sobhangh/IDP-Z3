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
from z3 import Solver, sat, unsat, is_not, is_eq, is_bool

from Structure_ import *
from utils import *


def mk_solver(theory, atoms):
    solver = Solver()
    solver.add(theory)
    (reify, unreify) = reifier(atoms, solver)
    return solver, reify, unreify

def reifier(atoms, solver):
    # creates a proposition variable for each boolean expression
    # returns ({atom: predicateZ3}, {predicateZ3: atom})
    count, (reify, unreify) = 0, ({}, {})
    for atom in atoms.values():
        reify[atom] = atom.reified()
        unreify[atom.reified()] = atom
        if atom.type == 'bool':
            solver.add(atom.reified() == atom.translated)
    return (reify, unreify)
