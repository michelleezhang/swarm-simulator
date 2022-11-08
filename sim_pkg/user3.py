def usr(robot):
    
    id = robot.id

    while True:

        # if id == 3:
        #     pose = robot.get_pose()
        #     vec = robot.math.Vec2(-pose[0], -pose[1])
        #     robot.move_meters(vec)
        
        # if id == 5:
        #     pose = robot.get_pose()
        #     vec = robot.math.Vec2(-pose[0], -pose[1])
        #     robot.move_meters(vec)

        if id == 1:
            robot.set_vel(90, 90)
            pose = robot.get_pose()
            robot.delay(1000)
            pose2 = robot.get_pose()
            
            vel = (pose2[0] - pose[0])/1
            print(vel)
            robot.logger.info('Something happens')


            