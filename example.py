from z3 import Function, ForAll, And, Implies, Int, IntSort, Solver, ExprRef, simplify, help_simplify, Ints, Goal, Or, \
    Then, Tactic

from configcase import ConfigCase
from utils import flattenexpr


def theoryTestCase(case: ConfigCase):
    # Declares integers in a fixed range
    a, b, c, f, g = case.IntsInRange("a b c f g", 0, 10)

    # Declares a new enumerated type with constants
    Color, (red, green, blue) = case.EnumSort('Color', ['red', 'green', 'blue'])

    # Declares a constant of a previously declared type
    clr, = case.Consts('clr', Color)

    # Declares a Real Number, the values, the enumerated values are communicated to the GUI but
    # the value is not restricted to this enumeration
    d = case.Reals("d", [1.0, 2.5, 8.0])

    # Same as before, but the value is one of the enumerated ones
    e = case.Reals("e", [1.0, 3.5, 9.0], True)

    # Declares some boolean propositions
    p, q = case.Bools("p q")

    # Declares a function. The sorts before the last one are the inputs, and the last one is the output type.
    # Same holds for the values. The range of the function is restricted to this list of values
    k = case.Function("k", [IntSort(), IntSort()], [[1, 2, 3], [4, 5, 6]])

    # Declares a predicate. The domain of the predicate is restricted to the enumerated list
    pred = case.Predicate("pred", [IntSort()], [[1, 2, 3, 4, 5, 6, 7, 8, 9]])

    # Adds constraints to the theory
    case.add(pred(a))
    case.add(a > b + 2)
    case.add(a + 2 * c == 10)
    case.add(b + c <= 1000)
    case.add(d >= e)
    case.add(p != q)
    case.add(a + b + g == f)
    # solver.add(clr != green)
    # solver.add(p == (a == 1))


theoString = "global theory\r\n" \
             "def theory(case: ConfigCase):\r\n    # Declares integers in a fixed range\r\n    a, b, c, f, " \
             "g = case.IntsInRange(\"a b c f g\", 0, 10)\r\n\r\n    # Declares a new enumerated type with " \
             "constants\r\n    Color, (red, green, blue) = case.EnumSort('Color', ['red', 'green', 'blue'])\r\n\r\n   " \
             " # Declares a constant of a previously declared type\r\n    clr, = case.Consts('clr', Color)\r\n\r\n    " \
             "# Declares a Real Number, the values, the enumerated values are communicated to the GUI but\r\n    # " \
             "the value is not restricted to this enumeration\r\n    d = case.Reals(\"d\", [1.0, 2.5, 8.1])\r\n\r\n   " \
             " # Same as before, but the value is one of the enumerated ones\r\n    e = case.Reals(\"e\", [1.0, 3.5, " \
             "9.0], True)\r\n\r\n    # Declares some boolean propositions\r\n    p, q = case.Bools(\"p q\")\r\n\r\n   " \
             " # Declares a function. The sorts before the last one are the inputs, and the last one is the output " \
             "type.\r\n    # Same holds for the values. The range of the function is restricted to this list of " \
             "values\r\n    k = case.Function(\"k\", [IntSort(), IntSort()], [[1, 2, 3], [4, 5, 6]])\r\n\r\n    # " \
             "Declares a predicate. The domain of the predicate is restricted to the enumerated list\r\n    pred = " \
             "case.Predicate(\"pred\", [IntSort()], [[1, 2, 3, 4, 5, 6, 7, 8, 9]])\r\n\r\n    # Adds constraints to " \
             "the theory\r\n    case.add(pred(a))\r\n    case.add(a > b + 2)\r\n    case.add(a + 2 * c == 10)\r\n    " \
             "case.add(b + c <= 1000)\r\n    case.add(d >= e)\r\n    case.add(p != q)\r\n    case.add(a + b + g == " \
             "f)\r\n    # solver.add(clr != green)\r\n    # solver.add(p == (a == 1))\r\n"


def theo2(case: ConfigCase):
    solver = case.solver
    a = Int("a")
    f = Function('f', IntSort(), IntSort())
    solver.add(ForAll(a, Implies(And(0 < a, a < 10), f(a) == a)))
    solver.add(f(110) == 4)
    print(print(f(4).sort()))



if __name__ == '__main__':
    a, b, c, d = Ints('a b c d')
    g = Goal()
    g.add(Or(a == 0, a == 1), Or(b == 0, b == 1), a > b, Or(c == 1, d > c), d == 3)
    t = Tactic('ctx-solver-simplify')
    r = t(g)
    for i in r:
        for j in i:
            print("Flatten:")
            print(j)
            print(flattenexpr(j))
    print(r)
