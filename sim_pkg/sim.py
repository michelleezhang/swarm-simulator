import os
import importlib
import numpy as np
import time
import logging
import csv
from robot import Robot
from client_server import Bot_Server
from analyze import Sim_Stat_Logger

class Simulator():
    def __init__(self, config_data, initfile):
        '''
        Receives data from robots, updates the swarm accordingly, and sends data to the GUI
        '''
        self.config_data, self.initfile = config_data, initfile

        # Configuration variables
        self.num_robots = self.config_data["NUMBER_OF_ROBOTS"]
        self.comm_radius, self.packet_success, self.num_msgs, self.msg_size = self.config_data["COMM_RANGE"], self.config_data["PACKET_SUCCESS_PERC"], self.config_data["NUM_OF_MSGS"], self.config_data["MSG_SIZE"]
        self.arena_length, self.arena_height = self.config_data["LENGTH"], self.config_data["WIDTH"]
        self.time_async, self.rtf, self.sim_time_step, self.sim_time_max = self.config_data["TIME_ASYNC"], self.config_data["REAL_TIME_FACTOR"], self.config_data["SIM_TIME_STEP"], self.config_data["SIM_TIME"]
 
        # Other simulation variables 
        self.robot_radius = 0.06
        self.stop_sim = False
        self.num_collisions = 0

        # Instantiate client-server communications
        self.bot_server = Bot_Server("localhost", 8000, self.num_robots)

        # NEW: C+D
        if "EXTRA" in self.config_data:
            self.extra = self.config_data["EXTRA"]
            self.initial_num_robots = self.extra[0]
            self.x_b = self.extra[1]
            self.y_b = self.extra[2]
            self.tau_b = self.extra[3]
            self.x_d = self.extra[4]
            self.y_d = self.extra[5]
            self.r_d = self.extra[6]
            self.last_active_id = self.initial_num_robots - 1
            self.spawning = True 
            self.pause_length = 0

            if self.extra[7] == 1:
                self.reactivate = True # make this a param
                self.reactivate_queue = []
            else:
                self.reactivate = False
        else:
            self.initial_num_robots = self.num_robots
            self.last_active_id = self.num_robots - 1
            self.extra = None
        
        if "COLLISION_CHECK" in self.config_data and self.config_data["COLLISION_CHECK"] == 0:
            self.collision_check = False
        else:
            self.collision_check = True

        # Initialize swarm
        self.initialize_swarm()

        self.thread_start_time = 0

    def initialize_swarm(self):
        '''
        Initialize swarm
        '''
        if self.initfile != None:
            init_split = os.path.splitext(self.initfile) # Split .py ending from initfile name
            initfile, init_suffix = init_split[0], init_split[1] 

            if init_suffix == ".py":
                # Import initfile as a module
                imod = importlib.import_module("user." + initfile)

                # Pass in arrays of [0] * num_robots as input
                x, y, theta, a_ids = imod.init(self.num_robots, 
                                            np.zeros(self.num_robots),
                                            np.zeros(self.num_robots),
                                            np.zeros(self.num_robots),
                                            np.zeros(self.num_robots, dtype=int))
            elif init_suffix == ".csv":
                x, y, theta, a_ids = [], [], [], []
                with open("user/" + self.initfile, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        x.append(float(row[0]))
                        y.append(float(row[1]))
                        theta.append(float(row[2]))
                        a_ids.append(float(row[3]))
        else:
            x, y, theta, a_ids = np.random.uniform(-(self.arena_length - 0.1) / 2, (self.arena_length - 0.1) / 2, size=self.num_robots), np.random.uniform(-(self.arena_height - 0.1) / 2, (self.arena_height - 0.1) / 2, size=self.num_robots), np.zeros(self.num_robots), np.zeros(self.num_robots)

        if self.time_async == 1:
            clocks = np.random.rand(self.num_robots) * 0.001 # rand does 0 to 1 range automatically
        else:
            clocks = np.zeros(self.num_robots)
        
        # Overwrite birth positions for robots that spawn later # NEW: C+D
        if self.extra:
            for r_ind in range(self.initial_num_robots, self.num_robots):
                x[r_ind] = self.x_b
                y[r_ind] = self.y_b

        # Round x, y, and theta arrays to 3 decimal places using numpy
        x, y, theta = np.round(x, 3), np.round(y, 3), np.round(theta, 3)

        self.swarm = np.empty(self.num_robots, dtype=object)
        # self.swarm[:] = [Robot(i, x[i], y[i], theta[i], a_ids[i], clocks[i], self.num_robots) for i in range(self.num_robots)]
        # iterate through all elements of the numpy arrays and create the corresponding Robot objects in one go, making it more efficient compared to explicit loops.
        
        # NEW: C+D
        alive_status = np.zeros(self.num_robots, dtype=bool)
        alive_status[:self.initial_num_robots] = True # set the first initial_num_robots to active
        self.swarm[:] = [Robot(i, x[i], y[i], theta[i], a_ids[i], clocks[i], self.num_robots, alive_status[i]) for i in range(self.num_robots)]

    def launch(self, vis, gui):
        '''
        Runs the simulation loop
        '''
        try:
            # Start GUI
            if vis == 1:
                gui.launch()
        
            self.bot_server.start()

            # Initialize logger for simulation statistics 
            logging.basicConfig(level=logging.INFO, # format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[Sim_Stat_Logger('log_values.csv')])    # Log messages using the custom CSVHandler

            # Set up logging for swarm state tracking
            swarm_file = 'swarm_state_log.csv'
            with open(swarm_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                header = ['sim time', 'real time' 'swarm state']
                writer.writerow(header)

            first = True
            actual_rtf = self.rtf # The actual RTF during simulation will fluctuate over time
            adjusted_time_step = self.sim_time_step/self.rtf # Each iteration should ideally take exactly sim_time_step / rtf real seconds 
            delta_vis = 0
            integral_time = 0


            while not self.stop_sim:

                #this has to be first to avoid socket erros!
                datas = self.bot_server.recv(self.swarm) # Receive data

                if self.bot_server.num_connected < self.num_robots: # Prevent simulation from starting until all robot clients are connected to the server
                    continue

                # In the first iteration, initialize time variables
                if first:
                    # Variables to store time elapsed in simulation, time elapsed in real world, and start time of the current simulation loop iteration
                    self.sim_time, self.real_time, loop_start_time = 0.0001, 0, time.time()
                    if self.extra:
                        tau_loop_start_time = loop_start_time # NEW: C+D
                        self.next_spawn_time = 0
                    first = False
                    next_execution_time = 0 + adjusted_time_step #we only integrate every 1 time step.

                #check the time to move clocks forward
                t = time.time()
                elapsed_time_diff = t - loop_start_time
                loop_start_time = t

                #move wall clock forward
                self.real_time = self.real_time + elapsed_time_diff

                #move sim time forward (scaled by time factor)
                self.sim_time = self.sim_time + actual_rtf*elapsed_time_diff
                integral_time += actual_rtf*elapsed_time_diff
                # print(self.sim_time)


                #if enough time has elapsed to be approximately 1 time step
                if self.real_time >= next_execution_time:
                    #identify when we have to integrate next
                    next_execution_time = self.real_time + adjusted_time_step
                        
                    #set fresh data markers
                    self.bot_server.fresh_pose = np.full(self.num_robots, True)

                    # Log swarm state
                    with open(swarm_file, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        swarm_dict = {index: robot.posn for index, robot in enumerate(self.swarm)}
                        row = [self.sim_time, self.real_time, swarm_dict]
                        writer.writerow(row)

                    # NEW: C+D
                    if self.extra:
                        tau_b_diff = t - tau_loop_start_time
                        if not self.spawning:
                            if tau_b_diff >= self.pause_length:
                                self.spawning = True
                        elif (self.sim_time > self.next_spawn_time) and (tau_b_diff >= self.tau_b) and (self.last_active_id + 1) < self.num_robots:
                            empty_spot = True
                            # Check if any robots are already in x_b, y_b spot
                            for robot in self.swarm[:self.last_active_id + 1]:
                                if robot.alive and ((self.x_b - self.robot_radius <= robot.posn[0] <= self.x_b + self.robot_radius) and (self.y_b - self.robot_radius <= robot.posn[1] <= self.y_b + self.robot_radius)):
                                    empty_spot = False
                            if empty_spot:
                                if self.reactivate and self.reactivate_queue != []:
                                    id_to_activate = self.reactivate_queue.pop()
                                    # Reset all fields
                                    self.swarm[id_to_activate].posn[0] = self.x_b 
                                    self.swarm[id_to_activate].posn[1] = self.y_b
                                    self.swarm[id_to_activate].message_buffer = []
                                    self.swarm[id_to_activate].velocity = (0, 0)
                                    self.swarm[id_to_activate].collision_list = np.zeros(self.num_robots)
                                else:
                                    self.last_active_id += 1
                                    id_to_activate = self.last_active_id

                                if self.time_async == 1:
                                    self.swarm[id_to_activate].clock = np.random.rand() * 0.001
                                else:
                                    self.swarm[id_to_activate].clock = 0.0

                                self.swarm[id_to_activate].alive = True
                                tau_loop_start_time = t

                                # print('spawned!', id_to_activate, self.real_time)

                    # Integrate world here
                    self.integrate_world(integral_time)
                    integral_time = 0

                    # Update swarm state based on received data
                    if len(datas) != 0:
                        for data in datas:
                            self.update_state(data)

                    # Send updates to GUI 
                    if vis == 1:
                        delta_vis += self.sim_time_step
                        # Only allows visualization every 0.05 seconds (controls frame rate)
                        if delta_vis > 0.05: 
                            delta_vis = 0
                            # NEW: C+D
                            gui_swarm = self.swarm[np.array([robot.alive for robot in self.swarm])]
                            gui.update(gui_swarm, self.real_time, self.sim_time, actual_rtf)
                            # gui.update(self.swarm, self.real_time, self.sim_time, actual_rtf)

                else:
                    self.update_clocks()
                    # Update swarm state based on received data
                    if len(datas) != 0:
                        for data in datas:
                            self.update_state(data)


                # Time out simulator
                if self.sim_time >= self.sim_time_max: 
                    print("Sim time maxed out.")
                    self.stop_sim = True

            logging.info([0, self.num_collisions])

            self.bot_server.stop()
            if vis == 1:
                gui.stop_gui()
            
        except KeyboardInterrupt:
            pass # Allow clean termination by KeyboardInterrupt from the main program
    
    def update_state(self, data):
        '''
        Update swarm based on data received from the robots
        '''
        function = data["function"]
        robot_id = data["id"]
        thread_time = data["time"]

        # Get the time when the robot threads started (approximated by the time that the latest-starting robot thread began)
        if function == 0: # If we receive a function 0, ideally all bootloader threads should be one step before running usr function
            thread_time = data["params"]
            if thread_time > self.thread_start_time:
                self.thread_start_time = thread_time # Set it to be whatever the latest starting robot time is
        
        # print("TIME:", thread_time - self.thread_start_time) # time elapsed since the thread started
        
        if self.swarm[robot_id].alive: # NEW: C+D
            if function == 1: # set_LED
                self.swarm[robot_id].led = data["params"] 

            elif function == 2: # set_vel
                motor_full_speed = 180 * np.pi / 30 # motor_rpm = 180
                params = data["params"]
                self.swarm[robot_id].velocity = (params[0] / 100) * motor_full_speed, (params[1] / 100) * motor_full_speed

            elif function == 5: # send_msg
                msg = data["params"]
            
                sender_posn = self.swarm[robot_id].posn
                comm_dist = self.comm_radius**2 # this is the value squared
                
                # NEW: C+D
                for robot in self.swarm[:self.last_active_id+1]: 
                    if robot.id != robot_id and robot.alive: 
                # for robot in self.swarm:
                #     if robot.id != robot_id:
                        dist = (sender_posn[0] - robot.posn[0])**2 + (sender_posn[1] - robot.posn[1])**2
                        if dist < comm_dist: 
                            if np.random.uniform() < self.packet_success: # generate a random val and check if it's less than packet_success
                                if len(msg) > self.msg_size:
                                    msg = msg[:self.msg_size]
                                robot.message_buffer.append(msg) 
                                self.bot_server.fresh_messages[robot.id] = True
                                if len(robot.message_buffer) > self.num_msgs:
                                    robot.message_buffer = robot.message_buffer[-self.num_msgs:]

            elif function == 6:
                # Clear message buffer if recv_msg is called
                self.swarm[robot_id].message_buffer = []

            elif function == 7: # stop
                self.stop_sim = True
                
            elif function == 8:
                params = data["params"]
                #delay time is in ms, but clock is in s, so /1000
                self.swarm[robot_id].clock += (params / 1000) 
            
            elif function == 10:
                self.pause_length = data["params"]
                self.spawning = False
                self.next_spawn_time = (((self.sim_time + self.pause_length) // self.tau_b) + 1) * self.tau_b
                # this gets the nearest multiple of pause length to real time (that is also larger than real time)
    
    def update_clocks(self):
        for i in range(self.last_active_id+1): # NEW: C+D
        # for i in range(self.num_robots):
            robot = self.swarm[i]
            robot.clock = max(robot.clock, self.sim_time)

    
    def integrate_world(self, dt):
        '''
        Update positions of robots, while adjusting for collisions
        '''
        result_array = np.array([robot.integrate(dt) for robot in self.swarm[:self.last_active_id+1]]) # NEW: C+D
        # result_array = np.array([robot.integrate(dt) for robot in self.swarm])
        
        for i in range(self.last_active_id+1): # NEW: C+D
        # for i in range(self.num_robots):
            robot, pos = self.swarm[i], result_array[i]
            
            if robot.alive: # NEW: C+D
                # If robot is in death circle, KILL IT
                if self.extra and (self.x_d - self.r_d <= robot.posn[0] <= self.x_d + self.r_d) and (self.y_d - self.r_d <= robot.posn[1] <= self.y_d + self.r_d):
                    robot.alive = False
                    if self.reactivate:
                        self.reactivate_queue.append(robot.id)
                else:
                    if robot.posn[0] != pos[1] or robot.posn[1] != pos[2]: # If new pos is diff from old pos:
                        collision_will_occur = False

                        if self.collision_check: # If we want to turn on collisions
                            # Decrement time to collision for everyone
                            robot.collision_list -= dt

                            # Get a list of indices of all robots that have run out of time till collision
                            for r in np.where(robot.collision_list <= 0)[0]: 
                                if r != robot.id and r <= self.last_active_id and self.swarm[r].alive: # NEW: C+D
                                # if r != robot.id: # Avoid self-collision checks
                                    ir_dist = (self.swarm[r].posn[0] - pos[1])**2 + (self.swarm[r].posn[1] - pos[2])**2
                                    if ir_dist <= (2 * self.robot_radius)**2:
                                        self.num_collisions += 1  
                                        collision_will_occur = True
                                    else: # If two robots have collided, don't recalculate for them (will eventually recalculate when posn updates to a valid posn)
                                        # Recalculate time to collision
                                        # Calculate magnitude of velocity vector: note sqrt(x^2+y^2) >= sqrt(a^2+b^2) iff x^2+y^2 >= a^2+b^2
                                        vel1, vel2 = (self.swarm[r].velocity[0])**2 + (self.swarm[r].velocity[1])**2, (robot.velocity[0])**2 + (robot.velocity[1])**2
                                        max_v = max(vel1, vel2) # Select larger velocity
                                        robot.collision_list[r] = ir_dist / (2 * np.sqrt(max_v) * dt)  # time to collision


                        if not collision_will_occur:
                            robot.posn[0], robot.posn[1] = min(max(pos[1], -self.arena_length / 2 + self.robot_radius), self.arena_length / 2 - self.robot_radius), min(max(pos[2], -self.arena_height / 2 + self.robot_radius), self.arena_height / 2 - self.robot_radius) 
                    robot.posn[2], robot.clock = pos[0], max(robot.clock, self.sim_time)


if __name__ == '__main__':
    import argparse
    import json

    # Parse command line arguments to obtain the paths to the required files
    parser = argparse.ArgumentParser(description="Run the simulator")
    parser.add_argument("-c", "--configfile", type=str, help="Path to configuration file", required=True)
    parser.add_argument("-i", "--initfile", type=str, help="Path to initialization file", required=False) # default value: None
    args = parser.parse_args()

    # Unpack configuration data dictionary
    with open("user/" + args.configfile, 'r') as cfile:
        config_data = json.loads(cfile.read())
    cfile.close()

    simulator = Simulator(config_data, args.initfile)
    simulator.launch()