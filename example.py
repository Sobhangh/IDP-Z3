from z3 import *
from configcase import ConfigCase


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


case = ConfigCase(theory)

jsonstr = "{\"f\" : { \"1\"     : {\"ct\" : true, \"cf\" : false}}," \
          " \"g\" : { \"0\"     : {\"ct\" : true, \"cf\" : false}}," \
          " \"p\" : { \"true\"  : {\"ct\" : false, \"cf\" : true}}}"
case.loadStructureFromJson(jsonstr)

print("Model: ", case.model())
print("JSON: ", case.json_model())

cons = case.consequences()
