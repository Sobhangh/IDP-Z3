import threading

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

from configcase import *

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


class eval(Resource):
    def post(self):
        z3lock.acquire()
        global _main_ctx
        _main_ctx = None

        args = parser.parse_args()
        
        global theory
        theory = None
        exec(args['code'])

        case = ConfigCase(theory)
        method = args['method']
        active = args['active']
        print(args)
        out = {}
        if method == "init":
            out = case.initialisationlist()
        if method == "propagate":
            case.loadStructureFromJson(active)
            out = case.propagation()
        if method == "modelexpand":
            case.loadStructureFromJson(active)
            out = case.json_model()
        if method == "relevance":
            case.loadStructureFromJson(active)
            out = case.relevance()
        if method == "explain":
            case.loadStructureFromJson(active)
            out = case.explain(args['symbol'], args['value'])
        if method == "minimize":
            case.loadStructureFromJson(active)
            out = case.minimize(args['symbol'], args['minimize'])
        z3lock.release()
        print(out)
        return out


class meta(Resource):
    def post(self):
        args = parser.parse_args()
        exec(args['code'])
        global theory
        return ConfigCase(theory).metaJSON()


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
