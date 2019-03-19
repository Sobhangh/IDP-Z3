import itertools

from z3 import *


def universe(vsort):
    found = set()

    def rec(vsort):
        id = Z3_get_ast_id(vsort.ctx_ref(), vsort.as_ast())
        if id in found:
            raise AssertionError('recursive sorts are not supported')
        found.add(id)
        ctx = vsort.ctx
        if vsort.kind() == Z3_BOOL_SORT:
            return [BoolVal(True, ctx)]  # Only consider "True" for booleans
        elif vsort.kind() == Z3_BV_SORT:
            sz = vsort.size()
            return [BitVecVal(i, vsort) for i in range(2 ** sz)]
        elif vsort.kind() == Z3_DATATYPE_SORT:
            r = []
            for i in range(vsort.num_constructors()):
                c = vsort.constructor(i)
                if c.arity() == 0:
                    r.append(c())
                else:
                    domain_universe = []
                    for j in range(c.arity()):
                        domain_universe.append(rec(c.domain(j)))
                    r = r + [c(*args) for args in itertools.product(*domain_universe)]
            return r
        else:
            raise AssertionError('dont know how to deal with this sort')

    return rec(vsort)


def flatten(l):
    return [item for sublist in l for item in sublist]


def in_list(q, ls):
    outp = False
    for i in ls:
        outp = Or(q == i, outp)
    return outp


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def singleton(x):
    return [], x


def splitLast(l):
    return [l[i] for i in range(0, len(l) - 1)], l[len(l) - 1]


def applyTo(sym, arg):
    if len(arg) == 0:
        return sym
    return sym(arg)


def appended(arg, val):
    out = [x for x in arg]
    out.append(val)
    return out


def flattenexpr(e):
    out = []
    for i in e.children():
        out += flattenexpr(i)
    if is_app(e):
        out.append(e.decl())
    else:
        out.append(e)
    return out
