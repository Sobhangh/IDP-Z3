
from z3 import *

from LiteralQ import *
from utils import *

def is_really_constant(expr, valueMap):
    return (obj_to_string(expr) in valueMap) \
        or is_number(obj_to_string(expr)) \
        or is_string_value(expr) \
        or is_true(expr) or is_false(expr)

    
def has_ground_children(expr, valueMap):
    return all([is_ground(child, valueMap) for child in expr.children()])


def is_ground(expr, valueMap):
    return is_really_constant(expr, valueMap) or \
        (0 < len(expr.children()) and has_ground_children(expr, valueMap))
        

def is_symbol(symb, symbols):
    if is_expr(symb):
        symb = obj_to_string(symb)
    return str(symb) in symbols


def has_local_var(expr, valueMap, symbols):
    out = ( 0==len(expr.children()) and not is_symbol(expr, symbols) \
            and not is_really_constant(expr, valueMap)) \
        or ( 0 < len(expr.children()) \
            and any([has_local_var(child, valueMap, symbols) for child in expr.children()]))
    return out


def symbols_of(expr, symbols, ignored): # returns a dict {string: string}
    out = {} # for unicity (ordered set)
    try:
        name = expr.decl().name()
        if is_symbol(name, symbols) and not name in ignored:
            out[name] = name
    except: pass
    for child in expr.children():
        out.update(symbols_of(child, symbols, ignored))
    return out

############ with solvers

def mk_solver(theory, atoms):
    solver = Solver()
    solver.add(theory)
    (reify, unreify) = reifier(atoms, solver)
    return solver, reify, unreify

def reifier(atoms, solver):
    # creates predicates equivalent to the infinitely-quantified formulas or chained comparison
    # returns ({atomZ3: predicate}, {predicate: atomZ3})
    count, (reify, unreify) = 0, ({}, {})
    for atomZ3 in atoms:
        if is_quantifier(atomZ3) or hasattr(atomZ3, 'is_chained'):
            count += 1
            const = Const("iuzctedvqsdgqe"+str(count), BoolSort())
            solver.add(const == atomZ3)
            reify[atomZ3] = const
            unreify[const] = atomZ3
        elif hasattr(atomZ3, 'interpretation'):
            count += 1
            const = Const("iuzctedvqsdgqe"+str(count), BoolSort())
            solver.add(const == atomZ3.interpretation)
            reify[atomZ3] = const
            unreify[const] = atomZ3
        else:
            reify[atomZ3] = atomZ3
            unreify[atomZ3] = atomZ3
    return (reify, unreify)


def consequences(theory, atoms, ignored, solver=None, reify=None, unreify=None):
    """ returns a set of literalQs that are based on atoms and are consequences of the theory,
        ignoring the ignored literalQs
    """
    if solver is None:
        solver, reify, unreify = mk_solver(theory, atoms)

    out = {} # {LiteralQ: True}

    for reified, atomZ3 in unreify.items():# numeric variables or atom !
        if not LiteralQ(True, atomZ3) in ignored and not LiteralQ(False, atomZ3) in ignored:
            result, consq = solver.consequences([], [reified])

            if result==unsat:
                raise Exception("Not satisfiable !")

            if result==sat:
                if consq:
                    consq = consq[0].children()[1]
                    if is_not(consq):
                        out[LiteralQ(False, atomZ3)] = True
                    elif not is_bool(reified):
                        out[LiteralQ(True, consq  )] = True
                    else:
                        out[LiteralQ(True, atomZ3 )] = True
            else: # unknown -> restart solver
                out[LiteralQ(None, atomZ3 )] = True
                solver, reify, unreify = mk_solver(theory, atoms)
    return out    