#########################
## THis code was written by Drew Curtis
## for RESEARCH at Northwestern University
## Professor Rubenstein
## 2024.01.03
#########################

#########################
### This code, along with the other supporting .py files facilitate persistent scuplting on the coachbots.
#########################

import numpy as np

# python coachbot_simulator.py -u big_N_usr.py -c big_N_config.json -i big_N_init_pose.py

# Primary function for each robot
def usr(robot):
    import struct
    
    changed = False
    counts = 0
        
    while True:
        # print('Thread: ' + str(robot.id))
        counts += 1
        if not changed:
            robot.set_led(50,0,50)
        else:
            robot.set_led(100,100,100)

        t = robot.get_clock()
        if t > 60 and not changed:
            changed = True
            robot.set_led(100,100,100)
            print(str(robot.id) + ': time of change: ' + str(t) + ' : ' + str(counts))
                