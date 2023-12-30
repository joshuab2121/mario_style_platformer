import pygame
from tiles import Tile
import settings

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    pos = (col_index*settings.tile_size, row_index * settings.tile_size)
                    self.tiles.add (Tile(pos,settings.tile_size))

    def run(self):
        self.tiles.draw(self.display_surface)