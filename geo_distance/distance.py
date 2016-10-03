"""Contains the Distance and Distance3D classes that represent
distances in vector form between two points.
"""

from math import atan2, sin, cos, sqrt, pi


class Distance:
    """Represents a distance between two points in vector form.

    Two distances can be added or subtracted and distances can be
    transformed by an angle.
    """

    def __init__(self, x, y):
        """Instantiate a Distance object with components x and y."""

        self.x = x
        self.y = y

    def __add__(self, dist):
        """Add two Distance objects together and return a new
        Distance.
        """
        if not isinstance(dist, Distance):
            raise TypeError('Cannot add', type(dist),
                'to a', type(self), 'object.')

        x = self.x + dist.x
        y = self.y + dist.y
        z = 0

        if isinstance(self, Distance3D):
            z += self.z

        if isinstance(dist, Distance3D):
            z += dist.z

        if isinstance(self, Distance3D) or isinstance(dist, Distance3D):
            return Distance3D(x, y, z)

        return Distance(x,y)

    def __sub__(self, dist):
        """Subtract a Distance object from another Distance object
        and return a new Distance.
        """
        if not isinstance(dist, Distance):
            raise TypeError('Cannot subtract', type(dist),
                'from a', type(self), 'object.')

        return self + -1 * dist

    def __mul__(self, scalar):
        """Multiply a Distance object by a scalar and return a new
        Distance object.
        """
        x = self.x * scalar
        y = self.y * scalar

        if not isinstance(self, Distance3D):
            return Distance(x, y)

        z = self.z * scalar

        return Distance3D(x, y, z)

    def __rmul__(self, scalar):
        """Pre-multiply a Distance object by a scalar and return a
        new Distance object.
        """
        return self * scalar

    def __div__(self, scalar):
        """Divide a Distance object by a scalar and return a new
        Distance object.
        """
        return self * (1 / scalar)

    def get_magnitude(self):
        """Return the magnitude of the Distance object from its
        components.
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def get_bearing(self):
        """Return the bearing of the Distance object."""
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

    def __str__(self):
        """Return the components of a Distance object in a string.
        """
        return ('x: {0.x:f}, y: {0.y:f}'.format(self))


class Distance3D(Distance):
    """Represents a 3D distance between two points in vector form.

    Two distances can be added or subtracted and distances can be
    transformed by an angle in the xy plane.
    """

    def __init__(self, x, y, z):
        """Instantiate a Distance3D object with components x, y, and
        z."""
        super().__init__(x, y)
        self.z = z

    def get_magnitude(self):
        """Return the magnitude of the Distance3D object from its
        components.
        """
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def get_transform(self, angle):
        """Transform the Distance3D object by an angle clockwise and
        return a new Distance3D object.
        """
        dist = Distance(self.x, self.y)
        dist = dist.get_transform(angle)

        return Distance3D(dist.x, dist.y, self.z)

    @classmethod
    def from_magnitude(cls, dist, bearing, alt):
        """Return a new Distance object from a magnitude in the xy plane
        and a bearing.
        """
        return cls(dist * sin(bearing), dist * cos(bearing), alt)

    def __str__(self):
        """Return the components of a Distance3D object in a string.
        """
        return ('x: {0.x:f}, y: {0.y:f} z: {0.z:f}'.format(self))
