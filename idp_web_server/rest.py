# Copyright 2019-2023 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of IDP-Z3.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module implements the IDP-Z3 web server

To profile it, set with_profiling to True
"""

with_png = False
with_profiling = False

try:
    import snoop # for debugging
    snoop.install()
except:
    pass

from copy import copy
import os
import threading
import time
import traceback
import urllib.parse
from z3 import set_option

from flask import Flask, g, send_from_directory, request  # g is required for pyinstrument
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

from idp_engine import IDP
from idp_engine.utils import log, RUN_FILE

from idp_engine.Assignments import Status as S, str_to_IDP
from idp_engine.Expression import EQUALS
from .State import State
from .Inferences import explain, abstract
from .IO import Output, metaJSON
from .htmx import stateX, valuesX, explainX, wrap, render

import re

from folint.folint.SCA import lint_fo

if with_profiling:
    from pyinstrument import Profiler

if with_png:
    # library to generate call graph, for documentation purposes
    from pycallgraph2 import PyCallGraph
    from pycallgraph2.output import GraphvizOutput
    from pycallgraph2 import GlobbingFilter
    from pycallgraph2 import Config
    config = Config(max_depth=8)
    config.trace_filter = GlobbingFilter(
        exclude=['arpeggio.*', 'ast.*', 'flask*', 'json.*', 'pycallgraph2.*',
                'textx.*', 'werkzeug.*', 'z3.*']
        )


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.join(current_dir, os.pardir)

static_file_dir = os.path.join(current_dir, 'static')
examples_file_dir = os.path.join(current_dir, 'examples')
docs_file_dir = os.path.join(parent_dir, 'docs')
app = Flask(__name__)
CORS(app)

api = Api(app)


class HelloWorld(Resource):
    def get(self):
        import time
        time.sleep(100)
        return {'hello': 'world'}


z3lock = threading.Lock()
idps: "dict[str, IDP]" = {}  # {code_string : idp}


def idpOf(code):
    """
    Function to retrieve an IDP object for IDP code.
    If the object doesn't exist yet, we create it.
    `idps` is a dict which contains an IDP object for each IDP code.
    This way, easy caching can be achieved.

    :arg code: the IDP code.
    :returns IDP: the IDP object.
    """
    global idps
    if code in idps:
        return idps[code]
    else:
        idp = IDP.from_str(code)
        if 20 < len(idps):
            # remove oldest entry, to prevent memory overflow
            idps = {k: v for k, v in list(idps.items())[1:]}
        idps[code] = idp
        return idp


class run(Resource):
    """
    Handler for Web IDE
    """
    def post(self):
        """
        Method to run an IDP program with a procedure block.

        :returns stdout.
        """

        # allow pretty printing of large Z3 formula (see https://stackoverflow.com/a/19570420/474491)
        set_option(max_args=10000000, max_lines=1000000, max_depth=10000000, max_visited=1000000)

        log("start /run")
        with z3lock:  # don't remove it, or take care of the side-effect of timeout_seconds (in expand()) on other threads
            out = []  # list of printed lines
            try:
                start = time.process_time()
                if with_profiling:
                    g.profiler = Profiler()
                    g.profiler.start()

                parser = reqparse.RequestParser()
                parser.add_argument('code', type=str, help='Code')
                args = parser.parse_args()
                idp = idpOf(args['code'])
                try:
                    prints = idp.execute(capture_print=True)
                    if prints is not None:
                        out.append(prints[:-len(os.linesep)])  # drop last \n
                    out.append(f"\n> Executed in {round(time.process_time()-start, 3)} sec")
                except Exception as exc:
                    out.append(str(exc))

                log("end /run ")
                if with_profiling:
                    g.profiler.stop()
                    out.append(g.profiler.output_text(unicode=True, color=True))
            except Exception as exc:
                if with_profiling:
                    g.profiler.stop()
                traceback.print_exc()
                out.append(str(exc))
            out = os.linesep.join(out) + os.linesep

        # restore defaults in https://github.com/Z3Prover/z3/blob/master/src/api/python/z3/z3printer.py
        set_option(max_args=128, max_lines=200,
                   max_depth=20, max_visited=10000)
        return out


class meta(Resource):
    """
    Class which handles the meta.
    <<Explanation of what the meta is here.>>

    :arg Resource: <<explanation of resource>>
    """
    def post(self):
        """
        Method to export the metaJSON from the resource.

        :returns metaJSON: a json string containing the meta.
        """
        log("start /meta")
        with z3lock:  # don't remove it, or take care of the side-effect of timeout_seconds (in expand()) on other threads
            try:
                if with_profiling:
                    g.profiler = Profiler()
                    g.profiler.start()

                parser = reqparse.RequestParser()
                parser.add_argument('code', type=str, help='Code')
                args = parser.parse_args()
                idp = idpOf(args['code'])
                state = State.make(idp, "{}", "{}", "[]")
                # ensure the stateful solvers are initialized
                _ = state.solver
                _ = state.optimize_solver
                _ = state.solver_reified
                _ = state.optimize_solver_reified
                if not state.idp.display.manualRelevance:
                    state.determine_relevance()
                out = metaJSON(state)
                out["valueinfo"] = Output(state).fill(state)

                log("end /meta ")
                if with_profiling:
                    g.profiler.stop()
                    print(g.profiler.output_text(unicode=True, color=True))
                return out
            except Exception as exc:
                if with_profiling:
                    g.profiler.stop()
                traceback.print_exc()
                return str(exc)


class metaWithGraph(meta):  # subclass that generates call graphs
    def post(self):
        graphviz = GraphvizOutput()
        graphviz.output_file = 'docs/meta.png'
        with PyCallGraph(output=graphviz, config=config):
            return super().post()


class eval(Resource):
    def post(self):
        log("start /eval")
        with z3lock:  # don't remove it, or take care of the side-effect of timeout_seconds (in expand()) on other threads
            try:
                if with_profiling:
                    g.profiler = Profiler()
                    g.profiler.start()

                parser = reqparse.RequestParser()
                parser.add_argument('method', type=str, help='Method to execute')
                parser.add_argument('code', type=str, help='Code')
                parser.add_argument('active', type=str, help='Three-valued structure')
                parser.add_argument('previous_active', type=str, help='Previously propagated assignment')
                parser.add_argument('ignore', type=str, help='User-disabled laws to ignore')
                parser.add_argument('symbol', type=str, help='Symbol to explain or optimize')
                parser.add_argument('value', type=str, help='Value to explain')
                parser.add_argument('field', type=str, help='Applied Symbol whose range must be determined')
                parser.add_argument('minimize', type=bool, help='True -> minimize ; False -> maximize')
                parser.add_argument('with_relevance', type=bool, help='compute relevance if true')
                args = parser.parse_args()
                method = args['method']
                out = {}

                if method == "lint":
                    # Run FOLint, the FO(.) linter.
                    lint = lint_fo(args['code'])

                    # Match all the errors and format them in a nice dict.
                    msgs = re.findall(r'(Warning|Error): line (\d+) - colStart (\d+) - colEnd (\d+) => (.*)', lint)
                    errors = []
                    for msg in msgs:
                        error = {'type': msg[0],
                                 'line': msg[1],
                                 'colStart': msg[2],
                                 'colEnd': msg[3],
                                 'details': msg[4]
                                 }
                        errors.append(error)
                    out = errors
                elif method == "getEnglish":
                    idpModel = IDP.from_str(args['code'])
                    if args['symbol'] != "":  # check only that sentence
                        voc = (idpModel.vocabularies['decision'] if len(idpModel.theories) == 2 else
                               idpModel.vocabulary)
                        newTheory = (str(voc)
                                     + "theory {\n"
                                     + args['symbol']
                                     + "\n}\n"
                                     )
                        idpModel = IDP.from_str(newTheory)
                    out = {'EN': idpModel.EN()}
                else:
                    state = State.make(idpOf(args['code']),
                                       args['previous_active'],
                                       args['active'],
                                       args['ignore']
                                       )

                    if not state.satisfied:
                        out = explain(state)
                    elif method == "propagate":
                        if args.with_relevance:
                            state.determine_relevance()
                        out = Output(state).fill(state)
                    elif method == 'get_range':
                        out = state.get_range(args['field'])
                    elif method == 'relevance':
                        state.determine_relevance()
                        out = Output(state).fill(state)
                    elif method == "modelexpand":
                        generator = state.expand(max=1, timeout_seconds=0, complete=False)
                        # TODO: this copying is not needed?
                        out = copy(state)
                        out.assignments = copy(out.assignments)
                        out.assignments = list(generator)[0]
                        out = Output(out).fill(out)
                    elif method == "explain":
                        out = explain(state, args['value'])
                    elif method == "minimize":
                        # TODO: this copying is not needed?
                        out = copy(state)
                        out.assignments = copy(out.assignments)
                        out = out.optimize(args['symbol'], args['minimize'])
                        out = Output(out).fill(out)
                    elif method == "abstract":
                        out = abstract(state, args['active'])
                log("end /eval " + method)
                if with_profiling:
                    g.profiler.stop()
                    print(g.profiler.output_text(unicode=True, color=True))
                return out
            except Exception as exc:
                if with_profiling:
                    g.profiler.stop()
                traceback.print_exc()
                return f"{type(exc).__name__}: {exc}"


class evalWithGraph(eval):  # subcclass that generates call graphs
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('method', type=str, help='Method to execute')
        args = parser.parse_args()
        method = args['method']

        graphviz = GraphvizOutput()
        graphviz.output_file = 'docs/' + method + '.png'
        with PyCallGraph(output=graphviz, config=config):
            return super().post()


@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/IDE', methods=['GET'])
def serve_IDE():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)


@app.route('/examples/<path:path>', methods=['GET'])
def serve_examples_file(path):
    if not os.path.isfile(os.path.join(examples_file_dir, path)):
        return "file not found: " + path

    return send_from_directory(examples_file_dir, path)


# local help files
@app.route('/docs/<path:path>', methods=['GET'])
def serve_docs_file(path):
    if not os.path.isfile(os.path.join(docs_file_dir, path)):
        return "file not found: " + path

    return send_from_directory(docs_file_dir, path)


@app.route('/htmx', methods=['GET'])
def serve_htmx():
    """ returns the mobile welcome page """
    return send_from_directory(static_file_dir, 'htmx.html')


def get_idp(path):
    path = os.path.join(examples_file_dir, path)
    with open(path, mode='r', encoding='utf-8') as f:
        code = f.read()
    idp = idpOf(code)
    if 'default' in idp.structures:  # ignore defaults
        del idp.structures['default']
    return idp


@app.route('/htmx/file/open/<path:path>', methods=['GET'])
def file_open(path):
    """ returns a Single Page Application with FO(.) theory at `path` """
    idp = get_idp(path)
    state = State.make(idp, "{}", "{}", "[]")

    return wrap(static_file_dir, stateX(state))


def get_state(request):
    referer = request.headers.get('Referer')
    path = referer[referer.index('file/open/') + 10:]
    idp = get_idp(path)
    state = State.make(idp, "{}", "{}", "[]")
    for k, v in request.form.items():
        if "=" in k:
            terms = k.split(" = ")
            if v == "true":
                k, v = terms[0], terms[1]
            else:  # (k1=v1) = false --> create an entry for (k1=v1)
                k1, v1 = terms[0], terms[1]
                expr = state.assignments[k1].sentence
                val = str_to_IDP(v1, expr.type)
                expr = EQUALS([expr, val])
                state.assignments.assert__(expr, None, None)

        if v:
            sentence = state.assignments[k].sentence
            value = str_to_IDP(v, sentence.type)
            state.assert_(k, value)
            if state.environment and k in state.environment.assignments:
                state.environment.assert_(k, value)
    return state

@app.route('/htmx/state/post', methods=['POST'])
def state_post():
    state = get_state(request)

    # perform propagation
    if state.environment is not None:  # if there is a decision vocabulary
        state.environment.propagate(tag=S.ENV_CONSQ)
        state.assignments.update(state.environment.assignments)
        state._formula = None
    state.propagate(tag=S.CONSEQUENCE)
    state.determine_relevance()
    return stateX(state, update=True)

@app.route('/htmx/state/explain', methods=['POST'])
def state_explain():
    state = get_state(request)
    _ = state.solver_reified

    sentence, value = list(request.args.items())[0]
    if value == "true":
        pass
    elif value == "false":
        sentence = "~" + sentence
    else:
        # create an entry in state.assignments if it does not occur in the theory
        if sentence + " = " + value not in state.assignments:
            expr = state.assignments[sentence].sentence
            val = str_to_IDP(value, expr.type)
            to_explain = EQUALS([expr, val])
            state.assignments.assert__(to_explain, None, None)
        sentence = sentence + " = " + value

    (facts, laws) = state.explain(sentence)

    return render(explainX(state, facts, laws))

@app.route('/htmx/state/values', methods=['POST'])
def state_values():
    state = get_state(request)
    sentence, index = list(request.args.items())[0]
    state2 = state.copy()
    values = state2.get_range(sentence)

    return render(valuesX(state, sentence, values, index))

api.add_resource(HelloWorld, '/test')
if with_png:
    api.add_resource(metaWithGraph, '/meta')
    api.add_resource(evalWithGraph, '/eval')
else:
    api.add_resource(run,  '/run')
    api.add_resource(meta, '/meta')
    api.add_resource(eval, '/eval')

if __name__ == '__main__':
    app.run(debug=True)
