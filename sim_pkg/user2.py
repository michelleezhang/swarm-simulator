#!/usr/bin/env python2
from robot_class import Coachbot

robot = Coachbot((0,0,0))

def usr(robot):

    while True:
        val = robot.recv_msg()
        print(val)
        robot.set_led(100,0,0)
        robot.delay(1000)
        robot.set_led(0,100,0)
        robot.delay(1000)
        val = robot.recv_msg()

if __name__ == "__main__":
    usr(robot)