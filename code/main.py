import pygame
import settings
from tiles import Tile
from sys import exit
from level import Level
from game_data import level_0, level_1
from overworld import Overworld

class Game:
    def __init__(self):
        self.max_level = 1
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
    
    def create_level(self, current_level):
        if current_level == 0:
            self.level = Level(0, screen, self.create_overworld)
        elif current_level == 1:
            self.level = Level(1, screen, self.create_overworld)
        elif current_level == 2:
            self.level = Level(2, screen, self.create_overworld)
        elif current_level == 3:
            self.level = Level(3, screen, self.create_overworld)
        elif current_level == 4:
            self.level = Level(4, screen, self.create_overworld)
        elif current_level == 5:
            self.level = Level(5, screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)

        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
              

pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()
game = Game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # draw all our enemies
    # update everything
    screen.fill('black')
    game.run()
    
    # level.run()
    

    pygame.display.update()
    clock.tick(60)
