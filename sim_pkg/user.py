def usr(robot):
    
    import struct
    import math
    import timeit

    # Toggles for debug (all should be turned (True) on for final result)
    mig = True              # if True, robots drive to center
    coh = True              # if true, robots drive to center of swarm
    ali = True              # if true, robots align
    sep = True              # if true, robots separate

    # Parameters
    dist_thresh = 500       # distance threshold, set up high, ended up not using it
    num_robots = 20         # number of robots in simulation
    k_theta = 25            # general tuning parameter of P-controller
    k_mig = 200             # tuning parameter for migration
    k_coh = 1               # tuning parameter for cohesion
    k_ali = 1               # tuning parameter for alignment
    k_sep = 1.2             # tuning parameter for separation

    # init variables
    pos_x = [0] * num_robots
    pos_y = [0] * num_robots
    vel_x = [0] * num_robots
    vel_y = [0] * num_robots
    rec_poses = 0
    x_old = 0
    y_old = 0
    time_old = 0
    velx = 0
    vely = 0

    # gridpos = robot.math.Vec2(-3, -6)
    # print(gridpos)


    while True:
        # reset desired heading vector
        x_des = 0
        y_des = 0

        # get pose and save it
        pose = robot.get_pose()
        while not pose:
            pose = robot.get_pose()
        if pose:
            x = pose[0]
            y = pose[1]
            theta = pose[2]

        # get time for velocity
        time = robot.get_clock()
        # don't try to calculate velocity in first iteration
        if x_old != 0:
            if (time - time_old) > 0.0001:
                velx = (x - x_old)/(time - time_old)
                vely = (y - y_old)/(time - time_old)
                x_old = x
                y_old = y
                time_old = time
        # but still save old values for second iteration
        else:
            x_old = x
            y_old = y
            time_old = time


        # send position and velocity
        msg = struct.pack('ffiff', x, y, robot.id, velx, vely)
        # print("User code",type(msg))
        robot.send_msg(msg)
        # receive position and velocity from all robots in distance threshold
        msgs = robot.recv_msg()
        if len(msgs) > 0:
            # if a position is received, add repul velocity
            for i in range(len(msgs)):
                
                pose_rxed = struct.unpack('ffiff', msgs[i][:20])
                if ((pos_x[pose_rxed[2]]-x)**2+(pos_y[pose_rxed[2]]-y)**2) < dist_thresh:
                    pos_x[pose_rxed[2]] = pose_rxed[0]
                    pos_y[pose_rxed[2]] = pose_rxed[1]
                    vel_x[pose_rxed[2]] = pose_rxed[3]
                    vel_y[pose_rxed[2]] = pose_rxed[4]
                else:
                    pos_x[pose_rxed[2]] = 0.0001
                    pos_y[pose_rxed[2]] = 0.0001
                    vel_x[pose_rxed[2]] = 0.0001
                    vel_y[pose_rxed[2]] = 0.0001

        # check if all robots have sent a position yet
        if rec_poses < (num_robots-1):
            rec_poses = 0
            for i in range(num_robots):
                if pos_x[i] != 0:
                    rec_poses = rec_poses + 1
        if rec_poses == 0:
            rec_poses = 1

        # calculate the average of the position and velocity for controller
        pos_x_avg = sum(pos_x)/rec_poses
        pos_y_avg = sum(pos_y)/rec_poses
        vel_x_avg = sum(vel_x)/rec_poses
        vel_y_avg = sum(vel_y)/rec_poses
        rec_poses = 0
        # norm the average velocity, do not divide by 0
        if vel_x_avg <= 0.001:
            vel_norm = 1
        else:
            vel_norm = math.sqrt(vel_x_avg**2+vel_y_avg**2)
        vel_x_avg = vel_x_avg/vel_norm
        vel_y_avg = vel_y_avg/vel_norm

        if coh:
            # add cohesion to desired heading vector
            x_coh = (pos_x_avg - x)/math.sqrt((pos_x_avg - x)**2+(pos_y_avg - y)**2)
            y_coh = (pos_y_avg - y)/math.sqrt((pos_x_avg - x)**2+(pos_y_avg - y)**2)
            x_des = x_des + k_coh * x_coh
            y_des = y_des + k_coh * y_coh

        if mig:
            # add migration to desired heading vector
            x_des = x_des + k_mig * (-x) / 500
            y_des = y_des + k_mig * (-y) / 500

        if ali:
            # add alignment to desired heading vector
            x_des = x_des + k_ali * vel_x_avg
            y_des = y_des + k_ali * vel_y_avg

        if sep:
            # add separation to desired heading
            x_rep = 0
            y_rep = 0
            for i in range(num_robots):
                if ((pos_x[i]-x)**2 + (pos_y[i]-y)**2) > 0.01:
                    if i != robot.id:
                        x_rep = x_rep + (x - pos_x[i]) / ((pos_x[i] - x) ** 2 + (pos_y[i] - y) ** 2)
                        y_rep = y_rep + (y - pos_y[i]) / ((pos_x[i] - x) ** 2 + (pos_y[i] - y) ** 2)

            if math.sqrt(x_rep ** 2 + y_rep ** 2) > 0.001:
                x_des = x_des + k_sep * x_rep / math.sqrt(x_rep ** 2 + y_rep ** 2)
                y_des = y_des + k_sep * y_rep / math.sqrt(x_rep ** 2 + y_rep ** 2)

        # calculate desired heading theta
        theta_des = math.atan2(y_des, x_des)
        theta_diff = theta_des - theta

        # wrap the difference in theta to [-pi,pi)
        if theta_diff >= math.pi:
            theta_diff = theta_diff - 2*math.pi
        if theta_diff < -math.pi:
            theta_diff = theta_diff +  2* math.pi

        # P-controller for turning rate of robots speed 50
        vl = 20 + k_theta * theta_diff/math.pi
        vr = 20 - k_theta * theta_diff/math.pi

        # set the speed
        robot.set_vel(vr, vl)