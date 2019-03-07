from z3 import *
from z3.z3 import _py2expr

from configcase import ConfigCase


def theory(self):
    solver = self.solver
    a, b, c, f, g = Ints("a b c f g")
    self.relevantVals[a] = list(map(_py2expr, range(1, 10)))
    self.relevantVals[b] = list(map(_py2expr, range(1, 10)))
    self.relevantVals[c] = list(map(_py2expr, range(1, 10)))
    self.relevantVals[f] = list(map(_py2expr, range(1, 10)))
    self.relevantVals[g] = list(map(_py2expr, range(1, 10)))

    d, e = Reals("d e")
    p, q = Bools("p q")

    self.relevantVals[d] = list(map(_py2expr, [1.0, 2.5, 8.0]))
    self.relevantVals[e] = list(map(_py2expr, [1.0, 3.5, 9.0]))

    self.symbols = [a, b, c, d, e, f, g, p, q]

    solver.add(a > b + 2)
    solver.add(a + 2 * c == 10)
    solver.add(b + c <= 1000)
    solver.add(d >= e)
    solver.add(p != q)
    solver.add(a + b + g == f)
    # solver.add(p == (a == 1))


if __name__ == '__main__':
    case = ConfigCase(theory)

    jsonstr = "{\"f\" : { \"[1]\"     : {\"ct\" : true, \"cf\" : false}}," \
              " \"g\" : { \"[0]\"     : {\"ct\" : true, \"cf\" : false}}," \
              " \"p\" : { \"[true]\"  : {\"ct\" : false, \"cf\" : true}}}"
    case.loadStructureFromJson(jsonstr)

    print("Model: ", case.model())
    print("JSON: ", case.json_model())

    cons = case.consequences()
    print(cons)
