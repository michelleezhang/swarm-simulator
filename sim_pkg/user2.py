#!/usr/bin/env python2
from robot_class import Coachbot

robot = Coachbot((0,0,0))

def usr(robot):

    while True:
        # val = robot.recv_msg()
        
        robot.set_led(100,0,0)
        robot.delay(1000)
        robot.set_led(0,100,0)
        robot.delay(1000)
        val = robot.recv_msg(clear=True)
        print(val)
        robot.delay(1000)

if __name__ == "__main__":
    usr(robot)