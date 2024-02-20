from flask import Flask, render_template, request
import folium


app = Flask(__name__, static_folder='static')


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
    print(data)
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
m.get_root().html.add_child(folium.Element("""<iframe id="iframe" src="https://www.google.com/maps/embed?pb=!4v1707984391055!6m8!1m7!1szLTYPGvYKMsvfFDDPZz4Dw!2m2!1d48.8296814503996!2d2.261544657986094!3f236.3444103256701!4f1.9340393629049117!5f0.7820865974627469" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""))
m.get_root().html.add_child(folium.CssLink('static/css/universal.css'))

m.save("templates/index.html")
app.run(host="localhost", port=8080, debug=True)
