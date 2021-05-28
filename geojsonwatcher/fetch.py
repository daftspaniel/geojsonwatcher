""" Module deals with the request of the data from the source and converting into a Report."""
import urllib.request
import json

from geojsonwatcher.data_structures.feature import Feature
from geojsonwatcher.data_structures.report import Report
from geojsonwatcher.common.log import log

EARTHQUAKE_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"


def fetch_data() -> Report:
    """
        Fetch data from the feed.
    """
    response = urllib.request.urlopen(EARTHQUAKE_URL)
    json_data = response.read()
    return process_quake_feed(json.loads(json_data))


def process_quake_feed(loaded_json: dict) -> Report:
    """
        Generate a list of Feature objects.
    """
    out = []
    for feature in loaded_json['features']:
        quake = feature['properties']
        log(quake)
        out.append(Feature(quake['mag'], quake['time'], quake['place'], quake['url']))
    log('Making report...')
    latest_report = Report('Latest', loaded_json['metadata'], out)
    latest_report.sort_entries()
    log('Finished report.')
    return latest_report
