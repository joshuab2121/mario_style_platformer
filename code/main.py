import pygame
import settings
from tiles import Tile
from sys import exit
from level import Level
from game_data import level_0, level_1

pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()
# lvl = input("Pick a level: (1,2)")
# if lvl == '1':

#     level = Level(level_0, screen)
# else:
#     level = Level(level_1, screen)
level = Level(level_0, screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # draw all our enemies
    # update everything
    screen.fill('grey')
    level.run()
    
    pygame.display.update()
    clock.tick(60)
