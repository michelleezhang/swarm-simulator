

def init(swarmsize, x, y, theta, a_ids):
	from math import pi
	for i in range(0,swarmsize):
		if i == 0:
			x[i] = 0.0
			y[i] = 0.0
			a_ids[i] = i
			theta[i] = 0
	return x, y, theta, a_ids