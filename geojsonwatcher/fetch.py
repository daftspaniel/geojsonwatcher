import urllib.request
import json

from geojsonwatcher.feature import Feature
from geojsonwatcher.report import Report

EarthquakeUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

"""
    Fetch data from the feed.
"""


def fetch_data():
    response = urllib.request.urlopen(EarthquakeUrl)
    json_data = response.read()
    return process_quake_feed(json.loads(json_data))


"""
    Generate a list of Feature objects.
"""


def process_quake_feed(loaded_json):
    newlist = sorted(loaded_json['features'],
                     key=lambda feature: feature['properties']['mag'], reverse=True)

    out = []
    for feature in newlist:
        q = feature['properties']
        out.append(Feature(q['mag'], q['time'], q['place'], q['url']))

    return Report('Latest', loaded_json['metadata'], out)
