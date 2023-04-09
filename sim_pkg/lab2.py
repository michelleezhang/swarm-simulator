# Michelle Zhang
from email import message
from gettext import find

# IMPORTANTTT: this runs for EACH robot!!
def usr(robot):
	import struct
	import math
	import timeit

	# variable to toggle for 1-smoothing
	smooth = False

	# initialize variables for smoothing
	sum1 = 0
	sum2 = 0
	n = 0

	# intialize minimum hop count from each seed to very large numbers (effectively infinity)
	minhop1 = 21474836
	minhop2 = 21474836

	# intialize x and y coordinates for the seeds
	# seed 1: (0, 0)
	# seed 2: (15, 1)
	seed1x = 0
	seed1y = 0
	seed2x = 15
	seed2y = 1

	while True:
		time = robot.get_clock()
		if not smooth:
			# seeds send hopcount, location, and id
			if robot.assigned_id == 1: # seed 1
				robot.set_led(0, 0, 100)
				robot.send_msg(struct.pack('iii', 1, minhop2, robot.assigned_id))
			if robot.assigned_id == 2: # seed 2
				robot.set_led(0, 0, 100)
				robot.send_msg(struct.pack('iii', minhop1, 1, robot.assigned_id))

			# each robot recieves messages
			if robot.assigned_id == 0:
				a = False
				hopdiff = False # True if hop count changes
				i = 0
				msgs = robot.recv_msg()
				if len(msgs) > 0:			# if our message is non-empty
					while i < len(msgs):	# loop because messages may contain multiple messages at once
						a = True

						# unpack message
						umessage = struct.unpack('iii', msgs[i][:12])
						currhop1 = umessage[0]
						currhop2 = umessage[1]
						currseed = umessage[2]

						# set minimum hopcounts
						if (currhop1 < minhop1):
							minhop1 = currhop1
							hopdiff = True
						if (currhop2 < minhop2):
							minhop2 = currhop2
							hopdiff = True
						
						i = i + 1
					# at the end of this while loop, we have gone through all the messages from nearby robots
					# and obtained minhop 1 and minhop 2 (the shortest distances to the seeds)

					# forward location and incremented hop count
						robot.send_msg(struct.pack('iii', minhop1 + 1, minhop2 + 1, currseed))	
					
				# for 1-smoothing, obtain hop counts from all neighbors of the robot 
				# by doing a second loop for messaging 
					if smooth:
						robot.send_msg(struct.pack('ii', minhop1, minhop2))
						while robot.get_clock() > time + 3:
							messags = robot.recv_msg()
							if len(messags) > 0:
								while n < len(messags):
									u_message = struct.unpack('ii', messags[n][:8])
									finalhop1 = u_message[0]
									finalhop2 = u_message[1]

									sum1 += finalhop1
									sum2 += finalhop2 
									n += 1
								#robot.send_msg(struct.pack('ii', minhop1, minhop2))
					# LEDs for debugging 
					# if minhop2 % 2 == 0:
					# 	robot.set_led(0, 100, 0) # green
					# else:
					# 	robot.set_led(100, 0, 0) # red

				# assign coordinate system
				# x ranges 0 to 15
				# y ranges 0 to 31
				min_error = 21474836
				if i >= 3 and hopdiff and a: # if we have recieved at least 3 messages
					# loop through each possible x and y position

					for x in range(0, 16, 1): #edit middle -- start, end, time step (gaps )
						for y in range(0, 32, 1):
							# find distance
							dist1 = math.sqrt((seed1x - x)**2 + ((seed1y - y)/2)**2)
							dist2 = math.sqrt((seed2x - x)**2 + ((seed2y - y)/2)**2)

							# if smoothing, use averaged gradient value
							if smooth:
								minhop1 = ((sum1 + minhop1) / (n + 1)) - 0.5
								minhop2 = ((sum2 + minhop2) / (n + 1)) - 0.5

							# find total error
							totalerror = (dist1 - minhop1)**2 + (dist2 - minhop2)**2
							#print('error', totalerror, minhop1, minhop2)

							# assign x and y with the smallest error
							if totalerror <= min_error:
									min_error = totalerror
									finalx = x
									finaly = y
				
				# set LEDs
				try:
					print('final x/y: ', finalx, finaly)
					if finalx < 5: 
						robot.set_led(0, 100, 0)
					if finalx > 11:
						robot.set_led(0, 100, 0)
					if (-1.1 * finalx + 20) <= finaly <= (-1.1 * finalx + 32):
						robot.set_led(0, 100, 0)
				except:
					pass


			
