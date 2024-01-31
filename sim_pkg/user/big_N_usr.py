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
    first_part = True

    threshold = 10

    while True:

        robot.delay()
        
        counts += 1
        if not changed and first_part:
            robot.set_led(50,0,50)
        elif first_part:
            robot.set_led(100,100,100)

        t = robot.get_clock()
        if t > threshold and not changed:
            changed = True
            first_part = False
            robot.set_led(100,100,100)
            print(str(robot.id) + ': time of change: ' + str(t) + ' : ' + str(counts))
        
        if t > threshold + 5:
            robot.set_led(100,0,0)
            # print('entering delay 1 at: ' + str(t))
            robot.delay(2)
            robot.set_led(0,0,100)
            # print('entering delay 2 at: ' + str(robot.get_clock()))
            robot.delay(2)

            # t = t % 10

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