from flask import Flask, render_template, request
import folium
from modules import Loc
import time
app = Flask(__name__, static_folder='static')

loc = Loc.RandLoc()


@app.route('/')
def root():
    markers = [
        {
            'lat': 0,
            'lon': 0,
            'popup': 'This is the middle of the map.'
        }
    ]
    m.get_root().html.add_child(folium.Element(
        loc.generate_nearest_streetview_iframe()))
    m.save("templates/index.html")
    return render_template('index.html', markers=markers)


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    lat = data['lat']
    lng = data['lng']
    real_lat = loc.lat
    real_lng = loc.lon
    # Calculate the score based on the distance between the two points
    # and the user's guess
    distance = ((lat - real_lat)**2 + (lng - real_lng)**2)**0.5
    score = 1 - distance / 180
    print(score)
    print(f"Real: {real_lat}, {real_lng}" +
          f"Guess: {lat}, {lng}" + f"Distance: {distance}")
    # Print the score to the console

    return "ok"


@app.route('/connect', methods=['GET'])
def connect():
    # Accessing the parameters from the request
    data = request.args
    loc.access_token = data['code']

    return "ok"


m = folium.Map()
m.get_root().html.add_child(folium.Element("""
<div class="header">
  <h1>Header</h1>
  <p>My supercool header</p>
</div> """))
m._name = "map"
m._id = "1"
m.get_root().html.add_child(folium.JavascriptLink('static/js/universal.js'))


# Generate a iframe in the form of a string "<iframe width="640" height="480" src="https://www.mapillary.com/embed?map_style=Mapillary%20streets&amp;image_key=5377780175626061&amp;x=0.508403494278837&amp;y=0.5097834191221994&amp;style=image" frameborder="0"></iframe>" using the mapillary api and add it to the map

m.get_root().html.add_child(folium.CssLink('static/css/universal.css'))

m.save("templates/index.html")
app.run(host="localhost", port=8080, debug=True)
