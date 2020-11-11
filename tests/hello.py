import cProfile

import os,sys,inspect,time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,os.path.join(parentdir, 'Idp'))

print(parentdir)
import Inferences
from State import *
from Idp.utils import log
from Idp import *
from z3 import Solver



file = os.path.join(os.path.dirname(__file__), 'temp.idp')
model: File = idpparser.model_from_file(file)

log("parse")
if False:
    cProfile.run('State(model.translate)')
else:
    for i in range(1):
        c = State(model)
        #print(c.interpretations)
        log("translate")
        print(simplify(c.translate()))
        solver = Solver()
        solver.add(c.translate())
        print(solver.check())
        log("solve")
        print(list(str(l) for l in consequences(c.translate(), c.GUILines, {}).keys()))

# print(solver)
# print(solver.check())
# print(solver.model())

# print(c.relevantVals)