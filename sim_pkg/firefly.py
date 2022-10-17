import time
import random 

def usr(robot):

    T = random.randint(500,1000)
    curr_time = time.time()*1000
    print(T)
    while True:

        
        id = robot.id

        if id == 3:
            robot.set_led(0,100,0)
            robot.delay(100)
            robot.send_msg("(0,100,0)")
            robot.set_led(0,0,0)
            robot.delay(1000)

        else:
            val = robot.recv_msg(clear=True)
            if len(val[0]) > 1:
                print(val[0])
                delta_t = time.time()*1000 - curr_time
                
                
                if delta_t > 100:
                    curr_time = time.time()*1000
                    T = delta_t
                    print(T)
            robot.set_led(0,100,0)
            robot.delay(100)
            robot.send_msg("(0,100,0)")
            robot.set_led(0,0,0)
            robot.delay(int(T))
        