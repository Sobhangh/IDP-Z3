"""
Copyright 2020 Anonymous

    This file is distributed for the sole purpose of an article review.  It cannot be used for any other purpose.
"""
from z3 import Solver, sat, unsat, is_not, is_eq, is_bool

from .Structure_ import *
from .utils import *


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
        reify[atom.code] = atom.reified()
        unreify[atom.reified()] = atom
        if atom.type == 'bool':
            solver.add(atom.reified() == atom.translate())
    return (reify, unreify)
