# Michelle Zhang
def usr(robot):
    import struct
    import math
    import timeit

    # green :)
    robot.set_led(0, 100, 0)

    # define center of migration
    com = (0, 0)

    while True:
        # initialize component vectors
        v_alignment = [0, 0]
        v_cohesion = [0, 0]
        v_separation = [0, 0]
        v_migration = [0, 0]

        # get robot position
        robot_posn = robot.get_pose()

        if robot_posn:
            curr_x = robot_posn[0]
            curr_y = robot_posn[1]
            curr_theta = robot_posn[2]
            
            # recieve messages from all robots within communication range
            msgs = robot.recv_msg()
            i = 0
            mean_velocity = [0, 0]
            if len(msgs) > 0:
                mean_x = 0
                mean_y = 0

                while i < len(msgs):
                    rec_packet = struct.unpack('fff', msgs[i][:12])
                    rec_x = rec_packet[0]
                    rec_y = rec_packet[1]
                    rec_theta = rec_packet[2]

                    # ALIGNMENT
                    # velocity is approximated as a vector pointed in the direction of the robot's heading
                    # sum the recieved x and y components of "velocity" for each neighboring robot
                    mean_velocity[0] += math.cos(rec_theta)
                    mean_velocity[1] += math.sin(rec_theta)

                    # COHESION
                    # sum the recieved x and y positions for each neighboring robot
                    mean_x += rec_x
                    mean_y += rec_y

                    # SEPARATION
                    # calculate the distance from each neighboring robot
                    curr_dist = math.sqrt( (curr_x - rec_x)**2 + (curr_y - rec_y)**2 )

                    # create a vector pointed away from each neighboring robot
                    # magnitude is proportional to the distance
                    mini_separation = [(curr_x - rec_x), (curr_y - rec_y)]
                    v_separation[0] += 17 * curr_dist * mini_separation[0]
                    v_separation[1] += 17 * curr_dist * mini_separation[1]

                    i += 1 
                
                # divide mean velocity, x, and y positions by length of messages to find the average value
                # subtract current position to get a vector pointing in the direction of the average vector
                v_alignment[0] = (mean_velocity[0] / len(msgs)) - curr_x
                v_alignment[1] = (mean_velocity[1] / len(msgs)) - curr_y

                v_cohesion[0] = (mean_x / len(msgs)) - curr_x
                v_cohesion[1] = (mean_y / len(msgs)) - curr_y

 
            # normalize alignment, cohesion, and separation vectors
            if (v_alignment[0] != 0) and (v_alignment[1] != 0):
                alignment_mag = math.sqrt((v_alignment[0])**2 + (v_alignment[1])**2)
                v_alignment[0] = v_alignment[0] / alignment_mag
                v_alignment[1] = v_alignment[1] / alignment_mag
            
            if (v_cohesion[0] != 0) and (v_cohesion[1] != 0):
                cohesion_mag = math.sqrt((v_cohesion[0])**2 + (v_cohesion[1])**2)
                v_cohesion[0] = v_cohesion[0] / cohesion_mag
                v_cohesion[1] = v_cohesion[1] / cohesion_mag
            
            if (v_separation[0] != 0) and (v_separation[1] != 0):
                separation_mag = math.sqrt((v_separation[0])**2 + (v_separation[1])**2)
                v_separation[0] = v_separation[0] / separation_mag
                v_separation[1] = v_separation[1] / separation_mag

            # MIGRATION
			# calculate the x and y distances between com and the robot 
            v_migration[0] = com[0] - curr_x
            v_migration[1] = com[1] - curr_y


            # COMBINE
            # set up weights for the desired heading vector
            w_alignment = 1
            w_cohesion = 1
            w_separation = 1.2
            w_migration = 0.35

            # calculate the total vector for the robot's motion by summing the four vectors
            v_total_x = (w_alignment * v_alignment[0]) + (w_cohesion * v_cohesion[0]) + (w_separation * v_separation[0]) + (w_migration * v_migration[0])
            v_total_y = (w_alignment * v_alignment[1]) + (w_cohesion * v_cohesion[1]) + (w_separation * v_separation[1]) + (w_migration * v_migration[1])

             # calculate desired headiing
             # handle cases where the y and/or x components are 0
            if v_total_y == 0:
                if v_total_x >= 0: 
                    desired_theta = 0					# go straight right
                elif v_total_x < 0: 
                    desired_theta = math.pi				# go straight left
            elif v_total_x == 0:
                if v_total_y > 0:
                    desired_theta = math.pi / 2 		# go straight up
                elif v_total_y < 0:
                    desired_theta = -1 * math.pi / 2 	# go straight down
            else:
                # in any other cases, heading should simply be given by arctan
                desired_theta = math.atan2(v_total_y, v_total_x) 
            
            # set a velocity proportional to the difference between the desired and current heading
            heading_error = desired_theta - curr_theta
            turnrate = abs(heading_error) * 20 
            vel_x = turnrate 
            vel_y = turnrate 

            # optimizes turning direction
 			# if the total motion vector has a positive y component (quadrants 1 and 2), turn counterclockwise
 			# otherwise (quadrants 3 and 4), turn clockwise
            if v_total_y > 0:
                vel_x = -1 * abs(vel_x)
                vel_y = abs(vel_y)
            else:
                vel_x = abs(vel_x)
                vel_y = -1 * abs(vel_y)


            # SENDING MESSAGES
            robot.send_msg(struct.pack('fff', curr_x, curr_y, curr_theta))

            # obtain the time elapsed
            # the robot turns for 0.2 s and moves straight for 0.2 s
            robot_time = robot.get_clock()
            while robot.get_clock() < robot_time + 0.7: 
                print("STEP ONE")
                robot.set_vel(vel_x, vel_y)
                
            robot_time = robot.get_clock() 
            while robot.get_clock() < robot_time + 0.7:
                print("STEP TWO")
                robot.set_vel(35, 35)
            robot.set_vel(0, 0)
