from z3 import Function, ForAll, And, Implies, Int, IntSort, Solver, ExprRef

from configcase import ConfigCase


def theory(case: ConfigCase):
    a, b, c, f, g = case.IntsInRange("a b c f g", 0, 10)

    Color, (red, green, blue) = case.EnumSort('Color', ['red', 'green', 'blue'])
    clr, = case.Consts('clr', Color)

    d = case.Reals("d", [1.0, 2.5, 8.0])
    e = case.Reals("e", [1.0, 3.5, 9.0], True)
    p, q = case.Bools("p q")

    k = case.Function("k", [IntSort(), IntSort()], [[1, 2, 3], [4, 5, 6]], True)

    case.add(a > b + 2)
    case.add(a + 2 * c == 10)
    case.add(b + c <= 1000)
    case.add(d >= e)
    case.add(p != q)
    case.add(a + b + g == f)
    # solver.add(clr != green)
    # solver.add(p == (a == 1))


def theo2(case: ConfigCase):
    solver = case.solver
    a = Int("a")
    f = Function('f', IntSort(), IntSort())
    solver.add(ForAll(a, Implies(And(0 < a, a < 10), f(a) == a)))
    solver.add(f(110) == 4)
    print(print(f(4).sort()))


if __name__ == '__main__':
    solver = Solver()
    a = Int("a")
    f = Function('f', IntSort(), IntSort())
    solver.add(ForAll(a, Implies(And(0 < a, a < 10), f(a) == a)))
    solver.add(f(110) == 4)
    # print(a.num_args())
    # print(f.num_args())
    print(isinstance(f, ExprRef))
    print(isinstance(f(110), ExprRef))
    print(f(110).children())
    print(f(110).decl())
    print(solver.consequences([], [f(5) == 5]))
