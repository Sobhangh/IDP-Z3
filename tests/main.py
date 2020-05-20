
import inspect, os, sys, time, pprint

# add parent folder to import path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, os.path.join(parentdir, 'Idp'))

from Case import Case
from Inferences import metaJSON, propagation
from debugWithYamlLog import Log_file, log_calls
from utils import start
from Idp import idpparser, SymbolDeclaration
from Idp.Expression import Expression, AppliedSymbol, Variable, Fresh_Variable
from typing import Dict


# patch Log on Idp.Substitute #################################################

for i in [Expression, AppliedSymbol, Variable, Fresh_Variable]:
    i.substitute = log_calls(i.substitute)


###############################################################################

dir = os.path.dirname(__file__)
files = [os.path.join(dir, "1 sandbox/sandbox.idp")]
files += [x[0]+"/"+f for x in os.walk(dir) for f in x[2] if
          f.endswith(".idp") and not f.endswith("sandbox.idp")]
files.sort()
for file in files:
    print(file)
    Log_file(file)
    f = open(file, "r")
    theory = f.read()
    idp = idpparser.model_from_str(theory)

    expanded_symbols: Dict[str, SymbolDeclaration] = {}
    for expr in idp.subtences.values():
        expanded_symbols.update(expr.unknown_symbols())
    expanded_symbols2 = list(expanded_symbols.keys())
    case = Case(idp, "", expanded_symbols2)

    z3 = file.replace(".z3", ".z3z3")
    z3 = z3.replace(".idp", ".z3")
    if os.path.exists(z3):
        os.remove(z3)
    f = open(z3, "a")
    f.write("\r\n-- original ---------------------------------\r\n")
    f.write(theory)
    f.write("\r\n-- vocabulary -------------------------------\r\n")
    f.write("\r\n\r\n".join(str(t) for t in case.idp.vocabulary.translated))
    f.write("\r\n-- theory -----------------------------------\r\n")
    f.write("\r\n\r\n"
            .join(str(t) for t in case.idp.theory.translate(case.idp))
            + "\r\n")
    if case.idp.goal.translate() is not None:
        f.write("\r\n-- goal -----------------------------------\r\n")
        f.write(str(case.idp.goal.translate()) + "\r\n")
    f.write("\r\n-- subtences ------------------------------------\r\n")
    f.write("\r\n".join(str(t) for t in case.idp.subtences) + "\r\n")
    f.write("\r\n-- GUILines ------------------------------------\r\n")
    f.write("\r\n".join(str(t) for t in case.GUILines) + "\r\n")

    f.write("\r\n-- case -------------------------------------\r\n")
    f.write(str(case) + "\r\n")
    f.write("\r\n-- meta -------------------------------------\r\n")
    out = pprint.pformat(metaJSON(case.idp), width=120)
    f.write(out + "\r\n")
    f.write("\r\n-- propagation ------------------------------\r\n")
    out = pprint.pformat(propagation(case), width=120)
    f.write(out + "\r\n")

    f.close()
    print("----------------")

total = round(time.process_time()-start, 3)
print("*** Total: ", total)
f = open(os.path.join(dir, "duration.txt"), "w")
f.write(str(total))
f.close()
