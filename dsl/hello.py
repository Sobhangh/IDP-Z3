

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
print(parentdir)
import configcase
from DSLClasses import *

model: File = idpparser.model_from_str("""
vocabulary {

    Base : real
    Height: real
    Surface:real

    Convex
    Equilateral
}

theory {
    //Height=5.
    Convex => Surface = Height.
    ~Convex  => Surface = Height*Base.

    Convex => Equilateral.
}
""")
for i in range(1):
    c = ConfigCase(model.translate)
    c.assumptions = [c.atoms["Convex"]]
    out = c.propagation()
    print(out["Equilateral"]['[\"Equilateral\"]']["ct"]) # expected True

# solver = c.mk_solver()
# print(solver)
# print(solver.check())
# print(solver.model())

# print(c.relevantVals)