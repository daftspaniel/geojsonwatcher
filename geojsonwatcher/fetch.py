import urllib.request
import json

from geojsonwatcher.util import *

EarthquakeUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"


class Feature(object):
    def __init__(self, mag, time, place):
        self.mag = str(mag)
        self.time = timestamp_to_time(time)
        self.place = place


def fetch_data():
    response = urllib.request.urlopen(EarthquakeUrl)
    json_data = response.read()
    loaded_json = json.loads(json_data)
    newlist = sorted(loaded_json['features'],
                     key=lambda feature: feature['properties']['mag'], reverse=True)

    out = []
    for feature in newlist:
        q = feature['properties']
        out.append(Feature(q['mag'], q['time'], q['place']))

    return (loaded_json['metadata'], out)
