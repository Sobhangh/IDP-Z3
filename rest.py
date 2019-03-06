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

case = ConfigCase(theory)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class eval(Resource):
    def post(self):
        args = parser.parse_args()
        method = args['method']
        active = args['active']
        print(method, active)
        if method == "init":
            return case.initialisationlist()
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/test')
api.add_resource(eval, '/eval')

if __name__ == '__main__':
    app.run(debug=True)
