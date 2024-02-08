import numpy as np

class Robot():
    def __init__(self, id, x, y, theta, a_ids, clock, num_robots, alive):
        '''
        Internal representation of a robot in the simulator
        Contains all variables associated with a given robot
        '''
        self.id = id
        self.a_ids = a_ids
        self.posn = [x, y, theta]
        self.led = (50, 50, 50)
        self.velocity = (0, 0)
        self.message_buffer = []
        self.clock = clock 
        self.collision_list = np.zeros(num_robots) # List of times until collision with all other robots in the swarm
        
        self.alive = alive # NEW: C+D

    def integrate(self, delta_time):
        """
        Integrate the state of robot
        """
        pos = self.dynamics(np.array([[self.velocity[0]], [self.velocity[1]]]) * delta_time)
        pos[0] = (pos[0]+ np.pi) % (2 * np.pi) - np.pi
        return pos
    
    def dynamics(self, vel_vector):
        """
        State dynamic model used to integrate using Euler integration
        """
        friction = 0.6
        vel_vector = friction*vel_vector
        half_radius_of_wheel, dist_between_wheel = 0.0075, 0.08 # First value is half of the wheel's radius
        scaled_rad, scaled_cos, scaled_sin = (2 * half_radius_of_wheel)/dist_between_wheel, half_radius_of_wheel * np.cos(self.posn[2]), half_radius_of_wheel * np.sin(self.posn[2])

        state_matrix = np.array([[-scaled_rad, scaled_rad], 
                                 [scaled_cos, scaled_cos], 
                                 [scaled_sin, scaled_sin],
                                 [1.0, 0.0],
                                 [0.0, 1.0]])
        pos = (state_matrix@vel_vector) # calculate delta in theta and posn
        return np.array([self.posn[2] + pos[0][0], self.posn[0] + pos[1][0], self.posn[1] + pos[2][0]])