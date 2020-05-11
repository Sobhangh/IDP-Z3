
import os,sys,inspect,time, pprint

# add parent folder to import path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,os.path.join(parentdir, 'Idp'))

from Case import Case
from Inferences import *
from Solver import *
from debugWithYamlLog import log, Log, start, Log_file, nl
from Idp import idpparser, SymbolDeclaration
from Idp.Expression import Expression, AppliedSymbol, Variable, Fresh_Variable

from typing import Dict, Any

# patch Log on Idp.Substitute ##############################################################

indent = 0
def log(function):
    def _wrapper(*args, **kwds):
        global indent
        self = args[0]
        e0   = args[1]
        e1   = args[2]
        Log( f"{nl}|------------"
             f"{nl}|{'*' if self.is_subtence else ''}{self.str}"
             f"{' with '+','.join(e.__class__.__name__ for e in self.sub_exprs) if self.sub_exprs else ''}"
             f"{f' just {self.just_branch.str}' if self.just_branch else ''}"
             f"{nl}|+ {e0.code} -> {e1.code}{f'  (or {e0.str} -> {e1.str})' if e0.code!=e0.str or e1.code!=e1.str else ''}"
             , indent)
        indent +=4
        out = function(*args, *kwds)
        indent -=4
        Log( f"{nl}|== {'*' if out.is_subtence else ''}"
             f"{'!'+out.value.str if out.value is not None else '!!'+out.simpler.str if out.simpler is not None else out.str}"
             f"{' with '+','.join(e.__class__.__name__ for e in out.sub_exprs) if out.sub_exprs else ''}"
             f"{f' just {out.just_branch.str}' if out.just_branch else ''}"
          , indent )
        return out    
    return _wrapper

Expression    .substitute = log(Expression.substitute)
AppliedSymbol .substitute = log(AppliedSymbol.substitute)
Variable      .substitute = log(Variable.substitute)
Fresh_Variable.substitute = log(Fresh_Variable.substitute)

###########################################################################################

dir = os.path.dirname(__file__)
files  = [os.path.join(dir, "1 sandbox/sandbox.idp")]
files += [x[0]+"/"+f for x in os.walk(dir) for f in x[2] if f.endswith(".idp")]
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
    f.write("\r\n\r\n".join(str(t) for t in case.idp.theory.translate(case.idp))     + "\r\n")
    if case.idp.goal.translate() is not None:
        f.write("\r\n-- goal -----------------------------------\r\n")
        f.write(str(case.idp.goal.translate())     + "\r\n")
    f.write("\r\n-- subtences ------------------------------------\r\n")
    f.write("\r\n".join(str(t) for t in case.idp.subtences)     + "\r\n")
    f.write("\r\n-- GUILines ------------------------------------\r\n")
    f.write("\r\n".join(str(t) for t in case.GUILines)     + "\r\n")

    f.write("\r\n-- case -------------------------------------\r\n")
    f.write(str(case)+ "\r\n")
    f.write("\r\n-- meta -------------------------------------\r\n")
    out = pprint.pformat(metaJSON(case.idp), width = 120)
    f.write(out     + "\r\n")
    f.write("\r\n-- propagation ------------------------------\r\n")
    out = pprint.pformat(propagation(case), width = 120)
    f.write(out     + "\r\n")

    f.close()
    print("----------------")

total = round(time.process_time()-start,3)
print("*** Total: ", total)
f = open(os.path.join(dir, "duration.txt"), "w")
f.write(str(total))
f.close()