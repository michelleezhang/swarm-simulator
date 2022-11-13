# Swarm Simulation

## How to run 
run `python3 run` in sim_pkg folder one terminal. 

config.json file has the following options to set: 
1. TIME_ASYNC - 0 to make the robot time synced and 1 to introduce time asynchronous initialization for robots 
2. NUMBER_OF_ROBOTS - Number of robots to launch
3. COMM_RANGE - The range of communication
4. PACKET_SUCCESS_PERC - See the success rate of message packets
5. REAL_TIME_FACTOR - Maximum allowable real time factor
6. NUM_OF_MSGS - Maximum number of messages to keep in the buffer
7. WIDTH - width of the arena
8. LENGTH - length of the arena
9. USE_INIT_POS - use the initialization python program to initialize position of the robot
10. SIM_TIME_STEP - Set the simulation time step for each loop cycle

## Main files to see in the sim_pkg folder

1. simulator.py - The simulator server
2. robot_class.py - Implements the robot API of the real world robots for this simulation
3. visualization.py - uses pygame to visualize the robots
4. user.py - user code written by user to run 
5. run.py - launches all the processes and programs correctly, using the config.json



## Current structure (Outdated)
![Structure](workflow.drawio.png)

## Current Stats

<!-- The following user.py code was running 50 times 
```
def usr(robot):

    while True:
        robot.set_led(100,100,0)
        robot.delay(1000)
        robot.set_led(0,100,0)
        robot.delay(1000)

``` -->
<!-- T_real - 0.001 seconds; real time factor - 1 \
![T_real - 0.001 seconds; real time factor - 1](T_real_0.001_c_1.gif) 

T_real - 0.001 seconds; real time factor - 2 \
![T_real - 0.001 seconds; real time factor - 2](T_real_0.001_c_2.gif)

T_real - 0.001 seconds; real time factor - 0.5 \
![T_real - 0.001 seconds; real time factor - 0.5](T_real_0.001_c_0.5.gif)

T_real - 0.0001 seconds; real time factor - 1 \
![T_real - 0.0001 seconds; real time factor - 1](T_real_0.0001_c_1.gif)

T_real - 0.0001 seconds; real time factor - 2 \
![T_real - 0.0001 seconds; real time factor - 2](T_real_0.0001_c_2.gif)

T_real - 0.0001 seconds; real time factor - 0.5 \
![T_real - 0.0001 seconds; real time factor - 0.5](T_real_0.0001_c_0.5.gif) -->

Firefly

![Firefly](firefly.gif)

![Flocking](flocking.gif)

## License
[MIT](https://choosealicense.com/licenses/mit/)