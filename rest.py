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


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class eval(Resource):
    def post(self):
        case = ConfigCase(theory)

        args = parser.parse_args()
        method = args['method']
        active = args['active']
        print(method, active)
        if method == "init":
            return case.initialisationlist()
        if method == "propagate":
            case.loadStructureFromJson(active)
            out = case.propagation()
            print(out)
            return out
        if method == "modelexpand":
            case.loadStructureFromJson(active)
            print(case.json_model())
            return case.json_model()
        if method == "relevance":
            return {}

        return {'hello': 'world'}


class meta(Resource):
    def get(self):
        return ConfigCase(theory).metaJSON()


api.add_resource(HelloWorld, '/test')
api.add_resource(eval, '/eval')
api.add_resource(meta, '/meta')

if __name__ == '__main__':
    app.run(debug=True)
