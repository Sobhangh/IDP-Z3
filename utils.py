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
