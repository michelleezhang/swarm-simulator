#!/usr/bin/env python2
from robot_class import Coachbot
import signal
import sys
# from firefly import usr
# from radius_comm import usr
from user3 import usr
# from user2 import usr
# from user3 import usr
# from user4 import usr
# from user5 import usr

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
    usr(robot)