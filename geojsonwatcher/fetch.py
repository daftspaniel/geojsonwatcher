import urllib.request
import json

from geojsonwatcher.feature import Feature
from geojsonwatcher.report import Report

EarthquakeUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

"""
    Fetch data from the feed.
"""


def fetch_data() -> dict:
    response = urllib.request.urlopen(EarthquakeUrl)
    json_data = response.read()
    return process_quake_feed(json.loads(json_data))


"""
    Generate a list of Feature objects.
"""


def process_quake_feed(loaded_json : dict) -> dict:
    out = []
    for feature in loaded_json['features']:
        q = feature['properties']
        out.append(Feature(q['mag'], q['time'], q['place'], q['url']))
    latest_report = Report('Latest', loaded_json['metadata'], out)
    latest_report.sort_entries()
    return latest_report
