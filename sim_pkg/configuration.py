#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Singleton module exposing the configuration of the bot. Designed such that
sometime in the future it could read from ``/etc/coachos.conf`` or something
similar."""

from __future__ import absolute_import

from typing import Dict  # pylint: disable=unused-import
import pickle

import numpy as np

try:
    from coach_os.networking.utils import get_ip_address
except (ImportError, ValueError):
    from networking.utils import get_ip_address

__author__ = 'Marko Vejnovic <contact@markovejnovic.com>'
__copyright__ = 'Copyright 2022, Northwestern University'
__credits__ = ['Marko Vejnovic', 'Lin Liu', 'Billie Strong']
__license__ = 'Proprietary'
__version__ = '0.5.0'
__maintainer__ = 'Marko Vejnovic'
__email__ = 'contact@markovejnovic.com'
__status__ = 'Development'


def get_rotor_freq():
    # type: () -> float
    """
    Returns:
        int: The Vive-lighthouse rotor frequency in Hz.
    """
    return 60


def get_timer_freq():
    # type: () -> float
    """
    Returns:
        int: The default Vive-lighthouse timer frequency in Hz.
    """
    return 1e6


def get_zero_shift():
    # type: () -> np.ndarray
    """
    Returns:
        np.ndarray: The Vive-lighthouse angular zero offset in radian. This
        value is a calibration value and must be empirically determined.
    """
    return np.array([-1.56992011, -1.52214383])


def get_vive_height_in():
    # type: () -> float
    """
    Returns:
        float: The height between the vive and the vive sensor on the Coachbot
        in inches.
    """
    return 99.66


def get_playfield_bounding_box_in():
    # type: () -> np.ndarray
    """
    Returns:
        np.ndarray: The bounding box of the playfield in inches.
    """
    return 12 * np.array([  # In inches (hence *12)
        [-5, -8],
        [4, 7]
    ])


def get_vive_board_baudrate():
    # type: () -> int
    """
    Returns:
        int: The vive daughter-board baudrate.
    """
    return 19200


def get_is_debug():
    # type: () -> bool
    """
    Returns:
        bool: Whether the robot should in debug-mode.

    Note:
        Debug mode is an incredibly verbose mode that outputs a lot of data to
        the log. This will slow down your robot and may cause it to behave
        unexpectedly.
    """
    return True


def get_should_log_over_wire():
    # type: () -> bool
    """
    Controls whether the logs should be sent to the coachbot control server. If
    this is the case, then all log output is sent to the coachbot server syslog
    facility over UDP port 514. Make sure that this port is open and that
    syslog is configured to accept this.

    If this option is false, then the local syslog facility is used.

    Returns:
        bool: Whether the bot is logging over wire.
    """
    return True


def get_control_server_address():
    # type: () -> str
    """
    Returns:
        str: The IP address of the control server.
    """
    return '192.168.1.2'


def get_self_id():
    # type: () -> int
    """
    Returns:
        int: The identifying number of this coachbot.
    """
    return int(get_ip_address(get_running_interface()).split('.')[-1]) - 3


def get_control_server_rep_port():
    # type: () -> int
    """
    You should enter the port found here as it is in cctl.conf
    ``network.net_server_port_rep``.

    Returns:
        int: The port which is hosting cctl's network communication daemon.
    """
    return 16891


def get_control_server_pub_port():
    # type: () -> int
    """
    You should enter the port found here as it is in cctl.conf
    ``network.net_server_port_pub``.

    Returns:
        int: The port which is hosting cctl's network communication daemon.
    """
    return 16892


def get_self_rep_port():
    # type: () -> int
    """This is the REP port that self will be running the REP layer on.

    This should be equal to ``network.net_server_port_req`` (because cctl is
    making a REQ to this REP).
    """
    return 16893


def get_os_version():
    # type: () -> int
    """Returns the operating system version."""
    return 2


def get_legacy_configuration():
    """
    This function returns the legacy configuration from the config file. I am
    certain that this is superfluous, but I've matched the original
    implementation.

    Note:
        The operating system version has been overriden here by get_os_version.
        The config file does nothing regarding that.

    The pickle holds a list which has four elements:
    The first element is the user code version.
    The second element is the pinout of the left motor (a 4-list).
    The third element is the pinout of the right motor (a 4-list).
    The last element is the operating system version.

    Returns:
        List[any]: The legacy configuration
    """
    value = None
    with open('config', 'rb') as conf_file:
        value = pickle.load(conf_file)
    value[-1] = get_os_version()

    return value


def get_led_pinout():
    # type: () -> Dict[str, Dict[str, int]]
    """Returns the pinout of the LEDs.

    The output shape will be:

    .. code-block:: python

       {
           'red': {'pin': int},
           'green': {'pin': int},
           'blue': {'pin': int}
       }
    """
    return {
        'red': {'pin': 15, 'initial': 1},
        'green': {'pin': 16, 'initial': 1},
        'blue': {'pin': 18, 'initial': 1}
    }


def get_motor_pinout():
    # type: () -> Dict[str, Dict[str, Dict[str, int]]]
    """Returns the motor pinout as a dictionary.

    The dict returned will have the shape:

    .. code-block:: python

       {
           'left': {
            'in1': { 'pin': int, 'initial': int },
            'in2': { 'pin': int, 'initial': int },
            'pwm': { 'pin': int, 'initial': int },
            'stdby': { 'pin': int, 'initial': int }
           },
           'right': {
            'in1': { 'pin': int, 'initial': int },
            'in2': { 'pin': int, 'initial': int },
            'pwm': { 'pin': int, 'initial': int },
            'stdby': { 'pin': int, 'initial': int }
           },
       }

    Each of the entries will be a pin on the motor.
    """
    legacy_conf = get_legacy_configuration()
    return {
        'left': {
            'in1': {'pin': legacy_conf[1][0], 'initial': 1},
            'in2': {'pin': legacy_conf[1][1], 'initial': 1},
            'pwm': {'pin': legacy_conf[1][2], 'initial': 0},
            'stdby': {'pin': legacy_conf[1][3], 'initial': 0}
        },
        'right': {
            'in1': {'pin': legacy_conf[2][0], 'initial': 1},
            'in2': {'pin': legacy_conf[2][1], 'initial': 1},
            'pwm': {'pin': legacy_conf[2][2], 'initial': 0},
            'stdby': {'pin': legacy_conf[2][3], 'initial': 0}
        }
    }


def get_running_interface():
    # type: () -> str
    """Returns the interface the Coachbot is using to communicate with CCTL."""
    return 'wlan0'


def get_wheel_distance():
    # type: () -> float
    """Returns the distance between the wheels of the coachbot."""
    raise NotImplementedError()


def get_robot_radius():
    # type: () -> float
    """Returns the radius of the Coachbot."""
    raise NotImplementedError()


def get_command_server_port():
    # type: () -> int
    """Returns the binding ZMQ uses to bind to the main server."""
    return 5005


def get_com_range():
    # type: () -> float
    """Returns the communication range (in meters)."""
    return 3.5


def get_cctld_manager_host():
    # type: () -> str
    """Returns the management server path."""
    return 'tcp://192.168.1.2:16780'


def get_sensing_serial_port():
    # type: () -> str
    """Returns the UART serial RS-232 port that is used to communicate with the
    sensing vibe board.

    Note:
        The underlying system is unable to resolve symlinks. Ensure that you
        pass the full path: /dev/ttyAMA0
    """
    return '/dev/ttyAMA0'