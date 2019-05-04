import datetime
from time import strftime

"""
    Convert timestamp in GeoJSON to readable string date.
"""


def timestamp_to_string(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp/1000))


"""
    Convert timestamp in GeoJSON to readable string time.
"""


def timestamp_to_time(timestamp):
    geo_time = datetime.datetime.fromtimestamp(timestamp/1000).time()
    return geo_time.strftime("%H:%M:%S")

"""
    Get current time as string.
"""
def get_time():
    return str(datetime.datetime.now().time())
