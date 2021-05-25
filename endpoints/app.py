from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    pass


@app.route('/main')
def main():
    pass


@app.route('/last_response')
def last_response():
    pass


@app.route('/help')
def help():
    pass


@app.route('/ping')
def health():
    return 'pong'


if __name__ == "__main__":
    app.run(debug=True)