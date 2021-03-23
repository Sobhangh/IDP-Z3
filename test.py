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
try:
    import snoop # for debugging
    snoop.install()
except:
    pass

import argparse
from contextlib import redirect_stdout
import glob
import io
import os
import pprint
import pretty_errors
import sys
import threading
import time
import traceback
import re

# import pyximport;
# pyximport.install(language_level=3)

from idp_server.State import State, make_state
from idp_server.IO import Output, metaJSON
from idp_engine import IDP, Problem, model_expand
from idp_engine.Parse import idpparser
from idp_engine.utils import start, log, NEWL

z3lock = threading.Lock()


def generateZ3(theory):
    """
    Returns a string containing the theory and the initial API responses
    (/meta and /eval propagation).
    Also try to expand the theory and report error.
    """

    # capture stdout, print()
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            idp = idpparser.model_from_str(theory)
            if 'main' in idp.procedures:
                idp.execute()
            else:
                state = State(idp)
                out = Output(state).fill(state)

                print(
                    f"{NEWL}-- original ---------------------------------{NEWL}"
                    f"{theory}"
                    f"{NEWL}-- meta -------------------------------------{NEWL}"
                    f"{pprint.pformat(metaJSON(state), width=120)}{NEWL}"
                    f"{NEWL}-- propagation ------------------------------{NEWL}"
                    f"{pprint.pformat(out, width=120)}{NEWL}",
                    end ="")
        except Exception as exc:
            print(traceback.format_exc())
        return buf.getvalue()



def generate():
    # optional patch Log on idp_engine.Interpret  ####################################

    # for i in [Expression, AppliedSymbol, Variable]:
    #     i.substitute = log_calls(i.substitute)

    ###########################################################################

    dir = os.path.dirname(__file__)
    dir = os.path.join(dir, "tests")
    files = glob.glob("./tests/*/*.idp")
    files.sort()
    out_dict, error = {}, 0
    for file in files:
        if r"ignore" not in file:
            print(file)
            # Log_file(file) # optional
            f = open(file, "r")
            theory = f.read()
            output = generateZ3(theory)

            # Remove absolute paths from output.
            output = re.sub(r'(/.*)(?=IDP-Z3/)', '', output)
            output = re.sub(r'(/.*)(?=web-IDP-Z3/)', '', output)

            z3 = file.replace(".z3", ".z3z3")
            z3 = z3.replace(".idp", ".z*")
            ok = False
            for result in glob.glob(z3):
                f = open(result, "r")
                if output == f.read():
                    ok = True
                    break
                f.close()
            if not ok:
                out_dict[file] = "**** unexpected result !"
                error = 1

                f = open(z3.replace(".z*", ".z3"), "w")
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
            # avoid files meant to raise an error
            if file_name not in ['./tests/1 procedures/ok.idp',
                './tests/1 procedures/is_enumerated 2.idp',
                './tests/5 polygon/Sides3.idp',
                './tests/9 DMN1.ignore/disjoint.idp',
                './tests/9 DMN1.ignore/nondeterministic.idp',
                './tests/9 DMN1.ignore/middle.idp',]:
                try:
                    log(f"start /eval {file_name}")
                    with open(file_name, "r") as fp:

                        idp = idpparser.model_from_str(fp.read())
                        given_json = ""

                        if idp.procedures == {}:
                            state = make_state(idp, given_json)
                            generator = state.expand(max=1,complete=False, extended=True)
                            list(generator)[0]  # ignore result
                            out = Output(state).fill(state)
                        else:
                            idp.execute()
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

    test = """
vocabulary {
    p : () → 𝔹
}

theory {
    p().
}
structure {}

procedure main() {
    print("ok")
}
"""
    kb = IDP.parse(test)
    T, S = kb.get_blocks("T, S")
    kb.execute()
    for model in model_expand(T,S):
        print(model)

    error = 0
    if "generate" in args.TEST:
        error = generate()
    if "pipeline" in args.TEST:
        p_error = pipeline()
        error = max(error, p_error)

    sys.exit(error)
