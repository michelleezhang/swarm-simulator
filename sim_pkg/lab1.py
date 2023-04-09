# Michelle Zhang and Demiana Barsoum

def usr(robot):
    import struct
    import math
    time = robot.get_clock()
    last = time
    desired_distance= 0.17
    previous_dist = 0
    currentdist = 0
    
# set initial velocity of robot 1
    if robot.id == 1:
        robot.set_vel(25,25)
    # if robot.id == 0:
    #     robot.set_vel(5,5)
        
    while True:
        t = robot.get_clock() #gets time
        pose_t=robot.get_pose() # gets pose The syscall that returns the robot's global pose (x, t, theta).
        print('ROBOT', robot.id)
        if pose_t: 
            if robot.id == 0:
                pose0=pose_t
				# robot 0 sends its position to robot 1
                robot.send_msg(struct.pack('ffi', pose0[0], pose0[1],robot.id)) # send pose x,y in message
            if  robot.id == 1:
                pose1=pose_t
                         
        #if we received a message, unpack it
        msgs = robot.recv_msg()
        if len(msgs) > 0:
            if robot.id == 0:
                currentdist_rxed = struct.unpack('fi', msgs[0][:8])
                currentdist = currentdist_rxed[0]
                print('Current Distance is ', currentdist_rxed[0]) # prints the current distance between robots
                
            if robot.id == 1:
                print('hihihi')
                pose_rxed= struct.unpack('ffi', msgs[0][:12])	# unpack position 0 from message
                pose0 = pose_rxed[0:2] # the 1st and 2nd elements from the message make up the position
                #print('robot ',robot.id,' received position ',pose_rxed[0],pose_rxed[1],' from robot ', pose_rxed[2])
                currentdist = math.sqrt( (pose1[0] - pose0[0])**2 + (pose1[1] - pose0[1])**2 )
                robot.send_msg(struct.pack('fi', currentdist, robot.id))	# robot 1 sends its current distance to robot 0 
                
                # robot 1 orbits robot 0
                currentdiff = abs(currentdist - desired_distance)	# difference between current and desired distance
                pastdiff = abs(desired_distance - previous_dist)	# difference between previous and desired distance
                
                if currentdist > desired_distance: # if the distance is too large
                    if currentdiff > pastdiff: # if the distance is getting farther from desired_distance, go in a tighter circle (l > r)
                        robot.set_vel(45, -12) 
                    elif currentdiff <= pastdiff: # if the distance is getting closer to desired_distance, go in a wide circle (l < r)                     
                        robot.set_vel(30, 15) 
                elif currentdist <= desired_distance: # if the distance is too small
                    if currentdiff > pastdiff: # if the distance is getting farther from desired_distance, go straight (l = r)
                        robot.set_vel(30, 30) 
                    elif currentdiff <= pastdiff: # if the distance is getting closer to desired_distance, go in a wide circle
                        robot.set_vel(15, 37) 
            previous_dist = currentdist	# update previous distance
            
		# the LED color of the robots changes based on their distance
        if currentdist > desired_distance:
         #   print(robot.id, "RED")
            robot.set_led(100, 0, 0) # set LED to red
        elif currentdist <= desired_distance:
              #  print(robot.id, 'GREEN')
                robot.set_led(0, 100, 0) # set LED to green 