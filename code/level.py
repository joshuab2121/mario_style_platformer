import pygame
from tiles import Tile, StaticTile, Crate, Coin, Palm
from player import Player
import settings
from support import import_csv_layout, import_cut_graphics
from particles import ParticleEffect
from enemy import Enemy
from decoration import Sky, Water, Clouds
from random import randint
from game_data import levels

class Level:
    def __init__(self, current_level, surface, create_overworld):
        # level setup
        self.display_surface = surface
        self.world_shift = 0
        # self.current_x = None
        self.current_x = 0
        print(current_level)
        print(levels[current_level])
        self.current_level = current_level
        level_data = levels[current_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld

        # bg_palms setup
        bg_palms_layout = import_csv_layout(level_content['bg_palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palms_layout, 'bg_palms')

        # coins setup
        coins_layout = import_csv_layout(level_content['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        # constraints setup
        constraints_layout = import_csv_layout(level_content['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')

        # crates setup
        crates_layout = import_csv_layout(level_content['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')

        # enemies setup
        enemies_layout = import_csv_layout(level_content['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

        # fg_palms setup
        fg_palms_layout = import_csv_layout(level_content['fg_palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palms_layout, 'fg_palms')

        # grass setup
        grass_layout = import_csv_layout(level_content['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        
        # player setup
        player_layout = import_csv_layout(level_content['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain setup
        terrain_layout = import_csv_layout(level_content['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * settings.tile_size
        self.water = Water(settings.screen_height - 40, level_width)
        self.clouds = Clouds(400, level_width, randint(10,30))

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * settings.tile_size
                    y = row_index * settings.tile_size
                    pos = (x,y)
                    sprite = pygame.sprite.Sprite()
                    if type == 'bg_palms':
                        sprite = Palm(settings.tile_size, pos, 'graphics/terrain/palm_bg', val)
                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(settings.tile_size, pos, 'graphics/coins/gold')
                        if val == '1':
                            sprite = Coin(settings.tile_size, pos, 'graphics/coins/silver')
                    if type == 'constraints':
                        sprite = Tile(settings.tile_size, pos)
                    if type == 'crates':
                        sprite = Crate(settings.tile_size, pos)
                    if type == 'enemies':
                        sprite = Enemy(settings.tile_size, pos)
                    if type == 'fg_palms':
                        if val == '3':
                            pos = tuple(map(lambda x, y: x+y, pos, (randint(0,30),randint(0,30))))
                            sprite = Palm(settings.tile_size, pos, 'graphics/terrain/palm_small', val)
                        if val == '4':
                            sprite = Palm(settings.tile_size, pos, 'graphics/terrain/palm_large', val)
                        pass
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(settings.tile_size, pos, tile_surface)
                        
                    if type == 'player':
                        pass
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(settings.tile_size, pos, tile_surface)
                    sprite_group.add(sprite)
        return sprite_group
    
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * settings.tile_size
                y = row_index * settings.tile_size
                pos = (x,y)
                if val == '0':
                    sprite = Player(pos, self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)     
                if val == '1':
                    hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(settings.tile_size,pos, hat_surface)
                    self.goal.add(sprite)
    
    def create_jump_particles(self, pos):
        if self.player.sprite.facing == 'right':
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)

        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing == 'right':
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)

            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    pos = (col_index*settings.tile_size, row_index * settings.tile_size)
                    self.tiles.add(Tile(settings.tile_size, pos))
                if cell == 'P':
                    pos = (col_index*settings.tile_size, row_index * settings.tile_size)
                    self.player.add(Player(pos,self.display_surface, self.create_jump_particles))

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

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.fg_palms_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top= sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
            
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > .10:
            player.on_ceiling = False

    def enemy_collision_reverse(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraints_sprites, False):
                enemy.reverse()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level, self.new_max_level)
            
        # if keys[pygame.K_ESCAPE]:

    def run(self):        
        # run the entire game / level

        self.input()

        # decoration 
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        
        # bacground palms
        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)
        # enemy
        self.enemies_sprites.update(self.world_shift)
        self.enemies_sprites.draw(self.display_surface)

        # constraints
        self.constraints_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        # crates
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)
        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        

        # foreground palms
        self.fg_palms_sprites.update(self.world_shift)
        self.fg_palms_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # player 
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # Water
        self.water.draw(self.display_surface, self.world_shift)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)
        
        # # level tiles 
        # # self.tiles.update(self.world_shift)
        # # self.tiles.draw(self.display_surface)
        self.scroll_x()

        # # player 
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)
        
