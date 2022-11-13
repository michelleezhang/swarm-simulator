#!/usr/bin/env python3
"""
Visualization 

__author__ = 'Devesh Bhura <devbhura@gmail.com>'
__copyright__ = 'Copyright 2022, Northwestern University'
__credits__ = ['Marko Vejnovic', 'Lin Liu']
__license__ = 'Proprietary'
__version__ = '0.5.0'
__maintainer__ = 'Devesh Bhura'
__email__ = 'devbhura@gmail.com'
__status__ = 'Research'
"""
import socket
import sys
import traceback
import json
import pygame
import numpy as np
import pandas as pd
import time

with open('config.json', 'r') as myfile:
    data=myfile.read()
config_var = json.loads(data)
socket_port_pandas = pd.read_csv("port.csv", header=None)
socket_port_numpy = socket_port_pandas.to_numpy()
SOCKET_PORT_NUMBER = int(socket_port_numpy[0][0])

ARENA_LENGTH = config_var["LENGTH"]
ARENA_WIDTH = config_var["WIDTH"]
RADIUS_OF_ROBOT = 0.105/2
class Dict2Class(object):
    """
    Convert a dict to a class. 
    """
    def __init__(self,my_dict):
        for key in my_dict:
            setattr(self,key,my_dict[key])


def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 2,
        head_width: int = 4,
        head_height: int = 2,
    ):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, int(head_height / 2)),  # Center
        pygame.Vector2(int(head_width / 2), int(-head_height / 2)),  # Bottomright
        pygame.Vector2(int(-head_width / 2), int(-head_height / 2)),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, int(arrow.length() - (head_height / 2))).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start
        

    pygame.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)


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
        self.client_socket.connect((socket.gethostname(), SOCKET_PORT_NUMBER))
        self.set_vis_id()
        # pygame.display.set_caption("Swarm Simulation Visualization ")
        pygame.display.flip()
        self.font = pygame.font.SysFont('samanata', 24)
        self.font_num = pygame.font.SysFont('samanata', 18)

    
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
        Update the states
        """
        num_of_robot = len(data)
        robot_state = [0]*num_of_robot
        i=0
        for key in data:
            robot_state[i] = Dict2Class(data[key])
            # print(robot_state[i].id)
            i+=1
        
        self.update(robot_state,num_of_robot)

    def update(self, robot_state, num_of_robot):
        """
        Update the screen
        """
        self.screen.fill((0,0,0)) #clear screen
        for i in range(0,num_of_robot):
            robo = robot_state[i]
            # print(robo.usr_led)
            # Print number
            data_string = str(i)
            text = self.font_num.render(data_string,True,(255,255,255))
            textRect = text.get_rect()
            
            colour = robo.usr_led #green
            colour = (int(colour[0]*2.55), int(colour[1]*2.55), int(colour[2]*2.55))
            pos_x =(robo.pos_y + ARENA_LENGTH/2)*self.x_fac
            pos_y = (robo.pos_x + ARENA_WIDTH/2)*self.y_fac
            angle = robo.angle
            
            circle_x_y = (int(pos_x), int(pos_y))
            textRect.center = circle_x_y
            
            # if i == 4:
            #     print("Circle x y", circle_x_y)
            #     print("Robo x y", robo.pos_x, robo.pos_y)
            circle_radius = int(RADIUS_OF_ROBOT*self.x_fac)
            border_width = 2 #0 = filled circle
            pygame.draw.circle(self.screen, (128,0,128,25), circle_x_y, circle_radius)
            pygame.draw.circle(self.screen, colour, circle_x_y, circle_radius, border_width)
            
            # draw an arrow
            center = pygame.Vector2(pos_x,pos_y)
            end = pygame.Vector2(int(pos_x+circle_radius*np.sin(angle)), int(pos_y+circle_radius*np.cos(angle)))
            draw_arrow(self.screen, center, end, pygame.Color("dodgerblue"), 4, 6, 4)
            # Show the number 
            # self.screen.blit(text, textRect)
     
    
    def update_time_msg(self,real_time, sim_time, rtf):
        """
        """
        data_string = 'Real time factor '+str(rtf)+ 'x |'+ 'Real time: ' + str(real_time) + 'seconds | ' + 'Sim time:' + str(sim_time) + 'seconds'
        text = self.font.render(data_string,True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (750,900-25)
        self.screen.blit(text, textRect)
        pygame.display.flip()

    def loop(self):
        T_vis = 0.6
        while True:
            
            # data_send = '0b11'
            # self.client_socket.sendall(data_send.encode())
            # # print("Waiting for client to receive")
            msg = self.client_socket.recv(10*4096)
            _start_time_vis = time.time()
            msg = msg.decode('utf-8')
            msg = json.loads(msg)
            # print(msg)  
            data_send = '0b11'
            self.client_socket.sendall(data_send.encode())
            _time = self.client_socket.recv(4*1024)
            _time = _time.decode('utf-8')
            # ctr = time.index('0b0')
            # sim_time = float(time[:ctr])
            # sim_time = round(sim_time,2)
            # real_time = float(time[ctr+3:])
            # real_time = round(real_time,2)
            _time = json.loads(_time)
            sim_time = _time[0]
            sim_time = round(sim_time,2)
            real_time = _time[1]
            real_time = round(real_time,2)
            rtf = float(_time[2])
            rtf = round(rtf,1)
            # print('Vis:',real_time)
            self.update_states(msg)
            self.update_time_msg(real_time,sim_time, rtf)
            _vis_time_delta = time.time() - _start_time_vis
            # if _vis_time_delta < T_vis:
            #     time.sleep(T_vis-_vis_time_delta)
            # print("Visual time taken:",_vis_time_delta)

            

def main():
    try:
        vis = visualization()
        vis.loop()
    except KeyboardInterrupt:
        print("Visualization Shutdown requested...exiting")
        vis.client_socket.close()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    except BaseException:
        vis.client_socket.close()
    sys.exit(0)

if __name__ == "__main__":
    main()