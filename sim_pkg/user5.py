def usr(robot):
	import struct
	import math
	import timeit
	import random

	# virtual radius of robot
	vrad = 0
	# set ids for robots with corresponding LEDs
	# set the virtual radius of robot
	if robot.assigned_id==0:
		robot.set_led(100,0,0)
		vrad = 0.13
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
		vrad = 0.18
	else:
		robot.set_led(0,0,100)
		vrad = 0.39

	# x, y, location of the arena center
	centerx = 0
	centery = 0

	# tolerance value for the turning
	turntol = 0.08


	while True:
		# get robot's pose (x,y,theta)
		pose_t=robot.get_pose()

		# check robot's position
		if pose_t: #check pose is valid before using
			pose=pose_t
			#print('The postion of robot ',robot.id,' is ', pose[0],pose[1],pose[2])

			# update robot x and y values
			rposx = pose[0]
			rposy = pose[1]
			rtheta = pose[2] #between 0 and pi and -pi and 0


			# find vector from robot center to arena center - make into unit vector
			# distance from robot to arena center
			distToCen = math.sqrt((centerx-rposx)**2 + (centery-rposy)**2)

			# vector pointing from robot to arena center
			vecToCenx = 0
			vecToCeny = 0

			# not on top of the arena center
			if distToCen != 0:
				# x component
				vecToCenx = (centerx-rposx)/distToCen

				# y component
				vecToCeny = (centery-rposy)/distToCen


			# calculate motion vector
			# taxis: attraction to arena center, unit vector - same as the vecToCen already calculated
			vtaxisx = vecToCenx
			vtaxisy = vecToCeny

			# random motion, unit vector
			vrandx = random.uniform(0,2*math.pi)
			vrandx = math.cos(vrandx)
			vrandy = random.uniform(0,2*math.pi)
			vrandy = math.sin(vrandy)
			# multiply by crand to weight the magnitude
			crand = 0.65 # paper used 0.6
			vrandx = crand*vrandx
			vrandy = crand*vrandy

			# repulsion from nearby robots
			vrepulx = 0
			vrepuly = 0

			# keep track of neighbors
			neighbors = []

			# determine the neighbors in the communication radius
			msgs = robot.recv_msg()
			# there are received messages
			#if robot.id == 3:
			#	print(len(msgs))
			if len(msgs) > 0:
				for i in range(len(msgs)): #repeat for however many messages are here
					# unpack message
					msg = struct.unpack_from('iff', msgs[i])
					#print(struct.calcsize('iff'))

					# other robot id
					obotID = msg[0]
					if obotID not in neighbors: # check if already added it as a neighbor
						neighbors.append(obotID)
						#if robot.id ==3:
						#	print(len(neighbors))

						# neighbor's x and y values
						obotx = msg[1]
						oboty = msg[2]

						# calculate distance between robots
						distbtwn = math.sqrt((obotx-rposx)**2 + (oboty-rposy)**2)

						# checking distances
						#if robot.id == 0:
						#	print(distbtwn)

						# assume neighbor has same radius
						if distbtwn < 2*vrad:
							# overlapping, need to move away
							# move in vector in opposite direction
							tmpx = (rposx-obotx)/distbtwn
							tmpy = (rposy-oboty)/distbtwn

							vrepulx = vrepulx + tmpx
							vrepuly = vrepuly + tmpy

			# limit max repulsion (paper used 6.4)
			if math.sqrt(vrepulx**2 + vrepuly**2) > 6.4:
				if vrepulx < 0: #preserve sign
					vrepulx = -3.5
				else:
					vrepulx = 3.5
				if vrepuly <0:
					vrepuly = -3.5
				else:
					vrepuly = 3.5


			# total motion vector
			motionvx = vtaxisx + vrandx + vrepulx
			motionvy = vtaxisy + vrandy + vrepuly

			# unit motion vector for the while loop
			magmotion = math.sqrt((motionvx**2)+(motionvy**2))
			umotionx = motionvx/magmotion
			umotiony = motionvy/magmotion

			# turn to point in motion vector direction
			while abs(umotionx-math.cos(rtheta))>turntol and abs(umotiony-math.sin(rtheta))>turntol:
				# turn towards the left
				robot.set_vel(-100,100)

				#if abs(motionvx) - abs(math.cos(rtheta)) >= 0:
				#	robot.set_vel(-100,100)
				#else: #turn towards the right
				#	robot.set_vel(100,-100)


				# get the current pose
				# get robot's pose (x,y,theta)
				pose_t=robot.get_pose()

				# check robot's position
				if pose_t: #check pose is valid before using
					pose=pose_t
					#print('The postion of robot ',robot.id,' is ', pose[0],pose[1],pose[2])

					# update robot x and y values
					rposx = pose[0]
					rposy = pose[1]
					rtheta = pose[2]

			# end while loop

			# robot move forward according to the motion vector
			# get the current time
			timestart = robot.get_clock()
			currtime = timestart
			while currtime - timestart < 1.5: # go for this many seconds
				# velocity proportional to magnitude of motion vector
				#print(magmotion)
				if magmotion < 0.5:
					vel = 20
				elif magmotion < 1.2:
					vel = 45
				else:
					vel = 60
				robot.set_vel(vel, vel)
				# update current position
				# get robot's pose (x,y,theta)
				pose_t=robot.get_pose()

				# check robot's position
				if pose_t: #check pose is valid before using
					pose=pose_t
					#print('The postion of robot ',robot.id,' is ', pose[0],pose[1],pose[2])

					# update robot x and y values
					rposx = pose[0]
					rposy = pose[1]
					rtheta = pose[2]

					currtime = robot.get_clock()
					robot.send_msg(struct.pack('iff', robot.id, rposx, rposy))

			# end while loop
			robot.send_msg(struct.pack('iff', robot.id, rposx, rposy))