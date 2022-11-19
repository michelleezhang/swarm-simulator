#!/usr/bin/env python2
from robot_class import Coachbot
import signal
import sys
import argparse
import importlib
# from firefly import usr
# from radius_comm import usr
# from user import usr
# from user2 import usr
# from user3 import usr
# from user4 import usr
# from user5 import usr

parser = argparse.ArgumentParser(description='Run the simulator')

parser.add_argument('-fn', '--filename', type=str, help="Name of the file with the .py extension")

args = parser.parse_args()

fn = importlib.import_module(args.filename)


robot = Coachbot()

def sigterm_handler(signum, _):
    """
    sigterm handler
    """
    # print("Client to be killed !")
    robot.client_socket.close()
    sys.exit(1)
    

if __name__ == "__main__":
    # create a sigterm handler here
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    fn.usr(robot)