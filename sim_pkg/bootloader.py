#!/usr/bin/env python2
import os
import traceback
import importlib
import socket, errno
from bot_api.coachbot_api import Coachbot
from client_server import Bot_Client
import time


class Bootloader():
    def __init__(self, userfile, config_data):
        '''
        A bootloader for the given user code
        '''
        self.userfile = os.path.splitext(userfile)[0] # Remove .py ending from userfile name
        self.buffer_size = config_data["NUM_OF_MSGS"] * config_data["MSG_SIZE"]
        self.msg_type = config_data["MSG_TYPE"]
        self.rtf = config_data["REAL_TIME_FACTOR"]

        if "LOG_FILE" in config_data:
            self.log_file = config_data["LOG_FILE"]
        else:
            self.log_file = None

    def launch(self, barrier, id, a_ids=-1):
        '''
        Creates a robot instance to run the user file
        '''
        try:
            # Create a Coachbot instance with given id number
            bot_client = Bot_Client("localhost", 8000, self.buffer_size, self.rtf)
            bot_client.start()
            robot = Coachbot(bot_client, self.msg_type, id, a_ids, self.log_file)

            # Run usr function in userfile module
            fn = importlib.import_module("user." + self.userfile) # Import userfile as a module
            barrier.wait() # Wait for all robot threads to reach this point before starting the usr function
            robot.send_start_time(time.time()) 

            fn.usr(robot)
            bot_client.stop() # NOTE: This usually isn't run because it does not get called until after usr is complete
            
        except KeyboardInterrupt:
            bot_client.stop() # Allow clean termination by KeyboardInterrupt from the main program
        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                pass 
                # TODO: this is a temporary fix -- suppresses connection reset error (or bad file descriptor) from the bootloader, prevents errors when robot threads terminate earlier than expected
                # This works but would be better to use some kind of stop event based on the simulator ending
            else:
                print(f"bootloader.py: {e}. Full traceback below:")
                traceback.print_exc()
        except Exception as e:
            print(f"bootloader.py: {e}. Full traceback below:")
            traceback.print_exc()

if __name__ == '__main__':
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Run the robots")
    parser.add_argument("-u", "--userfile", type=str, help="Path to user code file", required=True)
    parser.add_argument("-c", "--configfile", type=str, help="Path to configuration file", required=True)
    parser.add_argument("-n", "--numbots", type=str, help="Number of robots to run", required=True)
    args = parser.parse_args()

    with open("user/" + args.configfile, 'r') as cfile:
        config_data = json.loads(cfile.read())
    cfile.close()

    bootloader = Bootloader(args.userfile, config_data)
    for i in range(args.numbots):
        bootloader.launch(i)