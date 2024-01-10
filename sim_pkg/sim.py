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

        # Initialize swarm
        self.initialize_swarm()

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
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        x.append(float(row['x']))
                        y.append(float(row['y']))
                        theta.append(float(row['theta']))
                        a_ids.append(float(row['a_ids']))
        else:
            x, y, theta, a_ids = np.random.uniform(-(self.arena_length - 0.1) / 2, (self.arena_length - 0.1) / 2, size=self.num_robots), np.random.uniform(-(self.arena_height - 0.1) / 2, (self.arena_height - 0.1) / 2, size=self.num_robots), np.zeros(self.num_robots), np.zeros(self.num_robots)

        if self.time_async == 1:
            clocks = np.random.rand(self.num_robots) * 0.001 # rand does 0 to 1 range automatically
        else:
            clocks = np.zeros(self.num_robots)

        # Round x, y, and theta arrays to 3 decimal places using numpy
        x, y, theta = np.round(x, 3), np.round(y, 3), np.round(theta, 3)

        self.swarm = np.empty(self.num_robots, dtype=object)
        self.swarm[:] = [Robot(i, x[i], y[i], theta[i], a_ids[i], clocks[i], self.num_robots) for i in range(self.num_robots)]
        # iterate through all elements of the numpy arrays and create the corresponding Robot objects in one go, making it more efficient compared to explicit loops.

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

            first = True
            actual_rtf = self.rtf # The actual RTF during simulation will fluctuate over time
            real_time_step = self.sim_time_step / actual_rtf # Each iteration should ideally take exactly sim_time_step / rtf real seconds 
            delta_vis = 0
            
            while not self.stop_sim:
                datas = self.bot_server.recv(self.swarm) # Receive data
                
                if self.bot_server.num_connected < self.num_robots: # Prevent simulation from starting until all robot clients are connected to the server
                    continue

                # In the first iteration, initialize time variables
                if first:
                    # Variables to store time elapsed in simulation, time elapsed in real world, and start time of the current simulation loop iteration
                    self.sim_time, real_time, loop_start_time = 0.0001, 0, time.time()
                    first = False

                # Update swarm state based on received data
                if len(datas) != 0:
                    for data in datas:
                        self.update_state(data)
                
                # Send updates to GUI 
                if vis == 1:
                    delta_vis += real_time_step
                    # Only allows visualization every 0.05 seconds (controls frame rate)
                    if delta_vis > 0.05: 
                        delta_vis = 0
                        gui.update(self.swarm, real_time, self.sim_time, actual_rtf)
                
                # Increment simulation time
                self.sim_time += self.sim_time_step

                # Integrate world here
                self.integrate_world(self.sim_time_step)

                #find elapsed time (time since last while loop ran)
                #Calling time.time() twice will give 2 different results, so we use t to call it once
                t = time.time()
                elapsed_time_diff = t - loop_start_time
                loop_start_time = t

                # Time out simulator
                if self.sim_time >= self.sim_time_max: 
                    print("Sim time maxed out.")
                    self.stop_sim = True

                # Increment real time
                real_time += real_time_step
            
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
            
            for robot in self.swarm:
                if robot.id != robot_id:
                    dist = (sender_posn[0] - robot.posn[0])**2 + (sender_posn[1] - robot.posn[1])**2
                    if dist < comm_dist: 
                        if np.random.uniform() < self.packet_success: # generate a random val and check if it's less than packet_success
                            if len(msg) > self.msg_size:
                                msg = msg[:self.msg_size]
                            robot.message_buffer.append(msg) 
                            if len(robot.message_buffer) > self.num_msgs:
                                robot.message_buffer = robot.message_buffer[-self.num_msgs:]

        elif function == 6:
            # Clear message buffer if recv_msg is called
            self.swarm[robot_id].message_buffer = []

        elif function == 7: # stop
            self.stop_sim = True
            
        elif function == 8:
            params = data["params"]
            self.swarm[robot_id].clock += (params / 1000) 

    def integrate_world(self, dt):
        '''
        Update positions of robots, while adjusting for collisions
        '''
        result_array = np.array([robot.integrate(dt) for robot in self.swarm])
        
        for i in range(self.num_robots):
            robot, pos = self.swarm[i], result_array[i]
            
            if robot.posn[0] != pos[1] or robot.posn[1] != pos[2]: # If new pos is diff from old pos:
                collision_will_occur = False
                # Decrement time to collision for everyone
                robot.collision_list -= dt

                # Get a list of indices of all robots that have run out of time till collision
                for r in np.where(robot.collision_list <= 0)[0]: 
                    if r != robot.id: # Avoid self-collision checks
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