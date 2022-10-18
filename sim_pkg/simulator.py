#!/usr/bin/env python3
"""
Main Server for Swarm Simulation 
"""

import socket
import sys
import json
import select
import time
import re
import numpy as np
import csv
from itertools import chain
# import pygame
# file = open('time.csv','w')
# writer = csv.writer(file)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM is for TCP 
server_socket.bind((socket.gethostname(),1245)) # Binds to port 1245
server_socket.listen(1)
open_client_sockets = [] # current clients handler
messages_to_send = [] # future message send handler
elapsedDIffList = []

with open('config.json', 'r') as myfile:
    data=myfile.read()
config_var = json.loads(data)
RADIUS_OF_VISIBILITY = config_var["RADIUS_OF_VISIBILITY"]
PACKET_SUCCESS_PERC = config_var["PACKET_SUCCESS_PERC"]
NUM_OF_ROBOTS = config_var["number_of_robots"]

class BotDiffDrive:
    """
    Bot Diff Drive robot with all the math
    """
    def __init__(self):
        """
        Define base variables. 
        All values are expected in metres, seconds and radians. 
        """
        self.pos_x = 0 
        self.pos_y = 0 
        self.pos_angle = 0 
        self.left_wheel_angle = 0
        self.right_wheel_angle = 0 
        self.radius_of_wheel = 0.5
        self.distance_between_wheel = 0.5
        

    def integrate(self,u_left, u_right, delta_time):
        """
        Integrate the state of robot
        """
        state_matrix = np.array([[-self.radius_of_wheel/(2*self.distance_between_wheel), self.radius_of_wheel/(2*self.distance_between_wheel)], 
                                 [self.radius_of_wheel*np.cos(self.pos_angle)/2, self.radius_of_wheel*np.cos(self.pos_angle)/2], 
                                 [self.radius_of_wheel*np.sin(self.pos_angle)/2, self.radius_of_wheel*np.sin(self.pos_angle)/2],
                                 [1, 0],
                                 [0, 1] ])
        
        velocity_vector = np.array([[u_left],[u_right]])

        delta_pos = state_matrix@velocity_vector * delta_time

        self.pos_angle += delta_pos[0][0]
        self.pos_x += delta_pos[0][1]
        self.pos_y += delta_pos[0][2]
        self.left_wheel_angle += delta_pos[0][3]
        self.right_wheel_angle += delta_pos[0][4]

        


def msg_decode(msg: bytes) -> list:
    """
    Decodes the message
    """
    packet = msg.decode('utf-8')
    # print("Stuff")
    # print(packet)
    result = [_.start() for _ in re.finditer('0b', packet)] 
    
    result.append(len(packet))
    data_arr = []
    for i in range(len(result)-1):
        num = packet[result[i]:result[i+1]]
        if num[2] == '1' or num[2] == '0':
            # print(num)
            num = int(num,2)
            data_arr.append(num) 
        else:
            data_arr.append(num[2:])  
    # print(data_arr)
    return data_arr

class BotSim:
    """
    Defines Bot Class for simulation    
    """
    def __init__(self, id, usr_led,clk,delay=0):
        self.id = id
        self.usr_led = usr_led
        self.pos_x = 3+id*12
        self.pos_y = 3+id*12
        self.delay = delay
        self.clk = clk

def conv_to_json(robot_state, num_of_robot:int)->dict:
    """
    Convert data to dict so that it can be json dumped
    """
    json_dict = {}
    for i in range(1,num_of_robot+1):
        json_dict[i] = robot_state[i].__dict__
    # print(json_dict)
    return json_dict

def update_time(robot_state:list, num_of_robot:int, sim_time:float)-> list:
    """
    Updates time of robot clocks
    """
    for i in range(1,num_of_robot+1):
        if robot_state[i].clk < sim_time:
           robot_state[i].clk = sim_time
    
    return robot_state

def update_msg_buffer(msg_buffer:list, MSG_BUFFER_SIZE:int, num_of_robot:int,msg:bytes, robot_id:int,robot_states:list)->list:
    """
    Update Message Buffer
    """
    ref_x = robot_states[robot_id].pos_x
    ref_y = robot_states[robot_id].pos_y
    # print("In update_msg_buffer")

    if robot_id == num_of_robot:
        range_of_val = range(1,robot_id+1)
    else:
        range_of_val = chain(range(1,robot_id),range(robot_id+1,num_of_robot+1))
    # print("Range of val:", range_of_val)
    for i in range_of_val:
        curr_pos_x = robot_states[i].pos_x
        curr_pos_y = robot_states[i].pos_y
        d = np.sqrt((ref_x - curr_pos_x)**2 + (ref_y - curr_pos_y)**2)
        if d < RADIUS_OF_VISIBILITY:
            msg_buffer[i] = msg_buffer[i]+ msg
            if len(msg_buffer[i]) > MSG_BUFFER_SIZE:
                msg_buffer[i] = msg_buffer[i][-MSG_BUFFER_SIZE:]
    # print(type(msg_buffer[2]))
    return msg_buffer

def initialize_robots():
    """
    Initialize the number of robots
    """
    flag = True
    vis_fd = -1
    vis_socket = None
    fd_to_id_map = {}
    num_of_robot = 0
    real_time_factor = config_var["REAL_TIME_FACTOR"]
    robot = BotSim(id=0,usr_led=(0,0,0),clk=0)
    robot_state = [robot]*(NUM_OF_ROBOTS+1)
    robot_id = -1*np.ones((NUM_OF_ROBOTS+1))
    id_to_socket_map = {}
    while flag:
        try:
            rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, []) # apending reading n writing socket to list
            for current_socket in rlist: 
                if current_socket is server_socket: # if there is a new client
                    (new_socket, address) = server_socket.accept() 
                    try:
                        data = new_socket.recv(1024)
                    except Exception:
                        data = '0b0'
                        data = data.encode('utf-8')
                    # sim_ticks +=1
                    if len(data) != 0:
                        msg = data.decode('utf-8')
                        
                        # print(msg)
                        if int(msg,2) ==7:
                            
                            num_of_robot += 1
                            # print(fd_to_id_map)
                            id_to_socket_map[num_of_robot] = new_socket
                            # msg1 = str(bin(num_of_robot))
                            fd_to_id_map[new_socket.fileno()] = num_of_robot
                            # new_socket.sendall(msg1.encode('utf-8'))
                            robot_state[num_of_robot] = BotSim(id=num_of_robot,usr_led=(50,50,50),clk=0)
                            robot_id[num_of_robot] = num_of_robot
                        elif int(msg,2) == 5:
                            vis_fd = new_socket.fileno()
                            vis_socket = new_socket
                            msg1 = str(real_time_factor)
                            # print(vis_socket)
                            new_socket.sendall(msg1.encode('utf-8'))
                            print("Got vis connected")
                        elif msg == 1:
                            msg1 = str(bin(-1))
                            new_socket.sendall(msg.encode('utf-8'))
                    open_client_sockets.append(new_socket) # clients list
                
                
                
        except Exception:
            continue
        if num_of_robot == NUM_OF_ROBOTS and vis_fd>0:
            # print("DONE")
            flag = False
    
    for key, curr_socket in id_to_socket_map.items():
        msg1 = str(bin(key))
        # fd_to_id_map[new_socket.fileno()] = num_of_robot
        curr_socket.sendall(msg1.encode('utf-8'))
    
    # print(id_to_socket_map)


    return vis_fd, vis_socket, fd_to_id_map, robot_state, robot_id

def loop():
    """
    Loop through to get data from bot classes
    """
    # rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, []) # apending reading n writing socket to list
    # serversocket, address = s.accept()
    # msg = s.recv(1024)
    # print(msg.decode("utf-8"))
    
    
    
    sim_time_start = time.time()
    notslept = 0
    real_time_factor = config_var["REAL_TIME_FACTOR"]
    T_real = 0.0001
    T_sim = real_time_factor*T_real
    
    # sim_ticks = 0 
    # sim_time_or = time.time()
    sim_time_curr = 0.0001
    # robot = BotSim(id=0,usr_led=(0,0,0),clk=sim_time_curr)
    # robot_state = [robot]*NUM_OF_ROBOTS
    
    delta_vis = 0
    real_time_curr = 0
    msg_buffer = [bytes('0','utf-8')]*1000
    MSG_BUFFER_SIZE = 1024
    num_of_robot = NUM_OF_ROBOTS
    vis_fd, vis_socket, fd_to_id_map, robot_state, robot_id = initialize_robots()
    while True:
        
        real_time_now_start = time.time()
        try:
            rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, []) # apending reading n writing socket to list
            # sim_time_real = time.time()
            # print(rlist)
            for current_socket in rlist: # sockets that can be read
                # print("In Loop")
                if current_socket.fileno() == vis_fd:
                    # print(vis_socket)
                    continue

                if current_socket.fileno() in fd_to_id_map.keys():
                    
                    if robot_state[fd_to_id_map[current_socket.fileno()]].clk > sim_time_curr:
                        continue
                    # print(current_socket.fileno())
                data = current_socket.recv(4*1024)
                if len(data) == 0:
                    gibberish = 0
                    print("Gibberish")
                else:
                    
                    # broadcast_message(current_socket, "\r" + '<' + data + '> ')
                    msg = msg_decode(data)
                    if msg[2] == 3:
                        robot_state[int(msg[1])].clk += (msg[3]/1000)
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        continue
                    elif msg[2] == 4:
                        # print('Message sent:',msg[3])
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        msg_for_buffer = bytes(msg[3],'utf-8')
                        random_bool = np.random.uniform() < PACKET_SUCCESS_PERC
                        if random_bool is True:
                            msg_buffer = update_msg_buffer(msg_buffer,MSG_BUFFER_SIZE,num_of_robot,msg_for_buffer,msg[1],robot_state)
                        # print("New msg buffer:", msg_buffer)
                        continue
                    elif msg[2] == 5:
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        # print(type(msg_buffer))
                        clear_bool = current_socket.recv(1024)
                        current_socket.sendall(msg_buffer[msg[1]])
                        if clear_bool.decode('utf-8') == 'True':
                            msg_buffer[msg[1]] = bytes('0','utf-8')
                        # print('Send data:')
                        continue
                    elif msg[2] == 6:
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        type_time = current_socket.recv(1024)
                        time_val = robot_state[int(msg[1])].clk
                        time_val = str(round(time_val,4))
                        current_socket.sendall(time_val.encode('utf-8'))
                    elif msg[2] == 2:
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        if msg[1] in robot_id:
                            usr_led_ = (msg[3],msg[4],msg[5])
                            robot_state[int(msg[1])].usr_led = usr_led_
                            # else:
                            #     print("FLAG")
                            #     robot_id[int(msg[1])] = msg[1]
                            #     robot = BotSim(id=msg[1],usr_led=(msg[3],msg[4],msg[5]),clk=sim_time_curr)
                            #     robot_state[int(msg[1])] = robot
                    # data_csv = [sim_ticks,time.time()-sim_time_or]
                # writer.writerow(data_csv)
            # sim_time = time.time() - sim_time_start
            
            # Only allows visualization every 0.005 seconds
            delta_vis += T_real
            if delta_vis > 0.005: 
                # print("call vis")
                delta_vis = 0
                if vis_fd>0:
                    # Need to change this part. Json Dumps not working. Maybe look at something else
                    msg1 = conv_to_json(robot_state, num_of_robot)
                    # msg1 = '0b1011'
                    vis_socket.sendall(json.dumps(msg1).encode('utf-8'))
                    # sim_ticks +=1
                    # vis_socket.send(msg1.encode('utf-8'))
                    recv_msg = vis_socket.recv(1024)
                    
                    # Send time to visualization
                    data_string = str(sim_time_curr) + '0b0' + str(real_time_curr)
                    vis_socket.sendall(data_string.encode('utf-8'))
                    # print(recv_msg.decode('utf-8'))
                # visualisation(screen, robot_id, robot_state, num_of_robot)
                # sim_time_start = time.time()
            # print(time.time() - start_of_loop, " seconds ")
            # print("fd to id:", fd_to_id_map)
            # sim_time_curr += delta_t
            # robot_state = update_time(robot_state,num_of_robot,sim_time_curr)
            
            real_time_now_end = time.time()
            elapsed_time_diff = real_time_now_end - real_time_now_start
            # print("Elapsed time diff:",elapsed_time_diff)
            # print("T_real", T_real)
            if elapsed_time_diff < T_real:
                sim_time_curr += T_sim
                real_time_curr += T_real
                robot_state = update_time(robot_state,num_of_robot,sim_time_curr)
                
                real_time_now_end = time.time()
                elapsed_time_diff = real_time_now_end - real_time_now_start
                time.sleep(T_real - elapsed_time_diff)
                # print("sleep")
            else:
                sim_time_curr += real_time_factor*elapsed_time_diff
                real_time_curr += elapsed_time_diff
                robot_state = update_time(robot_state,num_of_robot,sim_time_curr)
                elapsedDIffList.append(elapsed_time_diff)
                notslept += 1
                # print(notslept)
            # visualisation(screen, robot_id, robot_state)
            # print("Sim time:",sim_time_curr)
            # print("real time:", time.time())
        except Exception: # See for some specific exception you expect
            # print("Some error")
            continue
        
        
    server_socket.close()

def main():
    try:
       loop()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    sys.exit(0)


if __name__ == "__main__":
    main()
