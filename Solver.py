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
from z3 import Solver, sat, unsat, is_not, is_eq, is_bool, is_expr, obj_to_string, is_string_value

from Structure_ import *
from utils import *

def is_really_constant(expr):
    return is_number(obj_to_string(expr)) \
        or is_string_value(expr) \
        or is_true(expr) or is_false(expr)

def is_symbol(symb, symbols):
    if is_expr(symb):
        symb = obj_to_string(symb)
    return str(symb) in symbols


def has_local_var(expr, symbols):
    out = ( 0==len(expr.children()) and not is_symbol(expr, symbols) \
            and not is_really_constant(expr)) \
        or ( 0 < len(expr.children()) \
            and any([has_local_var(child, symbols) for child in expr.children()]))
    return out


def getAtoms(expr, symbols):
    out = {}  # Ordered dict: string -> Z3 object
    for child in expr.children():
        out.update(getAtoms(child, symbols))
    if is_bool(expr) and len(out) == 0 and not atom_as_string(expr).startswith('_') and \
        ( not has_local_var(expr, symbols) or is_quantifier(expr) ): # for quantified formulas
        out = {atom_as_string(expr): expr}
    return out

def atom_as_string(expr):
    return str(expr).replace("==", "=").replace("!=", "≠").replace("<=", "≤")


############ with solvers

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


def consequences(theory, atoms, ignored, solver=None, reify=None, unreify=None):
    """ returns a set of literalQs that are based on atoms and are consequences of the theory,
        ignoring the ignored literalQs
    """

    if solver is None:
        solver, reify, unreify = mk_solver(theory, atoms)

    out = {} # {LiteralQ: True}
    todo = [k for (v,k) in reify.items() \
            if not LiteralQ(Truth.TRUE, v) in ignored and not LiteralQ(Truth.FALSE, v) in ignored]


    # try mass propagation first
    result, consqs = solver.consequences([], todo)
    if result==unsat:
        raise Exception("Not satisfiable !")
    elif result==sat:
        for consq in consqs:
            consq = consq.children()[1]
            t = True
            if is_not(consq):
                t, consq = False, consq.arg(0)
            t = Truth.TRUE if t else Truth.FALSE
            # try to unreify it
            if is_eq(consq):
                symbol = consq.children()[0]
                if symbol in unreify:
                    out[ LiteralQ(t, Equality(unreify[symbol], consq.children()[1])) ] = True
                else:
                    print("???", str(consq))
            elif consq in unreify:
                out[LiteralQ(t, unreify[consq])] = True
            else:
                print("???", str(consq))
        return out
    # else: # unknown satisfiability, e.g. due to non-linear equations
    # restart solver and continue 
    solver, _, unreify = mk_solver(theory, atoms)

    # pre-compute possible values
    solver2, _, _ = mk_solver(theory, atoms)
    result2 = solver2.check()

    # optimal propagation, considering each atom separately
    for reified in todo:# numeric variables or atom !
        result, consq = solver.consequences([], [reified])

        optimal = True
        if result==unsat:
            raise Exception("Not satisfiable !")
        elif result==sat:
            if consq:
                optimal = False
                consq = consq[0].children()[1]
                t = True
                if is_not(consq):
                    t, consq = False, consq.arg(0)
                t = Truth.TRUE if t else Truth.FALSE
                if consq in unreify:
                    out[LiteralQ(t, unreify[consq])] = True
                elif is_eq(consq):
                    symbol = consq.children()[0]
                    if symbol in unreify:
                        out[ LiteralQ(t, Equality(unreify[symbol], consq.children()[1])) ] = True
        else: # unknown -> restart solver
            solver, _, unreify = mk_solver(theory, atoms)

        if optimal and result2 == sat: # try optimal propagation
            value = solver2.model().eval(reified)

            if str(value) != str(reified): # exclude Length(1) == Length(1) (irrelevant)
                solver.push()
                solver.add(Not(reified == value))
                result3 = solver.check()
                solver.pop()

                if result3 == sat:
                    pass
                elif result3 == unsat: # atomZ3 can have only one value
                    if is_bool(reified):
                        out[LiteralQ(Truth.TRUE if is_true(value) else Truth.FALSE, unreify[reified])] = True
                    else:
                        out[LiteralQ(Truth.TRUE, Equality(unreify[reified], value))] = True
                else:
                    print("can't propagate with", Not(reified == value))
    if result2 != sat:
        #TODO reify the non linear equations, find their thruth value, then use a solver ?
        print("can't find a model")
    return out    