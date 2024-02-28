#!/usr/bin/env python2
import os
import base64
import time
import csv

class Coachbot():
    def __init__(self, bot_client, msg_type, id_n=-1, a_ids=-1, log_file=None):
        '''
        Define API for Coachbots
        When a method is called, it sends a request to the simulator. For some methods, it receives a response back and returns it
        Each method (except log) is identified by a unique number, allowing the simulator and coachbot to coordinate what data should be interchanged
            1: set_led
            2: set_vel
            3: get_clock
            4: get_pose
            5: send_msg
            6: recv_msg
            7: stop_sim
            8: delay
            9: start_new_loop
            10: pause_spawning
            _: log
        '''
        self.virtual_id = a_ids 
        self.id = id_n
        self.bot_client = bot_client
        self.log_file = log_file

        # TODO: can only send messages of the same type for a given usr file 
        if msg_type == 0:
            self.msg_type = str
        elif msg_type == 1:
            self.msg_type = bytes

    def set_led(self, r, g, b):
        payload = {
            "id": self.id,
            "function": 1,
            "params": (r, g, b),
            "time": time.time()
        }
        self.bot_client.send(payload)
    
    def set_vel(self, left, right):
        # Scale left and right values -- upper bound at 100, lower bound at -100
        left = min(max(left, -100), 100)
        right = min(max(right, -100), 100)

        payload = {
            "id": self.id,
            "function": 2,
            "params": (left, right),
            "time": time.time()
        }
        self.bot_client.send(payload)

    def get_clock(self):
        payload = {
            "id": self.id,
            "function": 3,
            "time": time.time()
        }
        response = self.bot_client.send(payload)
        return float(response["response"])
    
    def get_pose(self):
        payload = {
            "id": self.id,
            "function": 4,
            "time": time.time()
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
            "params": msg,
            "time": time.time()
        }
   
        self.bot_client.send(payload)

    def recv_msg(self, clear=True):
        # TODO: clear doesn't seem to do anything
        payload = {
            "id": self.id,
            "function": 6,
            "time": time.time()
        }
        response = self.bot_client.send(payload)

        msg_buffer = response["response"]

        if msg_buffer:
            if self.msg_type == str:
                return msg_buffer
            
            list = []
            for msg in msg_buffer:
                msg = base64.b64decode(msg)
                list.append(msg)
            return list
        else: # In client_server.py, we have it so that if response["response"] == False, then that means the socket is already closed
            return []

    def stop_sim(self):
        payload = {
            "id": self.id,
            "function": 7,
            "time": time.time()
        }
        self.bot_client.send(payload)
    
    def delay(self, delay_time=20):
        payload = {
            "id": self.id,
            "function": 8,
            "params": delay_time,
            "time": time.time()
        }
        self.bot_client.send(payload)

    def start_new_loop(self,delay_time=20):
        payload = {
            "id": self.id,
            "function": 9,
            "params": delay_time,
            "time": time.time()
        }
        self.bot_client.manage_thread(payload)

    def log(self, message, log_file=None):
        '''
        Log robot messages
        '''
        log_directory = "coachbot_logs"
        os.makedirs(log_directory, exist_ok=True) # If it doesn't already exist, create a folder to store bot logs

        if log_file == None:
            if self.log_file == None:
                log_file = f"{self.virtual_id}_{self.id}_log.csv"
            else:
                log_file = self.log_file + ".csv"

        log_path = f"{log_directory}/{log_file}"

        if type(message) == str:
            csv_payload = [message]
        else:
            csv_payload = message

        try:
            with open(log_path, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(csv_payload)
        except FileNotFoundError:
             with open(log_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(csv_payload)
    
    def send_start_time(self, start_time):
        payload = {
            "id": self.id,
            "function": 0,
            "params": start_time,
            "time": time.time()
        }
        self.bot_client.send(payload)
    
    def pause_spawning(self, pause_length):
        payload = {
            "id": self.id,
            "function": 10,
            "params": pause_length,
            "time": time.time()
        }
        self.bot_client.send(payload)
