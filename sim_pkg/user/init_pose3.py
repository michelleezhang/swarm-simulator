'''
Lab 3
'''
def init(swarmsize, x, y, theta, a_ids):
    for i in range(swarmsize):
        y[i] = (i % 10) * 0.2 - 1
        x[i] = (i / 10) * 0.2 - 2
        a_ids[i] = 0
        theta[i] = 0
        if i % 3 == 0:
            a_ids[i] = 1
        elif i % 3 == 1:
            a_ids[i] = 0
        else:
            a_ids[i] = 2
    
    return x, y, theta, a_ids