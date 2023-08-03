import argparse
import json
import time
import multiprocessing as mp
import threading
from bootloader import Bootloader
from sim import Simulator
from gui import GUI

def run_threads(bootloader, simulator, num_robots): 
    '''
    Starts a thread that calls bootloader launch for each robot 
    '''
    threads = [threading.Thread(target=bootloader.launch, args=(i, simulator.swarm[i].a_ids)) for i in range(num_robots)]
    for thread in threads:
        thread.start()

def main(userfile, config_data, initfile):
    '''
    Runs the robots, simulator, and GUI in parallel. 
    If the program is interrupted, terminate all processes cleanly.
    '''
    print("Simulation initiated.")

    # Number of robots
    num_robots = config_data["NUMBER_OF_ROBOTS"]
    # Boolean switch determines whether or not to run the GUI
    vis = config_data["USE_VIS"]

    # Initialize classes and run processes simultaneously
    bootloader = Bootloader(userfile, config_data)
    simulator = Simulator(config_data, initfile)
    if vis == 1:
        gui = GUI(config_data)
    elif vis == 0:
        gui = None

    # Start simulator process (this process also runs the gui)
    s_proc = mp.Process(target=simulator.launch, args=(vis, gui))
    s_proc.start()
    time.sleep(2) # TODO: This value may need to be adjusted
                   # The clients connect extremely quickly and may connect before the simulator server starts receiving data -- a large pause here is needed to prevent important commands at the beginning of the user code from being missed

    # TODO: for python2 compatibility on the bootloader, need to specify path to py2 and py3 interpreter on user's machine -- pool_context.set_executable(...)  
    r_proc = mp.Process(target=run_threads, args=(bootloader, simulator, num_robots))
    r_proc.start()

    # Wait for simulator to complete or terminate cleanly
    try:
        s_proc.join() # Wait for simulator process to complete
        r_proc.terminate() # Terminate the robot process after the simulator process is finished
        print("Simulation completed.")

    except KeyboardInterrupt:
        s_proc.terminate()
        r_proc.terminate()
        print("User interrupted: Simulation terminated.")

if __name__ == '__main__':
    # Parse command line arguments to obtain the paths to the required files
    parser = argparse.ArgumentParser(description="Run the robots, simulator, and GUI")
    parser.add_argument("-u", "--userfile", type=str, help="Path to user code file", required=True)
    parser.add_argument("-c", "--configfile", type=str, help="Path to configuration file", required=True)
    parser.add_argument("-i", "--initfile", type=str, help="Path to initialization file", required=False) # default value: None
    parser.add_argument("-n", "--num", type=str, help="Number of batches to run", required=False) # default value: None
    args = parser.parse_args()

    # Unpack configuration data dictionary
    with open("user/" + args.configfile, 'r') as cfile:
        config_data = json.loads(cfile.read())
    cfile.close()

    if args.num == None:
        num_iters = 1
    else:
        num_iters = int(args.num)
        
    for i in range(num_iters):
        # Run main function
        main(args.userfile, config_data, args.initfile)