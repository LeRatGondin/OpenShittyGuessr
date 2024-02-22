import requests
import random
import geopandas as gpd
values = [12.9045108, -61.321936900000004, 13.1045108, -61.1219369]


def lat():
    lat = 0
    lon = 0
    access_token = None
    while lat == 0 and lon == 0:
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
        lon, lat = road['center']['lon'], road['center']['lat']
        values = [lat-0.1, lon-0.1, lat+0.1, lon+0.1]
        print(f'{lat-0.1},{lon-0.1},{lat+0.1},{lon+0.1}')


values = [round(value, 3) for value in values]
print(values)
url = f"https://graph.mapillary.com/images?bbox={','.join(str(value) for value in values)}&make=GoPro&fields=id,make,captured_at"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'OAuth MLYARAKMLP2RF9wPB3kw1iCe7aPm39nVp39ZCFopsnFoqcEyJZCvHSvYvVprvCG9TFwhUGP2nFJhVkc4xWRV97YFcZBWmeGmqT7I0R4t4zrk3cG26zWF1thaAOpLBh0gZDZD'
}
response = requests.get(headers=headers, url=url)
print(response.json())
