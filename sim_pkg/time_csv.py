import numpy as np
import matplotlib.pyplot as plt
data = np.genfromtxt('time.csv',delimiter=',')

plt.plot(data[:,1],data[:,0])
plt.xlabel('Real time [s]')
plt.ylabel('Sim time [ticks]')
# plt.xlim([0,4000])
plt.title('Real time vs simulation time')
plt.savefig('time2.png')