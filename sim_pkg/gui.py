import contextlib
with contextlib.redirect_stdout(None): # Suppresses "Hello from the pygame" message 
    import pygame
import numpy as np
import os
import shutil

class GUI:
    def __init__(self, config_data, trial_number):
        '''
        A GUI to display the simulation
        Receives data from the simulator and draws the swarm onscreen
        '''
        self.arena_length, self.arena_height = config_data["LENGTH"], config_data["WIDTH"]
        self.screen_length, self.screen_height = (900 / self.arena_height) * self.arena_length, 900 # Scales screen size by given arena dimensions
        self.radius = 5
        self.arrow_width, self.arrow_height = self.radius / 3, self.radius / 2
        self.x_fac, self.y_fac = self.screen_length / self.arena_length, self.screen_height / self.arena_height
        self.frame_num = 0
        if "VIDEO_NAME" in config_data:
            self.video_folder = config_data["VIDEO_NAME"] + "_" + str(trial_number)
            # Delete directory if it already exists and make a new one
            if os.path.exists(self.video_folder):
                shutil.rmtree(self.video_folder)
            
            os.makedirs(self.video_folder)
            
        else:
            self.video_folder = None

    def launch(self):
        '''
        Initialize pygame and specify display settings
        '''
        pygame.font.init()
        self.font = pygame.font.SysFont('samanata', 24)
        self.window = pygame.display.set_mode((self.screen_length, self.screen_height))

    def stop_gui(self):
        '''
        Stop the GUI
        '''
        if self.video_folder != None:
            pass
            # convert folder and delete
        pygame.quit()
    
    def update(self, state, real_time, sim_time, rtf):
        '''
        Update the screen
        '''
        self.window.fill((0, 0, 0)) # Clear the screen before redrawing (color it black)

        # Draw robots
        for robot in state:
            # Scale coordinates to screen size
            position = self.to_pygame(robot.posn) 

            # Draw circle
            pygame.draw.circle(self.window, robot.led, position, self.radius)

            # Draw arrow
            arrow = pygame.Vector2(position[0] - int(position[0] + self.radius * np.sin(robot.posn[2])), 
                                   position[1] - int(position[1] + self.radius * np.cos(robot.posn[2])))
            angle = -np.radians(arrow.angle_to(pygame.Vector2(1, 0)))
            verts = [self.rotate_in_place(0, self.arrow_height, angle, position), # Center
                     self.rotate_in_place(self.arrow_width, -self.arrow_height, angle, position),  # Bottom right
                     self.rotate_in_place(-self.arrow_width, -self.arrow_height, angle, position)] # Bottom left
            pygame.draw.polygon(self.window, (230, 230, 250), verts)

        # Draw text
        time_text = self.font.render('Real time factor ' + f'{rtf:.2f}x | Real time: ' + f'{real_time:.2f} seconds | Sim time: ' + f'{sim_time:.2f} seconds', 
                                     True, (255,255,255))
        self.window.blit(time_text, (170, 100)) # Blit is like the "draw" equivalent for text/images

        # Update the display to show the latest changes
        pygame.display.flip()

        # Save video 
        if self.video_folder != None:
            pygame.image.save(self.window, f"{self.video_folder}/frame{self.frame_num}.png")
            self.frame_num += 1

        # Keep pygame screen open (or quit if the user closes the screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_gui()
        
    def to_pygame(self, coord):
        '''
        Convert robot coordinates to pygame coordinates 
        '''
        return (coord[0] + self.arena_length / 2) * self.x_fac, (-coord[1] + self.arena_height / 2) * self.y_fac
    # NOTE: Pygame coordinate system has (0,0) in the top-left and positive y is downward direction

    def rotate_in_place(self, x, y, theta, posn):
        '''
        Return arrow coordinates (x, y) rotated by theta, centered at posn
        '''
        cos_theta, sin_theta = np.cos(theta), np.sin(theta)
        return x * cos_theta - y * sin_theta + posn[0], x * sin_theta + y * cos_theta + posn[1] 
    
if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Run the GUI")
    parser.add_argument("-c", "--configfile", type=str, help="Path to configuration file", required=True)
    args = parser.parse_args()

    with open("user/" + args.configfile, 'r') as cfile:
        config_data = json.loads(cfile.read())
    cfile.close()

    gui = GUI(config_data)
    gui.launch()