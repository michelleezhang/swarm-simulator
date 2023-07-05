from matplotlib import pyplot as plt
import numpy as np
from numpy import genfromtxt

class Analyzer:
    def __init__(self):
        pass
    def plot_collisions(self):
        collision_counts = genfromtxt('collisions.csv')
        bins = np.arange(0, np.max(collision_counts), 200, dtype=int)
        #print(bins, collision_counts)

        fig, ax = plt.subplots(1, 1)
        ax.hist(collision_counts, bins)
        ax.set_xlabel('no. of collisions')
        ax.set_ylabel('no. of simulations')
        ax.locator_params(axis='y', integer=True)
        plt.show()