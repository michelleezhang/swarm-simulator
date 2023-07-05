'''
Lab 2
'''
def init(swarmsize, x, y, theta, a_ids):
    import math
    
    for i in range(swarmsize):
        y[i] = (i % 16) * 0.11 - 1 + (math.floor(i / 16) % 2) * 0.055
        x[i] = (i / 16) * 0.08 - 1
        a_ids[i] = 0
        theta[i] = 0
        if i == 0:
            a_ids[i] = 1
        elif i == 240:
            a_ids[i] = 2
    return x, y, theta, a_ids