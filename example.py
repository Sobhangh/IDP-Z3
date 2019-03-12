from z3 import Function, ForAll, And, Implies, Int, IntSort, EnumSort

from configcase import ConfigCase
from utils import universe


def theory(case: ConfigCase):
    solver = case.solver

    a, b, c, f, g = case.IntsInRange("a b c f g", 0, 10)

    Color, (red, green, blue) = case.EnumSort('Color', ['red', 'green', 'blue'])
    clr, = case.Consts('clr', Color)

    d = case.Reals("d", [1.0, 2.5, 8.0])
    e = case.Reals("e", [1.0, 3.5, 9.0], True)
    p, q = case.Bools("p q")

    solver.add(a > b + 2)
    solver.add(a + 2 * c == 10)
    solver.add(b + c <= 1000)
    solver.add(d >= e)
    solver.add(p != q)
    solver.add(a + b + g == f)
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
    cc = ConfigCase(theo2)
    # print(cc.model())
    # print(cc.list_of_propositions())
    # print(cc.consequences())
