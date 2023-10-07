## -------------- IMPORTS ---------------
# External Imports
import flask
from flask import jsonify, request
import opensky_api

# Local Imports
import airportsdata as apd

# Python Standard Library Imports
import json
import sys
import threading
import time
## ------------ END IMPORTS -------------

## --------- SECRETS MANAGEMENT ---------
try:
    f = open("secrets.json")
    secrets = json.load(f)
    f.close()
except:
    print("Secrets file does not exist! ADD IT :(")
    sys.exit()
    # It's a JSON file.
    # dict with username and password values for opensky network login
## ------- END SECRETS MANAGEMENT -------

## ---------- VARIABLE INITS ------------
# IDK, you can comment this lmao
state_history = [[{
    "icao24": "xyz123",
    "lat": 27.1923,
    "lon": -81.372,
    "vert_rate": 5,
}]]

# Init server and api objects
web_app = flask.Flask(__name__)
opensky_app = opensky_api.OpenSkyApi(username=secrets["username"], password=secrets["password"])


# Load airports db using ICAO standard codes
airports = apd.load('ICAO')

# Set Daytona as default airport
airport = airports['KDAB']

lat = airport['lat']
lon = airport['lon']

# Coordinates for initial load.
#   Kinda just here for demo purposes. Will be removed later.
initial_coordinates = [
    {"lat": 51.505, "lon": -0.09, "name": "Plane 1"},
    {"lat": 40.7128, "lon": -74.006, "name": "Plane 2"}
]
## ---------- END VARIABLE INITS ----------

## --------- START AJAX FUNCTIONS ---------
# Index page load
@web_app.route("/")
def hello_world():
    return flask.render_template('index.html')

# Aircraft State Vector Management
@web_app.route("/states")
def states():
    return state_history[len(state_history)-1]

# Get initial marker coordinates
# Gets initial coordinates for demo. Overall unnecessary.
@web_app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    return jsonify(initial_coordinates)

# Update coordinates in some form. This can later call the API.
@web_app.route('/update_coordinates', methods=['POST'])
def update_coordinates():
    new_coords = [
        {"lat": 29.1802, "lon": -81.0598, "name": "KDAB"}
    ]
    return jsonify(new_coords)

# Set airport based on form input.
@web_app.route('/set_airport', methods=['POST'])
def set_airport():
    data = request.get_json()
    icao = str(data)

    try:
        airport = airports[icao]
    except:
        # Reset to default
        airport = airports['KDAB']
        print("Error in airport search. Likely invalid ICAO code.")

    airport_coords = {'lat': airport['lat'], 'lon': airport['lon']}
    return jsonify(airport_coords)
## -------- END AJAX FUNCTIONS --------

## -------- GENERAL FUNCTIONS ---------
def get_updated_states():
    sys.stdout.flush()
    try:
        new_states = opensky_app.get_states(bbox=(lat - 1, lat + 1, lon - 1, lon + 1)).states
        print("gotten states owo", flush=True)
        state_history.append(new_states)
    except:
        print("unable to get states", flush=True)
    time.sleep(30)


if __name__ == "__main__":
    # z = threading.Thread(target=get_updated_states, args=())
    # z.start()
    web_app.run()