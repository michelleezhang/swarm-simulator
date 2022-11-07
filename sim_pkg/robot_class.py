#!/usr/bin/env python2
"""
Define Robot class that will act as an API

"""

import socket
import re
import json
import numpy as np
import math_utils
from control import MotorController, PIDController
import csv

with open('config.json', 'r') as myfile:
    data=myfile.read()
config_var = json.loads(data)
NUM_OF_MSGS = config_var["NUM_OF_MSGS"]
val = []
with open('port.csv', 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        val.append(row)
SOCKET_PORT_NUMBER = int(val[0][0])

class BotModel:
    def __init__(self):
        pass

class Coachbot:
    """
    Represents the base Coachbot
    """
    def __init__(self, id_n = -1):
        """
        Initializes coachbot
        """
        self.id_ = id_n
        self.usr_led = (0,0,0)
        self.pos_x = 3
        self.pos_y = 3
        self.clk = 0        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.settimeout(0.5)
        self.client_socket.connect((socket.gethostname(), SOCKET_PORT_NUMBER))
        self.set_id()
    
    @property
    def id(self):  # pylint: disable=invalid-name
        # type: () -> int
        """
        Facility for fetching the identification number of the current robot.
        Warning:
            For legacy reasons, this property is settable, however, you should
            never do this! **Under no circumstance** should you be modifying
            this variable in user code.
        You can use this property to return the current robot id, for example:
        .. code-block:: python
            # Set the color of bot 3 to red and others to green.
            robot.set_led(*((100, 0, 0) if robot.id == 3 else (0, 100, 0)))
        Returns:
            int: The id number of self.
        """
        return self.id_

    @property
    def math(self):
        """A convenience property for fetching the functions available in
        `coach_os.math_utils <coach_os.html#module-coach_os.math_utils>`_.
        For example, you can do:
        .. code-block:: python
           pos, theta = robot.get_pose_blocking()
           robot.logger.info(
                'My position is: %s' % (robot.math.clamp_angle(theta)))
        Returns:
            module: All functions in math_utils.
        """
        return math_utils

    @property
    def units(self):
        """
        A convenience property for fetching the functions available in
        `coach_os.units <coach_os.html#module-coach_os.units>`_.
        Example:
        .. code-block:: python
           robot.units.convert_distance(1, 'm', 'cm')  # Returns 100
        Returns:
            module: All functions in units.
        """
        # return units
        raise NotImplementedError

    @property
    def coordinates(self):
        """A convenience property for fetching the functions available in
        `coach_os.coordinates <coach_os.html#module-coach-os.coordinates>`_.
        Example:
        .. code-block:: python
           robot.coordinates.bot_in_bounds(np.ndarray([[0, 0], [0, 0]]))
        Returns:
            module: All functions in coordinates.
        """
        # return coordinates
        raise NotImplementedError

    @property
    def configuration(self):
        """
        A convenience property for fetching the functions available in
        `coach_os.configuration
        <coach_os.html#module-coach_os.configuration>`_.
        Example:
        .. code-block:: python
           robot.configuration.get_is_debug()
        Returns:
            module: All functions in configuration.
        """
        raise NotImplementedError
        # return configuration

    def set_id(self):
        """
        Sets id during initialization
        """
        data = '0b111'
        self.client_socket.sendall(data.encode('utf-8'))
        data = self.client_socket.recv(1024)
        msg = int(data.decode('utf-8'),2)
        if msg>-1:
            self.id_ = msg

    def msg_encode(self,fnc_num, data):
        """
        Encodes data
        """
        client = str(bin(2))
        robot_id = str((bin(self.id_)))
        fnc = str(bin(fnc_num))
        packet = client+robot_id+fnc+data
        return packet.encode('utf-8')
    
    def msg_decode(self,msg):
        """
        Decodes data
        """
        packet = msg.decode('utf-8')
        result = [_.start() for _ in re.finditer('0b', packet)] 
        result.append(len(packet))
        data_arr = []
        for i in range(len(result)-1):
            num = packet[result[i]:result[i+1]]
            num = int(num,2)
            data_arr.append(num)
    
        return data_arr

    def send_data(self,fnc_num,data):
        """
        Sends data
        """
        data_string = self.msg_encode(fnc_num,data)
        self.client_socket.sendall(data_string)
        data = self.client_socket.recv(1024)
        # msg = self.msg_decode(data)

    def set_led(self,r,g,b):
        # type: (int, int, int) -> None
        """ Sets the color of the onboard LED.
        Note:
            Function number  - 2
            This function **does not accept values between 0-255**. Allowable
            values are between 0 - 100.
        Parameters:
            r (int): red value (0 - 100).
            g (int): green value (0 - 100).
            b (int): blue value (0 - 100).
        """
        m_range = (0, 100)
        self.usr_led = (r,g,b)
        info = str(bin(r)) + str(bin(g)) + str(bin(b))
        self.send_data(2,info)

    def delay(self, delay_time=200):
        # type: (float) -> None
        """Waits some milliseconds (default 200).
        Function number  - 3
        Parameters:
            millis: The amount of time to wait.
        """
        info = str(bin(delay_time))
        self.send_data(3,info)
    
    def set_vel(self, left, right):
        # type: (int|float, int|float) -> None
        """
        Sets the speed for the left and right wheel in percentage values.
        Function Number 7
        Parameters:
            left (int): The left motor speed (-100 - 100)
            right (int): The right motor speed (-100 - 100)
        """
        # info = str(bin(left))+ str(bin(right))
        info = "0bset_val"
        self.send_data(7,info)
        if left > 100:
            left = 100
        elif left < -100:
            left = -100
        if right > 100:
            right = 100
        elif right < -100:
            right = -100
        val = [left, right]
        val = json.dumps(val)
        self.client_socket.sendall(val.encode('utf-8'))
        msg = self.client_socket.recv(1024)

    def move_meters(self, position, max_error=1e-1):
        # type: (Vec2, float) -> None
        """
        Moves the coachbot by the given position vector.
        Note:
            This is a blocking operation.
        Todo:
            This function has an incorrect implementation.
        Parameters:
            position (Vec2): The vector describing the displacement of the
            Coachbot.
        """
        current_pos, current_theta = self.get_pose_blocking()
        target_pos = current_pos + position
        # self.logger.debug('move_meters: My target position is %s', target_pos)

        # This vector represents the vector from the current position to the
        # target position.
        delta_pos = target_pos - current_pos

        self.rotate_to_theta(position.angle())

        angle_controller = PIDController((1.0, 2.0, 1e-1),
                                         current_theta, delta_pos.angle(),
                                         circle_max=np.pi)
        distance_controller = PIDController((-80.0, -40.0, 0.0),
                                            abs(delta_pos), 0.0)

        while abs(distance_controller.last_error) > max_error:
            current_pos, current_theta = self.get_pose_blocking(10.0)
            delta_pos = target_pos - current_pos

            speed = distance_controller.step(abs(delta_pos))

            angle_controller.set_point = delta_pos.angle()
            angle = angle_controller.step(current_theta)

            pow_l, pow_r = \
                MotorController.power_from_relative_angle_speed(angle, speed)

            # self.logger.debug('move_meters: current_pos: %s; '
            #                   'current_theta: %s; delta_pos: %s; speed: %s; '
            #                   'angle: %s; pow_l: %s; pow_r: %s',
            #                   current_pos, current_theta, delta_pos, speed,
            #                   angle, pow_l, pow_r)

            self.set_vel(pow_l, pow_r)

    def get_clock(self):
        # type: () -> float
        """
        Function number 6
        Returns:
            float: The time elapsed since the program started in seconds.
        """
        info = '0btime'
        # print("In recv_msg")
        self.send_data(6,info)
        data_string = str("sim_time")
        self.client_socket.sendall(data_string.encode('utf-8'))
        msg = self.client_socket.recv(4*1024)
        msg = msg.decode('utf-8')
        msg = float(msg)
        return msg

    def send_msg(self, msg):
        # type: (bytes) -> bool
        """Attempts to transmit the given message returning whether it was
        successful.
        Function number  - 4
        Parameters:
            msg (bytes): The message to attempt to transmit. This message must be
            of size ``coach_os.custom_net.MSG_LEN - 8`` or shorter. Longer
            messages are trimmed. The ``-8`` is here due to being a legacy bug.
        """
        
        if type(msg) == str:
            info = 'str'
            # msg = msg.encode('utf-8')
        else:
            info = 'bytes'
        info = '0b'+info
        self.send_data(4,info)
        self.client_socket.sendall(msg)
        msg = self.client_socket.recv(1024)
        return True


    def recv_msg(self, clear=True):
        # type: (bool) -> list
        """
        Reads up to ``custom_net.talk.MAX_MSG_NUM`` messages since the last
        invokation. If this function does not have any new updates to send, it
        will return an empty list.
        Function number  - 5
        Parameters:
            clear (bool): Whether to clear the message buffer after reading.
        Returns:
            list[str]: Up to ``custom_net.MAX_MSG_NUM`` messages since last
            invokation.
        """
        info = '0bdata'
        # print("In recv_msg")
        data_string = self.msg_encode(5,info)
        self.client_socket.sendall(data_string)
        num = self.client_socket.recv(1024)
        num = int(num.decode('utf-8'))
        # print("Sent data. Now waiting for msg")
        data_string = str(clear)
        self.client_socket.sendall(data_string.encode('utf-8'))
        lst = []
        check_data_ = self.client_socket.recv(4*1024)
       

        for j in range(num):
            data_string = '0b1'
            self.client_socket.sendall(data_string.encode('utf-8'))

            msg = self.client_socket.recv(4*1024)
            # msg = msg.decode('utf-8')
            
            # msg = json.loads(msg)
            
            
            lst.append(msg)
            
        # print(lst)
        return lst


    def get_pose(self):
        #  type: () -> tuple[float, float, float] | None
        """
        This function retrieves the pose of the robot, if it can. If it can't
        it returns None.
        Function number - 8
        Returns:
            tuple[float, float, float] | None: The global pose as a tuple (x,
            y, theta) if new data available since last invokation, None
            otherwise.
        """
        info = '0bpose'
        # print("In recv_msg")
        self.send_data(8,info)
        data_string = 'new_pose'
        self.client_socket.sendall(data_string.encode('utf-8'))
        msg = self.client_socket.recv(int(NUM_OF_MSGS*1024))
        msg = msg.decode('utf-8')
        msg = json.loads(msg)
        return msg
        

    def get_pose_blocking(self, delay_millis=200.0):
        # type: (float) -> tuple[Vec2, float]
        """
        Returns the pose of the bot. This function waits until data is
        available.
        Warning:
            This function may enter a state where no data can be retrieved.
            This can occur when the robot exits the bounds of the playpen. In
            that case, this function will simply **block execution**.
        Returns:
            tuple[Vec2, float]: The pos_x, pos_y, theta of the robot.
        """
        pos_x_, pos_y_, angle =  self.get_pose()
        return (math_utils.Vec2(pos_x_,pos_y_), angle)
    
    def rotate_with_power(self, power):
        # type: (int) -> None
        """Rotates the Coachbot in place with power. Positive power rotates
        CCW, while negative power rotates CW.
        Parameters:
            power (int): The amount of power to rotate to Coachbot with.
        """
        self.set_vel(-power, power)

    def rotate_to_theta(self, theta, max_error=1e-1,
                        pid_coeffs=(100.0, 10.0, 1.0)):
        # type: (float, float, Tuple[float, float, float]) -> None
        """Rotates the Coachbot in place to a target theta. Blocks.
        Parameters:
            theta (float): The target theta to rotate to.
            max_error (float): The maximum acceptable error.
        """
        _, current_theta = self.get_pose_blocking()

        controller = PIDController(pid_coeffs, current_theta, theta,
                                   circle_max=np.pi)
        controller.max_value = 100.0

        while abs(controller.last_error) > max_error:
            _, current_theta = self.get_pose_blocking(10.0)

            power = controller.step(current_theta)

            # self.logger.debug('rotate_to_theta: Rotating from %s to %s; '
            #                   'power: %s; error: %s',
            #                   current_theta, theta, power,
            #                   controller.last_error)

            self.rotate_with_power(int(power))
