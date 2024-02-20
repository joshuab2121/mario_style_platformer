import pygame

class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()

        # coins
        self.coin = pygame.image.load('graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50,61))
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF', 30)

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar,(20,10))
        width = current / full * 152 #Health indicator width
        health_rect = pygame.Rect(54, 39, width, 4)
        pygame.draw.rect(self.display_surface, '#dc4949', health_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, '#33323d')
        x = (self.coin_rect.midright[0] + 10)
        y = self.coin_rect.centery
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (x,y))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)