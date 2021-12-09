# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
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

from contextlib import redirect_stdout
from copy import copy
import os
import threading
import time
import traceback
from z3 import set_option

from flask import Flask, g, send_from_directory  # g is required for pyinstrument
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

from idp_engine import IDP
from idp_engine.utils import log, RUN_FILE

from idp_engine.Parse import TypeDeclaration
from .State import State
from .Inferences import explain, abstract, get_relevant_questions
from .IO import Output, metaJSON

from typing import Dict

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
idps: Dict[str, IDP] = {}  # {code_string : idp}


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
    Class which handles the run.
    <<Explanation of what the run is here.>>

    :arg Resource: <<explanation of resource>>
    """
    def post(self):
        """
        Method to run an IDP program with a procedure block.

        :returns stdout.
        """

        # allow pretty printing of large Z3 formula (see https://stackoverflow.com/a/19570420/474491)
        set_option(max_args=10000000, max_lines=1000000, max_depth=10000000, max_visited=1000000)

        log("start /run")
        with z3lock:
            try:
                start = time.process_time()
                if with_profiling:
                    g.profiler = Profiler()
                    g.profiler.start()

                parser = reqparse.RequestParser()
                parser.add_argument('code', type=str, help='Code')
                args = parser.parse_args()
                idp = idpOf(args['code'])
                # capture stdout, print()
                with open(RUN_FILE, mode='w', encoding='utf-8') as buf, redirect_stdout(buf):
                    try:
                        idp.execute()
                        print(f"\n> Executed in {round(time.process_time()-start, 3)} sec")
                    except Exception as exc:
                        print(exc)
                with open(RUN_FILE, mode='r', encoding='utf-8') as f:
                    out = f.read()
                os.remove(RUN_FILE)

                log("end /run ")
                if with_profiling:
                    g.profiler.stop()
                    print(g.profiler.output_text(unicode=True, color=True))
            except Exception as exc:
                if with_profiling:
                    g.profiler.stop()
                traceback.print_exc()
                out = str(exc)

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
        with z3lock:
            try:
                if with_profiling:
                    g.profiler = Profiler()
                    g.profiler.start()

                parser = reqparse.RequestParser()
                parser.add_argument('code', type=str, help='Code')
                args = parser.parse_args()
                idp = idpOf(args['code'])
                state = State.make(idp, "{}", "{}")
                if not state.idp.display.manualRelevance:
                    get_relevant_questions(state)
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
        with z3lock:
            try:
                if with_profiling:
                    g.profiler = Profiler()
                    g.profiler.start()

                parser = reqparse.RequestParser()
                parser.add_argument('method', type=str, help='Method to execute')
                parser.add_argument('code', type=str, help='Code')
                parser.add_argument('active', type=str, help='Three-valued structure')
                parser.add_argument('previous_active', type=str, help='Previous input by user')
                # parser.add_argument('expanded', type=str, action='append', help='list of expanded symbols')
                parser.add_argument('symbol', type=str, help='Symbol to explain or optimize')
                parser.add_argument('value', type=str, help='Value to explain')
                parser.add_argument('field', type=str, help='Applied Symbol whose range must be determined')
                parser.add_argument('minimize', type=bool, help='True -> minimize ; False -> maximize')
                parser.add_argument('with_relevance', type=bool, help='compute relevance if true')
                args = parser.parse_args()
                #print(args)
                # expanded = tuple([]) if args['expanded'] is None else tuple(args['expanded'])
                method = args['method']
                out = {}
                if method == "checkCode":
                    idpModel = IDP.from_str(args['code'])
                    if args['symbol'] != "":  # check only that sentence
                        newTheory = (str(idpModel.vocabulary)
                                     + "theory {\n"
                                     + args['symbol']
                                     + "\n}\n"
                                     )
                        idpModel = IDP.from_str(newTheory)
                    # remove enumerations of functions/predicates
                    for block in list(idpModel.theories.values()) + list(idpModel.structures.values()):
                        block.interpretations = {k:v
                            for k,v in block.interpretations.items()
                            if v.is_type_enumeration == True}
                    assert len(idpModel.theories) == 1 and len(idpModel.structures)<=1, \
                        "Can't check code containing more than 1 theory or structure."
                    state = State(idpModel)  # don't use cache.  May raise an error
                    next(state.expand(max=1, timeout=0))
                    out = {"result": "ok"}
                else:
                    state = State.make(idpOf(args['code']),
                                    args.get('previous_active', None),
                                    args['active'])

                    if not state.propagate_success:
                        out = explain(state)
                    elif method == "propagate":
                        if args.with_relevance:
                            get_relevant_questions(state)
                        out = Output(state).fill(state)
                    elif method == 'get_range':
                        out = state.get_range(args['field'])
                    elif method == 'relevance':
                        get_relevant_questions(state)
                        out = Output(state).fill(state)
                    elif method == "modelexpand":
                        generator = state.expand(max=1, timeout=0, complete=False)
                        out = copy(state)
                        out.assignments = out.assignments.copy(shallow=True)
                        out.assignments = list(generator)[0]
                        out = Output(out).fill(out)
                    elif method == "explain":
                        out = explain(state, args['value'])
                    elif method == "minimize":
                        out = copy(state)
                        out.assignments = out.assignments.copy(shallow=True)
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
