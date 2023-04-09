# Michelle Zhang
def usr(robot):
	import struct
	import math
	import timeit
	import random 

	# center of gravity (position of lightbulb)
	cog = (0, 0) 
	
	# setting LED colors based on id
	if robot.assigned_id==0:
		robot.set_led(100,0,0)
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
	else:
		robot.set_led(0,0,100)

	while True:
		# obtain robot's current position
		robot_posn = robot.get_pose()

		# initialize vectors for calculating heading
		v_phototaxis = [0, 0]
		v_repulsion = [0, 0]
		v_random = [0, 0]

		if robot_posn:
			curr_x = robot_posn[0]
			curr_y = robot_posn[1]
			curr_theta = robot_posn[2]
			# curr_theta is 0 when the pointy side faces the +x direction
			# it increases counterclockwise to pi inclusive (-x direction) 
			# then it flips to -pi (not inclusive) and goes down to 0

			# PHOTOTAXIS
			# calculate the x and y distances between cog and the robot 
			x_dist = cog[0] - curr_x
			y_dist = cog[1] - curr_y

			# create a unit vector pointing from the robot to the cog (divide each component by magnitude)
			ptaxis_magnitude = math.sqrt( (x_dist)**2 + (y_dist)**2 )
			v_phototaxis[0] = x_dist / ptaxis_magnitude
			v_phototaxis[1] = y_dist / ptaxis_magnitude

			# REPULSION
			# note possible internuclear robot distance ranges from: 0.12 to 0.4 based on communication range

			# set the radii for the robots based on id
			# two id case:
			if robot.assigned_id == 0:
				curr_radius = 0.09
			elif robot.assigned_id == 1:
				curr_radius = 0.15 
			else:
				curr_radius = 0.20 
 
			k = 17

			# each robot sends its x and y coordinate
			robot.send_msg(struct.pack('ff', curr_x, curr_y))

			# each robot recieves messages from neighbors
			msgs = robot.recv_msg()
			i = 0
			if len(msgs) > 0:
				while i < len(msgs):
					# the following is repeated for each neighbor
					# obtain the x, y coordinates of the neighboring robot
					rec_packet = struct.unpack('ff', msgs[i][:8])
					rec_x = rec_packet[0]
					rec_y = rec_packet[1]

					# calculate the distance from it 
					curr_dist = math.sqrt( (curr_x - rec_x)**2 + (curr_y - rec_y)**2 )

					if curr_dist < (2 * curr_radius): 
						# if the robots overlap (the distance between them becomes too small)

						# create a unit vector pointing from the neighbor to the current robot 
						# (effectively pointing away from the neighbor)
						j_v_repulsion = [(curr_x - rec_x) / curr_dist, (curr_y - rec_y) / curr_dist]

						# scale the repulsion vector by the following magnitude
						j_repulsion_mag = k * ((2 * curr_radius) - curr_dist)
						j_v_repulsion[0] = j_repulsion_mag * j_v_repulsion[0]
						j_v_repulsion[1] = j_repulsion_mag * j_v_repulsion[1]

						# add this new repulsion vector to the overall repulsion vector
						v_repulsion[0] += j_v_repulsion[0]
						v_repulsion[1] += j_v_repulsion[1]

					i += 1

			# RANDOM
			# generate two random x and y values for the vector
			# (subtract to ensure you can get negative values)
			rand_x = random.randint(1, 800) - 400
			rand_y = random.randint(1, 800) - 400
			
			# create a unit random vector (divide each component by magnitude)
			rand_mag = math.sqrt( (rand_x)**2 + (rand_y)**2 )
			v_random[0] = rand_x / rand_mag
			v_random[1] = rand_y / rand_mag

			c = 0.8 

			# COMBINE
			# calculate the total vector for the robot's motion by summing the three vectors
			v_total_x = v_phototaxis[0] + v_repulsion[0] + c * v_random[0]
			v_total_y = v_phototaxis[1] + v_repulsion[1] + c * v_random[1]

			# calculate the desired heading
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
				
			# optimizes turning direction
			# if the total motion vector has a positive y component (quadrants 1 and 2), turn counterclockwise
			# otherwise (quadrants 3 and 4), turn clockwise
			if v_total_y > 0:
				direction = True
			else:
				direction = False

			# turn while the current heading is NOT within a reasonable range around the desired heading
			# direction of the turn is given by the above booleans
			while curr_theta < desired_theta - 0.09 or curr_theta > desired_theta + 0.09:
				if direction: 
					robot.set_vel(-20, 20)
				else:
					robot.set_vel(20, -20)
				
				# update current heading 
				updateposn = robot.get_pose()
				if updateposn:
					curr_theta = updateposn[2]

			# obtain the time elapsed
			robot_time = robot.get_clock()
			# move straight for some amount of time (here, 1.6 s)
			while robot.get_clock() < robot_time + 1.6:
				robot.set_vel(50, 50)
			
			robot.set_vel(0,0)