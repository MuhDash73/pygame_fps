import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        #xy = 1800
        #2.5(12/150)=how far up per move
        #2.5(12/(1800/12))=ukw
        size = 5
        self.image = pygame.Surface((size,size))
        self.image.fill("orange")
        self.x = player.cords.x
        self.y = player.cords.y
        self.z = 0
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.direction = player.direction
        self.player = player
        self.enemies = player.enemies
        self.speed = 1
        self.raycastables = player.raycastables
        self.shoot()

    def shoot(self):
        surface  = pygame.display.get_surface()
        hit = False
        while not hit:
            self.x += self.speed * self.direction[0]
            self.y += self.speed * self.direction[1]
            if not self.player.up_direction == 0:
                self.z += self.speed * ((self.player.up_direction * abs(self.player.up_direction)) / 1800)
            self.rect.center = (self.x, self.y)
            for enemy in pygame.sprite.spritecollide(self, self.enemies, False):
                if not enemy.immune:
                    try:
                        if enemy.bottom < self.z < enemy.top:
                            enemy.hp -= 1
                            enemy.immune = True
                    except:
                        enemy.hp -= 1
                        enemy.immune = True
                        #print(self.z)
                    if enemy.hp <= 0:
                        enemy.alive = False
                        enemy.kill()
            try:
                if self.raycastables[int(self.y/TILESIZE)][int(self.x/TILESIZE)] == 1:
                    hit = True
            except Exception as e:
                hit = True
        #print(self.z)
        self.kill()