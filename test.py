"""
A testing file for the IDP-Z3 project.
This file includes three tests:
    * generate
    * pipeline
    * api

The generation test creates a idp-z3 file for every .idp file in the tests
directory. These files can be used to manually verify if everything is still in
order.

The pipeline test will run model expansion and propagation for every .ipd file
in the tests directory. It records the output of these operations, which is
also printed at the end. If during this any file returns with an error, the
test will exit with code 1, so that it can be used in an automated testing
pipeline.

The api test will call the idp-engine API.

By default, the generate and api tests are run.

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

from idp_web_server.State import State
from idp_web_server.IO import Output, metaJSON
from idp_engine import IDP, Theory, model_expand, Status as S
from idp_engine.utils import (start, log, NEWL, RUN_FILE,
                              redirect_stdout, redirect_stderr_to_stdout)

z3lock = threading.Lock()


def generateZ3(theory):
    """
    Returns a string containing the theory and the initial API responses
    (/meta and /eval propagation).
    Also try to expand the theory and report error.
    """

    # capture stdout, print()
    with open(RUN_FILE, mode='w', encoding='utf-8') as buf, \
        redirect_stdout(to=buf), redirect_stderr_to_stdout():
        try:
            idp = IDP.from_str(theory)
            if 'main' in idp.procedures:
                idp.execute()
            else:
                state = State(idp)
                state.propagate()
                state.determine_relevance()
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
    with open(RUN_FILE, mode='r', encoding='utf-8') as f:
        return f.read()
    os.remove(RUN_FILE)



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

            # stabilize the output
            if 'minimize.idp' in file:
                output = re.sub(r'^f :=.*\n?', '', output, flags=re.MULTILINE)

            # Remove absolute paths from output.
            output = re.sub(r'(/.*)(?=site-packages/)', '', output, flags=re.MULTILINE)
            output = re.sub(r'(/.*)(?=IDP-Z3/)', '', output, flags=re.MULTILINE)
            # output = re.sub(r'(/.*)(?=web-IDP-Z3/)', '', output, flags=re.MULTILINE)

            # remove the folder
            output = re.sub(r'site-packages/', '', output, flags=re.MULTILINE)
            output = re.sub(r'IDP-Z3/', '', output, flags=re.MULTILINE)
            # output = re.sub(r'web-IDP-Z3/', '', output, flags=re.MULTILINE)

            # remove line numbers in error messages
            output = re.sub(r'line \d+,', 'line ??,', output, flags=re.MULTILINE)

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
            if '.error' not in file_name:
                try:
                    log(f"start /eval {file_name}")
                    with open(file_name, "r") as fp:

                        idp = IDP.from_str(fp.read())

                        if idp.procedures == {}:
                            state = State.make(idp, "{}", "{}", "[]")
                            state.determine_relevance()
                            generator = state.expand(max=1,complete=False)
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

def api():
    # capture stdout, print()
    error = 0
    with open(RUN_FILE, mode='w', encoding='utf-8') as buf, \
        redirect_stdout(to=buf), redirect_stderr_to_stdout():
        try:
            test = """
                vocabulary {
                    p, q : () → 𝔹
                }

                theory {
                    p() => q().
                }
                structure {}

                procedure main() {
                    print("ok")
                }
            """
            kb = IDP.from_str(test)
            T, S1 = kb.get_blocks("T, S")
            kb.execute()
            for model in model_expand(T,S1,sort=True,complete=True):
                print(model)
                print()
            problem = Theory(T)
            problem.assert_("p()", True, S.GIVEN)
            print(problem.propagate().assignments)
        except Exception as exc:
            print(traceback.format_exc())
            error = 1
    with open(RUN_FILE, mode='r', encoding='utf-8') as f:
        output = f.read()
    os.remove(RUN_FILE)
    with open(os.path.join("./tests/api.z3"), "w") as fp:
        fp.write(output)
    return error


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the tests')
    parser.add_argument('TEST', nargs='*', default=["generate", "api"])
    args = parser.parse_args()

    error, g_error, p_error, a_error = 0, 0, 0, 0
    if "generate" in args.TEST:
        g_error = generate()
        error = g_error
    if "pipeline" in args.TEST:
        p_error = pipeline()
        error = max(error, p_error)
    if "api" in args.TEST:
        a_error = api()
        error = max(error, a_error)

    print(f'G: {g_error}, P: {p_error}, A: {a_error}')
    sys.exit(error)
