#!/usr/bin/env python3
"""
Visualization
"""
import socket
import sys
import traceback
import json
import pygame

with open('config.json', 'r') as myfile:
    data=myfile.read()
config_var = json.loads(data)

ARENA_LENGTH = config_var["LENGTH"]
ARENA_WIDTH = config_var["WIDTH"]
RADIUS_OF_ROBOT = 0.105/2
class Dict2Class(object):
    """

    """
    def __init__(self,my_dict):
        for key in my_dict:
            setattr(self,key,my_dict[key])


# class bot_sim:
#     """
    
#     """
#     def __init__(self, id, usr_led,clk,delay=0):
#         self.id = id
#         self.usr_led = usr_led
#         self.pos_x = 3
#         self.pos_y = 3
#         self.clk = clk
#         self.delay = delay

class visualization:

    def __init__(self):
        """
        """
        pygame.init()
        (length, width) = (1500, 900)
        
        self.x_fac = length/ARENA_LENGTH
        self.y_fac = width/ARENA_WIDTH
        self.screen = pygame.display.set_mode((length, width))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((socket.gethostname(), 1245))
        self.set_vis_id()
        # pygame.display.set_caption("Swarm Simulation Visualization ")
        pygame.display.flip()
        self.font = pygame.font.SysFont('samanata', 24)

    
    def set_vis_id(self):
        data = '0b101'
        self.client_socket.sendall(data.encode())
        print("Connected")
        data = self.client_socket.recv(1024)
        self.rt_factor = data.decode('utf-8')
        # if data.decode() != str(bin(2)):
        #     print("Error in connecting to simulator server")
    
    def update_states(self, data):
        """
        """
        num_of_robot = len(data) +1
        robot_state = [0]*num_of_robot
        i=1
        for key in data:
            robot_state[i] = Dict2Class(data[key])
            # print(robot_state[i].id)
            i+=1
        
        self.update(robot_state,num_of_robot)

    def update(self, robot_state, num_of_robot):
        """
        """
        self.screen.fill((0,0,0)) #clear screen
        for i in range(1,num_of_robot):
            robo = robot_state[i]
            # print(robo.usr_led)
            colour = robo.usr_led #green
            pos_x = robo.pos_x*self.x_fac
            pos_y = robo.pos_y*self.y_fac
            circle_x_y = (int(pos_x), int(pos_y))
            circle_radius = int(RADIUS_OF_ROBOT*self.x_fac)
            border_width = 2 #0 = filled circle
            pygame.draw.circle(self.screen, colour, circle_x_y, circle_radius, border_width)
     
    
    def update_time_msg(self,real_time, sim_time):
        """
        """
        data_string = 'Real time factor '+self.rt_factor+ 'x |'+ 'Real time: ' + str(real_time) + 'seconds | ' + 'Sim time:' + str(sim_time) + 'seconds'
        text = self.font.render(data_string,True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (750,900-25)
        self.screen.blit(text, textRect)
        pygame.display.flip()

    def loop(self):

        while True:
            # print("Waiting for client to receive")
            msg = self.client_socket.recv(10*4096)
            msg = msg.decode('utf-8')
            msg = json.loads(msg)
            # print(msg)  
            data_send = '0b11'
            self.client_socket.sendall(data_send.encode())
            time = self.client_socket.recv(4*1024)
            time = time.decode('utf-8')
            ctr = time.index('0b0')
            sim_time = float(time[:ctr])
            sim_time = round(sim_time,2)
            real_time = float(time[ctr+3:])
            real_time = round(real_time,2)
            # print('Vis:',real_time)
            self.update_states(msg)
            self.update_time_msg(real_time,sim_time)
            # gn = self.client_socket.recv(1024)
            # print('Visual loop')

def main():
    try:
        vis = visualization()
        vis.loop()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()