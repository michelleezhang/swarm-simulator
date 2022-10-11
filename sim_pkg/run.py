import subprocess
import time
from pathlib import Path
def main():
    path = str(Path(__file__).parent)
    print("Enter the number of robots to launch")
    num = input()
    # print(path)
    subprocess.Popen(['python3', 'simulator.py'],close_fds=True,cwd=path)
    time.sleep(1)
    for i in range(int(num)):
        subprocess.Popen(['python2','user.py'],close_fds=True,cwd=path)
    # subprocess.Popen(['python2','user2.py'],close_fds=True,cwd=path)
    res = subprocess.run(['python3','visualization.py'],cwd=path)

if __name__ == '__main__':
    main()

