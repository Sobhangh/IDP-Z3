from configcase import ConfigCase
from z3 import *


def theory(self):
    solver = self.solver
    a, b, c, f, g = Ints("a b c f g")
    self.relevantVals[a] = list(range(1, 10))
    self.relevantVals[b] = list(range(1, 10))
    self.relevantVals[c] = list(range(1, 10))
    self.relevantVals[f] = list(range(1, 20))
    self.relevantVals[g] = list(range(1, 20))

    d, e = Reals("d e")
    p, q = Bools("p q")

    self.relevantVals[d] = [1, 2.5, 8]
    self.relevantVals[e] = [1, 3.5, 9]

    self.symbols = [a, b, c, d, e, f, g, p, q]

    solver.add(a > b + 2)
    solver.add(a + 2 * c == 10)
    solver.add(b + c <= 1000)
    solver.add(d >= e)
    solver.add(p != q)
    solver.add(a + b + g == f)
    # solver.add(p == (a == 1))


def structure(self):
    return [
        # self.as_symbol("a") == 2,
        # self.as_symbol("f") == 1,
        # self.as_symbol("g") == 0,
        self.as_symbol("p") == True
    ]


case = ConfigCase(theory, structure)

print("Model: ", case.model())
print("JSON: ", case.json_model())
print(case.consequences())

c = case.consequences()
