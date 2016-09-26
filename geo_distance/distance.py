"""Contains the Distance class that represents distances in vector form
between two points.
"""

from math import atan2, sin, cos, sqrt, pi, copysign

class Distance(object):

    """Represents a distance between two points in vector form.

    Two distances can be added or subtracted and distances can be
    transformed by an angle.
    """

    def __init__(self, x, y):
        """Instantiate a Distance object with components x and y."""
        self.x = x
        self.y = y

    def __add__(self, dist):
        """Add two Distance* objects together and return a new
        Distance*.
        """
        x = self.x + dist.x
        y = self.y + dist.y
        z = 0

        if (isinstance(self, Distance3D)):
            z += self.z
        if (isinstance(dist, Distance3D)):
            z += dist.z

        if (isinstance(self, Distance3D) or isinstance(dist, Distance3D)):
            return Distance3D(x, y, z)

        return Distance(x,y)

    def __sub__(self, dist):
        """Subtract a Distance* object from another Distance* object
        and return a new Distance*.
        """
        x = self.x - dist.x
        y = self.y - dist.y
        z = 0

        if (isinstance(self, Distance3D)):
            z += self.z
        if (isinstance(dist, Distance3D)):
            z -= dist.z

        if (isinstance(self, Distance3D) or isinstance(dist, Distance3D)):
            return Distance3D(x, y, z)

        return Distance(x, y)

    def __str__(self):
        """Print the components of a Distance object."""
        return ('x: {0.x:f}, y: {0.y:f}'.format(self))

    def get_magnitude(self):
        """Return the magnitude of the Distance object from its
        components.
        """

        return sqrt(self.x ** 2 + self.y ** 2)

    def get_bearing(self):

        return atan2(self.x, self.y) % (2 * pi)

    def get_transform(self, angle):
        """Transform the Distance object by an angle clockwise and
        return a new Distance.
        """

        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)

        return Distance(x, y)

    @classmethod
    def from_magnitude(cls, dist, bearing):
        """Return a new Distance object from a magnitude in the xy plane
        and a bearing.
        """

        return cls(dist * sin(bearing), dist * cos(bearing))

class Distance3D(Distance):

    """Subclass of Distance with an additional component (z)"""

    def __init__(self, x, y, z):
        """Instantiate a Distance3D object with components x, y, and z."""
        super(Distance3D, self).__init__(x, y)
        self.z = z

    def __str__(self):
        """Print the components of a Distance3D object."""
        return ('x: {0.x:d}, y: {0.y:d} z: {0.z:d}'.format(self))

    def get_magnitude(self):
        """Return the magnitude of the Distance3D object from its
        components.
        """

        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def get_transform(self, angle):
        """Transform the Distance3D object by an angle clockwise and
        return a new Distance3D object.
        """

        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        z = self.z

        return Distance3D(x, y, z)

    @classmethod
    def from_magnitude(cls, dist, bearing, alt):
        """Return a new Distance object from a magnitude in the xy plane
        and a bearing.
        """

        return cls(dist * sin(bearing), dist * cos(bearing), alt)
