import settings
import pygame
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.middle = pygame.image.load('graphics/decoration/sky/sky_middle.png').convert()
        self.bottom = pygame.image.load('graphics/decoration/sky/sky_bottom.png').convert()
        self.horizon = horizon

        # stretch 
        self.top = pygame.transform.scale(self.top,(settings.screen_width, settings.tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(settings.screen_width, settings.tile_size))
        self.middle = pygame.transform.scale(self.middle,(settings.screen_width, settings.tile_size))

    def draw(self, surface):
        for row in range(settings.vertical_tile_number):
            y = row * settings.tile_size
            if row < self.horizon:
                surface.blit(self.top, (0,y))
            elif row == self.horizon:
                surface.blit(self.middle, (0,y))
            else:
                surface.blit(self.bottom, (0,y))

class Water:
    def __init__(self, top, level_width):
        water_start = -settings.screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + settings.screen_width) / water_tile_width) + 5
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            pos = (x,y)
            sprite = AnimatedTile(192, pos, 'graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)

class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder('graphics/decoration/clouds')
        min_x = -settings.screen_width
        max_x = level_width + settings.screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            pos = (x,y)
            sprite = StaticTile(0, pos, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
        
    