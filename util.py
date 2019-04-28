import datetime

"""
    Convert timestamp in GeoJSON to readable string date.
"""
def timestamp_to_string(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp/1000))
