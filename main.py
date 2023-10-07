import flask
import json
import sys

app = flask.Flask(__name__)

try:
    f = open("secrets.json")
    secrets = json.load(f)
    f.close()
except:
    sys.exit()
    print("Secrets file does not exist! ADD IT :(")
    # It's a JSON file.
    # dict with username and password values for opensky network login


@app.route("/")
def hello_world():
    return flask.render_template('index.html')


if __name__ == "__main__":
    app.run()
