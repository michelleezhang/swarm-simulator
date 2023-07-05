import numpy as np

class Robot():
    def __init__(self, id, x, y, theta, num_robots, clock=0, a_ids=-1):
        self.id = id
        self.x = x
        self.y = y
        self.theta = theta
        self.a_ids = a_ids
        self.led = (50, 50, 50)
        self.velocity = (0, 0)

        self.message_buffer = []

        self.clock = clock 
        
        self.radius_of_wheel = 0.015
        self.half_distance_between_wheel = 0.04

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
        state_matrix = np.array([[-self.radius_of_wheel/(2.0*self.half_distance_between_wheel), self.radius_of_wheel/(2.0*self.half_distance_between_wheel)], 
                                 [self.radius_of_wheel*np.cos(self.theta)/2.0, self.radius_of_wheel*np.cos(self.theta)/2.0], 
                                 [self.radius_of_wheel*np.sin(self.theta)/2.0, self.radius_of_wheel*np.sin(self.theta)/2.0],
                                 [1.0, 0.0],
                                 [0.0, 1.0] ])
        pos = (state_matrix@vel_vector)
        pos = np.array([self.theta + pos[0][0], self.x + pos[1][0], self.y + pos[2][0]])

        return pos