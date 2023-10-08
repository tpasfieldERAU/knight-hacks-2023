# -------------- IMPORTS --------------
# External Imports
import flask
from flask import jsonify, request
import opensky_api
import pyowm

# Local Imports
import airportsdata as apd
import plane_generator as pg

# Python Standard Library Imports
import json
import sys
import time
import random as rnd
import string
import threading


# --------- SECRETS MANAGEMENT ---------
flag = True

try:
    f = open("secrets.json")
    secrets = json.load(f)
    f.close()
except:
    flag = False
    # print("Secrets file does not exist! ADD IT :(")
    # sys.exit()
    # It's a JSON file.
    # dict with username and password values for opensky network login

if flag:
    owm = pyowm.OWM(secrets["wkey"])

# ---------- VARIABLE INITS ------------
# IDK, you can comment this lmao
state_history = [[{
    "icao24": "xyz123",
    "lat": 27.1923,
    "lon": -81.372,
    "vert_rate": 5,
}]]

# Init server and api objects
web_app = flask.Flask(__name__)
if flag:opensky_app = opensky_api.OpenSkyApi(username=secrets["username"], password=secrets["password"])


# Load airports db using ICAO standard codes
airports = apd.load('ICAO')

icao = 'KDAB'
# Set Daytona as default airport
airport = airports[icao]

lat = airport['lat']
lon = airport['lon']

planes = []

if flag:
    mgr = owm.weather_manager()
    weather = mgr.weather_at_coords(lat, lon).weather
    temp = weather.temperature("fahrenheit")['temp']
    rain = "Not Yet Implemented"  # weather.rain
    rain_level = weather.detailed_status  # rain["1hr"]
    vis = weather.visibility(unit="miles")

# --------- START AJAX FUNCTIONS ---------
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
    count = rnd.randint(5, 65)
    global planes

    js_planes = []
    for i in range(count):
        reg = "N" + str(rnd.randint(100, 999)) + rnd.choice(string.ascii_uppercase) + rnd.choice(string.ascii_uppercase)
        mod = pg.mods[rnd.randint(0, len(pg.mods)-1)]
        alt = rnd.randint(1500, 50000)
        plat = lat + rnd.gauss(0.0, 0.20)
        plon = lon + rnd.gauss(0.0, 0.20)
        hspeed = rnd.randint(70, 300)
        vspeed = rnd.gauss(0.0, 25.0)
        head = rnd.randint(0, 359)

        if round(rnd.random()):
            arv = icao
            dep = "KDUL"
            plane = pg.Plane(reg, mod, plat, plon, alt, vspeed, hspeed, head, arv, dep)
        else:
            plane = pg.Plane(reg, mod, plat, plon, alt, vspeed, hspeed, head)
        planes.append(plane)
        js_planes.append(vars(plane))
    return jsonify(js_planes)

# Update coordinates in some form. This can later call the API.
@web_app.route('/update_coordinates', methods=['POST'])
def update_coordinates():
    js_planes = []
    for plane in planes:
        js_planes.append(vars(plane))
    return jsonify(js_planes)


# Set airport based on form input.
@web_app.route('/set_airport', methods=['POST'])
def set_airport():
    global airport
    global lat
    global lon
    global icao

    data = request.get_json()
    icao = str(data)
    try:
        airport = airports[icao]
    except KeyError:
        # Reset to default
        airport = airports['KDAB']
        print("Error in airport search. Likely invalid ICAO code.")

    airport_coords = {'lat': airport['lat'], 'lon': airport['lon']}
    lat = airport['lat']
    lon = airport['lon']
    return jsonify(airport_coords)


@web_app.route('/get_weather', methods=['GET'])
def get_weather():
    if not flag:
        return jsonify([{'temp':"Missing Weather API", 'rain':"Missing Weather API", 'vis':"Missing Weather API"}])
    return jsonify([{'temp':temp, 'rain':rain_level, 'vis':vis}])

@web_app.route('/update_weather', methods=['POST'])
def update_weather():
    if not flag:
        return jsonify([{'temp': "Missing Weather API", 'rain': "Missing Weather API", 'vis': "Missing Weather API"}])
    weather = mgr.weather_at_coords(lat, lon).weather
    temp = weather.temperature("fahrenheit")['temp']
    rain = "Not Yet Implemented"  # weather.rain
    rain_level = weather.detailed_status  # rain["1hr"]
    print(rain_level)
    vis = weather.visibility(unit="miles")
    return jsonify([{'temp':temp, 'rain':rain_level, 'vis':vis}])



# -------- GENERAL FUNCTIONS ---------
def get_updated_states():
    dt = 5.0
    while True:
        for plane in planes:
            plane.timeStep(dt)
        time.sleep(dt)


if __name__ == "__main__":
    z = threading.Thread(target=get_updated_states, args=())
    z.start()
    web_app.run()
