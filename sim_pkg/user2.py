def usr(robot):

    while True:
        # val = robot.recv_msg()
        
        # robot.delay()
        id = robot.id

        if id == 3:
            robot.send_msg("(0,100,0)")
            robot.delay(50)
            
        elif id == 4:
            robot.delay(10000)
            val = robot.recv_msg(clear=True)
            print(val)
            print("length:", len(val))