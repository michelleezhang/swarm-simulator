def usr(robot):

    a = 's'
    st = ''

    for i in range(1024):
        st += a

    while True:
        # val = robot.recv_msg()
        
        robot.delay(1000)
        id = robot.id

        if id == 3:
            robot.delay(200)
            robot.send_msg(st)
            
            
        elif id == 4:
            robot.delay(6000)
            val = robot.recv_msg(clear=True)
            # print(val)
            # print("length:", len(val))
        
        elif id == 6:
            robot.delay(1000)
            robot.set_vel(10, -10)