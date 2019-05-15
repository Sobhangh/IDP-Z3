

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
print(parentdir)
import configcase
from DSLClasses import *

model: File = idpparser.model_from_str("""
vocabulary {
    type Domain = {1..2}
    p
    q(Domain)
    x : Domain
    y(Domain): Domain
}

theory {
    p | q(1) & ~ q(2).
    x=1 | y(1)=1 | y(2)=1.
}
""")

c = ConfigCase()

model.translate(c)

print(c.mk_solver())
print(c.mk_solver().check())
print(c.model())
