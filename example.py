from z3 import *
import json


def exampletheory(solver):
    a, b, c = Ints("a b c")
    d, e = Reals("d e")
    p, q = Bools("p q")
    solver.add(a > b + 2)
    solver.add(a + 2 * c == 10)
    solver.add(b + c <= 1000)
    solver.add(d >= e)
    solver.add(p != q)
    return [a, b, c, d, e, p, q]


def model_to_json(m, symbols):
    output = {}
    for symb in symbols:
        val = m[symb]
        print(symb, symb.sort())
        output[obj_to_string(symb)] = obj_to_string(val)
    return json.dumps(output)


def getmodel(solver):
    s.check()
    return s.model()


s = Solver()
symbols = exampletheory(s)
m = getmodel(s)

print("Model: ", m)
print("JSON: ", model_to_json(m, symbols))
