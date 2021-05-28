""" Misc utility functions. """
import datetime

def timestamp_to_string(timestamp) -> str:
    """ Convert timestamp in GeoJSON to readable string date. """
    return str(datetime.datetime.fromtimestamp(timestamp / 1000))


def timestamp_to_time(timestamp) -> str:
    """ Convert timestamp in GeoJSON to readable string time. """
    geo_time = datetime.datetime.fromtimestamp(timestamp / 1000).time()
    return geo_time.strftime("%H:%M:%S")


def get_time() -> str:
    """ Get current time as string. """
    return str(datetime.datetime.now().time())

def sanitise_text(text):
    """ Tidy text for display on screen."""
    return text.replace("'", "").strip()
