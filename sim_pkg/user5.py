time_step = 2
robot_radius = 0.056 #0.08
message_radius = robot_radius*3.8
import math
import struct

def usr(robot):    
    count = 3
    num_robots = 1
    received = 0
    incoming_pos_dict = {}
    vo = {}
    dict_ORCA = {}
    new_vel = {}
    invalid = 0
    finished_turning = 0

    print("update check 2")
    while True:
        robot.delay()

        if robot.id == 1:
            curr_pose = robot.get_pose()
            while not curr_pose:
                curr_pose = robot.get_pose()
            curr_x = curr_pose[0]
            curr_y = curr_pose[1]
            curr_theta = curr_pose[2]   
            # desired_x = -0.1
            # desired_y = -0.4
                
            desired_pose = N_init_positions(robot.id)
            if desired_pose == False:
                desired_x = curr_x
                desired_y = curr_y
            else:
                desired_x = desired_pose[0]
                desired_y = desired_pose[1]
            # robot.logger.info(desired_x)
            # robot.logger.info("done with desired position")

            # robot.logger.info(curr_pose)
            # send count for 2 seconds                
            last = robot.get_clock()
            while(robot.get_clock()-last) < 0.3:
                # to_send = package_string([count%3])
                # # robot.logger.info(to_send)
                # did_send = robot.send_msg(to_send)
                robot.send_msg(struct.pack('fi', (robot.get_clock()- last), (count%3)))
                robot.delay()
            # robot.logger.info("sent count")

            start_time = robot.get_clock()
            if (count%3) == 0:
                # robot.logger.info("in 0")
                robot.set_led(255,0,0)
                curr_pose = robot.get_pose()
                while not curr_pose:
                    curr_pose = robot.get_pose()
                curr_x = curr_pose[0]
                curr_y = curr_pose[1]
                curr_theta = curr_pose[2]  
                # calculate own optimal velocity
                own_vopt_x = desired_x-curr_x
                own_vopt_y = desired_y-curr_y
                # own_vopt_x = own_vopt_x/(math.sqrt(own_vopt_x**2+own_vopt_y**2))
                # own_vopt_y = own_vopt_y/(math.sqrt(own_vopt_x**2+own_vopt_y**2))
                opt_theta = math.atan2(own_vopt_y, own_vopt_x)
                # robot.logger.info(opt_theta * (180 / math.pi))
                # robot.logger.info("calculated own optimal velocity")

                # send and receive own and other position
                flush = robot.recv_msg()
                last = robot.get_clock()
                while(robot.get_clock()-last) < 0.7:
                    # robot.logger.info(i)
                    for i in range(2):             
                        # send message with pose
                        # to_send = package_string([robot.id, curr_x, curr_y, curr_theta, own_vopt_x, own_vopt_y])
                        # did_send = robot.send_msg(to_send)
                        # robot.logger.info(did_send)
                        # robot.delay()
                        robot.send_msg(struct.pack('ifffff', robot.id, curr_x, curr_y, curr_theta, own_vopt_x, own_vopt_y))

                    rec_str = robot.recv_msg()
                    # robot.delay()
                    if len(rec_str) > 0:
                        # print(rec_str)
                        check_string = unpack_other_pos_string(robot, rec_str)
                        if len(check_string) > 2:
                            passive_position = check_string
                            # robot.logger.info(len(passive_position)/6)
                            i = 0
                            while i <(len(passive_position)-5):    
                                incoming_pos_dict[passive_position[i]] = [passive_position[i+1], passive_position[i+2], passive_position[i+3], passive_position[i+4], passive_position[i+5]]
                                i = i+6
                # robot.logger.info(incoming_pos_dict)

                updated_x = own_vopt_x
                updated_y = own_vopt_y
                desired_theta = opt_theta
                for key in incoming_pos_dict:                    
                    dist_check = math.sqrt((curr_x-incoming_pos_dict[key][0])**2 + (curr_y-incoming_pos_dict[key][1])**2)
                    # robot.logger.info(key)
                    if dist_check < message_radius:
                        vo[key] = compute_boudaries(robot, curr_pose, incoming_pos_dict[key])
                        # robot.logger.info(vo[key])
                        w = compute_w(robot, vo[key], updated_x, updated_y, incoming_pos_dict[key][3],
                                    incoming_pos_dict[key][4])
                        # robot.logger.info(w)
                        n = compute_n(vo[key], w, updated_x, updated_y, incoming_pos_dict[key][3],
                                    incoming_pos_dict[key][4])
                        # robot.logger.info(n)
                        dict_ORCA[key] = gen_ORCA_line(robot, vo[key], n, w, updated_x, updated_y)
                        # robot.logger.info(dict_ORCA[key])
                        output = combine_ORCAs(robot,updated_x, updated_y, dict_ORCA, vo, key)
                        updated_x = output[0]
                        updated_y = output[1]
                        # robot.logger.info(output)
                        if output[0] == 0 and output[1] == 0:
                            invalid = 1
                            robot.set_led(0,0,0)
                        else:
                            desired_theta = math.atan2(output[1], output[0])
                            # robot.logger.info(desired_theta * (180 / math.pi))
                wait(robot, start_time, end_time=1)
                # robot.logger.info("finished waiting")
            elif (count%3) == 1:
                # robot.logger.info("in 1")
                robot.set_led(0,255,0)
                if invalid == 0:
                        # while (robot.get_clock()-start_time) < 1.9:
                    finished_turning = turn_to_angle(robot, curr_theta, desired_theta,start_time)
                wait(robot, start_time, end_time=2)
            elif (count%3) == 2:
                # robot.logger.info("in 2")
                dist = math.sqrt((curr_x-desired_x)**2 + (curr_y-desired_y)**2)
                # robot.logger.info(invalid)
                if abs(dist) > 0.05 and invalid == 0 and finished_turning == True:
                    robot.set_led(0,0,255)
                    robot.set_vel(60,60)
                    # robot.delay(700)
                    # robot.set_vel(0,0)                    
                elif abs(dist) < 0.05:
                    robot.set_led(0,0,0)
                elif invalid == 1:
                    robot.set_led(255,255,255)
                elif finished_turning==False:
                    robot.set_led(255,0,255)
                invalid = 0                
                wait(robot, start_time, end_time=0.5)
            vo = {}
            dict_ORCA = {}
            # incoming_pos_dict = {}
            robot.set_vel(0,0)
            dist = math.sqrt((curr_x-desired_x)**2 + (curr_y-desired_y)**2)
            count += 1
            

        else:
            curr_pose = robot.get_pose()
            while not curr_pose:
                curr_pose = robot.get_pose()
            curr_x = curr_pose[0]
            curr_y = curr_pose[1]
            curr_theta = curr_pose[2]   
            # desired_x = -0.1
            # desired_y = -0.4
                
            desired_pose = N_init_positions(robot.id)
            if desired_pose == False:
                desired_x = curr_x
                desired_y = curr_y
            else:
                desired_x = desired_pose[0]
                desired_y = desired_pose[1]
            # robot.logger.info(desired_x)
            # robot.logger.info("done with desired position")
            
            # robot.logger.info(curr_pose)
            # send count for 2 seconds
            flush = robot.recv_msg()
            last = robot.get_clock()        
            time_elapsed = robot.get_clock() - last
            while(time_elapsed) < 0.3:
                # if received == 0:
                rec_str = robot.recv_msg()
                # robot.delay(50) #110
                # robot.logger.info(len(rec_str))
                if len(rec_str) > 0:
                    # print("before unpack")
                    count_received = struct.unpack('fi', rec_str[0][:8])
                    # print(count_received)
                    if abs(count_received[1]) < 3:
                        if (count_received[1] != count): # and (received == 0):
                            count = count_received[1]
                            # if robot.id == 3:
                            #     print(count)
                            received = 1
                            time_elapsed = count_received[0]
                            last = robot.get_clock()
                            # robot.logger.info(rec_str)
                            # robot.logger.info("received count")
                        else:
                            time_elapsed = time_elapsed + (robot.get_clock() - last)
            
            if received==1:
                start_time = robot.get_clock()
                if (count%3) == 0:
                    # robot.logger.info("in 0")
                    robot.set_led(255,0,0) 
                    curr_pose = robot.get_pose()                   
                    while not curr_pose:
                        curr_pose = robot.get_pose()
                    curr_x = curr_pose[0]
                    curr_y = curr_pose[1]
                    curr_theta = curr_pose[2]
                    
                    # calculate own optimal velocity
                    own_vopt_x = desired_x-curr_x
                    own_vopt_y = desired_y-curr_y
                    # own_vopt_x = own_vopt_x/(math.sqrt(own_vopt_x**2+own_vopt_y**2))
                    # own_vopt_y = own_vopt_y/(math.sqrt(own_vopt_x**2+own_vopt_y**2))
                    opt_theta = math.atan2(own_vopt_y, own_vopt_x)
                    # robot.logger.info(opt_theta * (180 / math.pi))
                    # robot.logger.info("calculated own optimal velocity")

                    # send and receive own and other position
                    flush = robot.recv_msg()
                    last = robot.get_clock()
                    while(robot.get_clock()-last) < 0.7:
                        # robot.logger.info(i)
                        for i in range(2):             
                            # send message with pose
                            # to_send = package_string([robot.id, curr_x, curr_y, curr_theta, own_vopt_x, own_vopt_y])
                            # did_send = robot.send_msg(to_send)
                            # print(to_send)
                            # robot.delay()
                            robot.send_msg(struct.pack('ifffff', robot.id, curr_x, curr_y, curr_theta, own_vopt_x, own_vopt_y))

                        rec_str = robot.recv_msg()
                        # robot.delay()
                        if len(rec_str) > 2:
                            check_string = unpack_other_pos_string(robot, rec_str)
                            if len(check_string) > 2:
                                passive_position = check_string
                                # robot.logger.info(len(passive_position)/6)
                                i = 0
                                while i <(len(passive_position)-5):    
                                    incoming_pos_dict[passive_position[i]] = [passive_position[i+1], passive_position[i+2], passive_position[i+3], passive_position[i+4], passive_position[i+5]]
                                    i = i+6
                    # robot.logger.info(incoming_pos_dict)
                
                    updated_x = own_vopt_x
                    updated_y = own_vopt_y
                    desired_theta = opt_theta
                    for key in incoming_pos_dict:
                        dist_check = math.sqrt((curr_x-incoming_pos_dict[key][0])**2 + (curr_y-incoming_pos_dict[key][1])**2)
                        # robot.logger.info(key)  
                        if dist_check < message_radius:
                            vo[key] = compute_boudaries(robot, curr_pose, incoming_pos_dict[key])
                            # robot.logger.info(vo[key])
                            w = compute_w(robot, vo[key], updated_x, updated_y, incoming_pos_dict[key][3],
                                        incoming_pos_dict[key][4])
                            # robot.logger.info(w)
                            n = compute_n(vo[key], w, updated_x, updated_y, incoming_pos_dict[key][3],
                                        incoming_pos_dict[key][4])
                            # robot.logger.info(n)
                            dict_ORCA[key] = gen_ORCA_line(robot, vo[key], n, w, updated_x, updated_y)
                            # robot.logger.info(dict_ORCA[key])
                            output = combine_ORCAs(robot, updated_x, updated_y, dict_ORCA, vo, key)
                            updated_x = output[0]
                            updated_y = output[1]
                            # robot.logger.info(output)
                            if output[0] == 0 and output[1] == 0:
                                invalid = 1
                                robot.set_led(255,255,255)
                            else:
                                desired_theta = math.atan2(output[1], output[0])
                                # robot.logger.info(desired_theta * (180 / math.pi))
                    wait(robot, start_time, end_time=1)
                    # robot.logger.info("finished waiting")
                elif (count%3) == 1:
                    # robot.logger.info("in 1")
                    robot.set_led(0,255,0)
                    if invalid == 0:
                            # while (robot.get_clock()-start_time) < 1.9:
                        finished_turning = turn_to_angle(robot, curr_theta, desired_theta,start_time)
                    wait(robot, start_time, end_time=2)
                elif (count%3) == 2:
                    # robot.logger.info("in 2")                    
                    dist = math.sqrt((curr_x-desired_x)**2 + (curr_y-desired_y)**2)
                    # robot.logger.info(invalid)
                    if abs(dist) > 0.05 and invalid == 0 and finished_turning == True:
                        robot.set_led(0,0,255)
                        robot.set_vel(60,60)
                        # robot.delay(700)
                        # robot.set_vel(0,0)                    
                    elif abs(dist) < 0.05:
                        robot.set_led(0,0,0)
                    elif invalid == 1:
                        robot.set_led(255,255,255)
                    elif finished_turning==False:
                        robot.set_led(255,0,255)
                    invalid = 0              
                    wait(robot, start_time, end_time=0.5)
            vo = {}
            dict_ORCA = {}
            # incoming_pos_dict = {}
            received = 0            
            robot.set_vel(0,0)
            dist = math.sqrt((curr_x-desired_x)**2 + (curr_y-desired_y)**2)
            
            


#param: list of values to send
#returns: string with comma delimeters with the first value being the number of values sent
def package_string(to_send):
    strg = str(len(to_send))
    comma = ","
    for i in range(len(to_send)):
        strg += comma
        strg += str(to_send[i])
    # print(strg)
    return strg

def unpack_string(robot, str):
    # robot.logger.info(str)
    # robot.logger.info(len(str))
    string_return = []
    j = 0
    while j < (len(str)):
        ret_temp = str[j].split('\x01')
        ret = ret_temp[0].split(',')
        # if robot.id == 3:
        #     print(str)
        #     print(ret_temp)
        #     print(ret)    
        str_len = int(ret[0])
        # print(str_len)
        # print(ret)        
        # if robot.id == 3:
        #     print(str_len, (len(ret)-1))        
        if str_len == (len(ret)-1):
            i = 1
            invalid = 0
            while i <= str_len:
                # print(ret[i+1])
                try:
                    float(ret[i])
                except:
                    print(str)
                    invalid = 1
                i = i+1
            i = 1
            if invalid == 0:
                while i <= str_len:
                    # print(ret[i+1])
                    string_return.append(float(ret[i]))
                    i = i+1
        # # robot.logger.info(string_return)
        j = j + 1
    return string_return

def unpack_other_pos_string_old(robot, str):
    # robot.logger.info(str)
    # robot.logger.info(len(str))
    string_return = []
    j = 0
    while j < (len(str)):        
        ret_temp = str[j].split('\x01')
        ret = ret_temp[0].split(',')           
        str_len = int(ret[0])   
        if str_len > 2:     
            if str_len == (len(ret)-1):
                if robot.id == 3:
                    print(ret)
                i = 1
                invalid = 0
                while i <= str_len:
                    # print(ret[i+1])
                    try:
                        float(ret[i])
                    except:
                        print(str)
                        invalid = 1
                    i = i+1
                i = 1
                if invalid == 0:
                    while i <= str_len:
                        # print(ret[i+1])
                        string_return.append(float(ret[i]))
                        i = i+1
                # robot.logger.info(string_return)
        j= j+1
    return string_return

def unpack_other_pos_string(robot, str):
    # robot.logger.info(len(str))
    string_return = []
    i = 0
    while i < (len(str)):
    # robot.logger.info(str[0])
        temp = struct.unpack('ifffff',str[i][:24])
        j = 0
        while j < len(temp):
            string_return.append(temp[j])
            j = j+1
        i = i +1
    return string_return

def package_pos_string(id, x, y, theta):
    str = "{},{},{},{}".format(id, x, y, theta)
    return str

def unpack_pos_string(robot, str):
    # robot.logger.info(type(str[0]))
    ret_temp = str[0].split('\x01')
    ret = ret_temp[0].split(',')
    # for_angle = ret[3].split('\x00')
    # robot.logger.info(ret)
    # robot.logger.info("split str")
    id = float(ret[0])
    x = float(ret[1])
    y = float(ret[2])
    theta = float(ret[3])
    # robot.logger.info("Output %f %f %f", id, x, y)
    return [id, x, y, theta]

def find_desired_theta(curr_x, curr_y, target_x, target_y):
    import math
    if curr_y == target_y:
        target_y += 0.01
    desired_theta = math.atan(((curr_x-target_x)/(curr_y-target_y)))
    if curr_y > target_y:
        desired_theta = - ((math.pi/2) + desired_theta)
    else:
        desired_theta = (math.pi/2) - desired_theta
    return desired_theta

def turn_to_angle(robot, curr_theta, desired_theta, starting_time):
    import math
    desired_theta_360 = (desired_theta + (2*math.pi)) % (2*math.pi)
    curr_theta_360 = (curr_theta + (2*math.pi)) % (2*math.pi)
    half_line = (curr_theta_360 + (math.pi)) % (2*math.pi)
    # robot.logger.info(half_line)
    while abs(curr_theta_360 - desired_theta_360) > 0.1:
        curr_theta_360 = (curr_theta + (2*math.pi)) % (2*math.pi)
        if curr_theta_360 > half_line:
            if (desired_theta_360 < half_line) or (desired_theta_360 > curr_theta_360):
                robot.set_vel(-80, 80)
            else:
                robot.set_vel(80, -80)
        else:
            if (desired_theta_360 < half_line) and (desired_theta_360 > curr_theta_360):
                robot.set_vel(-80, 80)
            else:
                robot.set_vel(80, -80)
        curr_pose = robot.get_pose()
        if curr_pose:
            curr_theta = curr_pose[2]
        # robot.delay()
        if (check_time(robot, starting_time, end_time=1.9)) == True:
            robot.set_vel(0,0)
            return False
    robot.set_vel(0,0)
    return True

# returns list with boundary conditions
# https://math.stackexchange.com/questions/543496/how-to-find-the-equation-of-a-line-tangent-to-a-circle-that-passes-through-a-g
def compute_boudaries(robot, own_pos, other_pos):
    import math
    own_x = own_pos[0]
    own_y = own_pos[1]
    other_x = other_pos[0]
    other_y = other_pos[1]
    
    # finding center point of the two tangent lines
    x2 = other_x - own_x
    y2 = other_y - own_y
    x1 = x2 / time_step
    y1 = y2 / time_step
    r2 = 2 * robot_radius
    r1 = r2 / time_step

    dx, dy = -x1, -y1
    dxr, dyr = -dy, dx
    d = math.sqrt(dx ** 2 + dy ** 2)
    # robot.logger.info('%f %f' %(d, r1))
    if d < r1:
        d = r1+0.00000000000001

    rho = r1 / d
    ad = rho ** 2
    bd = rho * math.sqrt(1 - rho ** 2)
    T1x = x1 + ad * dx + bd * dxr
    T1y = y1 + ad * dy + bd * dyr
    T2x = x1 + ad * dx - bd * dxr
    T2y = y1 + ad * dy - bd * dyr
    # robot.logger.info(T1x)

    m1 = T1y / T1x
    m2 = T2y / T2x
    den = (T2x - T1x)
    if den == 0:
        den = 0.0000001
    m3 = ((T2y - T1y) / den)
    b3 = T1y - (m3 * T1x)
    cx = x1
    cy = y1
    cr = r1
    return [m1, m2, m3, b3, cx, cy, cr, T1x, T1y, T2x, T2y]

#checks if inside boudaries and returns true if it is in the velocity obstacle 
def if_valid_velocity(m1, m2, m3, b3, cx, cy, cr, T1x, T1y, T2x, T2y, x_check, y_check):
    import math
    ang1 = (math.atan2(T1y, T1x) + (2*math.pi)) % (2*math.pi)
    ang2 = (math.atan2(T2y, T2x) + (2*math.pi)) % (2*math.pi)
    ang_check = (math.atan2(y_check,x_check) + (2*math.pi)) % (2*math.pi)
    if (abs(ang1-ang2)<math.pi):
        if (ang_check <= ang1 and ang_check >= ang2) or (ang_check >= ang1 and ang_check <= ang2):
            if (((x_check-cx)**2 + (y_check-cy)**2) <= cr**2):
                return True
            y_m3 = m3*x_check + b3
            if (0 <= b3 and y_check >= y_m3) or (0 >= b3 and y_check <= y_m3):
                return True
    else:
        if (ang1>ang2):
            if (ang_check >= ang1 or ang_check <= ang2):
                if (((x_check-cx)**2 + (y_check-cy)**2) <= cr**2):
                    return True
                y_m3 = m3*x_check + b3
                if (0 <= b3 and y_check >= y_m3) or (0 >= b3 and y_check <= y_m3):
                    return True
        elif (ang2>ang1):
            if (ang_check > ang2 or ang_check < ang1):
                if (((x_check-cx)**2 + (y_check-cy)**2) <= cr**2):
                    return True
                y_m3 = m3*x_check + b3
                if (0 <= b3 and y_check >= y_m3) or (0 >= b3 and y_check <= y_m3):
                    return True
    return False

#https://www.wyzant.com/resources/answers/255269/find_the_point_on_the_line_6x_y_9_that_is_closest_to_the_point_3_8
def compute_w_old(robot, vo, own_vopt_x, own_vopt_y, other_vopt_x, other_vopt_y):
    import math
    # import sympy as sym
    # robot.logger.info('here')
    
    # calculate va-vb optimal
    v_opt_x = own_vopt_x-other_vopt_x
    v_opt_y = own_vopt_y-other_vopt_y

    # calculate distance to each tangent line
    # x = sym.symbols(r'x')
    # Fx = (x-v_opt_x)**2+(vo[0]*x-v_opt_y)**2
    # Fx_dot = Fx.diff(x)
    x_res = (v_opt_x + vo[0]*v_opt_y)/(1+vo[0]**2)
    tan1_x = x_res
    tan1_y = (vo[0]*x_res)
    tan1_dist = math.sqrt((tan1_x-v_opt_x)**2+(tan1_y-v_opt_y)**2)

    # x = sym.symbols(r'x')
    # Fx = (x - v_opt_x) ** 2 + (vo[1] * x - v_opt_y) ** 2
    # Fx_dot = Fx.diff(x)
    x_res = (v_opt_x + vo[1]*v_opt_y)/(1+vo[1]**2)
    tan2_x = x_res
    tan2_y = (vo[1] * x_res)
    tan2_dist = math.sqrt((tan2_x - v_opt_x) ** 2 + (tan2_y - v_opt_y) ** 2)

    closest_dist = tan1_dist
    closest_x = tan1_x
    closest_y = tan1_y
    # check if close to bottom curve
    y_m3 = vo[2] * v_opt_x + vo[3]
    if (0 < vo[3] and v_opt_y < y_m3) or (0 > vo[3] and v_opt_y > y_m3):
        # if so, check distance to circle
        # x = sym.symbols(r'x')
        # Fx = (x - v_opt_x) ** 2 + (sym.sqrt(vo[6]**2 - x**2) - v_opt_y) ** 2
        # Fx_dot = Fx.diff(x)
        x_res_plus = ((vo[6]*(vo[4]-v_opt_x))/math.sqrt(vo[4]**2 - 2*vo[4]*v_opt_x + vo[5]**2 - 2*vo[5]*v_opt_y + v_opt_x**2 + v_opt_y**2)) + vo[4]
        x_res_minus = -((vo[6]*(vo[4]-v_opt_x))/math.sqrt(vo[4]**2 - 2*vo[4]*v_opt_x + vo[5]**2 - 2*vo[5]*v_opt_y + v_opt_x**2 + v_opt_y**2)) + vo[4]
        c_x_plus = x_res_plus
        c_y_plus = (math.sqrt(vo[6]**2 - (x_res_plus-vo[4])**2)) + vo[5]
        c_dist_plus = math.sqrt((c_x_plus - v_opt_x) ** 2 + (c_y_plus - v_opt_y) ** 2)
        c_x_minus = x_res_minus
        c_y_minus = (math.sqrt(vo[6]**2 - (x_res_minus-vo[4])**2)) + vo[5]
        c_dist_minus = math.sqrt((c_x_minus - v_opt_x) ** 2 + (c_y_minus - v_opt_y) ** 2)
        # print("minus: (%f, %f) %f, plus: (%f,%f) %f" %(c_x_minus, c_y_minus, c_dist_minus, c_x_plus, c_y_plus, c_dist_plus))
        if c_dist_plus > c_dist_minus:
            closest_dist = c_dist_minus
            return [(c_x_minus - v_opt_x),(c_y_minus - v_opt_y)]
        closest_dist = c_dist_plus
        return [(c_x_plus - v_opt_x),(c_y_plus - v_opt_y)]
    # compare all the distances to see which is smallest
    if closest_dist > tan2_dist:
        closest_dist = tan2_dist
        closest_x = tan2_x
        closest_y = tan2_y

    # subtract that closest point with vopt
    res_vect_x = closest_x - v_opt_x
    res_vect_y = closest_y - v_opt_y
    # return resulting vector
    return [res_vect_x, res_vect_y]

def compute_w(robot, vo, own_vopt_x, own_vopt_y, other_vopt_x, other_vopt_y):
    import math
    # import sympy as sym
    # robot.logger.info('here')

    # calculate va-vb optimal
    v_opt_x = own_vopt_x-other_vopt_x
    v_opt_y = own_vopt_y-other_vopt_y
    #   print("v_opt: %f %f" %(v_opt_x,v_opt_y))
    x_res_plus = ((vo[6]*(vo[4]-v_opt_x))/math.sqrt(vo[4]**2 - 2*vo[4]*v_opt_x + vo[5]**2 - 2*vo[5]*v_opt_y + v_opt_x**2 + v_opt_y**2)) + vo[4]
    x_res_minus = -((vo[6]*(vo[4]-v_opt_x))/math.sqrt(vo[4]**2 - 2*vo[4]*v_opt_x + vo[5]**2 - 2*vo[5]*v_opt_y + v_opt_x**2 + v_opt_y**2)) + vo[4]
    c_x_plus = x_res_plus
    c_y_plus = (math.sqrt(vo[6]**2 - (x_res_plus-vo[4])**2)) + vo[5]
    c_dist_plus = math.sqrt((c_x_plus - v_opt_x) ** 2 + (c_y_plus - v_opt_y) ** 2)
    c_x_minus = x_res_minus
    try: 
        c_y_minus = (math.sqrt(vo[6]**2 - (x_res_minus-vo[4])**2)) + vo[5]
        c_dist_minus = math.sqrt((c_x_minus - v_opt_x) ** 2 + (c_y_minus - v_opt_y) ** 2)
        if c_dist_plus > c_dist_minus:
            closest_dist = c_dist_minus
            closest_x = c_x_minus
            closest_y = c_y_minus
        else:
            closest_dist = c_dist_plus
            closest_x = c_x_plus
            closest_y = c_y_plus
    except:
        closest_dist = c_dist_plus
        closest_x = c_x_plus
        closest_y = c_y_plus

    #   print("to circle: %f %f" %(closest_x,closest_y))

    x_res = (v_opt_x + vo[0]*v_opt_y)/(1+vo[0]**2)
    tan1_x = x_res
    tan1_y = (vo[0]*x_res)
    tan1_dist = math.sqrt((tan1_x-v_opt_x)**2+(tan1_y-v_opt_y)**2)
    #   print("to line 1: %f %f" %(tan1_x,tan1_y))

    # if ((v_opt_x - vo[4])**2 + (v_opt_y - vo[5])**2 < vo[6]**2):
    y_m3 = vo[2] * closest_x  + vo[3]
    y_m3_center = vo[2] * vo[4] + vo[3]
    if ((vo[5] <= y_m3_center and closest_y <= y_m3) or (vo[5] >= y_m3_center and closest_y >= y_m3)):
        # print("on boundary side of circle")
        closest_dist = tan1_dist
        closest_x = tan1_x
        closest_y = tan1_y

    x_res = (v_opt_x + vo[1]*v_opt_y)/(1+vo[1]**2)
    tan2_x = x_res
    tan2_y = (vo[1] * x_res)
    tan2_dist = math.sqrt((tan2_x - v_opt_x) ** 2 + (tan2_y - v_opt_y) ** 2)

    #   print("to line 2: %f %f" %(tan2_x,tan2_y))

    y_m3 = vo[2] * tan1_x + vo[3]
    y_m3_center = vo[2] * vo[4] + vo[3]
    if ((vo[5] <= y_m3_center and tan1_y <= y_m3) or (vo[5] >= y_m3_center and tan1_y >= y_m3)):
        # print("on boundary side t1")
        if tan1_dist < closest_dist:
            closest_dist = tan1_dist
            closest_x = tan1_x
            closest_y = tan1_y

    y_m3 = vo[2] * tan2_x + vo[3]
    y_m3_center = vo[2] * vo[4] + vo[3]
    if ((vo[5] <= y_m3_center and tan2_y <= y_m3) or (vo[5] >= y_m3_center and tan2_y >= y_m3)):
    # print("on boundary side t2")
        if tan2_dist < closest_dist:
            closest_dist = tan2_dist
            closest_x = tan2_x
            closest_y = tan2_y
    #   print(closest_x, closest_y)
    return [(closest_x-v_opt_x),(closest_y-v_opt_y)]

def compute_n(vo, w, own_vopt_x, own_vopt_y, other_vopt_x, other_vopt_y):
    import math
    w_angle = math.atan2(w[1],w[0])
    if if_valid_velocity(vo[0],vo[1],vo[2],vo[3],vo[4],vo[5],vo[6],vo[7],vo[8],vo[9],vo[10],own_vopt_x-other_vopt_x, own_vopt_y-other_vopt_y):
      return [math.cos(w_angle), math.sin(w_angle)]
    else:
      if w_angle < 0:
        w_angle = w_angle%(math.pi)
      else:
        w_angle = w_angle-(math.pi)
      return [math.cos(w_angle), math.sin(w_angle)]

def construct_ORCA(robot, n, w, own_vopt_x, own_vopt_y):
    ORCA_x = ((own_vopt_x+0.75*w[0])*n[0])
    ORCA_y = ((own_vopt_y+0.75*w[1])*n[1])
    # robot.logger.info([ORCA_x, ORCA_y])
    return [own_vopt_x+1*w[0], own_vopt_y+1*w[1]]

def get_ORCA_angle(vo, ORCA_x, ORCA_y, own_vopt_x, own_vopt_y, other_vopt_x, other_vopt_y):
  import math
  # convert optimal angle to 360
  opt_angle_360 = (math.atan2(own_vopt_y, own_vopt_x) + (2*math.pi)) % (2*math.pi)
  # convert the orca line angles to 360
  orca_angle_360 = (math.atan2(ORCA_y, ORCA_x)+ (2*math.pi)) % (2*math.pi)
  orca_half_line = (orca_angle_360 + (math.pi)) % (2*math.pi)
  # if the angle is in the velocity obstacle
  if if_valid_velocity(vo[0],vo[1],vo[2],vo[3],vo[4],vo[5],vo[6],vo[7],vo[8],vo[9],vo[10],own_vopt_x-other_vopt_x, own_vopt_y-other_vopt_y):
    # if it's closer to the half line
    if (abs(opt_angle_360-orca_angle_360) > abs(opt_angle_360-orca_half_line)):
        # convert back to -pi/2 to pi/2 range
      if math.atan2(ORCA_y, ORCA_x) < 0:
        return math.atan2(ORCA_y, ORCA_x)%(math.pi)
      else:
        return math.atan2(ORCA_y, ORCA_x)-(math.pi)
    # if it's closer to the orca angle line, return that
    else:
      return math.atan2(ORCA_y, ORCA_x)
  else:
    # print("not in vo")
    return math.atan2(own_vopt_y, own_vopt_x)

def gen_ORCA_line(robot, vo, n, w, own_vopt_x, own_vopt_y):
    try:
        slope = -n[0]/n[1]
    except: 
        slope = -n[0]/0.00001
    intercept = (own_vopt_y+0.5*w[1]) + (-slope)*(own_vopt_x+0.5*w[0])
    check_x = vo[4]
    check_y = slope*vo[4]+intercept
    check_y_2 = vo[5]
    check_x_2 = (vo[5]-intercept)/slope
    #   robot.logger.info("to check ORCA: %f, %f and %f, %f" %(check_x, check_y, check_x_2, check_y_2))
    if if_valid_velocity(vo[0],vo[1],vo[2],vo[3],vo[4],vo[5],vo[6],vo[7],vo[8],vo[9],vo[10],check_x, check_y) or if_valid_velocity(vo[0],vo[1],vo[2],vo[3],vo[4],vo[5],vo[6],vo[7],vo[8],vo[9],vo[10],check_x_2, check_y_2):
        # robot.logger.info("flipping intercept circle")
        intercept = -intercept
    elif abs(slope - vo[0]) < 0.00001:  
        # robot.logger.info("parallel to vo[0] %f %f" %(vo[1], slope))
        if vo[1] == slope:
            slope = slope + 0.000001
        intersect_x = intercept/(vo[1]-slope)
        intersect_y = vo[1]*intersect_x
        # print(intersect_x, intersect_y)
        if if_valid_velocity(vo[0],vo[1],vo[2],vo[3],vo[4],vo[5],vo[6],vo[7],vo[8],vo[9],vo[10],intersect_x, intersect_y):
        #   robot.logger.info("flipping intercept m1")
            intercept = -intercept 
    elif abs(slope - vo[1]) < 0.00001:  
        if vo[1] == slope:
            slope = slope + 0.000001  
        # robot.logger.info("parallel to vo[1] %f %f" %(vo[0], slope))
        intersect_x = intercept/(vo[0]-slope)
        intersect_y = vo[0]*intersect_x
        # print(intersect_x, intersect_y)
        if if_valid_velocity(vo[0],vo[1],vo[2],vo[3],vo[4],vo[5],vo[6],vo[7],vo[8],vo[9],vo[10],intersect_x, intersect_y):
        #   robot.logger.info("flipping intercept m2")
            intercept = -intercept 
    return [slope, intercept]

def get_ORCA_vel(vo, own_vopt_x, own_vopt_y, ORCA_line):
  if if_valid_velocity(vo[0],vo[1],vo[2],vo[3],vo[4],vo[5],vo[6],vo[7],vo[8],vo[9],vo[10],own_vopt_x, own_vopt_y):
    closest_x = (-ORCA_line[1]*ORCA_line[0] + ORCA_line[0]*own_vopt_y + own_vopt_x)/(ORCA_line[0]**2+1)
    closest_y = ORCA_line[0]*closest_x+ORCA_line[1]
    return [closest_x, closest_y]
  else:
    return [own_vopt_x, own_vopt_y]

# combining ORCAs
def combine_ORCAs(robot, opt_x, opt_y, dict_ORCA, dict_vo, checking_id):
    found = 0
    if len(dict_ORCA) == 1:
        # robot.logger.info('only 1  in dict')
        return get_ORCA_vel(dict_vo[checking_id], opt_x, opt_y, dict_ORCA[checking_id])
    if len(dict_ORCA) > 1:
        if if_valid_velocity(dict_vo[checking_id][0],dict_vo[checking_id][1],dict_vo[checking_id][2],dict_vo[checking_id][3],
                        dict_vo[checking_id][4],dict_vo[checking_id][5],dict_vo[checking_id][6],dict_vo[checking_id][7],dict_vo[checking_id][8],
                        dict_vo[checking_id][9],dict_vo[checking_id][10],opt_x, opt_y):
            # robot.logger.info("in collision path")
            for key in dict_ORCA:
                if key != checking_id:
                    den = dict_ORCA[checking_id][0]-dict_ORCA[key][0]
                    if den == 0:
                        den = 0.000001
                    intersect_x = (dict_ORCA[key][1]-dict_ORCA[checking_id][1])/(den)
                    intersect_y = dict_ORCA[checking_id][0]*intersect_x + dict_ORCA[checking_id][1]
                    invalid = 0
                    for inner_key in dict_ORCA:
                        if inner_key != checking_id:
                            if if_valid_velocity(dict_vo[inner_key][0],dict_vo[inner_key][1],dict_vo[inner_key][2],dict_vo[inner_key][3],
                                        dict_vo[inner_key][4],dict_vo[inner_key][5],dict_vo[inner_key][6],dict_vo[inner_key][7],dict_vo[inner_key][8],
                                        dict_vo[inner_key][9],dict_vo[inner_key][10],intersect_x, intersect_y):
                                invalid = 1
                    if invalid == 0:
                        if found == 0:
                            ideal_x = intersect_x
                            ideal_y = intersect_y
                            found = 1
                        else:
                            dist_intersect = math.sqrt((intersect_x - opt_x) ** 2 + (intersect_y - opt_y) ** 2)
                            dist_ideal = math.sqrt((ideal_x - opt_x) ** 2 + (ideal_y - opt_y) ** 2)
                            if dist_intersect < dist_ideal:
                                ideal_x = intersect_x
                                ideal_y = intersect_y
            if found == 1:
                return [ideal_x, ideal_y]
            else:
                # robot.logger.info("no valid options")
                return [0,0]
        else:
            return [opt_x,opt_y]

def wait(robot, start_time, end_time):
    while (robot.get_clock() - start_time) < end_time:
        pass
    return

# if time is up, then returns True
def check_time(robot, start_time, end_time):
    if (robot.get_clock() - start_time) > end_time:
        return True
    else:
        return False

def init_positions(robot_id):
    start = 0
    between_each = 0.25
    if robot_id == start:
        return [0, -0.02]
    if robot_id == start+1:
        return [0, between_each]
    if robot_id == start+2:
        return [0.0, between_each*2]
    if robot_id == start+3:
        return [0.0, between_each*3]
    if robot_id == start+4:
        return [0, between_each*4]
    if robot_id == start+5:
        return [0, between_each*5]
    if robot_id == start+6:
        return [0.2, between_each*5]    
    if robot_id == start+7:
        return [0.4, between_each*4]
    if robot_id == start+8:
        return [0.6, between_each*3]
    if robot_id == start+9:
        return [0.8, between_each*2]
    if robot_id == start+10:
        return [1.0, between_each]
    if robot_id == start+11:
        return [1.2, 0.0]
    if robot_id == start+12:
        return [1.4, 0.0]
    if robot_id == start+13:
        return [1.4, between_each]
    if robot_id == start+14:
        return [1.4, between_each*2]    
    if robot_id == start+15:
        return [1.4, between_each*3]
    if robot_id == start+16:
        return [1.4, between_each*4]
    if robot_id == start+17:
        return [1.4, between_each*5]
    if robot_id == start+18:
        return [1.2, between_each*5]
    if robot_id == start+19:
        return [1.2, between_each*4]
    if robot_id == start+20:
        return [-0.8, 0]    
    if robot_id == start+21:
        return [-0.8, 0.8]
    if robot_id == start+22:
        return [0.0, 0.8]
    if robot_id == start+23:
        return [0.8, 0.8]
    if robot_id == start+24:
        return [-0.05, 0]
    if robot_id == start+25:
        return [-0.9, 0.9]
    if robot_id == start+26:
        return [0.0, 0.9]    
    if robot_id == start+27:
        return [0.9, 0.9]
    if robot_id == start+28:
        return [0.6, 0.9]
    if robot_id == start+29:
        return [-0.6, 0.9]
    if robot_id == start+30:
        return [0.3, 0.95]
    if robot_id == start+31:
        return [-0.3, 0.9]

def N_init_positions(robot_id):
    height = 11
    between_each = 0.3
    init_pose = {}

    init_pose[0] = [-2.5,-1.5]
    count = 1
    x = init_pose[0][0]
    y = init_pose[0][1]

    # column 1
    for j in range(height-1):
        y = y+between_each
        init_pose[count] = [x,y]
        count = count + 1

    # column 2
    x = x+between_each
    y = init_pose[0][1]-between_each
    for k in range(height):
        y = y+between_each
        init_pose[count] = [x,y]
        count = count + 1
    
    # column 3
    x = x+between_each
    y = init_pose[0][1]-between_each
    for k in range(height):
        y = y+between_each
        init_pose[count] = [x,y]
        count = count + 1

    # diagonal
    for i in range(height):
        x = x+between_each
        init_pose[count] =[x,y]
        count = count + 1
        y = y-between_each
        init_pose[count] =[x,y]
        count = count + 1       

    # extra part of N
    y = init_pose[0][1] + ((height-1)*between_each)
    for c in range(6):
        init_pose[count] = [x,y]
        y = y - between_each
        count = count+1

    # end column left
    x = x + between_each
    y = init_pose[0][1]
    for a in range(height):
        init_pose[count] = [x,y]
        y = y+between_each
        count = count + 1

    #end column middle
    x = x + between_each
    y = init_pose[0][1]
    for b in range(height):
        init_pose[count] = [x,y]
        y = y+between_each
        count = count + 1

    #end column right
    x = x + between_each
    y = init_pose[0][1]
    for b in range(height):
        init_pose[count] = [x,y]
        y = y+between_each
        count = count + 1

    # side bar 
    x = init_pose[0][0]+between_each*3
    y = init_pose[0][1]
    for c in range(6):
        init_pose[count] = [x,y]
        y = y + between_each
        count = count+1

    # print(count-1)
    if robot_id in init_pose:
        return init_pose[robot_id]
    else:
        return False
