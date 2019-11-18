import cProfile

import os,sys,inspect,time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,os.path.join(parentdir, 'Idp'))

print(parentdir)
import Inferences
from Theory import *
from utils import log
from Idp import *




file = os.path.join(os.path.dirname(__file__), 'temp.idp')
model: File = idpparser.model_from_file(file)

log("parse")
if False:
    cProfile.run('ConfigCase(model.translate)')
else:
    for i in range(1):
        c = ConfigCase(model)
        #print(c.interpretations)
        log("translate")
        print(simplify(c.translate()))
        solver, _, _ = mk_solver(c.translate(), c.idp.atoms.values())
        print(solver.check())
        log("solve")
        print(list(str(l) for l in consequences(c.translate(), c.idp.atoms.values(), {}).keys()))

# solver = c.mk_solver()
# print(solver)
# print(solver.check())
# print(solver.model())

# print(c.relevantVals)