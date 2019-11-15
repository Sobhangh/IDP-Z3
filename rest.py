"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""

import threading
import traceback

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from textx import TextXError

from Inferences import *
from LiteralQ import *
from Idp import idpparser

# library to generate call graph, for documentation purposes
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from pycallgraph2 import GlobbingFilter
from pycallgraph2 import Config
config = Config(max_depth=8)
config.trace_filter = GlobbingFilter(
    exclude=['arpeggio.*','ast.*','flask*', 'json.*', 'pycallgraph2.*', 'textx.*','werkzeug.*', 'z3.*']
    )


static_file_dir   = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
examples_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples')
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
        return {'hello': 'world'}


z3lock = threading.Lock()
cases = {} #{code_string : ConfigCase}

def caseOf(code):
    global cases
    if code in cases:
        return cases[code]
    else:
        idpModel = idpparser.model_from_str(code)
        case = ConfigCase(idpModel)
        if 20<len(cases):
            del cases[0] # remove oldest entry, to prevent memory overflow
        cases[code] = case
        return case

class eval(Resource):
    def post(self):
        global cases
        log("start /eval")
        with z3lock:
            try:
                args = parser.parse_args()
                #print(args)

                case = caseOf(args['code'])

                method = args['method']
                struct_json = args['active']
                case.structure = loadStructure(case.idp, struct_json)

                out = {}
                if method == "propagate":
                    out = case.propagation(args['expanded'])
                if method == "modelexpand":
                    out = case.expand()
                if method == "relevance":
                    out = case.propagation(args['expanded']) #TODO
                if method == "explain":
                    out = case.explain(args['symbol'], args['value'])
                if method == "minimize":
                    out = case.optimize(args['symbol'], args['minimize'])
                if method == "abstract":
                    if args['symbol'] != "": # theory to explain ?
                        newTheory = ( str(idpparser.model_from_str(args['code']).vocabulary)
                                    + "theory {\n"
                                    + args['symbol']
                                    + "\n}"
                        )
                        idpModel = idpparser.model_from_str(newTheory)
                        case = ConfigCase(idpModel)
                    out = case.abstract()
                log("end /eval " + method)
                return out
            except Exception as exc:
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

class meta(Resource):
    def post(self):
        global cases
        log("start /meta")
        with z3lock:
            try:
                args = parser.parse_args()
                try:
                    case = caseOf(args['code'])
                    return case.metaJSON()
                except Exception as exc:
                    traceback.print_exc()
                    return repr(exc)
            except Exception as exc:
                traceback.print_exc()
                return str(exc)

class metaWithGraph(meta): # subclass that generates call graphs
    def post(self):
        graphviz = GraphvizOutput()
        graphviz.output_file = 'docs/meta.png'
        with PyCallGraph(output=graphviz, config=config):
            return super().post()


@app.route('/', methods=['GET'])
def serve_dir_directory_index():
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


api.add_resource(HelloWorld, '/test')
api.add_resource(eval, '/eval') # use evalWithGraph instead of eval, to generate call graphs.
api.add_resource(meta, '/meta')

if __name__ == '__main__':
    app.run(debug=True)
