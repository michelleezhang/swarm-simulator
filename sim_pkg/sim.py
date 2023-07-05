import os
import importlib
import numpy as np
from robot import Robot
from client_server import Bot_Server
import time
import itertools

class Simulator():
    def __init__(self, config_data, initfile):
        '''
        Runs the simulation.
        Receives data from robots, updates the swarm accordingly, and sends data to the GUI.
        '''
        self.config_data = config_data
        self.initfile = initfile

        # Configuration variables
        self.num_robots = self.config_data["NUMBER_OF_ROBOTS"]
        self.comm_radius = self.config_data["COMM_RANGE"]
        self.packet_success = self.config_data["PACKET_SUCCESS_PERC"]
        self.num_msgs = self.config_data["NUM_OF_MSGS"]
        self.msg_size = self.config_data["MSG_SIZE"]
        self.arena_length = self.config_data["LENGTH"]
        self.arena_height = self.config_data["WIDTH"]
        self.rtf = self.config_data["REAL_TIME_FACTOR"]
        self.use_init = self.config_data["USE_INIT_POS"]
        self.sim_time_step = self.config_data["SIM_TIME_STEP"]
        self.sim_time_max = self.config_data["SIM_TIME"]
        self.time_async = self.config_data["TIME_ASYNC"]

 
        # Other simulation variables 
        self.motor_rpm = 180 # rpm
        self.motor_full_speed = self.motor_rpm* 2*np.pi / 60
        self.robot_radius = 0.105/2 # TODO: might need to adjust this value 

        self.stop_sim = False
        self.num_collisions = 0

        # Instantiate client-server communications
        self.bot_server = Bot_Server("localhost", 8000, self.num_robots)

        self.swarm = np.empty(self.num_robots, dtype=object)

        # Initialize swarm
        self.initialize_swarm(self.swarm)


    def initialize_swarm(self, swarm):
        '''
        Initialize swarm according to initfile.
        '''
        if self.use_init == 1:
        # Import initfile as a module
            initfile = os.path.splitext(self.initfile)[0] # Remove .py ending from initfile name
            imod = importlib.import_module("user." + initfile)

            # Pass in arrays of [0] * num_robots as input
            x, y, theta, a_ids = imod.init(self.num_robots, 
                                    [0 for _ in range(self.num_robots)], 
                                    [0 for _ in range(self.num_robots)], 
                                    [0 for _ in range(self.num_robots)],
                                    [0 for _ in range(self.num_robots)]) 
        elif self.use_init == 0:
            x = [np.random.uniform(-(self.arena_length - 0.1) / 2, (self.arena_length - 0.1) / 2) for _ in range(self.num_robots)]
            y = [np.random.uniform(-(self.arena_height - 0.1) / 2, (self.arena_height - 0.1) / 2) for _ in range(self.num_robots)]
            theta = [0 for _ in range(self.num_robots)]

        if self.time_async == 1:
            clocks = [np.random.uniform(0, 1) * 0.001 for _ in range(self.num_robots)]
        else:
            clocks = [0 for _ in range(self.num_robots)]

        for i in range(self.num_robots):
            # Truncate values to 3 decimal places
            curr_x = float(f'{x[i]:.3f}')
            curr_y = float(f'{y[i]:.3f}')
            curr_theta = float(f'{theta[i]:.3f}')
            curr_robot = Robot(i, curr_x, curr_y, curr_theta, self.num_robots, clocks[i], a_ids[i])

            # Set swarm entry to robot
            swarm[i] = curr_robot

    def launch(self, vis, gui):
        try:
            # Start GUI
            if vis == 1:
                gui.launch()
            
            # Start server
            self.bot_server.start()

            time.sleep(2) # lines up w sleep time from the coachbot_simulator.py so everything starts at the same time

            actual_rtf = self.rtf # this will be some value initially, but will change slightly over time
            T_sim = self.sim_time_step 
            T_real = T_sim/actual_rtf

            self.sim_time = 0.0001
            delta_vis = 0
            self.real_time = 0
            real_time_now_start = time.time()
            actual_rtf_list = []
            
            while not self.stop_sim:
                datas = self.bot_server.recv(self.swarm) # receive data
                
                if len(datas) != 0:
                    # print(f"Received data: ", datas)
                    for data in datas:
                        self.update_state(data)

                if vis == 1:
                    delta_vis += T_real
                    # Only allows visualization every 0.05 seconds
                    if delta_vis > 0.05: 
                        delta_vis = 0
                        self.rtf = np.mean(actual_rtf_list)
                        actual_rtf_list = []
                        gui.update(self.swarm, self.real_time, self.sim_time, self.rtf)
                
                self.sim_time += T_sim

                # Integrate world here
                self.integrate_world(T_sim)
    
                real_time_now_end = time.time()
                elapsed_time_diff = real_time_now_end - real_time_now_start
                real_time_now_start = time.time()

                # time out simulator!
                if self.real_time >= self.sim_time_max: # SIM_TIME -- max time we want sim to run
                    # TODO: change to self.sim_time
                    print("Sim time maxed out.")
                    self.stop_sim = True

                if elapsed_time_diff < T_real:
                    self.real_time += T_real
                    actual_rtf = T_sim/T_real
                    diff = T_real - elapsed_time_diff
                    if diff > 0:
                        time.sleep(diff)
                else:
                    
                    self.real_time += elapsed_time_diff
                    actual_rtf = T_sim/elapsed_time_diff
                    
                actual_rtf_list.append(actual_rtf)

            self.bot_server.stop()
            if vis == 1:
                gui.stop()
    
        except KeyboardInterrupt:
            pass
    
    def update_state(self, data):
        function = data["function"]
        robot_id = data["id"]

        if function == 1: # set_LED
            params = data["params"]
            r = params[0]
            b = params[1]
            g = params[2]
            self.swarm[robot_id].led = (r, b, g)
        elif function == 2: # set_vel
            params = data["params"]
            l = (params[0] / 100) * self.motor_full_speed
            r = (params[1] / 100) * self.motor_full_speed
            self.swarm[robot_id].velocity = (l, r)
        elif function == 5: # send_msg
            params = data["params"]

            sender = self.swarm[robot_id]
            for robot in self.swarm:
                if robot.id != robot_id:
                    dist = np.sqrt((sender.x - robot.x)**2 + (sender.y - robot.y)**2)
                    if dist < self.comm_radius:
                        random_bool = np.random.uniform() < self.packet_success
                        if random_bool:
                            msg = params[0]
                            if len(msg) > self.msg_size:
                                msg = msg[:self.msg_size]

                            robot.message_buffer.append(msg) # ISSUE: Adding to the message buffer affects communication scalability
                            if len(robot.message_buffer) > self.num_msgs:
                                robot.message_buffer = robot.message_buffer[-self.num_msgs:]
                            
        elif function == 6:
            # Clear message buffer if recv_msg is called
            self.swarm[robot_id].message_buffer = []
        elif function == 7: # stop
            self.stop_sim = True
        elif function == 8:
            params = data["params"]
            self.swarm[robot_id].clock += (params[0] / 1000)

    def integrate_world(self, dt):  
        for robot in self.swarm:
            pos = robot.integrate(dt)
            robot.theta = pos[0]

            check_collision = True # yes, check for collision
            collide_flag = True # no, no collision has occured

            # BROAD PHASE
            if check_collision: 
                # NARROW PHASE
                collide_flag = self.check_collision(robot, pos)
            
            if collide_flag:
                robot.x = pos[1]
                robot.y = pos[2]
                # adjust for wall collisions
                robot.x = max(robot.x, -self.arena_height / 2 + self.robot_radius)
                robot.x = min(robot.x, self.arena_height / 2 - self.robot_radius)
                robot.y = max(robot.y, -self.arena_length / 2 + self.robot_radius)
                robot.y = min(robot.y, self.arena_length / 2 - self.robot_radius)

            robot.clock = max(robot.clock, self.sim_time) 

    def check_collision(self, robot, pos):
        range_val = itertools.chain(range(0, robot.id), range(robot.id + 1, self.num_robots))
        for j in range_val:

            x1 = self.swarm[j].x
            y1 = self.swarm[j].y

            dist = np.sqrt((x1 - pos[1])**2 + (y1 - pos[2])**2)
            if dist <= 2 * self.robot_radius:
                self.num_collisions += 1 # NOTE: collision number is scaled -- will count +1 if ANY collision occurs at a given iteration (not total number)
                return False
        return True