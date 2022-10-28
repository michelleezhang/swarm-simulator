# -*- coding: utf-8 -*-

"""
This, perhaps poorly named module contains functions which build messages
further passed-on to message buffers.

I do not understand the purpose of many of the functions here, but they are
required for normal operation.
"""

from __future__ import absolute_import

try:
    from coach_os.math_utils import signed_max, clamp_to_range
except (ImportError, ValueError):
    from math_utils import signed_max, clamp_to_range


__author__ = 'Marko Vejnovic <contact@markovejnovic.com>'
__copyright__ = 'Copyright 2022, Northwestern University'
__credits__ = ['Marko Vejnovic', 'Lin Liu', 'Billie Strong']
__license__ = 'Proprietary'
__version__ = '0.5.0'
__maintainer__ = 'Marko Vejnovic'
__email__ = 'contact@markovejnovic.com'
__status__ = 'Production'


MOTOR_MESSAGE_FORMAT = '{motor_left}|{motor_right}|0'


def build_motor_message(left, right):
    # type: (float, float) -> str
    """Given a set of inputs left and right, this function ensures these values
    are within expected bounds of +-(20, 100) and encodes them in a motor
    message format.

    The legacy name for this function was `motor_control`.

    Parameters:
        left (float): The left motor power (-100 <= l <= 100)
        right (float): The right motor power (-100 <= r <= 100)

    Note:
        If the values of either ``left`` or ``right`` are too small (< 20),
        this function will clamp them to 20.

    Returns:
        str: A string encoding the inputs ready to be sent to the robot.
    """
    def _clamp(val):
        # type: (float) -> int
        return int(signed_max(clamp_to_range(val, (-100.0, 100.0)), 20.0))

    left_i, right_i = _clamp(left), _clamp(right)
    return MOTOR_MESSAGE_FORMAT.format(motor_left=left_i, motor_right=right_i)