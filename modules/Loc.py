import requests
import random
import geopandas as gpd
import json


access_token = json.load(open('config.json'))['access_token']


class RandLoc:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.access_token = None
        while self.lat == 0 and self.lon == 0:
            world = gpd.read_file('modules/world.shp')
            areas = world.area
            valid_shapes = [shape for shape, area in zip(
                world.geometry, areas) if area > 2]
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
            self.lon, self.lat = round(road['center']['lon'], 5), round(
                road['center']['lat'], 5)

    def generate_nearest_mappilary_id(self):

        url = f"https://graph.mapillary.com/images?fields=id&bbox={self.lon-0.001},{self.lat-0.001},{self.lon+0.001},{self.lat+0.001}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {access_token}'
        }
        response = requests.get(headers=headers, url=url)
        data = response.json()
        if data == {"data": []} or "error" in data:
            return None
        photo_id = data['data'][0]['id']
        self.photo_id = photo_id
        return photo_id


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
