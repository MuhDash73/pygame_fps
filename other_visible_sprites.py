import pygame 

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, x, y , groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(center = (x,y))