import pygame 
from settings import *

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, x, y , groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(center = (x,y))

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        self.player = player
        self.image = pygame.Surface((200, 20))
        self.rect = self.image.get_rect(bottomleft = (20, HEIGHT-20))
        self.image.fill("red")
        self.background = HealthBarBackground(self.rect, 5, groups)
        super().__init__(groups)
    
    def update(self, others):
        self.image = pygame.Surface((self.player.hp*2, 20))
        self.rect = self.image.get_rect(bottomleft = (20, HEIGHT-20))
        self.image.fill("red")

class HealthBarBackground(pygame.sprite.Sprite):
    def __init__(self, oldrect, increase, groups):
        super().__init__(groups)
        dincrease = increase * 2
        self.image = pygame.Surface((oldrect.width + dincrease, oldrect.height + dincrease))
        self.image.fill("black")
        self.rect = self.image.get_rect(center = oldrect.center)


class StartMenu(pygame.sprite.Sprite):
    def __init__(self, image, groups):
        super().__init__(groups)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft = (0,0))

class EndScreen(pygame.sprite.Sprite):
    def __init__(self, image, groups):
        super().__init__(groups)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft = (0,0))