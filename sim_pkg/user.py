def usr(robot):

    while True:
        
        robot.delay(1000)
        robot.set_led(0,100,0)
        robot.delay(1000)
        robot.set_led(100,100,0)
        val = robot.send_msg("Who is this?")
        id  = robot.id
        # print(id)
        robot.delay()
