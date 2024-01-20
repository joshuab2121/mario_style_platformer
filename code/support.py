from os import walk
import pygame
from csv import reader
import settings

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width() / settings.tile_size)
    tile_num_y = int(surface.get_height() / settings.tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * settings.tile_size
            y = row * settings.tile_size
            new_surf = pygame.Surface((settings.tile_size, settings.tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x,y, settings.tile_size, settings.tile_size))
            cut_tiles.append(new_surf)
    
    return cut_tiles