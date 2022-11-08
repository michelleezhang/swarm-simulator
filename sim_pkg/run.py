import subprocess
import time
from pathlib import Path
import json
import sys
import socketserver
import csv
import numpy as np
from init_pose import init


# sim_process_ = 0 
robot_processes_ = []
# vis_processes_ = 0

def write_to_csv(free_port):
    """
    Write avaliable port number to csv file
    """
    f = open('port.csv', 'w')
    num = [free_port]
    with f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(num)

    # close the file
    f.close()

def init_pos(swarmsize):
    """
    Initialize the position
    """
    x = [0]*swarmsize
    y = [0]*swarmsize
    theta = [0]*swarmsize
    a_ids = [0]*swarmsize

    x, y, theta, a_ids = init(swarmsize,x,y,theta,a_ids)
    id = [i for i in range(swarmsize)]

    data = np.array([id, x, y, theta, a_ids]).T
    np.savetxt("init.csv", data, delimiter=",", fmt="%.2f",
           header="ID, x, y, theta, a_ids")


def run():
    """
    Opens all the programs involved
    """


    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]

    write_to_csv(free_port)
    
    path = str(Path(__file__).parent)
    with open('config.json', 'r') as myfile:
        data=myfile.read()
    config_var = json.loads(data)
    num = config_var["NUMBER_OF_ROBOTS"]
    init_pos(num)
    
    # print(path)
    sim_process_ = subprocess.Popen(['python3', 'simulator.py'],close_fds=True,cwd=path)
    time.sleep(1)
    for i in range(int(num)):
        r_process = subprocess.Popen(['python2','bootloader.py'],close_fds=True,cwd=path)
        robot_processes_.append(r_process)
    # subprocess.Popen(['python2','user2.py'],close_fds=True,cwd=path)
    vis_processes_ = subprocess.Popen(['python3','visualization.py'],close_fds=True,cwd=path)

    return sim_process_, robot_processes_, vis_processes_

def main():
    """
    
    """
    sim_process, robot_processes, vis_process = run()
    
    try:
        # pass
        sim_process.wait()
        for process in robot_processes:
            process.wait()
        vis_process.wait()

    except KeyboardInterrupt:
        # Kill the processes. Currently kills the robot subprocess and everything seems to die.
        # subprocess.poll 
        for process in robot_processes:
            subprocess.Popen.terminate(process)
            stdout, stderr = process.communicate()
            # print(stdout)
            # print(stderr)
        
        subprocess.Popen.terminate(sim_process)
        
        try:
            subprocess.Popen.terminate(vis_process)
        except:
            pass

        
        print('Interrupted')
        # subprocess.run(['find','.','-name','*.pyc','-delete'])
        sys.exit(1)
            


if __name__ == '__main__':
    main()

