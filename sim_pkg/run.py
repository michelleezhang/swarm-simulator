import subprocess
import time
from pathlib import Path
import json
def main():
    path = str(Path(__file__).parent)
    with open('config.json', 'r') as myfile:
        data=myfile.read()
    config_var = json.loads(data)
    num = config_var["NUMBER_OF_ROBOTS"]
    # print(path)
    subprocess.Popen(['python3', 'simulator.py'],close_fds=True,cwd=path)
    time.sleep(1)
    for i in range(int(num)):
        subprocess.Popen(['python2','bootloader.py'],close_fds=True,cwd=path)
    # subprocess.Popen(['python2','user2.py'],close_fds=True,cwd=path)
    res = subprocess.run(['python3','visualization.py'],cwd=path)

if __name__ == '__main__':
    main()

