import subprocess
import time
from pathlib import Path
import json
import sys
# sim_process_ = 0 
robot_processes_ = []
# vis_processes_ = 0

def run():
    """
    Opens all the programs involved
    """

    path = str(Path(__file__).parent)
    with open('config.json', 'r') as myfile:
        data=myfile.read()
    config_var = json.loads(data)
    num = config_var["NUMBER_OF_ROBOTS"]
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
    sim_process_, robot_processes_, vis_processes_ = run()
    flag = True
    while flag:

        try:
            pass
        except KeyboardInterrupt:
            # Kill the processes. Currently kills the robot subprocess and everything seems to die.
            
            for process_ in robot_processes_:
                subprocess.Popen.terminate(process_)
            try:
                subprocess.Popen.terminate(sim_process_)
            except:
                pass
            
            try:
                subprocess.Popen.terminate(vis_processes_)
            except:
                pass

            flag = False
            print('Interrupted')
            sys.exit(1)


if __name__ == '__main__':
    main()

