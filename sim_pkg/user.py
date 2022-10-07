from robot_class import bot

robot = bot((0,0,0))

def usr(robot):

    while True:
        robot.set_led(100,0,0)
        robot.delay(5000)
        robot.set_led(0,100,0)
        robot.delay(5000)


if __name__ == "__main__":
    usr(robot)