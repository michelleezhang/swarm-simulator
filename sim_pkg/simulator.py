#!/usr/bin/env python3
"""
Main Server for Swarm Simulation 

__author__ = 'Devesh Bhura <devbhura@gmail.com>'
__copyright__ = 'Copyright 2022, Northwestern University'
__credits__ = ['Marko Vejnovic', 'Lin Liu']
__license__ = 'Proprietary'
__version__ = '0.5.0'
__maintainer__ = 'Devesh Bhura'
__email__ = 'devbhura@gmail.com'
__status__ = 'Research'

"""
import random
import socket
import sys
import json
import select
import time
import re
import numpy as np
import csv
from itertools import chain
import math
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
RADIUS_OF_VISIBILITY = config_var["COMM_RANGE"]
PACKET_SUCCESS_PERC = config_var["PACKET_SUCCESS_PERC"]
NUM_OF_ROBOTS = config_var["NUMBER_OF_ROBOTS"]
NUM_OF_MSGS = config_var["NUM_OF_MSGS"]
ARENA_LENGTH = config_var["LENGTH"]
ARENA_WIDTH = config_var["WIDTH"]
RADIUS_OF_ROBOT = 0.105/2
TIME_ASYNC = config_var["TIME_ASYNC"]

real_time_factor = config_var["REAL_TIME_FACTOR"]
motor_rpm = 10 
motor_full_speed = motor_rpm* 2*np.pi / 60


class BotDiffDrive:
    """
    Bot Diff Drive robot with all the math
    """
    def __init__(self, id_=0, pos_x_=0.0, pos_y_=0.0, pos_angle_=0.0, clk_=0, usr_led_=(0,0,0)):
        """
        Define base variables. 
        All values are expected in metres, seconds and radians. 
        """
        self.id = id_
        self.pos_x = pos_x_
        self.pos_y = pos_y_
        self.pos_angle = pos_angle_
        self.left_wheel_angle = 0
        self.right_wheel_angle = 0
        self.radius_of_wheel = 0.015
        self.distance_between_wheel = 0.04
        self.clk = clk_
        self.usr_led = usr_led_
        

    def integrate(self,u_left, u_right, delta_time):
        """
        Integrate the state of robot
        """
        
        
        velocity_vector = np.array([[u_left],[u_right]])

        # Forward Kinematics from SLAM 
        pos = self.ForwardKinematics2(velocity_vector*delta_time)
        pos[0] = (pos[0]+ np.pi) % (2 * np.pi) - np.pi
        # self.pos_angle  = pos[0]
        # self.pos_x = pos[1]
        # self.pos_y = pos[2]
        # self.left_wheel_angle += u_left*delta_time
        # self.left_wheel_angle = (self.left_wheel_angle + np.pi) % (2 * np.pi) - np.pi
        # self.right_wheel_angle += u_right*delta_time
        # self.right_wheel_angle = (self.right_wheel_angle + np.pi) % (2 * np.pi) - np.pi


        # state_vec = np.array([[self.pos_angle],[self.pos_x],[self.pos_y],[self.left_wheel_angle],[self.right_wheel_angle]])

        # k1 = self.dynamics(velocity_vector,state_vec[0][0])* delta_time
        
        # k2 = self.dynamics(velocity_vector,state_vec[0][0]+k1[0][0]/2.)*delta_time
        
        # k3 = self.dynamics(velocity_vector,state_vec[0][0]+k2[0][0]/2.)*delta_time

        # k4 = self.dynamics(velocity_vector,state_vec[0][0]+k3[0][0])*delta_time
        
        # delta_pos = (1/6.0)*(k1+2.0*k2+2.0+k3+k4)
        # delta_pos =  self.dynamics(velocity_vector, state_vec[0][0])* delta_time
        # delta_pos =  self.dynamics(velocity_vector, state_vec[0][0], delta_time)
        

        # print("Delta pos:", delta_pos)
        # Euler integration update
        # self.pos_angle += delta_pos[0][0]
        # self.pos_angle = (self.pos_angle + np.pi) % (2 * np.pi) - np.pi
        # self.pos_x += delta_pos[1][0]
        # self.pos_y += delta_pos[2][0]
        # self.left_wheel_angle += delta_pos[3][0]
        # self.left_wheel_angle = (self.left_wheel_angle + np.pi) % (2 * np.pi) - np.pi
        # self.right_wheel_angle += delta_pos[4][0]
        # self.right_wheel_angle = (self.right_wheel_angle + np.pi) % (2 * np.pi) - np.pi

        # if u_left!=0.0:
            # print(delta_pos)
            # print("Pos x:", self.pos_x)
            # print("Pos y:", self.pos_y)
            # print("Pos angle:", self.pos_angle)
        return pos
        
    def dynamics(self, vel_vector, angle , dt):
        """
        State dynamic model 
        """
        pos_angle_ = angle
    
        state_matrix = np.array([[-self.radius_of_wheel/(2.0*self.distance_between_wheel), self.radius_of_wheel/(2.0*self.distance_between_wheel)], 
                                 [self.radius_of_wheel*np.cos(pos_angle_)/2.0, self.radius_of_wheel*np.cos(pos_angle_)/2.0], 
                                 [self.radius_of_wheel*np.sin(pos_angle_)/2.0, self.radius_of_wheel*np.sin(pos_angle_)/2.0],
                                 [1.0, 0.0],
                                 [0.0, 1.0] ])
        
        pos = state_matrix@vel_vector

        return pos
    
    def ForwardKinematics2(self, wheel_vel):
        """
        As per Modern Robotics 
        """
        r = self.radius_of_wheel
        d = self.distance_between_wheel
        u_x = wheel_vel[0][0]
        u_y = wheel_vel[1][0]
        # thetadot xdot ydot
        V = np.array([-r*u_x/(2.0*d)+r*u_y/(2.0*d), r*u_x/2.0 + r*u_y/2.0, 0])

        delq_b = [0, 0, 0]
        if V[0]==0.0:
            delq_b[0] = 0
            delq_b[1] = V[1]
            delq_b[2] = V[2]
            
        else:
            delq_b[0] = V[0]
            delq_b[1] = (V[1]*np.sin(V[0])+V[2]*(np.cos(V[0])-1))/V[0]
            delq_b[2] = (V[2]*np.sin(V[0])+V[1]*(1 - np.cos(V[0])))/V[0]

        phi = self.pos_angle
        x = self.pos_x
        y = self.pos_y
        mult_mat = np.array([[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
        delq = mult_mat@np.array([[delq_b[0]], [delq_b[1]], [delq_b[2]]])
        pos = np.array([phi+delq[0][0], x+delq[1][0], y+delq[2][0]])
        return pos
    
    def ForwardKinematics(self, wheel_vel):
        """
        As per SLAM
        """
        r = self.radius_of_wheel
        d = self.distance_between_wheel
        u_x = wheel_vel[0][0]
        u_y = wheel_vel[1][0]
        # thetadot xdot ydot
        V = np.array([-r*u_x/(2.0*d)+r*u_y/(2.0*d), r*u_x/2.0 + r*u_y/2.0, 0])

        Tbbhat = self.integrate_twist(V)

        q_x = self.pos_x
        q_theta = self.pos_angle
        q_y = self.pos_y
        Twb = np.array([[np.cos(q_theta), -np.sin(q_theta), q_x], [np.sin(q_theta), np.cos(q_theta), q_y], [0, 0, 1]])

        Twbhat = Twb@Tbbhat

        pos = np.array([np.arccos(Twbhat[0][0]), Twbhat[0][2], Twbhat[1][2]])

        return pos
    
    def integrate_twist(self, V):
        """
        As per SLAM
        """
        if V[0]==0.0:
            v = [0, 0]
            v[0] = V[1]
            v[1] = V[2]
            Tbb_hat = np.array([[1, 0, v[0]],[0, 1, v[1]], [0, 0, 1]])
            
            return Tbb_hat
        
        theta_s = V[0]
        v = [0, 0]
        v[0] = V[1]/theta_s
        v[1] = -V[2]/theta_s


        Tsb = np.array([[1, 0, v[0]],[0, 1, v[1]], [0, 0, 1]])
        Tss_hat = np.array([[np.cos(theta_s), -np.sin(theta_s), 0], [np.sin(theta_s), np.cos(theta_s), 0], [0, 0, 1]])
        Tbs = np.array([[1, 0, -v[0]],[0, 1, -v[1]], [0, 0, 1]])
       
        Tbb_hat = Tbs@Tss_hat@Tsb
        return Tbb_hat
        


def convert_list_to_dict(lst):
    """
    Converts a list to dictionary    
    """
    res_dct = {str(i): lst[i] for i in range(0, len(lst))}
    return res_dct
        
def transform_from_map_to_base(pos_x:float, pos_y:float, angle:float):
    """
    Transform from map frame to base
    """
    vec_m = np.array([[pos_x],[pos_y], [1]])
    T_bm = np.array([[1, 0, -ARENA_LENGTH/2],
                    [0, 1, -ARENA_WIDTH/2],
                    [0, 0, 1]])

    vec_b = T_bm@vec_m

    return vec_b[0][0], vec_b[1][0], angle

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
    Defines Bot Class for simulation visualization   
    """
    def __init__(self, id):
        self.id = id
        self.usr_led = (0,0,0)
        self.pos_x = 0
        self.pos_y = 0
        self.angle = 0


def conv_to_json(robot_state, num_of_robot:int)->dict:
    """
    Convert data to dict so that it can be json dumped
    """
    json_dict = {}
    for i in range(0,num_of_robot):
        robot = BotSim(id=robot_state[i].id)
        robot.pos_x = robot_state[i].pos_x
        robot.pos_y = robot_state[i].pos_y
        robot.angle = robot_state[i].pos_angle
        robot.angle = (robot.angle + np.pi) % (2 * np.pi) - np.pi
        robot.usr_led = robot_state[i].usr_led
        json_dict[i] = robot.__dict__
    # print(json_dict)
    return json_dict

def update_time(robot_state:list, num_of_robot:int, sim_time:float)-> list:
    """
    Updates time of robot clocks
    """
    for i in range(0,num_of_robot):
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
        range_of_val = range(0,robot_id)
    else:
        range_of_val = chain(range(0,robot_id-1),range(robot_id,num_of_robot))
    # print("Range of val:", range_of_val)
    for i in range_of_val:
        curr_pos_x = robot_states[i].pos_x
        curr_pos_y = robot_states[i].pos_y
        d = np.sqrt((ref_x - curr_pos_x)**2 + (ref_y - curr_pos_y)**2)
        if d < RADIUS_OF_VISIBILITY:
            random_bool = np.random.uniform() < PACKET_SUCCESS_PERC
            if random_bool:
                if len(msg) > MSG_BUFFER_SIZE:
                    msg = msg[:MSG_BUFFER_SIZE]
                msg_buffer[i].append(msg)
                if len(msg_buffer[i])> NUM_OF_MSGS:
                    msg_buffer[i] = msg_buffer[i][-NUM_OF_MSGS:]
                
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
    robot = BotDiffDrive(id_=0)
    robot_state = [robot]*(NUM_OF_ROBOTS)
    robot_id = -1*np.ones((NUM_OF_ROBOTS))
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
                            
                            
                            # print(fd_to_id_map)
                            id_to_socket_map[num_of_robot] = new_socket
                            # msg1 = str(bin(num_of_robot))
                            fd_to_id_map[new_socket.fileno()] = num_of_robot
                            # new_socket.sendall(msg1.encode('utf-8'))
                            robot_state[num_of_robot] = BotDiffDrive(id_=num_of_robot)
                            robot_state[num_of_robot].pos_y = random.uniform(-(ARENA_LENGTH-0.1)/2, (ARENA_LENGTH-0.1)/2)
                            robot_state[num_of_robot].pos_x = random.uniform(-(ARENA_WIDTH-0.1)/2, (ARENA_WIDTH-0.1)/2)
                            robot_state[num_of_robot].usr_led = (50,50,50)
                            if TIME_ASYNC ==  1:
                                val_ = random.uniform(0,1)*0.001
                                robot_state[num_of_robot].clk = val_
                            else:
                                robot_state[num_of_robot].clk = 0
                            robot_id[num_of_robot] = num_of_robot
                            num_of_robot += 1
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

def integrate_world(robot_states:list, num_of_robot:int, wheel_vel_arr:list, curr_time, prev_time, dt):
    """ 
    Integrates the world
    """
    # delta_time = real_time_factor*(curr_time - prev_time)
    delta_time = dt
    for i in range(0, num_of_robot):
        wheel_vel = wheel_vel_arr[i]
        u_l = wheel_vel[0]
        u_r = wheel_vel[1]
        pos = robot_states[i].integrate(u_l,u_r,delta_time)
        range_of_val = chain(range(0,i),range(i+1,num_of_robot))

        # check for collision with robots
        collision_flag_ = True
        for j in range_of_val:
            x1_ = robot_states[j].pos_x
            y1_ = robot_states[j].pos_y
            d = np.sqrt((x1_-pos[1])**2 + (y1_ - pos[2])**2)
            if d <= 2*RADIUS_OF_ROBOT:
                collision_flag_ = False
        robot_states[i].pos_angle = pos[0]
        if collision_flag_ == True:
            robot_states[i].pos_x = pos[1]
            robot_states[i].pos_y = pos[2]

        # check for collision with walls
        if robot_states[i].pos_x - RADIUS_OF_ROBOT  < -ARENA_WIDTH/2:
           robot_states[i].pos_x = -ARENA_WIDTH/2 + RADIUS_OF_ROBOT
        elif robot_states[i].pos_x + RADIUS_OF_ROBOT > ARENA_WIDTH/2:
            robot_states[i].pos_x = ARENA_WIDTH/2 - RADIUS_OF_ROBOT
        
        if robot_states[i].pos_y - RADIUS_OF_ROBOT < -ARENA_LENGTH/2:
           robot_states[i].pos_y = -ARENA_LENGTH/2 + RADIUS_OF_ROBOT
        elif robot_states[i].pos_y + RADIUS_OF_ROBOT > ARENA_LENGTH/2:
            robot_states[i].pos_y = ARENA_LENGTH/2 - RADIUS_OF_ROBOT


    return robot_states

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
    T_real = 0.002
    T_sim = real_time_factor*T_real
    
    # sim_ticks = 0 
    # sim_time_or = time.time()
    sim_time_curr = 0.0001
    # robot = BotSim(id=0,usr_led=(0,0,0),clk=sim_time_curr)
    # robot_state = [robot]*NUM_OF_ROBOTS
    buffer_list_size = 16
    delta_vis = 0
    real_time_curr = 0
    sim_time_delt = 0.0
    msg_buffer = [[]]*(NUM_OF_ROBOTS)
    MSG_BUFFER_SIZE = 1024
    num_of_robot = NUM_OF_ROBOTS
    wheel_vel_arr  = [np.array([0,0])]*(NUM_OF_ROBOTS)
    vis_fd, vis_socket, fd_to_id_map, robot_state, robot_id = initialize_robots()
    real_time_now_start = time.time()
    while True:
        
        
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
                        # delay
                        robot_state[int(msg[1])].clk += (msg[3]/1000)
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        continue
                    elif msg[2] == 4:
                        # send_msg
                        # print('Message sent:',msg[3])
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        msg_for_buffer = current_socket.recv(1024*4)
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        msg_type = msg[3]
                        msg_buffer = update_msg_buffer(msg_buffer,MSG_BUFFER_SIZE,num_of_robot,msg_for_buffer,msg[1],robot_state)
                        # print("New msg buffer:", msg_buffer)
                        continue
                    elif msg[2] == 5:
                        # recv_msg
                        arr = msg_buffer[msg[1]]
                        
                        len_ = len(arr)
                        size_ = len_
                        data_string = str(size_)
                        current_socket.sendall(data_string.encode('utf-8'))
                        # print(type(msg_buffer))
                        clear_bool = current_socket.recv(1024)
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        # start_j = 0
                        # end_j = 20

                        for j in range(len_):
                            check_data_ = current_socket.recv(1024)
                            # data_send = convert_list_to_dict(arr[j])
                            data = arr[j]
                            # print(type(data))
                            # start_j+=20
                            # end_j = min(end_j+20, len_)
                            # data = json.dumps(data_send)
                            # print(data)
                            current_socket.sendall(data)

                        if clear_bool.decode('utf-8') == 'True':
                            msg_buffer[msg[1]] = []
                        # print('Send data:')
                        continue
                    elif msg[2] == 6:
                        # get_clock
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        type_time = current_socket.recv(1024)
                        time_val = robot_state[int(msg[1])].clk
                        time_val = str(round(time_val,4))
                        current_socket.sendall(time_val.encode('utf-8'))
                    elif msg[2] == 7:
                        # Set wheel velocity
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        vel = current_socket.recv(1024)
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        vel = vel.decode('utf-8')
                        vel = json.loads(vel)
                        # print(vel)
                        wheel_pow = np.array([vel[0],vel[1]])
                        # print("Wheel power:", wheel_pow)
                        # print("motor_full_speed", motor_full_speed)
                        wheel_vel = motor_full_speed*wheel_pow
                        wheel_vel_arr[int(msg[1])] = wheel_vel
                        # print("Wheel velocity:",wheel_vel)
                    elif msg[2] == 8:
                        # get_pose
                        data_string = '0b1'
                        current_socket.sendall(data_string.encode('utf-8'))
                        pose_type = current_socket.recv(1024)
                        local_id = int(msg[1])
                        pos_tuple = [robot_state[local_id].pos_x, robot_state[local_id].pos_y, robot_state[local_id].pos_angle]
                        # x_, y_, theta_ = transform_from_map_to_base(pos_tuple[0], pos_tuple[1], pos_tuple[2])
                        # pos_tuple = [x_,y_,theta_]
                        pos_tuple = json.dumps(pos_tuple)
                        current_socket.sendall(pos_tuple.encode('utf-8'))

                    elif msg[2] == 2:
                        # set_led
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
            
            delta_time = T_sim
            if sim_time_delt != 0.0:
                robot_state = integrate_world(robot_state, num_of_robot, wheel_vel_arr, curr_time = time.time(), prev_time = real_time_now_start, dt = sim_time_delt)

            real_time_now_end = time.time()
            elapsed_time_diff = real_time_now_end - real_time_now_start
            # print("Elapsed time diff:",elapsed_time_diff)
            # print("T_real", T_real)
            real_time_now_start = time.time()

            if elapsed_time_diff < T_real:
                real_time_now_loop_start = time.time()
                sim_time_curr += T_sim
                sim_time_delt = T_sim
                real_time_curr += T_real
                robot_state = update_time(robot_state,num_of_robot,sim_time_curr)
                
                real_time_now_loop_end = time.time()
                elapsed_time_diff_loop = real_time_now_loop_end - real_time_now_loop_start
                diff = T_real - elapsed_time_diff - elapsed_time_diff_loop
                if diff>0:
                    time.sleep(T_real - elapsed_time_diff)
                # print("sleep")
            else:
                sim_time_curr += real_time_factor*elapsed_time_diff
                sim_time_delt = real_time_factor*elapsed_time_diff
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
