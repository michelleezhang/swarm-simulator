def usr(robot):
    
    id = robot.id

    while True:

        if id == 3:
            pose = robot.get_pose()
            vec = robot.math.Vec2(-pose[0], -pose[1])
            robot.move_meters(vec)
        
        if id == 5:
            pose = robot.get_pose()
            vec = robot.math.Vec2(-pose[0], -pose[1])
            robot.move_meters(vec)
            