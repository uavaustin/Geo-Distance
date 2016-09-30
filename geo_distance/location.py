"""Handles representating a GPS location and finding a location with a
distance object and the distance between GPS locations using a flat-
earth approximation.
"""

from math import sin, cos, asin, atan2, pi, sqrt
from .distance import Distance, Distance3D


class Location(object):

    EARTH_RADIUS = 6371008.00 #6378137
    EARTH_ECCEN = 0.0818191908

    """Represents a GPS location with a latitude and longitude
    with respect to the ground.
    """

    def __init__(self, lat, lon):
        """Instantiate a Location object with lat and long"""
        self.lat = lat
        self.lon = lon

    def __str__(self):
        """Return the components of a Location object (long/lat)"""
        return "long: {0.long:f}, lat: {0.lat:f}".format(self)

    def __add__(self, other):
        """Adds a Distance to the current Location and returns a new Location"""
        if not isinstance(other, Distance):
            raise TypeError('Cannot add ', type(other), 
                ' to a Location/AerialLocation')

        invHav = aHaversine(self, other)
        magnitude = invHav[0]
        bearing   = invHav[1]
        altitude  = 0

        if isinstance(self, AerialLocation):
            altitude += self.alt
        if isinstance(other, Distance3D):
            altitude += other.z

        if isinstance(self, AerialLocation) or isinstance(other, Distance3D):
            return Distance3D.from_magnitude(magnitude, bearing, altitude)

        return Distance.from_magnitude(dist, bearing)

    def __sub__(self, other):
        if not (isinstance(other, Distance) or isinstance(other, Location)):
            raise TypeError('Cannot subtract ', type(other),
                ' from a Location/AerialLocation')

        if isinstance(other, Distance):
            __add__(other.reverse()) #replace with multiply



    def _get_earth_radii(self):
        """Return the radii used for the flat-earth approximation."""
        r_1 = (EARTH_RADIUS * (1 - EARTH_ECCEN ** 2) /
               (1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2) ** (3 / 2))
        r_2 = EARTH_RADIUS / sqrt(1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2)

        return r_1, r_2

    def get_distance(self, loc, angle=0): #Replaced by Location - Location
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

    def get_location(self, dist): #Replaced by Location + dist/Location - dist
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


class AerialLocation(Location):
    
    """Subclass of Location with an altitude."""

    def __init__(self, lat, lon, alt):
        """Instantiate an AerialLocation object with lat, lon, and alt."""
        super().__init__(lat, lon)
        self.alt  = alt

    def __str__(self):
        """Return the components of an AerialLocation object (long/lat/alt)"""
        return "long: {0.long:f}, lat: {0.lat:f}, alt: {0.alt:f}".format(self)
