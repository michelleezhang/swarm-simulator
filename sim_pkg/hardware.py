#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
The hardware module exposes hardware interactions available to coach-os.
"""

from __future__ import absolute_import

import os
from typing import Sequence, Optional, Union  # pylint: disable=unused-import

if not os.environ.get('DRY_RUN'):
    import RPi.GPIO as g

try:
    from .math_utils import clamp_to_range
    from .configuration import get_led_pinout, get_motor_pinout
    from .data_structures import SingletonMeta
except (ImportError, ValueError):
    # pylint: disable=relative-import
    from math_utils import clamp_to_range
    from configuration import get_led_pinout, get_motor_pinout
    from data_structures import SingletonMeta
    # pylint: enable=relative-import


__author__ = 'Marko Vejnovic <contact@markovejnovic.com>'
__copyright__ = 'Copyright 2022, Northwestern University'
__credits__ = ['Marko Vejnovic', 'Lin Liu', 'Billie Strong']
__license__ = 'Proprietary'
__version__ = '0.5.0'
__maintainer__ = 'Marko Vejnovic'
__email__ = 'contact@markovejnovic.com'
__status__ = 'Development'


class GPIO:
    """This class handles all the GPIO operations.

    Warning:
        You must never store the initialized value of this class. The following
        is invalid and yields unexpected behavior across threads:

        .. code-block:: python

           my_gpio = GPIO()
           my_gpio.set_motor_duty_cycle('left', 100)
           my_gpio.set_motor_duty_cycle('right', 100)

        This is due to the fact that only the call to ``GPIO()`` guarantees
        that the class is not being used by other threads. In other words, if
        you want to achieve something like the previous, you must:

        .. code-block:: python

           GPIO().set_motor_duty_cycle('left', 100)
           GPIO().set_motor_duty_cycle('right', 100)

    Note:
        Initializing this class will not automatically setup the GPIO pins.
        This class is a Singleton and will therefore prevent the GPIO pins from
        being set multiple times, but, you are still responsible for calling
        the appropriate ``setup_*`` functions.
    """

    __metaclass__ = SingletonMeta

    def __init__(self):
        g.setmode(g.BOARD)
        self._motor_pinout = get_motor_pinout()
        self._led_pinout = get_led_pinout()
        self._motors_are_ready = False
        self._leds_are_ready = False
        self._motor_pwms = {'left': None, 'right': None}
        self._led_pwms = {'red': None, 'green': None, 'blue': None}

    def setup_leds(self, frequency=120):
        """Sets up the LEDs.

        Parameters:
            frequency (int): The LED frequency.
        """
        if self._leds_are_ready:
            return

        for color, led_info in self._led_pinout.items():
            g.setup(led_info['pin'], g.OUT, initial=led_info['initial'])
            self._led_pwms[color] = g.PWM(led_info['pin'], frequency)
            self._led_pwms[color].start(95)

        self._leds_are_ready = True

    def set_led_pow(
            self,
            red,  # type: Union[int, Sequence[int]]
            green=None,  # type: Optional[int]
            blue=None  # type: Optional[int]
    ):
        """Sets the LED value to a set of RGB powers.

        This function has two call signatures:

        .. code-block:: python

           GPIO().set_led_pow([0, 0, 0])
           GPIO().set_led_pow(0, 0, 0)

        Parameters:
            red (Union[int, Sequence]): If this is a list, then the list values
                are used as the arguments, otherwise -- The power to set the
                red LED to (0-100)
            green (Optional[int]): The power to set the green LED to (0-100).
                Must be provided if the first parameter is not an iterable.
            blue (Optional[int]): The power to set the blue LED to (0-100).
                Must be provided if the first parameter is not an iterable.
        """
        if isinstance(red, Sequence):
            green = red[1]
            blue = red[2]
            red = red[0]

        if red is None or green is None or blue is None:
            raise AttributeError(
                'Invalid arguments passed to GPIO.set_led_pow')

        val_range = (0, 100)
        for name, val in {'red': red, 'green': green, 'blue': blue}.items():
            self._led_pwms[name].ChangeDutyCycle(
                100 - clamp_to_range(val, val_range))

    def setup_motors(self):
        """Sets up motor control if it already has not been set up."""
        if self._motors_are_ready:
            return

        self._setup_motor('left')
        self._setup_motor('right')
        self._setup_pwm()
        self._motors_are_ready = True

    def _setup_motor(self, motor):  # pylint: disable=no-self-use
        # type: (str) -> None
        motor_pinout = self._motor_pinout[motor]
        for pin_info in motor_pinout.values():
            g.setup(pin_info['pin'], g.OUT, initial=pin_info['initial'])

    def _setup_pwm(self, frequency=600.0):
        # type: (float) -> None
        self._motor_pwms = {
            'left': g.PWM(self._motor_pinout['left']['pwm']['pin'],
                          frequency),
            'right': g.PWM(self._motor_pinout['right']['pwm']['pin'],
                           frequency)
        }

        for motor_pwm in self._motor_pwms.values():
            motor_pwm.start(0)

    def set_motor_standby(self, motor, should_stdby=True):
        # type: (str, bool) -> None
        """Sets a motor to standby or not.

        Parameters:
            motor (str): Which motor to set the standby state to.
            should_stdby (bool): Whether the motor should be set to standby.
                True by default.
        """
        g.output(self._motor_pinout[motor]['stdby']['pin'],
                 int(not should_stdby))

    def set_motor_duty_cycle(self, motor, duty_cycle):
        # type: (str, int) -> None
        """Sets the duty cycle on a motor."""
        self._motor_pwms[motor].ChangeDutyCycle(duty_cycle)

    def set_motor_direction(self, motor, clockwise):
        # type: (str, bool) -> None
        """Sets the motor direction.

        Parameters:
            motor (str): Which motor to control. Valid values are 'left' and
            'right'.
            clockwise (bool): Whether the motor should spin CW or CCW.

        Todo:
            It is possible that I have inverted clockwise.
        """
        in1 = int(clockwise)
        in2 = int(not clockwise)
        g.output(self._motor_pinout[motor]['in1']['pin'], in1)
        g.output(self._motor_pinout[motor]['in2']['pin'], in2)
        g.output(self._motor_pinout[motor]['stdby']['pin'], 1)