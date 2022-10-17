#!/usr/bin/env python2
from robot_class import Coachbot
from radius_comm import usr

robot = Coachbot((0,0,0))

if __name__ == "__main__":
    usr(robot)