from flask import Flask, render_template, request
import folium
from modules import Loc

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


m = folium.Map()
m.get_root().html.add_child(folium.Element("""
<div class="header">
  <h1>Header</h1>
  <p>My supercool header</p>
</div> """))
m._name = "map"
m._id = "1"
m.get_root().html.add_child(folium.JavascriptLink('static/js/universal.js'))

m.get_root().html.add_child(folium.Element(
    loc.generate_nearest_streetview_iframe()))
m.get_root().html.add_child(folium.CssLink('static/css/universal.css'))

m.save("templates/index.html")
app.run(host="localhost", port=8080, debug=True)
