import requests
import random
import geopandas as gpd


class RandLoc:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.access_token = None
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
            print(f'{self.lat-0.1},{self.lon-0.1},{self.lat+0.1},{self.lon+0.1}')

    def generate_nearest_streetview_iframe(self):
        url = f"https://graph.mapillary.com/images?fields=id&bbox=12.9045108,-61.321936900000004,13.1045108,-61.1219369"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth MLYARAKMLP2RF9wPB3kw1iCe7aPm39nVp39ZCFopsnFoqcEyJZCvHSvYvVprvCG9TFwhUGP2nFJhVkc4xWRV97YFcZBWmeGmqT7I0R4t4zrk3cG26zWF1thaAOpLBh0gZDZD'
        }
        response = requests.get(headers=headers, url=url)
        print(response.json())
        iframe = """
        <iframe 
        src="https://www.mapillary.com/embed?image_key=550092599700936&style=photo" 
        height="480" 
        width="640"  
        frameborder="0">
        </iframe>"""
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
