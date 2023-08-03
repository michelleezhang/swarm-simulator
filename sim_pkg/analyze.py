import argparse
import logging
import csv
from matplotlib import pyplot as plt
import numpy as np

class Sim_Stat_Logger(logging.StreamHandler):
    def __init__(self, filename):
        '''
        A logger that keeps track of statistics from the simulation
        '''
        super().__init__() # Super is used to call a method from a parent or superclass within a subclass, so here, the logger is also initialized
        self.filename = filename

    def emit(self, record):
        '''
        Open CSV file and record a data row
        '''
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(record.msg)

class Analyzer():
    def __init__(self, filename):
        '''
        Class to hold methods for plotting simulation statistics
        '''
        self.filename = filename

    def plot_collisions(self):
        '''
        Plot number of collisions as a histogram
        '''
        # Read the CSV file into a numpy array using genfromtxt
        data_array = np.genfromtxt(self.filename, delimiter=',', skip_header=0)

        # Extract the values from a specific column (here, we use column 1)
        column_index = 1
        if len(data_array.shape) > 1:
            collision_counts = data_array[:, column_index]
        else:
            collision_counts = data_array[column_index]

        bins = np.histogram_bin_edges(collision_counts, bins='auto')

        plt.hist(collision_counts, bins)
        plt.xlabel('no. of collisions')
        plt.ylabel('no. of simulations')
        plt.locator_params(axis='y', integer=True)
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot simulation statistics")
    parser.add_argument("-f", "--filename", type=str, help="Name of csv file", required=True)
    args = parser.parse_args()

    analyzer = Analyzer(args.filename)
    analyzer.plot_collisions()