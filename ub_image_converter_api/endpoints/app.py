from flask import Flask, request
from ..middleware.response import RequestHandler 

app = Flask(__name__)

@app.route('/', methods=["POST"])
def index():
    a = request.get_json()
    r = RequestHandler(a)
    return r.build_response()


@app.route('/ping')
def health():
    r = {"msg": "pong"}
    return r


if __name__ == "__main__":
    app.run(debug=True)
