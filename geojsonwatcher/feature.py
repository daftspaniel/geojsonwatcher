from geojsonwatcher.util import timestamp_to_time

"""
    GeoJSON earthquake class.
"""


class Feature(object):
    def __init__(self, mag, time, place):
        self.mag = str(mag)
        self.time = timestamp_to_time(time)
        self.place = place
