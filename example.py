from configcase import ConfigCase


def theory(case: ConfigCase):
    solver = case.solver
    a, b, c, f, g = case.IntsInRange("a b c f g", 0, 10)

    d = case.Reals("d", [1.0, 2.5, 8.0])
    e = case.Reals("e", [1.0, 3.5, 9.0], True)
    p, q = case.Bools("p q")

    solver.add(a > b + 2)
    solver.add(a + 2 * c == 10)
    solver.add(b + c <= 1000)
    solver.add(d >= e)
    solver.add(p != q)
    solver.add(a + b + g == f)
    # solver.add(p == (a == 1))
