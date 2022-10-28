def usr(robot):

    while True:
        # val = robot.recv_msg()
        
        # robot.delay()
        id = robot.id

        if id == 3:
            robot.delay(50)
            robot.send_msg("(0,100,0)")
            
            
        elif id == 4:
            robot.delay(5000)
            val = robot.recv_msg(clear=True)
            print(val)
            print("length:", len(val))
        
        elif id == 6:
            robot.delay(1000)
            robot.set_vel(10, -10)