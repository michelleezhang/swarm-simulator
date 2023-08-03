#!/usr/bin/env python2
import base64

class Coachbot():
    def __init__(self, bot_client, msg_type, id_n=-1, a_ids=-1):
        '''
        Define API for Coachbots
        When a method is called, it sends a request to the simulator. For some methods, it receives a response back and returns it
        Each method is identified by a unique number, allowing the simulator and coachbot to coordinate what data should be interchanged
            1: set_led
            2: set_vel
            3: get_clock
            4: get_pose
            5: send_msg
            6: recv_msg
            7: stop_sim
            8: delay
        '''
        self.assigned_id = a_ids 
        self.id = id_n
        self.bot_client = bot_client

        # TODO: can only send messages of the same type for a given usr file 
        if msg_type == 0:
            self.msg_type = str
        elif msg_type == 1:
            self.msg_type = bytes

    def set_led(self, r, g, b):
        payload = {
            "id": self.id,
            "function": 1,
            "params": (r, g, b)
        }
        self.bot_client.send(payload)
    
    def set_vel(self, left, right):
        # Scale left and right values -- upper bound at 100, lower bound at -100
        left = min(max(left, -100), 100)
        right = min(max(right, -100), 100)

        payload = {
            "id": self.id,
            "function": 2,
            "params": (left, right)
        }
        self.bot_client.send(payload)

    def get_clock(self):
        payload = {
            "id": self.id,
            "function": 3
        }
        response = self.bot_client.send(payload)
        return float(response["response"])
    
    def get_pose(self):
        payload = {
            "id": self.id,
            "function": 4
        }
        response = self.bot_client.send(payload)
        return response["response"] 
    
    def send_msg(self, msg):
        if type(msg) == bytes:
            self.msg_type = bytes
            msg = base64.b64encode(msg).decode("utf-8") # Unpack -- bytes can't be serialized
        elif type(msg) == str:
            self.msg_type = str
    
        payload = {
            "id": self.id,
            "function": 5,
            "params": msg
        }
   
        self.bot_client.send(payload)

    def recv_msg(self, clear=True):
        # TODO: clear doesn't seem to do anything
        payload = {
            "id": self.id,
            "function": 6
        }
        response = self.bot_client.send(payload)

        msg_buffer = response["response"]

        if self.msg_type == str:
            return msg_buffer
        
        list = []
        for msg in msg_buffer:
            msg = base64.b64decode(msg)
            list.append(msg)
        return list

    def stop_sim(self):
        payload = {
            "id": self.id,
            "function": 7
        }
        self.bot_client.send(payload)
    
    def delay(self, delay_time):
        payload = {
            "id": self.id,
            "function": 8,
            "params": delay_time
        }
        self.bot_client.send(payload)