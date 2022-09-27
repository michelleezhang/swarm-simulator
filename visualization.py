# import pygame
import socket, sys, traceback
import pickle, time, json

from sympy import true

class bot_sim:
    def __init__(self, id, usr_led,clk,delay=0):
        self.id = id
        self.usr_led = usr_led
        self.pos_x = 3
        self.pos_y = 3
        self.clk = clk
        self.delay = delay

class visualization:

    def __init__(self):
        
        (width, height) = (1500, 1000)
        # self.screen = pygame.display.set_mode((width, height))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((socket.gethostname(), 1245))

        # pygame.display.flip()
    
    # def update(self, robot_state, num_of_robot):
    #     for i in range(num_of_robot):
    #         robo = robot_state[i]
    #         # print(robo.usr_led)
    #         colour = robo.usr_led #green
    #         circle_x_y = (i*2, i*2)
    #         circle_radius = 8
    #         border_width = 1 #0 = filled circle
    #         pygame.draw.circle(self.screen, colour, circle_x_y, circle_radius, border_width)
    #     pygame.display.flip()

    def loop(self):

        time_start = time.time()
        while True:
            
            if time.time() - time_start > 0.001:  
                # self.client_socket.connect((socket.gethostname(), 1245))  
                data_send = '0b101'
                self.client_socket.send(data_send.encode())
                msg = self.client_socket.recv(4096)
                # flag = True
                # msg = []
                # while flag:
                    
                #     try:
                #         msg = self.client_socket.recv(4096)
                #     except Exception:
                #         a = 0
                #     if len(msg)>0:
                #         flag = False
                # print('Done with getting message')
                if len(msg)>1:
                    msg = json.loads(msg)
                    print(msg)
                    l = len(msg)
                    print("size", l)
                    time_start = time.time()
                else:
                    msg = '0'
                
            # data_send = '0b11'
            # self.client_socket.send(data_send.encode())
            # gn = self.client_socket.recv(1024)
            print('loop')

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