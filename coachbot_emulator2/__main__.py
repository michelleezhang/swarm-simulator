#!/usr/bin/env python2
from coachbot_emulator2.coachbot import Coachbot
import signal
import sys
import argparse
import importlib

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
    sys.exit(0)
    

if __name__ == "__main__":
    # create a sigterm handler here
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    fn.usr(robot)
