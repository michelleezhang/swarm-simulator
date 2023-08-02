import argparse
import json
import time
import multiprocessing as mp
from bootloader import Bootloader
from sim import Simulator
from gui import GUI

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

    # List of processes to run
    processes = []

    # Initialize classes and run processes simultaneously
    bootloader = Bootloader(userfile, config_data)
    simulator = Simulator(config_data, initfile)
    if vis == 1:
        gui = GUI(config_data)
    elif vis == 0:
        gui = None

    # Start simulator process (this process also runs the gui)
    s_proc = mp.Process(target=simulator.launch, args=(vis, gui))
    processes.append(s_proc)
    s_proc.start()
    time.sleep(2) # Ensures sim server and gui time start initializing before the sim clients

    for i in range(num_robots):
        proc_context = mp.get_context('spawn') # When creating a child process, create and use a completely new, independent Python interpreter process each time -- this is the setting most compatible across different systems (works for macOS, windows, and most linux distributions)
        r_proc = proc_context.Process(target=bootloader.launch, args=(i, simulator.swarm[i].a_ids)) 
        r_proc.start()
        processes.append(r_proc)
    # TODO: for python2 compatibility on the bootloader, need to specify path to py2 and py3 interpreter on user's machine -- pool_context.set_executable(...)  

    # pool_context = mp.get_context('spawn') # When creating a child process, create and use a completely new, independent Python interpreter process each time -- this is the setting most compatible across different systems (works for macOS, windows, and most linux distributions)
    # pool = pool_context.Pool(processes=num_robots) # The `processes` argument specifies the maximum number of worker processes that can be created 
    # for i in range(num_robots):
    #     # Submit tasks to the pool using apply_async() -- create a total of num_robots instances of the bootloader process to run, passing in i as the robot id
    #     pool.apply_async(bootloader.launch, args=(i, simulator.swarm[i].a_ids))
    # pool.close()
    # processes.append(pool)

    # Wait for processes to finish running or terminate cleanly
    try:
        for process in processes:
            process.join()
        print("Simulation completed.")
    except KeyboardInterrupt:
        active_processes = mp.active_children() # This gives a list of all active processes (including child processes)
        for process in active_processes:
            process.terminate()
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