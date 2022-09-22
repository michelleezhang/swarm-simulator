import socket
import sys, traceback, pickle, json, select
import arcade
from dataclasses import dataclass
from datetime import datetime
from time import sleep
import numpy as np
from robot_class import bot
import re
import pygame

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(),1245))
server_socket.listen(1)
open_client_sockets = [] # current clients handler
messages_to_send = [] # future message send handler

def msg_decode(msg):

    packet = msg.decode()
    result = [_.start() for _ in re.finditer('0b', packet)] 
    result.append(len(packet))
    data_arr = []
    for i in range(len(result)-1):
        num = packet[result[i]:result[i+1]]
        num = int(num,2)
        data_arr.append(num)
    
    return data_arr

class bot_sim:
    def __init__(self, id, usr_led,clk,delay=0):
        self.id = id
        self.usr_led = usr_led
        self.pos_x = 3
        self.pos_y = 3
        self.clk = clk
        self.delay = delay
        # self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.connect((socket.gethostname(), 1234))
        # self.s.bind((socket.gethostname(),1234))
        # self.s.listen(5)
        # self.clientsocket, self.address = self.s.accept()

def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist: # if current socket in iteration has reading abilities
            client_socket.send(data)
            messages_to_send.remove(message) # remove from future send handler

def broadcast_message(sock, message):
    for socket in open_client_sockets:
        if socket != server_socket and socket != sock:
            socket.send(message)

def init():
#     SCREEN_WIDTH = 600
#     SCREEN_HEIGHT = 600

# # Open the window. Set the window title and dimensions (width and height)
#     arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Swarms")
#     arcade.set_background_color(arcade.color.WHITE)
#     arcade.start_render()
    (width, height) = (300, 200)
    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()

def visualisation(screen, robot_id, robot_state):

    for i in range(len(robot_id)):

        if robot_id[i] >0:
            robo = robot_state[i]
            print(robo.usr_led)
            colour = robo.usr_led #green
            circle_x_y = (i*2, i*2)
            circle_radius = 8
            border_width = 1 #0 = filled circle

            pygame.draw.circle(screen, colour, circle_x_y, circle_radius, border_width)
            pygame.display.flip()
            
def loop():
    
    
    # init()
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, []) # apending reading n writing socket to list
    # serversocket, address = s.accept()
    # msg = s.recv(1024)
    # print(msg.decode("utf-8"))
    robot_id = -1*np.ones((10000))
    robot = bot_sim(id=0,usr_led=(100,100,100),clk=datetime.now())
    robot_state = [robot]*10000

    sim_time_start = datetime.now()
    num_of_robot = 0
    
    (width, height) = (1500, 1000)
    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()

    while True:
        sim_time = datetime.now() - sim_time_start
        
        try:
            rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, []) # apending reading n writing socket to list

            for current_socket in rlist: # sockets that can be read
                if current_socket is server_socket: # if there is a new client
                    (new_socket, address) = server_socket.accept() 
                    try:
                        data = new_socket.recv(1024)
                    except Exception:
                        data = '0b0'
                        data = data.encode()
                    
                    if len(data) != 0:
                        msg = data.decode()
                        # print(msg)
                        if int(msg,2) ==7:
                            # print(num_of_robot)
                            num_of_robot += 1
                            msg1 = str(bin(num_of_robot))
                            new_socket.send(msg1.encode())
                        elif msg == 1:
                            msg1 = str(bin(-1))
                            new_socket.send(msg.encode())
                    open_client_sockets.append(new_socket) # clients list
                else:
                    data = current_socket.recv(1024)
                    if len(data) == 0:
                        open_client_sockets.remove(current_socket) # remove user if he quit.
                        print("Connection with client closed.")
                        # send_waiting_messages(wlist) # send message to specfic client

                    else:
                       
                        # broadcast_message(current_socket, "\r" + '<' + data + '> ')
                        # msg = pickle.loads(data)
                        # print(msg)
                        # msg1 = pickle.dumps((3))
                        msg = msg_decode(data)
                        data_string = '0b1'
                        current_socket.send(data_string.encode())
                        if len(msg)>1:
                            # print(msg)
                        # print(msg)
                        # led = msg.led()
                            # if msg !=1:
                            # print(msg)
                            if msg[1] in robot_id:
                                robot = bot_sim(id=msg[1],usr_led=(msg[3],msg[4],msg[5]),clk=datetime.now())
                                robot_state[int(msg[1])] = robot
                            else:
                                robot_id[int(msg[1])] = msg[1]
                                robot = bot_sim(id=msg[1],usr_led=(msg[3],msg[4],msg[5]),clk=datetime.now())
                                robot_state[int(msg[1])] = robot
            visualisation(screen, robot_id, robot_state)
            
        except Exception:
            print("Some error")

        # visualisation(screen, robot_id, robot_state)
        
    server_socket.close()

def main():
    try:
       loop()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
