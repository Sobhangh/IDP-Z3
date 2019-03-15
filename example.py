from z3 import Function, ForAll, And, Implies, Int, IntSort, Solver, ExprRef

from configcase import ConfigCase


def theory(case: ConfigCase):
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
