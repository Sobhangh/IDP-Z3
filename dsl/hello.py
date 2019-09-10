import cProfile

import os,sys,inspect,time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
print(parentdir)
import configcase
from Theory import *
from utils import log
from DSLClasses import *




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
        print(simplify(c.theory()))
        solver, _, _ = mk_solver(c.theory(), c.atoms.values())
        print(solver.check())
        log("solve")
        print(list(str(l) for l in consequences(c.theory(), c.atoms.values(), {}).keys()))

# solver = c.mk_solver()
# print(solver)
# print(solver.check())
# print(solver.model())

# print(c.relevantVals)