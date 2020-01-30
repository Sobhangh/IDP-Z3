
import os,sys,inspect,time, pprint

# add parent folder to import path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,os.path.join(parentdir, 'Idp'))

from Case import *
from Inferences import *
from Solver import *
from utils import log, start
from Idp import *


dir = os.path.dirname(__file__)
files = [x[0]+"/"+f for x in os.walk(dir) for f in x[2] if f.endswith(".idp")]
#files += ["/home/pcarbonn/Documents/repos/sealconstraints/OmniSeal/specification.z3"]
#files = ["/home/pcarbonn/Documents/repos/autoconfigz3/tests/sandbox/sandbox.idp"]
#files = ["/home/pcarbonn/Documents/repos/autoconfigz3/tests/isa/isa.idp"]
#files = ["/home/pcarbonn/Documents/repos/autoconfigz3/tests/prime/prime.idp"]
#files = ["/home/pcarbonn/Documents/repos/autoconfigz3/tests/polygon/Length(3).idp"]
#files = ["/home/pcarbonn/Documents/repos/autoconfigz3/tests/isa/definition.idp"]
for file in files:
    print(file)
    idp = idpparser.model_from_file(file)  

    expanded_symbols = {}
    for expr in idp.theory.subtences.values():
        expanded_symbols.update(expr.unknown_symbols())
    expanded_symbols = tuple(expanded_symbols.keys())
    case = Case(idp, "", expanded_symbols)

    z3 = file.replace(".z3", ".z3z3")
    z3 = z3.replace(".idp", ".z3")
    print(z3)
    if os.path.exists(z3):
        os.remove(z3)
    f = open(z3, "a")
    f.write("\r\n\r\n".join(str(t) for t in case.idp.vocabulary.translated))
    f.write("\r\n-- theory\r\n")
    f.write("\r\n\r\n".join(str(t) for t in case.idp.theory.translated)     + "\r\n")
    f.write("\r\n-- atoms\r\n")
    f.write("\r\n".join(str(t) for t in case.GUILines)     + "\r\n")

    f.write("\r\n-- case\r\n")
    f.write(str(case)+ "\r\n")
    out = pprint.pformat(propagation(case), width = 120)
    f.write("\r\n-- propagation\r\n")
    f.write(out     + "\r\n")

    f.close()
print("*** Total: ", round(time.time()-start,3))