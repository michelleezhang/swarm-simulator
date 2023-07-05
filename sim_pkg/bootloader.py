#!/usr/bin/env python2
import os
import importlib
from bot_api.coachbot_api import Coachbot
from client_server import Bot_Client

class Bootloader():
    '''
    Run the given user code.
    '''
    def __init__(self, userfile, config_data):
        self.userfile = userfile
        self.config_data = config_data

    def launch(self, id, a_ids):
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

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Run the robots")
    parser.add_argument("-u", "--userfile", type=str, help="Path to user code file", required=True)
    args = parser.parse_args()

    bootloader = Bootloader(args.userfile)
    bootloader.launch()