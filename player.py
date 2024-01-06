import pygame
from support import import_folder
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index] 
        self.rect = self.image.get_rect(topleft = pos)

        # player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.facing = "right"

    def import_character_assets(self):
        character_path = 'graphics/character'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + '/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.get_status()]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        if self.facing == "left":
            self.image = pygame.transform.flip(animation[int(self.frame_index)],True, False)
        else:
            self.image = animation[int(self.frame_index)]
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing = "right"
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            return 'jump'
        elif self.direction.y > 0:
            return 'fall'
        elif self.direction.x != 0:
            return 'run'
        else:
            return "idle"
    def jump(self):
        self.direction.y = self.jump_speed
 
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        
        
