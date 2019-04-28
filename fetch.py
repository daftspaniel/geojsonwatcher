import urllib.request
import json
EarthquakeUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"


def fetch_data():
    response = urllib.request.urlopen(EarthquakeUrl)
    json_data = response.read()
    loaded_json = json.loads(json_data)
    newlist = sorted(loaded_json['features'],
                     key=lambda feature: feature['properties']['mag'], reverse=True)

    out = []
    for feature in newlist:
        q = feature['properties']
        out.append(str(q['mag']) + '\t' + str(q['time']) + '\t' + q['place'])

    return (loaded_json['metadata'], out)
