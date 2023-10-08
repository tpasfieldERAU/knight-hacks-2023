# knight-hacks-2023

**Project Concept:** Planespotting Assist Tool

**Thought Process:**
As students of Embry-Riddle Aeronautical University, we are very comfortable living next to an airport. Our student body consists of a massive proportion of pilots and our alumni commonly go into the industry. Sometimes they like to surprise the school and fly through Daytona. Often unusual or highly anticipated military planes fly through next to campus all the time.

After missing out on all kinds of cool planes that came through unannounced, we decided that we want to try and change that. We want to make an app that uses live flight tracking data in order to notify users of nearby aircraft that are coming by to land. We hope to utilize Leaflet and Flask to make a web app.

As a stretch goal we hope to use the data and the device's gyroscope to aid in the user locating the aircraft in the distance.

**Current Outline:**
1. Get Lat/Long of nearby airports to select.
2. Get all planes nearby using OpenSky Box Method.
3. Attempt to get flight plan data of aircraft (can't find free API).
4. (3 Backup) Attempt to make out own filter to guess if a plane is coming in to land.
5. Attempt to merge device gyroscope/compass/location to indicate where to look for the aircraft.
6. Text or push notification of desired aircraft.

## How to run:
We were unfortunately unable to setup hosting for the app in time. If you would like to experience our app, feel free to clone our repo. To run the app, simply run the `main.py` python script.

    cd knight-hacks-2023
    python3 main.py

Because it is not deployed and we are just putting API keys public, the API calls will not work and it should instead fall back to demo data.