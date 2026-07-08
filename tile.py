import pygame
from settings import *
from debug import debug

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft = pos)