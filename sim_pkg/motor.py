#! /usr/bin/env python

# pylint: disable-all

from __future__ import absolute_import

import logging
from time import sleep
import traceback

# TODO: Invalid import
try:
    from .messages import build_motor_message
    from .hardware import GPIO
except (ImportError, ValueError):
    from messages import build_motor_message
    from hardware import GPIO


def set_pow(buffer, left_power, right_power):
    """Sets the power of a motor.

    Parameters:
        buffer (multiprocessing.Array): The motor message array.
        left_power (float): The power to send to the left motor (-100, 100)
        right_power (float): The power to send to the right motor (-100, 100)
    """
    buffer.put(build_motor_message(left_power, right_power))


def drive(msg):
    t = 0.03
    l_lspeed = 0
    l_rspeed = 0
    GPIO().setup_motors()
    rspeed = 0
    lspeed = 0
    safecount = 0

    while True:
        sleep(t)

        try:
            if msg[2] == 0:
                safecount += 1
                if safecount > 30:
                    GPIO().set_motor_standby('left')
                    GPIO().set_motor_standby('right')
                    l_lspeed = 0
                    l_rspeed = 0
                continue

            safecount = 0
            lr = msg[:2]
            msg[2] = 0
            if len(lr) >= 2:
                lspeed = int(lr[0])
                rspeed = int(lr[1])

                if lspeed != l_lspeed:
                    GPIO().set_motor_duty_cycle('left', abs(lspeed))

                    if lspeed == 0:
                        GPIO().set_motor_standby('right', True)
                    else:
                        GPIO().set_motor_direction('left', lspeed < 0)
                    l_lspeed = lspeed

                if rspeed != l_rspeed:
                    GPIO().set_motor_duty_cycle('right', abs(rspeed))

                    if rspeed == 0:
                        GPIO().set_motor_standby('right', True)
                    else:
                        GPIO().set_motor_direction('right', rspeed < 0)
                    l_rspeed = rspeed

        except Exception as ex:
            logging.getLogger('system').error(
                'motor_py: %s.\n%s', ex, traceback.format_exc())