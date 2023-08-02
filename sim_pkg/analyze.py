from matplotlib import pyplot as plt
import numpy as np
import logging
import csv

class Sim_Stat_Logger(logging.StreamHandler):
    def __init__(self, filename):
        '''
        A logger that keeps track of statistics from the simulation
        '''
        super().__init__() # Super is used to call a method from a parent or superclass within a subclass, so here, the logger is also initialized
        self.filename = filename

    def emit(self, record):
        '''
        Open the CSV file and record a data row
        '''
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(record.msg)

class Analyzer():
    def __init__(self):
        '''
        '''
        self.collisions = True

    def plot_collisions(self):
        '''
        '''
        # Read the CSV file into a NumPy array using genfromtxt
        data_array = np.genfromtxt('log_values.csv', delimiter=',', skip_header=0)

        # Extract the values from a specific column (e.g., column index 1)
        
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
    analyzer = Analyzer()
    analyzer.plot_collisions()