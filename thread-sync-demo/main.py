import multiprocessing as mp
import threading
from bootloader import Bootloader
from sim import Simulator
import time

def run_threads(bootloader, num_robots): 
    '''
    Starts a thread that calls bootloader launch for each robot 
    '''
    # ######### UNEDITED #######################
    # threads = [threading.Thread(target=bootloader.launch, args=(i,)) for i in range(num_robots)] 
    # for thread in threads:
    #     thread.start()

    ######### OPTION ONE: Threading Barrier  #######################
    # Works well but would need to go into the user code somehow to place the stops for the barrier
    barrier = threading.Barrier(num_robots)
    threads = [threading.Thread(target=bootloader.launch, args=(i, barrier)) for i in range(num_robots)] 
    for thread in threads:
        thread.start()
    
def main():
    print("Simulation initiated.")
    num_robots = 5
    
    # Initialize classes and run processes simultaneously
    bootloader = Bootloader()
    simulator = Simulator()

    # Start simulator process (this process also runs the gui)
    s_proc = mp.Process(target=simulator.launch)
    s_proc.start()
    time.sleep(0.1)

    r_proc = mp.Process(target=run_threads, args=(bootloader, num_robots))
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
    main()