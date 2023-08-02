'''
Lab 4
'''
def init(swarmsize, x, y, theta, a_ids):
    import math
    import random
    for i in range(swarmsize):
        x[i] = (i % 10 - 5) * 0.3 + random.uniform(-0.1, 0.1)
        y[i] = (i / 10 - 5) * 0.3 + random.uniform(-0.05, 0.05) + 0.1
        a_ids[i] = i
        theta[i] = random.uniform(-math.pi, math.pi)

    return x, y, theta, a_ids

