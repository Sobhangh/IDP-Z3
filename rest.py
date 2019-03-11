import threading
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

from configcase import ConfigCase
from example import theory

app = Flask(__name__)
CORS(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('method', type=str, help='Method to execute')
parser.add_argument('active', type=str, help='Three-valued structure')
parser.add_argument('symbol', type=str, help='Symbol to explain')
parser.add_argument('value', type=str, help='Value to explain')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


z3lock = threading.Lock()


class eval(Resource):
    def post(self):
        z3lock.acquire()
        global _main_ctx
        _main_ctx = None

        case = ConfigCase(theory)
        args = parser.parse_args()
        method = args['method']
        active = args['active']
        print(method, active)
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
            out = case.outputstructure(True, True).m
        if method == "explain":
            case.loadStructureFromJson(active)
            out = case.explain(args['symbol'], args['value'])

        z3lock.release()
        print(out)
        return out


class meta(Resource):
    def get(self):
        return ConfigCase(theory).metaJSON()


api.add_resource(HelloWorld, '/test')
api.add_resource(eval, '/eval')
api.add_resource(meta, '/meta')

if __name__ == '__main__':
    app.run(debug=True)
