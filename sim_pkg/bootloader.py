#!/usr/bin/env python2
import os
import importlib
from bot_api.coachbot_api import Coachbot
from client_server import Bot_Client

class Bootloader():
    def __init__(self, userfile, config_data):
        '''
        A bootloader for the given user code
        '''
        self.userfile = os.path.splitext(userfile)[0] # Remove .py ending from userfile name
        self.buffer_size = config_data["NUM_OF_MSGS"] * config_data["MSG_SIZE"]
        self.msg_type = config_data["MSG_TYPE"]
        
    def launch(self, id, a_ids=-1):
        '''
        Creates a robot instance to run the user file
        '''
        try:
            # Create a Coachbot instance with given id number
            bot_client = Bot_Client("localhost", 8000, self.buffer_size)
            bot_client.start()
            robot = Coachbot(bot_client, self.msg_type, id, a_ids)

            # Run usr function in userfile module
            fn = importlib.import_module("user." + self.userfile) # Import userfile as a module
            fn.usr(robot)
            bot_client.stop() # NOTE: This usually isn't run because it does not get called until after usr is complete

        except KeyboardInterrupt:
            pass # Allow clean termination by KeyboardInterrupt from the main program
        except:
            pass # TODO: this is a temporary fix -- suppresses any exception from the bootloader, prevents errors when robot threads terminate earlier than expected
                 # This works but would be better to use some kind of stop event based on the simulator ending

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