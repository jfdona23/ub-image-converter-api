from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Image(Resource):
    def get(self):
        pass

    def post(self):
        pass


class Ping(Resource):
    def get(self):
        return 'pong'


@api.resource('/last_response')
class LastResponse(Resource):
    def get(self):
        pass


api.add_resource(Image, '/image', '/main')
api.add_resource(Ping, '/ping', endpoint='ping')

if __name__ == "__main__":
    app.run(debug=True)
