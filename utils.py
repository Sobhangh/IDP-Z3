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
import itertools, time

from z3 import *
from z3.z3 import _to_expr_ref

start = time.time()
def log(action):
    global start
    print(action, time.time()-start)
    start = time.time()


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
            print(vsort)
            raise AssertionError('dont know how to deal with this sort')

    return rec(vsort)


def update_term(t, args):
    # Update the children of term t with args.
    # len(args) must be equal to the number of children in t.
    # If t is an application, then len(args) == t.num_args()
    # If t is a quantifier, then len(args) == 1
    n = len(args)
    _args = (Ast * n)()
    for i in range(n):
        _args[i] = args[i].as_ast()
    return _to_expr_ref(Z3_update_term(t.ctx_ref(), t.as_ast(), n, _args), t.ctx)


def rewrite(s, f, t):
    """
    Replace f-applications f(r_1, ..., r_n) with t[r_1, ..., r_n] in s.
    """
    todo = [s]  # to do list
    cache = AstMap(ctx=s.ctx)
    while todo:
        n = todo[len(todo) - 1]
        if is_var(n):
            todo.pop()
            cache[n] = n
        elif is_app(n):
            visited = True
            new_args = []
            for i in range(n.num_args()):
                arg = n.arg(i)
                if not arg in cache:
                    todo.append(arg)
                    visited = False
                else:
                    new_args.append(cache[arg])
            if visited:
                todo.pop()
                g = n.decl()
                if eq(g, f):
                    new_n = substitute_vars(t, *new_args)
                else:
                    new_n = update_term(n, new_args)
                cache[n] = new_n
        else:
            assert (is_quantifier(n))
            b = n.body()
            if b in cache:
                todo.pop()
                new_n = update_term(n, [cache[b]])
                cache[n] = new_n
            else:
                todo.append(b)
    return cache[s]


def flatten(l):
    return [item for sublist in l for item in sublist]


def in_list(q, ls):
    if not ls: return True # e.g. for int, real
    if len(ls)==1: return q == ls[0]
    outp = []
    for i in ls:
        outp.append(q == i)
    return Or(outp)


def is_number(s):
    try:
        float(eval(s)) # accepts "2/3"
        return True
    except:
        return False


def singleton(x):
    return [], x


def splitLast(l):
    return l[:-1], l[-1]


def applyTo(sym, arg):
    if len(arg) == 0:
        return sym
    return sym(arg)


def objInList(obj, list):
    for i in list:
        if obj_to_string(obj) == obj_to_string(i):
            return True
    return False


def flattenexpr(e, symblist):
    out = []
    for i in e.children():
        out += flattenexpr(i, symblist)
    if is_app(e):
        if objInList(e.decl(), symblist):
            out.append(e)
    elif objInList(e, symblist):
        out.append(e)
    return out


def pairwiseEquals(arg, constants):
    return [arg[i] == constants[i] for i in range(0, len(arg))]
