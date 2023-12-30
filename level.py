import pygame
from tiles import Tile
from player import Player
import settings

class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    pos = (col_index*settings.tile_size, row_index * settings.tile_size)
                    self.tiles.add(Tile(pos,settings.tile_size))
                if cell == 'P':
                    pos = (col_index*settings.tile_size, row_index * settings.tile_size)
                    self.player.add(Player(pos))

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x 
        if player_x < settings.screen_width / 4 and direction_x <0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > settings.screen_width * 3/4 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):        
        self.tiles.update(self.world_shift)
        # level tiles 
        self.tiles.draw(self.display_surface)
        # level player 
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()
