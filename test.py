"""
A testing file for the IDP-Z3 project.
This file includes two tests:
    * generate
    * pipeline

The generation test creates a idp-z3 file for every .idp file in the tests
directory. These files can be used to manually verify if everything is still in
order.

The pipeline test will run model expansion and propagation for every .ipd file
in the tests directory. It records the output of these operations, which is
also printed at the end. If during this any file returns with an error, the
test will exit with code 1, so that it can be used in an automated testing
pipeline.

By default, the generate test is run.

Authors: Pierre Carbonelle, Simon Vandevelde
"""
import argparse
from contextlib import redirect_stdout
import glob
import io
import os
import pprint
import sys
import threading
import time
import traceback
from typing import Dict

# import pyximport; 
# pyximport.install(language_level=3)

from consultant.Case import Case
from consultant.Inferences import propagation, expand
from consultant.IO import metaJSON
from Idp import idpparser, SymbolDeclaration, NEWL
from Idp.utils import start, log
from consultant.Case import make_case

z3lock = threading.Lock()


def generateZ3(theory):
    """
    Returns a string containing the theory and the initial API responses
    (/meta and /eval propagation).
    Also try to expand the theory and report error.
    """

    idp = idpparser.model_from_str(theory)
    if 'main' in idp.procedures:
        # capture stdout, print()
        with io.StringIO() as buf, redirect_stdout(buf):
            try:
                idp.execute()
            except Exception as exc:
                print(traceback.format_exc())
            return buf.getvalue()

    expanded_symbols: Dict[str, SymbolDeclaration] = {}
    for expr in idp.subtences.values():
        expanded_symbols.update(expr.unknown_symbols())
    expanded_symbols2 = list(expanded_symbols.keys())
    case = Case(idp, expanded_symbols2)

    output = (
        f"{NEWL}-- original ---------------------------------{NEWL}"
        f"{theory}"
        f"{NEWL}-- meta -------------------------------------{NEWL}"
        f"{pprint.pformat(metaJSON(case.idp), width=120)}{NEWL}"
        f"{NEWL}-- propagation ------------------------------{NEWL}"
        f"{pprint.pformat(propagation(case), width=120)}{NEWL}"

        #additional debug info (optional)
        # f"{NEWL}-- vocabulary -------------------------------{NEWL}"
        # f"{NEWL.join(str(t) for t in case.idp.vocabulary.translated)}"
        # f"{NEWL}-- theory -----------------------------------{NEWL}"
        # f"{(NEWL+NEWL).join(str(t) for t in case.idp.theory.translate(case.idp))}{NEWL}"
        # f"{NEWL}-- goal -----------------------------------{NEWL}"
        # f"{str(case.idp.goal.translate())}{NEWL}"
        # f"{NEWL}-- subtences ------------------------------------{NEWL}"
        # f"{NEWL.join(str(t) for t in case.idp.subtences)}{NEWL}"
        # f"{NEWL}-- assignments ------------------------------------{NEWL}"
        # f"{NEWL.join(str(t) for t in case.assignments)}{NEWL}"
        # f"{NEWL}-- case -------------------------------------{NEWL}"
        # f"{str(case)}{NEWL}"
        )
    # try:
    #     expand(case)
    # except Exception as exc:
    #     output += f"{NEWL}error in expansion{NEWL}{str(exc)}"
    return output


def generate():
    # optional patch Log on Idp.Substitute ####################################

    # for i in [Expression, AppliedSymbol, Variable, Fresh_Variable]:
    #     i.substitute = log_calls(i.substitute)

    ###########################################################################

    dir = os.path.dirname(__file__)
    dir = os.path.join(dir, "tests")
    files = glob.glob("./tests/*/*.idp")
    files.sort()
    out_dict, error = {}, 0
    for file in files:
        print(file)
        # Log_file(file) # optional
        f = open(file, "r")
        theory = f.read()
        output = generateZ3(theory)

        z3 = file.replace(".z3", ".z3z3")
        z3 = z3.replace(".idp", ".z3")
        if os.path.isfile(z3):
            f = open(z3, "r")
            if output != f.read():
                out_dict[file] = "**** unexpected result !"
                error = 1
            f.close()

        f = open(z3, "w")
        f.write(output)
        f.close()

    total = round(time.process_time()-start, 3)
    print("*** Total: ", total)

    f = open(os.path.join(dir, "duration.txt"), "w")
    f.write(str(total))
    f.close()

    if out_dict:
        for k, v in out_dict.items():
            print("{: >60} {: >20}".format(k, v))
    else:
        print("All is ok !")
    return error


def pipeline():
    """
    Tries to model expand and propagate every .idp file in the tests directory.
    If any error is thrown, we exit at the end with code 1.
    This way, it can be used in a testing pipeline, as explained in
    https://docs.gitlab.com/ee/ci/
    """
    test_files = glob.glob("./tests/*/*.idp")
    out_dict = {}
    error = 0
    with z3lock:
        for file_name in test_files:
            try:
                log("start /eval")
                with open(file_name, "r") as fp:

                    idp = idpparser.model_from_str(fp.read())
                    given_json = ""

                    case = make_case(idp, given_json, tuple([]))

                    expand(case)
                    propagation(case)
                    log("end /eval ")
                    out_dict[file_name] = "Works."
            except Exception as exc:
                error = 1
                out_dict[file_name] = str(exc)
                log("end /eval ")

    for k, v in out_dict.items():
        print("{: >60} {: >20}".format(k, v))
    return error


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the tests')
    parser.add_argument('TEST', nargs='*', default=["generate"])
    args = parser.parse_args()

    error = 0
    if "generate" in args.TEST:
        error = generate()
    if "pipeline" in args.TEST:
        p_error = pipeline()
        error = max(error, p_error)

    sys.exit(error)
