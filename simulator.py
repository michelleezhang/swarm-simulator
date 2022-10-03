"""
Main Server for Swarm Simulation 
"""

import socket
import sys, traceback, pickle, json, select
from turtle import update
import arcade
from dataclasses import dataclass
from datetime import datetime
import time
import numpy as np
from robot_class import bot
import re
# import pygame

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM is for TCP 
server_socket.bind((socket.gethostname(),1245)) # Binds to port 1245
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
        self.delay = delay
        self.clk = clk

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
 
# def visualisation(screen, robot_id, robot_state, num_of_robot):

#     for i in range(num_of_robot+1):

#         if robot_id[i] >0:
#             robo = robot_state[i]
#             # print(robo.usr_led)
#             colour = robo.usr_led #green
#             circle_x_y = (15+i*15, 15+i*15)
#             circle_radius = 20
#             border_width = 2 #0 = filled circle

#             pygame.draw.circle(screen, colour, circle_x_y, circle_radius, border_width)
#     pygame.display.flip()

def conv_to_json(robot_state, num_of_robot):
    json_dict = {}
    for i in range(num_of_robot):
        json_dict[i] = robot_state[i].__dict__
    
    return json_dict

def update_time(robot_state, num_of_robot):

    for i in range(num_of_robot+1):
        if robot_state[i].clk < time.time():
           robot_state[i].clk = time.time()
    
    return robot_state

def loop():

    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, []) # apending reading n writing socket to list
    # serversocket, address = s.accept()
    # msg = s.recv(1024)
    # print(msg.decode("utf-8"))
    robot_id = -1*np.ones((10000))
    robot = bot_sim(id=0,usr_led=(100,100,100),clk=time.time())
    robot_state = [robot]*10000
    fd_to_id_map = {}
    sim_time_start = time.time()
    num_of_robot = 0
    (width, height) = (1500, 1000)
    # screen = pygame.display.set_mode((width, height))
    # pygame.display.flip()
    vis_fd = -1
    vis_socket = None
    while True:
        
        
        try:
            rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, []) # apending reading n writing socket to list
            sim_time_real = time.time()
            # print(rlist)
            for current_socket in rlist: # sockets that can be read
                
                if current_socket.fileno() == vis_fd:
                    print(vis_socket)
                    continue

                if current_socket.fileno() in fd_to_id_map.keys():
                    
                    if robot_state[fd_to_id_map[current_socket.fileno()]].clk > sim_time_real:
                        continue
                    # print(current_socket.fileno())

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
                            print(num_of_robot)
                            num_of_robot += 1
                            msg1 = str(bin(num_of_robot))
                            fd_to_id_map[new_socket.fileno()] = num_of_robot
                            new_socket.send(msg1.encode())
                            robot_state[num_of_robot] = bot_sim(id=num_of_robot,usr_led=(0,0,0),clk=time.time())
                        elif int(msg,2) == 5: 
                            vis_fd = new_socket.fileno()
                            vis_socket = new_socket
                            msg1 = str(bin(2))
                            print(vis_socket)
                            new_socket.send(msg1.encode())
                            print("Got vis connected")
                        elif msg == 1:
                            msg1 = str(bin(-1))
                            new_socket.send(msg.encode())
                    open_client_sockets.append(new_socket) # clients list
                else:
                    data = current_socket.recv(1024)
                    val_for_vis = '0b101'
                    if len(data) == 0:
                        gibberish = 0
                        print("Gibberish")
                        # open_client_sockets.remove(current_socket) # remove user if he quit.
                        # print("Connection with client closed.")
                        # send_waiting_messages(wlist) # send message to specfic client
                    # elif len(data) == 5:
                    #         print("enter this part")
                    #         msg1 = conv_to_json(robot_state, num_of_robot)
                    #         new_socket.send(json.dumps(msg1))
                    #         print("sent to vis")
                            # msg1 = pickle.dumps(robot_state[:num_of_robot])
                    else:
                       
                        # broadcast_message(current_socket, "\r" + '<' + data + '> ')
                        msg = msg_decode(data)
                        if msg[2] == 3:
                            robot_state[int(msg[1])].clk = time.time() + msg[3]/1000
                            data_string = '0b1'
                            current_socket.send(data_string.encode())
                            continue
                            
                        data_string = '0b1'
                        current_socket.send(data_string.encode())
                        if len(msg)>1:
                            # print(msg)
                        # print(msg)
                        # led = msg.led()
                            # if msg !=1:
                            # print(msg)
                            if msg[1] in robot_id:
                                robot = bot_sim(id=msg[1],usr_led=(msg[3],msg[4],msg[5]),clk=time.time())
                                robot_state[int(msg[1])] = robot
                            else:
                                robot_id[int(msg[1])] = msg[1]
                                robot = bot_sim(id=msg[1],usr_led=(msg[3],msg[4],msg[5]),clk=time.time())
                                robot_state[int(msg[1])] = robot
            sim_time = time.time() - sim_time_start
            
            # Only allows visualization every 0.005 seconds
            if sim_time > 0.005: 
                # print("call vis")
                if vis_fd>0:
                    # Need to change this part. Json Dumps not working. Maybe look at something else
                    msg1 = conv_to_json(robot_state, num_of_robot)
                    # msg1 = '0b1011'
                    vis_socket.sendall(json.dumps(msg1).encode('utf-8'))
                    # vis_socket.send(msg1.encode())
                    recv_msg = vis_socket.recv(1024)
                    # print(recv_msg.decode())
                # visualisation(screen, robot_id, robot_state, num_of_robot)
                sim_time_start = time.time()
            # print(time.time() - start_of_loop, " seconds ")
            # print("fd to id:", fd_to_id_map)
        
        except Exception:
            # print("Some error")
            continue
        robot_state = update_time(robot_state,num_of_robot)

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
