def usr(robot):

    while True:

        robot.delay()
        id = robot.id    
        
        if id == 3:
            robot.set_led(0,100,0)
            robot.send_msg("(0,100,0)")
            robot.delay(1000)
            robot.set_led(100,0,0)
            robot.send_msg("(100,0,0)")
            robot.delay(2000)
            robot.set_vel(10,-10)
            pose = robot.get_pose()
            print("Pose:", pose)

        elif id == 10:
            robot.set_led(100,100,0)
            robot.send_msg("(100,100,0)")
            robot.delay(2000)
            robot.set_led(100,100,100)
            robot.send_msg("(100,100,100)")
            robot.delay(2000)

        else:
            val = robot.recv_msg(clear=True)
            # print(val)
            if len(val)> 0:
                if val[0] == "(100,100,0)":
                    robot.set_led(100,100,0)
                    robot.delay()
                elif val[0] == "(0,100,0)":
                    robot.set_led(0,100,0)
                    robot.delay()
                elif val[0] == "(100,0,0)":
                    robot.set_led(100,0,0)
                    robot.delay()
                elif val[0] == "(100,100,100)":
                    robot.set_led(100,100,100)
                    robot.delay()
                
            else:
                continue
        
