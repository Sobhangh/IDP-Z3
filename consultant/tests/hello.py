import cProfile

import os,sys,inspect,time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,os.path.join(parentdir, 'Idp'))

print(parentdir)
import Inferences
from Case import *
from Solver import *
from Idp.utils import log
from Idp import *




file = os.path.join(os.path.dirname(__file__), 'temp.idp')
model: File = idpparser.model_from_file(file)

log("parse")
if False:
    cProfile.run('Case(model.translate)')
else:
    for i in range(1):
        c = Case(model)
        #print(c.interpretations)
        log("translate")
        print(simplify(c.translate()))
        solver, _, _ = mk_solver(c.translate(), c.GUILines)
        print(solver.check())
        log("solve")
        print(list(str(l) for l in consequences(c.translate(), c.GUILines, {}).keys()))

# solver = c.mk_solver()
# print(solver)
# print(solver.check())
# print(solver.model())

# print(c.relevantVals)