from geojsonwatcher.util import timestamp_to_time

"""
    GeoJSON earthquake class.
"""


class Feature(object):
    def __init__(self, mag, time, place, url):
        self.mag = str(mag)
        self.time = timestamp_to_time(time)
        location = place.split(',')
        self.site = location[0]
        if len(location) > 1:
            self.area = location[1]
        else:
            self.area = 'Unknown.'
        self.url = url
