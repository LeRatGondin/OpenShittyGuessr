import requests
import random
import geopandas as gpd


class RandLoc:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        while self.lat == 0 and self.lon == 0:
            world = gpd.read_file('modules/world.shp')
            areas = world.area
            valid_shapes = [shape for shape, area in zip(
                world.geometry, areas) if area > 0]
            if valid_shapes:
                shape = random.choice(valid_shapes)
            else:
                shape = None
            minx, miny, maxx, maxy = shape.bounds
            min_lat = random.uniform(miny, maxy)
            min_lon = random.uniform(minx, maxx)
            max_lat = min_lat + 0.2
            max_lon = min_lon + 0.2
            overpass_query = f"""
            [out:json];
            (
            way["highway"]({min_lat},{min_lon},{max_lat},{max_lon});
            way["residential"]({min_lat},{min_lon},{max_lat},{max_lon});
            way["footway"]({min_lat},{min_lon},{max_lat},{max_lon});
            );
            out center;
            """
            overpass_url = "http://overpass-api.de/api/interpreter"
            response = requests.get(overpass_url, params={
                                    'data': overpass_query})
            data = response.json()
            if not data['elements']:
                continue
            road = random.choice(data['elements'])
            self.lon, self.lat = road['center']['lon'], road['center']['lat']

    def generate_nearest_streetview_iframe(self):
        baseurl = "https://www.google.com/maps/embed/v1/streetview"
        params = {
            "location": f"{self.lat},{self.lon}",
            "heading": "151.78",
            "pitch": "-0.76",
            "key": "AIzaSyAY9lzcIlf6rTjb9fPgoEbLgN82hYQTDxk"
        }
        iframe = f'<iframe width="600" height="450" frameborder="0" style="border:0" src="{baseurl}?key={params["key"]}&location={params["location"]}&heading={params["heading"]}&pitch={params["pitch"]}" allowfullscreen></iframe>'
        return iframe


def decimal_to_dms(decimal, type):
    degrees = int(decimal)
    temp = abs(decimal - degrees) * 60
    minutes = int(temp)
    seconds = (temp - minutes) * 60

    direction = ''
    if type == 'lon':
        direction = 'E' if decimal > 0 else 'W'
    elif type == 'lat':
        direction = 'N' if decimal > 0 else 'S'

    return f"{abs(degrees)}°{minutes}'{seconds:.2f}\"{direction}"
