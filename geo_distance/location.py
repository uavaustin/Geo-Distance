"""Handles representating a GPS location and finding a location with a
distance object and the distance between GPS locations using a flat-
earth approximation.
"""

from math import sin, cos, asin, atan2, pi, sqrt, radians, degrees
from .distance import Distance, Distance3D
from pyproj import Geod
import geopy.distance

class Location(object):

    EARTH_RADIUS = 6371008.00 #6378137
    EARTH_ECCEN  = 0.0818191908

    """Represents a GPS location with a latitude and longitude
    with respect to the ground.
    """

    def __init__(self, lat, lon):
        """Instantiate a Location object with lat and long"""
        self.lat = lat
        self.lon = lon

    def __str__(self):
        """Return the components of a Location object (long/lat)"""
        return "long: {0.lon:f}, lat: {0.lat:f}".format(self)

    def __add__(self, dist):
        """Adds a Distance to the current Location and returns a new Location"""
        if not isinstance(dist, Distance):
            raise TypeError('Cannot add ', type(dist), 
                ' to a Location/AerialLocation')

        latitude, longitude = self.get_location(dist)
        altitude = 0

        if isinstance(self, AerialLocation):
            altitude += self.alt
        if isinstance(dist, Distance3D):
            altitude += dist.z

        if isinstance(self, AerialLocation) or isinstance(dist, Distance3D):
            return AerialLocation(latitude, longitude, altitude)

        return Location(latitude, longitude)

    def __sub__(self, other):
        """Subtracts a Distance from the current Location and returns a Location
        OR Subtracts a Location from current Location and returns a Distance
        """

        if not (isinstance(other, Distance) or isinstance(other, Location)):
            raise TypeError('Cannot subtract ', type(other),
                ' from a Location/AerialLocation')

        if isinstance(other, Distance):
            return __add__(other * -1)

        magnitude, bearing = self.get_distance(other)
        altitude = 0

        if isinstance(self, AerialLocation):
            altitude += self.alt
        if isinstance(other, AerialLocation):
            altitude -= other.alt

        if (isinstance(self, AerialLocation) or 
                isinstance(other, AerialLocation)):
            return Distance3D.from_magnitude(magnitude, bearing, altitude)

        return Distance.from_magnitude(magnitude, bearing)

    def get_distance(self, loc):
        """Wrapper method for get_distance; will call one of the methods for
        obtaining a distance vector between two locations.

        Called from a *Location object (AerialLocation or Location) and takes
        a *Location object (AerialLocation or Location) and returns a Distance* 
        (Distance3D or Distance, depending on inputs) object.
        Here's an example:
            >>> loc1 = Location(long, lat)
            >>> loc2 = AerialLocation(long, lat, alt)
            >>> loc1.get_distance(loc2)
            (magnitude, bearing)
        """

        global lmm
        global LOCATION_MATH_METHOD

        return lmm[LOCATION_MATH_METHOD](self, loc)

    def get_location(self, dist):
        """Wrapper method for getting location; will call one of the methods
        for obtaining a final location from an initial location and a distance
        vector.

        Called from a *Location object (AerialLocation or Location) and takes a
        Distance* (Distance3D or Disance object) and returns a final *Location
        (AerialLocation or Location, depending on inputs) object.
        Here's an example:
            >>> loc1 = AerialLocation(long, lat, alt)
            >>> dist = Distance(x_meters, y_meters)
            >>> loc1.get_location(dist)
            (latitude, longitude)
        """

        global lmm
        global LOCATION_MATH_METHOD

        return lmm[LOCATION_MATH_METHOD + 10](self, dist)

    def get_distance_geod(self, loc):
        wgs84_geod = Geod(ellps='WGS84')
        a, b, dist = wgs84_geod.inv(self.lon, self.lat, loc.lon, loc.lat,
            radians=True)
        return dist

    def get_location_geod(self, dist):
        wgs84_geod   = Geod(ellps='WGS84')
        lo, la, y, z = wgs84_geod.fwd(self.lon, self.lat, dist.get_magnitude(),
            radians=True)
        return (la, lo)

    def get_distance_old(self, loc): #Replaced by Location - Location (Vincenty)
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

        return (dist.get_magnitude(), dist.get_bearing())

    def get_location_old(self, dist): #Replaced by Location + dist/Location
        """Return a Location object dist away from the Location object
        using the flat-earth approximation.
        """

        e_radii = self._get_earth_radii()

        lat = dist.y / e_radii[0] + self.lat
        lon = dist.x / e_radii[1] / cos(self.lat) + self.lon
        alt = self.alt + dist.z

        return (lat, lon)

    def get_distance_vincenty(self, loc, angle=0): #Replaced by Loc - Loc
        """Get the distance between two Locations and return a Distance
        object using the flat-earth approximation.
        """

        point1 = (degrees(self.lat), degrees(self.lon))
        point2 = (degrees(loc.lat), degrees(loc.lon))
        distance = geopy.distance.vincenty(point1, point2).meters
        return (distance, self.get_bearing(loc))

    def get_location_vincenty(self, dist): #Replaced by Loc + dist/Loc - dist
        """Return a Location object dist away from the Location object
        using the flat-earth approximation.
        """

        point = (degrees(self.lat), degrees(self.lon))
        distance = geopy.distance.VincentyDistance(kilometers =
            dist.get_magnitude()/1000)
        bearing = degrees(dist.get_bearing())
        out = distance.destination(point=point, bearing=bearing)
        return (radians(out.latitude), radians(out.longitude))

    def haversine(self, loc): #get distance for Haversine
        """Takes two Locations and returns the Distance between them."""
        dLat = loc.lat - self.lat
        dLon = loc.lon - self.lon
        lat1 = self.lat
        lat2 = loc.lat

        a        = sin(dLat/2.0)**2 + cos(lat1)*cos(lat2)*sin(dLon/2.0)**2
        distance = 2.0*self.EARTH_RADIUS*asin(sqrt(a))
        bearing  = atan2(cos(lat2)*sin(dLon),cos(lat1)*sin(lat2)-
            sin(lat1)*cos(lat2)*cos(dLon))

        # print("Haversine Distance is {:f}".format(distance))
        # print("Haversine Bearing is  {:f}".format(bearing))

        return (distance, bearing)

    def aHaversine(self, dist): #get location for Haversine
        """Takes a Location and a Distance to return new location."""
        distance  = dist.get_magnitude()
        bearing   = dist.get_bearing()
        aDistance = distance/self.EARTH_RADIUS

        latOut = (asin((sin(self.lat)*cos(aDistance)))+
            cos(self.lat)*sin(aDistance)*cos(bearing))
        lonOut = self.lon+atan2(sin(bearing)*sin(aDistance)*cos(self.lat),
            cos(aDistance)-sin(self.lat)*sin(latOut))

        return (latOut, lonOut)

    def _get_earth_radii(self):
        """Return the radii used for the flat-earth approximation."""
        r_1 = (EARTH_RADIUS * (1 - EARTH_ECCEN ** 2) /
               (1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2) ** (3 / 2))
        r_2 = EARTH_RADIUS / sqrt(1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2)

        return r_1, r_2

    def get_bearing(self, loc):
        """Return the bearing from the Location object to loc."""
        lat2 = loc.lat
        lat1 = self.lat
        dLon = loc.lon - self.lon

        bearing = atan2(cos(lat2)*sin(dLon),cos(lat1)*sin(lat2)-
            sin(lat1)*cos(lat2)*cos(dLon))

        return bearing


class AerialLocation(Location):
    
    """Subclass of Location with an altitude."""

    def __init__(self, lat, lon, alt):
        """Instantiate an AerialLocation object with lat, lon, and alt."""
        super().__init__(lat, lon)
        self.alt  = alt

    def __str__(self):
        """Return the components of an AerialLocation object (long/lat/alt)"""
        return "long: {0.lon:f}, lat: {0.lat:f}, alt: {0.alt:f}".format(self)

FLAT_EARTH = 0
HAVERSINE  = 1
VINCENTY   = 2
GEOD       = 3

LOCATION_MATH_METHOD = VINCENTY

lmm={
        (FLAT_EARTH + 0): Location.get_distance_old,
        (HAVERSINE  + 0): Location.aHaversine,
        (VINCENTY   + 0): Location.get_distance_vincenty,
        (GEOD       + 0): Location.get_distance_geod,

        (FLAT_EARTH + 10): Location.get_location_old,
        (HAVERSINE  + 10): Location.haversine,
        (VINCENTY   + 10): Location.get_location_vincenty,
        (GEOD       + 10): Location.get_location_geod
    }