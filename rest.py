import threading
import traceback

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from textx import TextXError

from configcase import *
from dsl.DSLClasses import idpparser

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
app = Flask(__name__)
CORS(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('method', type=str, help='Method to execute')
parser.add_argument('code', type=str, help='Code')
parser.add_argument('active', type=str, help='Three-valued structure')
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
        case = ConfigCase(idpModel.translate)
        if 20<len(cases):
            del cases[0] # remove oldest entry, to prevent memory overflow
        cases[code] = case
        return case

class eval(Resource):
    def post(self):
        global cases
        with z3lock:
            try:
                args = parser.parse_args()

                case = caseOf(args['code'])

                method = args['method']
                active = args['active']
                #print(args)
                out = {}
                if method == "init":
                    out = case.atomsGrouped()
                if method == "propagate":
                    case.loadStructureFromJson(active)
                    out = case.propagation()
                if method == "modelexpand":
                    case.loadStructureFromJson(active)
                    out = case.expand()
                if method == "relevance":
                    case.loadStructureFromJson(active)
                    out = case.propagation() #TODO
                if method == "explain":
                    case.loadStructureFromJson(active)
                    out = case.explain(args['symbol'], args['value'])
                if method == "minimize":
                    case.loadStructureFromJson(active)
                    out = case.optimize(args['symbol'], args['minimize'])
                if method == "abstract":
                    if args['symbol'] != "": # theory to explain ?
                        newTheory = ( str(idpModel.vocabulary)
                                    + "theory {\n"
                                    + args['symbol']
                                    + "\n}"
                        )
                        idpModel = idpparser.model_from_str(newTheory)
                        case = ConfigCase(idpModel.translate)
                    case.loadStructureFromJson(active)
                    out = case.abstract()
                return out
            except Exception as exc:
                return str(exc)

class meta(Resource):
    def post(self):
        global cases
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
                return str(exc)


@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)


api.add_resource(HelloWorld, '/test')
api.add_resource(eval, '/eval')
api.add_resource(meta, '/meta')

if __name__ == '__main__':
    app.run(debug=True)
