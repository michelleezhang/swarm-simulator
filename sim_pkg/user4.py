def usr(robot):
	import struct
	import math
	import numpy as np
	import timeit


	# variable determining whether to do the regular or smoothing
	# 1= regular; 0 = smoothing
	regular = 0

	# generate array of Northwestern N
	# 0 = no color, 1 = purple
	Northwestern = np.zeros((16,16))
	# fill in the rectangles
	# two long vertical sides
	for Nx in range(0,3):
		for Ny in range(16):
			Northwestern[Nx,Ny] = 1
	for Nx in range(13,16):
		for Ny in range(16):
			Northwestern[Nx,Ny] = 1
	#two short on top and bottom of N
	for Nx in range(2,5):
		for Ny in range(0,2):
			Northwestern[Nx,Ny] = 1
	for Nx in range(11,14):
		for Ny in range(14,16):
			Northwestern[Nx,Ny] = 1
	#triangle at bottom
	Northwestern[2,2] = 1
	Northwestern[2,3] = 1
	Northwestern[3,2] = 1
	#triangle at top
	Northwestern[13,13] = 1
	Northwestern[12,13] = 1
	Northwestern[13,12] = 1
	# diagonal
	tmpdiag = 0
	for Nx in range(2,14):
		for Ny in range(11-tmpdiag,16-tmpdiag):
			Northwestern[Nx,Ny]=1
		tmpdiag = tmpdiag+1


	#some large count number as a place holder, no first count will ever be this high and will change
	# count1 corresponds to seed1, count2 corresponds to seed2
	count1 = 500
	count2 = 500

	# keep track of received gradient values from both seeds
	fromseed1 = np.zeros((3,1))
	fromseed2 = np.zeros((3,1))

	# minimize the error in the calculated distance and estimated distance
	# x, y value associated with this
	mindisterr = 1000000
	estx = 0
	esty = 0

	while True:
		# locally propagating gradient step
		# seed robots initiates gradient, non seed robots have id 0
		if robot.assigned_id != 0:
			count = 1

			# send message to neighbors within Com_Range with its count=1 and location (x,y) and robot assigned id
			# location is known from a global position
			# seed robot in bottom left corner
			if robot.assigned_id == 1:
				x1 = 0
				y1 = 0
				estx = x1
				esty = y1
				robot.send_msg(struct.pack('iffi', count,x1,y1,robot.assigned_id))
			# seed robot in bottom right corner
			if robot.assigned_id == 2:
				x2 = 15
				y2 = 0
				estx = x2
				esty = y2
				robot.send_msg(struct.pack('iffi', count,x2,y2,robot.assigned_id))

		else: # nonseed robots
			msgs = robot.recv_msg()
			# make sure there are received messages
			if len(msgs) > 0:
				# unpack message
				msg = struct.unpack('iffi', msgs[0][:16])

				msgcount = msg[0]
				robotID = msg[3]

				# maintain lowest count value
				# ignore messages that have higher counts
				if robotID == 1:
					if msgcount < count1:
						count1 = msgcount
						fromseed1[0,0] = msgcount
						fromseed1[1,0] = msg[1]
						fromseed1[2,0] = msg[2]
				if robotID == 2:
					if msgcount < count2:
						count2 = msgcount
						fromseed2[0,0] = msgcount
						fromseed2[1,0] = msg[1]
						fromseed2[2,0] = msg[2]

				# check there is a message from each seed
				if fromseed1[0,0]>0 and fromseed2[0,0]>0:
					# communication range from configuration file coachswarm
					r = 0.13

					# x and y values of seed 1
					seed1x = fromseed1[1,0]
					seed1y = fromseed1[2,0]

					# x and y values of seed 2
					seed2x = fromseed2[1,0]
					seed2y = fromseed2[2,0]

					#estimated distances to seeds
					estdist1 = 0
					estdist2 = 0

					if regular ==1:
						# distance to seed 1
						estdist1 = count1*r

						#distance to seed 2
						estdist2 = count2*r
					else: # use smooth method

						# neighbors increment count by 1 before sending it
						smoothcount1 = fromseed1[0,0] - 1
						smoothcount2 = fromseed2[0,0] - 1

						#each neighbor collects neighbor gradient values and computes average of itself and neighbor values
						estdist1 = (count1+smoothcount1)/2
						estdist2 = (count2+smoothcount2)/2

						# because of low resolution, average error of ~0.5r is added to distance estimates
						estdist1 = (estdist1-0.5)*r
						estdist2 = (estdist2-0.5)*r

						''' couldn't get this implementation to work
						numiters = 0
						for i in range(len(msgs)):
							smoothmsg = struct.unpack('iffi', msgs[0][:16])
							smoothmsgcount = smoothmsg[0]
							smoothrobotID = smoothmsg[3]
							# neighbors increment count by 1 before sending it
							smoothcount1 = 0
							smoothcount2 = 0
							if smoothrobotID == 1:
								smoothcount1 = smoothmsgcount
							if smoothrobotID == 2:
								smoothcount2 = smoothmsgcount

							estdist1 = (estdist1+smoothcount1)
							estdist2 = (estdist2+smoothcount2)
							numiters = numiters + 1
						estdist1 = (count1+estdist1)/(numiters+1)
						estdist2 = (count2+estdist2)/(numiters+1)
						# because of low resolution, average error of ~0.5r is added to distance estimates
						estdist1 = (estdist1-0.5)*r
						estdist2 = (estdist2-0.5)*r
						'''

					minidisterr = 1000000
					# the grid is 16 x 16
					for xval in range(16):
						for yval in range(16):
							# calculate distance to seed 1; multiplied by r
							calcdist1 = math.sqrt((seed1x-xval)**2 + (seed1y-yval)**2)*r
							# calculate distance to seed 2; multiplied by r
							calcdist2 = math.sqrt((seed2x-xval)**2 + (seed2y-yval)**2)*r

							# calculate error in calculated and estimated distances
							disterr = (calcdist1-estdist1)**2 + (calcdist2-estdist2)**2

							if disterr < mindisterr:
								mindisterr = disterr
								estx = xval
								esty = yval
								#print(estx)
					#end for loops


				# increments count by 1 and then send to neighbors
				sendcount = 0
				if robotID == 1:
					sendcount = count1 +1
				if robotID == 2:
					sendcount = count2 +1
				# send message to neighbors with minimum count incremented by 1
				robot.send_msg(struct.pack('iffi',sendcount,msg[1],msg[2],robotID))


		# set LED colors
		# check if this coordinate corresponds to a coordinate inside the N
		if Northwestern[int(estx),int(esty)] == 1:
			robot.set_led(66,28,82)
		else:
			robot.set_led(0,0,0)

		'''
		# use LED to debug hopcount
		if count1%2 == 0:
			robot.set_led(100,0,0)
		else:
			robot.set_led(0,0,100)

		if count2%2 == 0:
			robot.set_led(0,100,0)
		else:
			robot.set_led(0,0,100)


		# debug coordinates
		if esty > 12:
			robot.set_led(100,0,0)
		else:
			robot.set_led(0,0,100)
		'''