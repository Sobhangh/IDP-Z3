

import os,sys,inspect,time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
print(parentdir)
import configcase
from DSLClasses import *

start = time.time()
def log(action):
    global start
    print(action, time.time()-start)
    start = time.time()



file = os.path.join(os.path.dirname(__file__), 'temp.idp')
model: File = idpparser.model_from_file(file)

log("parse")
for i in range(1):
    c = ConfigCase(model.translate)
    #print(c.interpretations)
    log("translate")
    solver = c.mk_solver(with_assumptions=False)
    print(solver.check())
    log("solve")

# solver = c.mk_solver()
# print(solver)
# print(solver.check())
# print(solver.model())

# print(c.relevantVals)