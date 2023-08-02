#!/usr/bin/env python2
import os
import importlib
from bot_api.coachbot_api import Coachbot
from client_server import Bot_Client

class Bootloader():
    def __init__(self, userfile, config_data):
        '''
        A bootloader to the given user code
        '''
        self.userfile = userfile
        self.config_data = config_data

    def launch(self, id, a_ids=-1):
        '''
        Creates a robot instance to run the user file
        '''
        try:
            # Import userfile as a module
            userfile = os.path.splitext(self.userfile)[0] # Remove .py ending from userfile name
            fn = importlib.import_module("user." + userfile) 

            # Create a Coachbot instance with given id number
            bot_client = Bot_Client("localhost", 8000, self.config_data)
            bot_client.start()
            robot = Coachbot(bot_client, id, a_ids)

            # Run usr function in userfile module
            fn.usr(robot)

            bot_client.stop()

        except KeyboardInterrupt:
            pass

        except:
            # TODO: This usually means the server terminated before the client -- should try to find a way to isolate that error
            pass

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