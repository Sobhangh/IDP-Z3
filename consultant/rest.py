"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

with_png = False

from contextlib import redirect_stdout
import io
import os
import threading
import traceback

from flask import Flask, send_from_directory, g
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from textx import TextXError

from Idp import Idp, idpparser
from Idp.utils import log
from .State import make_state
from .Inferences import *
from .IO import *

from typing import Dict

#pyinstrument from pyinstrument import Profiler
# library to generate call graph, for documentation purposes
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from pycallgraph2 import GlobbingFilter
from pycallgraph2 import Config
config = Config(max_depth=8)
config.trace_filter = GlobbingFilter(
    exclude=['arpeggio.*','ast.*','flask*', 'json.*', 'pycallgraph2.*', 'textx.*','werkzeug.*', 'z3.*']
    )


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.join(current_dir, os.pardir)

static_file_dir   = os.path.join(current_dir, 'static')
examples_file_dir = os.path.join(current_dir, 'examples')
docs_file_dir     = os.path.join(parent_dir , 'docs')
app = Flask(__name__)
CORS(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('method', type=str, help='Method to execute')
parser.add_argument('code', type=str, help='Code')
parser.add_argument('active', type=str, help='Three-valued structure')
parser.add_argument('expanded', type=str, action='append', help='list of expanded symbols')
parser.add_argument('symbol', type=str, help='Symbol to explain or optimize')
parser.add_argument('value', type=str, help='Value to explain')
parser.add_argument('minimize', type=bool, help='True -> minimize ; False -> maximize')


class HelloWorld(Resource):
    def get(self):
        import time
        time.sleep(100)
        return {'hello': 'world'}


z3lock = threading.Lock()
idps: Dict[str, Idp] = {} # {code_string : idp}


def idpOf(code):
    """
    Function to retrieve an Idp object for IDP code.
    If the object doesn't exist yet, we create it.
    `idps` is a dict which contains an Idp object for each IDP code.
    This way, easy caching can be achieved.

    :arg code: the IDP code.
    :returns Idp: the Idp object.
    """
    global idps
    if code in idps:
        return idps[code]
    else:
        idp = idpparser.model_from_str(code)
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
        log("start /run")
        with z3lock:
            try:
                args = parser.parse_args()
                try:
                    idp = idpOf(args['code'])
                    # capture stdout, print()
                    with io.StringIO() as buf, redirect_stdout(buf):
                        try:
                            idp.execute()
                        except Exception as exc:
                            print(exc)
                        out = buf.getvalue()
                    return out
                except Exception as exc:
                    traceback.print_exc()
                    return repr(exc)
            except Exception as exc:
                traceback.print_exc()
                return str(exc)


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
                args = parser.parse_args()
                try:
                    idp = idpOf(args['code'])
                    state = make_state(idp, "{}")
                    out = metaJSON(idp)
                    out["propagated"] = Output(state).fill(state)
                    return out
                except Exception as exc:
                    traceback.print_exc()
                    return repr(exc)
            except Exception as exc:
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
                #pyinstrument g.profiler = Profiler()
                #pyinstrument g.profiler.start()

                args = parser.parse_args()
                #print(args)

                idp = idpOf(args['code'])
                method = args['method']
                given_json = args['active']
                expanded = tuple([]) if args['expanded'] is None else tuple(args['expanded'])

                state = make_state(idp, given_json)

                out = {}
                if method == "propagate":
                    out = Output(state).fill(state)
                if method == "modelexpand":
                    generator = state.expand(max=1,complete=False, extended=True)
                    state.assignments = list(generator)[0]
                    out = Output(state).fill(state)
                if method == "explain":
                    out = explain(state, args['value'])
                if method == "minimize":
                    state = state.optimize(args['symbol'], args['minimize'],
                        complete=False, extended=True)
                    out = Output(state).fill(state)
                if method == "abstract":
                    if args['symbol'] != "": # theory to explain ?
                        newTheory = ( str(idpparser.model_from_str(args['code']).vocabulary)
                                    + "theory {\n"
                                    + args['symbol']
                                    + "\n}\n"
                        )
                        idpModel = idpparser.model_from_str(newTheory)
                        expanded = {}
                        # for expr in idpModel.subtences.values():
                        #     expanded.update(expr.unknown_symbols())
                        expanded = tuple(expanded.keys())
                        state = make_state(idpModel, "")
                    out = abstract(state, given_json)
                log("end /eval " + method)
                #pyinstrument g.profiler.stop()
                #pyinstrument print(g.profiler.output_text(unicode=True, color=True))
                return out
            except Exception as exc:
                #pyinstrument g.profiler.stop()
                traceback.print_exc()
                return str(exc)

class evalWithGraph(eval): # subcclass that generates call graphs
    def post(self):
        args = parser.parse_args()
        method = args['method']

        graphviz = GraphvizOutput()
        graphviz.output_file = 'docs/'+ method + '.png'
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
