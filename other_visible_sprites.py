import pygame 
from settings import *

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, x, y , groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(center = (x,y))

class StartMenu(pygame.sprite.Sprite):
    def __init__(self, image, groups):
        super().__init__(groups)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft = (0,0))