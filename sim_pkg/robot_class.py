#!/usr/bin/env python2
"""
Define Robot class that will act as an API
"""

# from dataclasses import dataclass
# from time import sleep
import time
import socket
# import sys, traceback, pickle, json, select
import re


# @dataclass
# class Data:
#     timestamp = time.time()
#     led: tuple
#     delay: int
#     id: int

class bot:
    def __init__(self, usr_led, id_n = -1):
        self.id = id_n
        self.usr_led = usr_led
        self.pos_x = 3
        self.pos_y = 3
        self.clk = 0        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.settimeout(0.5)
        self.client_socket.connect((socket.gethostname(), 1245))
        self.set_id()
    
    def set_id(self):
        data = '0b111'
        self.client_socket.sendall(data.encode())
        data = self.client_socket.recv(1024)
        msg = int(data.decode(),2)
        if msg>0:
            self.id = msg

    def msg_encode(self,fnc_num, data):
        
        client = str(bin(2))
        robot_id = str((bin(self.id)))
        fnc = str(bin(fnc_num))
        packet = client+robot_id+fnc+data
        return packet.encode()
    
    def msg_decode(self,msg):
        packet = msg.decode()
        result = [_.start() for _ in re.finditer('0b', packet)] 
        result.append(len(packet))
        data_arr = []
        for i in range(len(result)-1):
            num = packet[result[i]:result[i+1]]
            num = int(num,2)
            data_arr.append(num)
    
        return data_arr

    def send_data(self,fnc_num,data):
        data_string = self.msg_encode(fnc_num,data)
        self.client_socket.sendall(data_string)
        data = self.client_socket.recv(1024)
        msg = self.msg_decode(data)

    def set_led(self,r,g,b):
        m_range = (0, 100)
        self.usr_led = (r,g,b)
        info = str(bin(r)) + str(bin(g)) + str(bin(b))
        self.send_data(2,info)

    def delay(self, delay_time):
        info = str(bin(delay_time))
        self.send_data(3,info)
    
    def set_vel(self, left, right):
        # type: (int|float, int|float) -> None
        """
        Sets the speed for the left and right wheel in percentage values.
        Parameters:
            left (int): The left motor speed (-100 - 100)
            right (int): The right motor speed (-100 - 100)
        """
        return None

    def rotate_with_power(self, power):
        # type: (int) -> None
        """Rotates the Coachbot in place with power. Positive power rotates
        CCW, while negative power rotates CW.
        Parameters:
            power (int): The amount of power to rotate to Coachbot with.
        """
        return None
        

    def rotate_to_theta(self, theta, max_error=1e-1,
                        pid_coeffs=(100.0, 10.0, 1.0)):
        # type: (float, float, Tuple[float, float, float]) -> None
        """Rotates the Coachbot in place to a target theta. Blocks.
        Parameters:
            theta (float): The target theta to rotate to.
            max_error (float): The maximum acceptable error.
        """
        

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
        return None

    def get_clock(self):
        # type: () -> float
        """
        Returns:
            float: The time elapsed since the program started in seconds.
        """
        return None

    def send_msg(self, msg):
        # type: (str) -> bool
        """Attempts to transmit the given message returning whether it was
        successful.
        Parameters:
            msg (str): The message to attempt to transmit. This message must be
            of size ``coach_os.custom_net.MSG_LEN - 8`` or shorter. Longer
            messages are trimmed. The ``-8`` is here due to being a legacy bug.
        """
        return None

    def recv_msg(self, clear=False):
        # type: (bool) -> list[str]
        """
        Reads up to ``custom_net.talk.MAX_MSG_NUM`` messages since the last
        invokation. If this function does not have any new updates to send, it
        will return an empty list.
        Parameters:
            clear (bool): Whether to clear the message buffer after reading.
        Returns:
            list[str]: Up to ``custom_net.MAX_MSG_NUM`` messages since last
            invokation.
        """
        return None

    def get_pose(self):
        #  type: () -> tuple[float, float, float] | None
        """
        This function retrieves the pose of the robot, if it can. If it can't
        it returns None.
        Returns:
            tuple[float, float, float] | None: The global pose as a tuple (x,
            y, theta) if new data available since last invokation, None
            otherwise.
        """
        return None
        

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
        return None
