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
        
        counts += 1
        if not changed:
            robot.set_led(50,0,50)
        else:
            robot.set_led(100,100,100)

        t = robot.get_clock()
        if t > 10 and not changed:
            changed = True
            robot.set_led(100,100,100)
            print(str(robot.id) + ': time of change: ' + str(t) + ' : ' + str(counts))
        
        # t = robot.get_clock()
        # if t > 10:
        #     t = t % 10

        # if t > 7.5:
        #     robot.set_led(100,0,0)
        # elif t > 5.0:
        #     robot.set_led(0,0,100)
        # elif t > 2.5:
        #     robot.set_led(100,0,0)
        # elif t > 0:
        #     robot.set_led(0,0,100)
        

        
        # robot.set_led(100,0,0)

        # robot.delay(2)

        # robot.set_led(0,0,100)

        # robot.delay(2)