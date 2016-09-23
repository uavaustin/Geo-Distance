"""Contains the Distance class that represents distances in vector form
between two points.
"""

from math import atan2, sin, cos, sqrt, pi, copysign


class Distance(object):

    """Represents a distance between two points in vector form.

    Two distances can be added together and distances can be transformed
    by an angle.
    """

    def __init__(self, x, y, z):
        """Instantiate a Distance object with components x, y, and z."""
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, dist):
        """Add two Distance objects together and return a new
        Distance.
        """

        x = self.x + dist.x
        y = self.y + dist.y
        z = self.z + dist.z

        return Distance(x, y, z)

    def __sub__(self, dist):
        """Subtract a Distance object and return a new Distance."""
        x = self.x - dist.x
        y = self.y - dist.y
        z = self.z - dist.z

        return Distance(x, y, z)

    def __str__(self):
        return ("x: %s, y: %s" % (self.x,self.y))

    def get_magnitude(self):
        """Return the magnitude of the Distance object from its
        components.
        """

        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def get_magnitude_xy(self):
        """Return the magnitude of the Distance object from its x and y
        components.
        """

        return sqrt(self.x ** 2 + self.y ** 2)

    def get_transform(self, angle):
        """Transform the Distance object by an angle clockwise and
        return a new Distance.
        """

        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        z = self.z

        return Distance(x, y, z)

    @staticmethod
    def from_magnitude(dist, bearing):
        """Return a new Distance object from a magnitude in the xy plane
        and a bearing.
        """

        return Distance(dist * sin(bearing), dist * cos(bearing), 0)
