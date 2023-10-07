import flask
import json
import sys
import requests

import opensky_api
import threading
import time

airport_code = "KDAB"
lat = 29.179962
long = -81.059972

try:
    f = open("secrets.json")
    secrets = json.load(f)
    f.close()
except:
    print("Secrets file does not exist! ADD IT :(")
    sys.exit()
    # It's a JSON file.
    # dict with username and password values for opensky network login

web_app = flask.Flask(__name__)
opensky_app = opensky_api.OpenSkyApi(username=secrets["username"], password=secrets["password"])

state_history = [
    [
        {
            "icao24": "xyz123",
            "lat": 27.1923,
            "lon": -81.372,
            "vert_rate": 5,
        }
    ]
]


@web_app.route("/")
def hello_world():
    return flask.render_template('index.html')


@web_app.route("/states")
def states():
    return state_history[len(state_history)-1]


def get_updated_states():
    sys.stdout.flush()
    try:
        new_states = opensky_app.get_states(bbox=(lat - 1, lat + 1, long - 1, long + 1)).states
        print("gotten states owo", flush=True)
        state_history.append(new_states)
    except:
        print("unable to get states", flush=True)
    time.sleep(30)


if __name__ == "__main__":
    # z = threading.Thread(target=get_updated_states, args=())
    # z.start()
    web_app.run()