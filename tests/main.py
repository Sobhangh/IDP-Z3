
import os,sys,inspect,time

# add parent folder to import path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,os.path.join(parentdir, 'dsl'))

import configcase
from Theory import *
from utils import log
from DSLClasses import *

dir = os.path.dirname(__file__)
files = [x[0]+"/"+f for x in os.walk(dir) for f in x[2] if f.endswith(".idp")]
#files += ["/home/pcarbonn/Documents/repos/sealconstraints/OmniSeal/specification.z3"]
#files = ["/home/pcarbonn/Documents/repos/autoconfigz3/tests/isa/isa.idp"]
for file in files:
    print(file)
    model = idpparser.model_from_file(file)
    c = ConfigCase(model)

    z3 = file.replace(".z3", ".z3z3")
    z3 = z3.replace(".idp", ".z3")
    print(z3)
    if os.path.exists(z3):
        os.remove(z3)
    f = open(z3, "a")
    f.write(c.print())
    f.close()