#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Exposes useful mathematical functions.

This module is purely functional and has no side effects.
"""

# pylint: disable=unused-import
from typing import Union, List, Tuple, Optional
# pylint: enable=unused-import
import numpy as np

__author__ = 'Marko Vejnovic <contact@markovejnovic.com>'
__copyright__ = 'Copyright 2022, Northwestern University'
__credits__ = ['Marko Vejnovic', 'Lin Liu', 'Billie Strong']
__license__ = 'Proprietary'
__version__ = '0.5.0'
__maintainer__ = 'Marko Vejnovic'
__email__ = 'contact@markovejnovic.com'
__status__ = 'Production'


def is_number(value, real=False):
    """Checks whether x is a number.

    Parameters:
        x: The number to check
        real (bool): Whether complex numbers should return false.

    Returns:
        Whether x is a (possibly only real) number
    """
    targets = (float, int) if real else (float, int, complex)
    return isinstance(value, targets)


def clamp_angle(angle, angle_range='2pi'):
    # type: (float, str) -> float
    """Given an angle of arbitrary range, this function removes periodic
    elements binding it to [-pi, pi].

    Parameters:
        angle (float): The input angle
        angle_range (str): Pass '2pi' to receive values in [0, 2pi], or '+-pi',
            to receive values in [-pi, pi]. Defaults to '2pi'

    Returns:
        float: The original angle with all periodic elements removed, bound to
        the provided range.
    """
    normalized = angle % (2 * np.pi)  # Between [0, 2pi]

    if angle_range in ('+-pi', '+- pi'):
        return normalized if normalized < np.pi else normalized - 2 * np.pi

    return normalized


def circular_mean(values):
    # type: (np.ndarray|list[float]) -> float
    """
    Parameters:
        values (np.ndarray | list[float]): A list or a np.ndarray of values.

    Returns:
        float: The circular mean of a collection.
    """
    if isinstance(values, list):
        values = np.array(values)

    return np.arctan2(np.mean(np.sin(values)), np.mean(np.cos(values)))


def clamp_to_range(val, min_max_range):
    # type: (float|int, tuple[float|int, float|int]) -> float|int
    """Clamps a value to a range.

    Parameters:
        val (float | int): The value to bind to the range,
        min_max_range (tuple[float | int, float | int]): The range in (min,
            max) form

    Returns:
        float | int: The inputted value bound to the given range.
    """
    return max(min(val, min_max_range[1]), min_max_range[0])


def signed_max(value, target):
    # type: (float|int, float|int) -> float|int
    """
    This function, given a value and a target ensures that the value is greater
    than the target by returning the target if the value is smaller than the
    target. However, unline a simple `max` this function handles negative
    values gracefully by ensuring that if `value` is negative, it must also be
    smaller than the negative of `target`.

    Parameters:
        value (float|int): The value to clamp
        target (float|int): The minimum the value must be greater than

    Returns:
        float|int: ``sgn(value) * max(value, target)``
    """
    return np.sign(value) * np.maximum(np.abs(value), np.abs(target))


def distance(point_1,   # type: Union[np.ndarray, List[float], float]
             point_2,   # type: Union[np.ndarray, List[float], float]
             x_2=None,  # type: Optional[float]
             y_2=None):
    """
    Returns the distance between two given points.

    This function always returns positive values.

    This function has two call signatures:
    distance(x1, y1, x2, y2) and distance(point_1, point_2)

    Parameters:
        point_1 (np.ndarray|List[float]|float): The first (2,) point.
        point_2 (np.ndarray|List[float]|float): The second (2,) point.
        x_2 (Optional[float]): If the previous values are float, this is the
            x-component of the 2nd coordinate
        y_2 (Optional[float]): If the previous values are float, this is the
            y-component of the 2nd coordinate

    Returns:
        float: The distance between two points.
    """
    if is_number(point_1) and is_number(point_2) and is_number(x_2) \
            and is_number(y_2):
        x_1 = point_1
        y_1 = point_2
        return np.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

    return np.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)


def angle_between(point_1, point_2):
    # type: (np.ndarray|list[float], np.ndarray|list[float]) -> float
    """
    Returns the angle between two given points.

    Parameters:
        point_1 (np.ndarray): The first (2,) point.
        point_2 (np.ndarray): The second (2,) point.

    Returns:
        float: The angle between two points.
    """
    return np.arctan2(point_2[1] - point_1[1], point_2[0], point_1[0])


class Vec2(object):
    """This class builds a simple 2-dimensional vector.

    This class was designed to simplify and standardize the API used when
    manipulating vector objects. The convenience of this class is that it
    guarantees that Vectors behave as you would expect them to.

    Example:

    .. code-block:: python

       Vec2(3, 4) + Vec2(1, 2) == Vec2(4, 6)
    """

    VALID_X = Union[float, int, np.ndarray, List[float], Tuple[float, float]]

    def __init__(self, x=0.0, y=0.0):
        # type: (Vec2.VALID_X, float) -> None
        if isinstance(x, (float, int)):
            self.data = np.array([x, y], dtype=np.double)
            return

        if len(x) != 2:
            raise ValueError(
                'If instantiating Vec2 with an array, the array must be ' +
                'of length 2.')
        self.data = np.array(x, dtype=np.double)

    @property
    def x(self):  # pylint: disable=invalid-name
        # type: () -> float
        """The x component of the vector."""
        return self.data[0]

    @property
    def y(self):  # pylint: disable=invalid-name
        # type: () -> float
        """The y component of the vector."""
        return self.data[1]

    def to_numpy(self):
        # type: () -> np.ndarray
        """Converts self to a numpy array. Returns a copy."""
        return np.copy(self.data)

    def __repr__(self):
        # type: () -> str
        return '<Vec2 ([%.15f, %.15f])>' % (self.x, self.y)

    def __str__(self):
        # type: () -> str
        return '[%.3f, %.3f]' % (self.x, self.y)

    def __eq__(self, __o):
        # type: (Vec2) -> bool
        return self.x == __o.x and self.y == __o.y

    def __ne__(self, __o):
        # type: (Vec2) -> bool
        return not self.__eq__(__o)

    def __abs__(self):
        return self.magnitude()

    def __add__(self, __o):
        # type: (Vec2) -> Vec2
        return Vec2(self.x + __o.x, self.y + __o.y)

    def __neg__(self):
        # type: () -> Vec2
        return Vec2(-self.x, -self.y)

    def __sub__(self, __o):
        return Vec2(self.x - __o.x, self.y - __o.y)

    def __mul__(self, __o):
        # type: (float) -> Vec2
        return Vec2(self.data * __o)

    def __div__(self, __o):
        # type: (float) -> Vec2
        return Vec2(self.data / __o)

    def dot(self, __o):
        # type: (Vec2) -> float
        """Returns the dot product of two vectors."""
        return np.dot(self.data, __o.data)

    def cross(self, __o):
        # type: (Vec2) -> float
        """Returns the magnitude of the cross-product."""
        return np.cross(self.data, __o.data)

    def magnitude(self):
        # type: () -> float
        """Returns the magnitude of the vector.

        Returns:
            (float): The magnitude of the vector
        """
        return np.sqrt(self.x**2 + self.y**2)

    def angle(self):
        # type: () -> float
        """Returns the angle of the vector.

        Returns:
            (float): The angle of the vector.
        """
        return np.arctan2(self.y, self.x)