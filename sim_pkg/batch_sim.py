#!/bin/bash
import sys
import subprocess

argnum = len(sys.argv)
num_runs = int(sys.argv[1])
user_file = sys.argv[2]
config_file = sys.argv[3]
if argnum == 5:
    init_file = sys.argv[4]

for i in range(num_runs):
    if argnum == 5:
        subprocess.run(['python3', 'coachbot_simulation.py', '-fn', user_file, '-c', config_file, '-i', init_file])
    elif argnum == 4:
        subprocess.run(['python3', 'coachbot_simulation.py', '-fn', user_file, '-c', config_file])
    else:
        print('Wrong number of arguments!')