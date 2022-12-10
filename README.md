# Swarm Simulation

## Download
Clone the repository in a folder

## How to run 
Go inside sim_pkg and run `python3 coachbot-simulation.py -fn <userfile>` in sim_pkg folder. The `user.py` file should be in `sim_pkg` folder. The user file name should be given without .py extension. <br/> 

config.json file has the following options to set: 
1. TIME_ASYNC - 0 to make the robot time synced and 1 to introduce time asynchronous initialization for robots 
2. NUMBER_OF_ROBOTS - Number of robots to launch
3. COMM_RANGE - The range of communication (in meters)
4. PACKET_SUCCESS_PERC - See the success rate of message packets (values in decimal range from 0 to 1)
5. REAL_TIME_FACTOR - Maximum allowable real time factor
6. NUM_OF_MSGS - Maximum number of messages to keep in the buffer
7. MSG_SIZE - Maximum size of each message in buffer
8. WIDTH - width of the arena
9. LENGTH - length of the arena
10. USE_INIT_POS - use the initialization python program to initialize position of the robot
11. SIM_TIME_STEP - Set the simulation time step for each loop cycle
12. USE_VIS - If 1, then visualizer will be used. If 0, then visualizer will not be used and instead all states and the time are logged automatically to sim.log

## Main files to see in the sim_pkg folder

1. simulator.py - The simulator server
2. robot_class.py - Implements the robot API of the real world robots for this simulation
3. visualization.py - uses pygame to visualize the robots
4. user.py - user code written by user to run 
5. coachbot-simulation.py - launches all the processes and programs correctly, using the config.json
6. bootloader.py - launches the user code with the custom coachbot class


## Current structure
![Structure](.github/images/workflow.drawio.png)

## Current Program examples

Firefly algorithm

![Firefly](.github/images/firefly.gif)

Flocking algorithm with collision 

![Flocking](.github/images/flocking.gif)

## Future improvements

Currently, there is a brute force solution to collision detection. Implementing a faster method of collision detection could speed up the collision detection

## License
[MIT](https://choosealicense.com/licenses/mit/)