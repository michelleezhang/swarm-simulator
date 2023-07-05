import contextlib
with contextlib.redirect_stdout(None): # Suppresses "Hello from the pygame" message 
    import pygame

class GUI:
    def __init__(self, config_data):
        self.config_data = config_data
        
        self.length = 1000
        self.height = 800
        self.radius = 9.9
        self.font_size = 20

    def launch(self):
        # Initialize pygame
        pygame.init()
        self.window = pygame.display.set_mode((self.length, self.height))
        self.font = pygame.font.SysFont('samanata', self.font_size)
        self.font_num = pygame.font.SysFont('samanata', 18) 
    
    def stop(self):
        pygame.quit()

    def update(self, state, real_time, sim_time, rtf):
        # Clear the screen before redrawing (color it black)
        self.window.fill((0, 0, 0))

        # Draw all robots
        for robot in state:
            position = self.to_pygame(robot.x, robot.y) # Scale coordinates to screen size
            pygame.draw.circle(self.window, robot.led, position, self.radius)
        
        self.display_time(real_time, sim_time, rtf) 

        pygame.display.flip()

        # Keep pygame screen open until time to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

    def display_time(self, real_time, sim_time, rtf):
        data_string = 'Real time factor ' + f'{rtf:.3f} x | Real time: ' + f'{real_time:.3f} seconds | Sim time:' + f'{sim_time:.3f} seconds'
        text = self.font.render(data_string, True, (255,255,255))
        
        self.window.blit(text, (200, 100))

    def to_pygame(self, x_coord, y_coord):
        """Convert coordinates into pygame coordinates (lower-left => top left)."""
        # the origin on screen is ( (x1 + x2) / 2, (y1 + y2) / 2 ), midpoit of its diagonal
        # or (self.length / 2), (self.height / 2)

        ARENA_LENGTH = 7.5
        ARENA_WIDTH = 4.5 # hight
        x_fac = self.length / ARENA_LENGTH
        y_fac = self.height / ARENA_WIDTH

        new_x =(y_coord + ARENA_LENGTH / 2) * x_fac 
        new_y = (x_coord + ARENA_WIDTH / 2) * y_fac
        
        return (int(new_x), int(new_y))