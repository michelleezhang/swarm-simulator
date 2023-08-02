import numpy as np

class Robot():
    def __init__(self, id, x, y, theta, a_ids, clock, num_robots):
        self.id = id
        self.a_ids = a_ids
        self.posn = [x, y]
        self.theta = theta
        self.led = (50, 50, 50)
        self.velocity = (0, 0)
        self.message_buffer = []
        self.clock = clock 
    
        self.collision_list = np.zeros(num_robots)

    def integrate(self, delta_time):
        """
        Integrate the state of robot
        """
        velocity_vector = np.array([[self.velocity[0]], [self.velocity[1]]])
        pos = self.dynamics(velocity_vector * delta_time)
        pos[0] = (pos[0]+ np.pi) % (2 * np.pi) - np.pi
        return pos
        
    def dynamics(self, vel_vector):
        """
        State dynamic model used to integrate using euler integration
        """
        radius_of_wheel = 0.015
        half_distance_between_wheel = 0.04

        state_matrix = np.array([[-radius_of_wheel/(2.0 * half_distance_between_wheel), radius_of_wheel/(2.0 * half_distance_between_wheel)], 
                                 [radius_of_wheel*np.cos(self.theta)/2.0, radius_of_wheel*np.cos(self.theta)/2.0], 
                                 [radius_of_wheel*np.sin(self.theta)/2.0, radius_of_wheel*np.sin(self.theta)/2.0],
                                 [1.0, 0.0],
                                 [0.0, 1.0] ])
        pos = (state_matrix@vel_vector)
        pos = np.array([self.theta + pos[0][0], self.posn[0] + pos[1][0], self.posn[1] + pos[2][0]])

        return pos