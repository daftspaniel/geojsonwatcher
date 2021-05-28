""" GeoJSON Structures. """
from geojsonwatcher.common.util import timestamp_to_time, sanitise_text


class Feature:
    """ Geo JSON feature class. """
    def __init__(self, mag, time, place, url):
        self.mag = f'{mag:.2f}'
        self.time = timestamp_to_time(time)
        location = place.split(',')
        self.site = sanitise_text(location[0])
        self.area = sanitise_text(location[1]) if len(
            location) > 1 else 'Unknown.'
        self.url = url

    def __str__(self):
        return ''# self.mag + ' ' + self.time + ' ' + self.site
