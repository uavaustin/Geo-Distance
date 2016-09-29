"""Handles representating a GPS location and finding a location with a
distance object and the distance between GPS locations using a flat-
earth approximation.
"""

from math import sin, cos, asin, atan2, pi, sqrt
from .distance import Distance, Distance3D


class Location(object):

    EARTH_RADIUS = 6371008.00 #6378137
    EARTH_ECCEN = 0.0818191908

    """Represents a GPS location with a lattitude, longitude, and
    altitude with respect to the ground.
    """

    def __init__(self, lat, lon, alt):
        """Instantiate a Location object at lat, lon and at alt."""
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def _get_earth_radii(self):
        """Return the radii used for the flat-earth approximation."""
        r_1 = (EARTH_RADIUS * (1 - EARTH_ECCEN ** 2) /
               (1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2) ** (3 / 2))
        r_2 = EARTH_RADIUS / sqrt(1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2)

        return r_1, r_2

    def __str__(self):
        return ("Latitude: %s, Longitude: %s, Altitude: %s" % (self.lat,
            self.lon, self.alt))

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def get_distance(self, loc, angle=0):
        """Get the distance between two Locations and return a Distance
        object using the flat-earth approximation.
        """

        e_radii = self._get_earth_radii()

        x = e_radii[1] * cos(self.lat) * (loc.lon - self.lon)
        y = e_radii[0] * (loc.lat - self.lat)
        z = loc.alt - self.alt

        dist = Distance(x, y, z)

        if angle:
            dist = dist.get_transform(angle)

        return dist

    def get_location(self, dist):
        """Return a Location object dist away from the Location object
        using the flat-earth approximation.
        """

        e_radii = self._get_earth_radii()

        lat = dist.y / e_radii[0] + self.lat
        lon = dist.x / e_radii[1] / cos(self.lat) + self.lon
        alt = self.alt + dist.z

        return Location(lat, lon, alt)

    def get_bearing(self, loc):
        """Return the bearing from the Location object to loc."""
        bearing = atan2(cos(lat2)*sin(dLon),cos(lat1)*sin(lat2)-
            sin(lat1)*cos(lat2)*cos(dLon))

        return bearing

    def haversine(self, loc):
        """Takes two Locations and returns the Distance between them."""
        dLat = loc.lat - self.lat
        dLon = loc.lon - self.lon
        lat1 = self.lat
        lat2 = loc.lat

        a        = sin(dLat/2.0)**2 + cos(lat1)*cos(lat2)*sin(dLon/2.0)**2
        distance = 2.0*self.EARTH_RADIUS*asin(sqrt(a))
        bearing  = atan2(cos(lat2)*sin(dLon),cos(lat1)*sin(lat2)-
            sin(lat1)*cos(lat2)*cos(dLon))

        print("Haversine Distance is {:f}".format(distance))
        print("Haversine Bearing is  {:f}".format(bearing))

        return Distance.from_magnitude(distance,bearing)

    def aHaversine(self, dist):
        """Takes a Location and a Distance to return new location."""
        distance  = dist.get_magnitude()
        bearing   = dist.get_bearing()
        aDistance = distance/self.EARTH_RADIUS

        latOut = (asin((sin(self.lat)*cos(aDistance)))+
            cos(self.lat)*sin(aDistance)*cos(bearing))
        lonOut = self.lon+atan2(sin(bearing)*sin(aDistance)*cos(self.lat),
            cos(aDistance)-sin(self.lat)*sin(latOut))

        return Location(latOut, lonOut, 0)
