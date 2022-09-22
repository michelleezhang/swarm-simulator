from dataclasses import dataclass
from datetime import date, datetime
from time import sleep
import time
import socket
import sys, traceback, pickle, json, select
import re


@dataclass
class Data:
    timestamp = datetime.now()
    led: tuple
    delay: int
    id: int

class bot:
    def __init__(self, usr_led, id_n = -1):
        self.id = id_n
        self.usr_led = usr_led
        self.pos_x = 3
        self.pos_y = 3
        self.clk = 0
        # self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.settimeout(0.5)
        self.client_socket.connect((socket.gethostname(), 1245))
        self.set_id()
        # data = 0
        # data_string = pickle.dumps((data))
        # self.client_socket.send(data_string)
        # data = self.client_socket.recv(1024)
        # msg = pickle.loads(data)
        # self.id = msg
        # self.s.bind((socket.gethostname(),1234))
        # self.s.listen(5)
        # self.clientsocket, self.address = self.s.accept()
    
    def set_id(self):
        data = '0b111'
        self.client_socket.send(data.encode())
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
        flag = True
        while flag == True:
            # ready = select.select([self.client_socket], [], [], .1)
            data_string = self.msg_encode(fnc_num,data)
            # data_string = pickle.dumps((data))
            self.client_socket.send(data_string)
            data = self.client_socket.recv(1024)
            msg = self.msg_decode(data)
            # msg = pickle.loads(data)
            # print(msg)
            
            flag = False


    def set_led(self,r,g,b):
        m_range = (0, 100)
        self.usr_led = (r,g,b)
        info = str(bin(r)) + str(bin(g)) + str(bin(b))
        # data = Data(led=self.usr_led, delay=0, id = self.id)
        self.send_data(2,info)

    def delay(self, delay):
        # time in milliseconds
        timeout = time.time()*1000 + delay - 5
        # self.client_socket.close()
        flag = True
        while flag:
            # data_string = pickle.dumps((1))
            data_string = '0b11'
            self.client_socket.send(data_string.encode())
            data = self.client_socket.recv(1024)
            msg = self.msg_decode(data)
            # print(msg)
            if time.time()*1000 > timeout:
                flag = False
                break
            # print("Delay done")
            
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.connect((socket.gethostname(), 1245))
        
        # data = self.client_socket.recv(1024)
        # msg = pickle.loads(data)
        # print(msg)
        self.clk = self.clk+delay