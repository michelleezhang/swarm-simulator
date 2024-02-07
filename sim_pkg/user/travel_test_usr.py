import numpy as np
from user import robot_movement as rm

# python coachbot_simulator.py -u user_travel_test.py -c config_travel_test.json -i init_travel_test.py
# python coachbot_simulator.py -b travel_test_batch.json

# Primary function for each robot
def usr(robot):
    import struct

    waypoints = np.array([[1,0],
                          [1,1],
                          [0,1],
                          [0,0]])
    
    kp = 200
    kd = 100
    ki = 0

    h_x = rm.PID_Manager(kp, kd, ki, limit = 100)
    h_x.set_goal(waypoints[0,0])
    h_y = rm.PID_Manager(kp, kd, ki, limit = 100)
    h_y.set_goal(waypoints[0,1])

    diffdrive = rm.DiffDrive()
    diffdrive.set_limits(100, -100)

    total_distance = 0

        
    while True:
       
        robot.start_new_loop()
        robot.set_led(0,0,100)

        #get pose
        pose_check = robot.get_pose()

        #only act if we have a valid pose check
        if pose_check:
            #get time
            time = robot.get_clock()


            #parse the pose check
            pose = pose_check
            if pose:
                x, y, ang = pose[0],pose[1],pose[2]

                d = getDistance(0,0,x,y)
                if d >= 0.99:
                    # print('Time to go 1m: ' + str(time))
                    robot.set_led(0,0,0)
                    robot.set_vel(0,0)
                    break


                #get the holonomic control for movement in x direction
                h_x.find_v(x,time)
                h_y.find_v(y,time)

                # #convert to ur and ul
                robot.set_vel(h_x.u, h_x.u)
                # robot.set_vel(30,30)

                # print(time, time%15)
            
                
                print(str(robot.id) + ': %.2f, %.2f, %.2f, %.2f, %.2f' % (time, x, y, h_x.u, h_y.u))
                # if robot.id == int(time % 15):
                #     print(str(robot.id) + ': %.2f, %.2f, %.2f' % (time, x, y))
                    
    return
        




# Function to calculate distance between two points
def getDistance(x1,y1,x2,y2):
    import math
    innerTerm = math.pow((x2-x1),2) + math.pow((y2-y1),2)
    d = math.pow(innerTerm,0.5)
    return d