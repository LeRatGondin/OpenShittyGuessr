from flask import Flask, render_template, request, make_response
from modules import Loc
import base64
from math import exp, pi
import threading
import time
import json

app = Flask(__name__, static_folder='static')

locations = []

config = json.load(open('config.json'))

if config['access_token'] == "":
    print("Please open the file setup.py and follow the instructions.")
    exit(1)


def add_location():
    while True:
        print(f"Thread {str(len(locations))} locations.")
        print("Generating new location...")
        while len(locations) >= 2:
            time.sleep(10)
            print("Waiting for locations to be used...")
        loc = Loc.RandLoc()
        photo_id = loc.generate_nearest_streetview_iframe()
        while photo_id is None:
            loc = Loc.RandLoc()
            photo_id = loc.generate_nearest_streetview_iframe()
        locations.append(loc)
        print("Location added.")


thread = threading.Thread(target=add_location)
thread.start()


@app.route('/')
def root():
    if len(locations) == 0:
        return "Loading locations..., please wait."
    markers = [
        {
            'lat': 0,
            'lon': 0,
            'popup': 'This is the middle of the map.'
        }
    ]
    loc = locations.pop(0)
    photo_id = loc.photo_id
    loc_str = f"{loc.lat},{loc.lon}"
    loc_str = base64.b64encode(loc_str.encode('utf-8')).decode('utf-8')
    page = make_response(render_template(
        'index.html', markers=markers, photo_id=photo_id))
    page.set_cookie('loc', loc_str)
    return page


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    lat = data['lat']
    lng = data['lng']
    page = make_response("ok")
    loc = f"{lat},{lng}"
    loc = base64.b64encode(loc.encode('utf-8')).decode('utf-8')
    page.set_cookie('found_loc', loc)
    return page


@app.route('/result')
def result():
    found_loc = base64.b64decode(
        request.cookies.get('loc')).decode('utf-8').split(',')
    real_loc = base64.b64decode(request.cookies.get(
        'found_loc')).decode('utf-8').split(',')
    found_lat = float(found_loc[0])
    found_lng = float(found_loc[1])
    real_lat = float(real_loc[0])
    real_lng = float(real_loc[1])
    distance = round(((found_lat - real_lat)**2 + (found_lng - real_lng)
                      ** 2)**0.5 * pi * 6371000 / 180, 2)
    distance_km = round(distance / 1000, 2)
    distance_str = f"{distance} m" if distance < 1000 else f"{distance_km} km"
    score = round(5000 * exp(-distance_km / 2000), 2)
    guess_location = {"lat": found_lat, "lng": found_lng}
    real_location = {"lat": real_lat, "lng": real_lng}
    formated_guess = Loc.decimal_to_dms(found_lat, "lat") + ", " +\
        Loc.decimal_to_dms(found_lng, "lon")
    formated_real = Loc.decimal_to_dms(real_lat, "lat") + ", " +\
        Loc.decimal_to_dms(real_lng, "lon")
    return render_template('result.html', formated_guess=formated_guess, formated_real=formated_real, real_location=real_location, guess_location=guess_location, distance=distance_str, score=score, bar=round(score / 50, 2))


app.run(host="localhost", port=8080, debug=True)
