import pygame
from settings import *
from debug import debug
from bullet import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface((1, 1))
        self.image.fill("white")
    
    def start(self, x, y, obstacle_sprites, groups, raycastables, enemies):
        super().__init__(groups)
        self.groups = groups
        self.x = x
        self.y = y
        self.cords = pygame.math.Vector2(self.x, self.y)
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = TILESIZE
        self.moving = 0
        self.side_moving = 0
        self.sensitivity = 0.25
        self.direction = pygame.math.Vector2(0, -1)
        self.up_direction = 0
        self.up_sensitivity = 0.5
        self.up_direction_cap = 150
        self.obstacle_sprites = obstacle_sprites
        self.raycastables = raycastables
        self.enemies = enemies
        self.shot = False
        self.hp = 100
        for enemy in self.enemies:
            self.enemy = enemy


    def restrict(self):
        if self.cords.x < 0:
            self.cords.x = 0
        elif self.cords.x > (WIDTH*TILESIZE) - self.rect.width:
            self.cords.x = (WIDTH*TILESIZE) - self.rect.width
        
        if self.cords.y < 0:
            self.cords.y = 0
        elif self.cords.y > (HEIGHT*TILESIZE) - self.rect.height:
            self.cords.y = (HEIGHT*TILESIZE) - self.rect.height

    def move(self, dx, dy):
        keys = pygame.key.get_pressed()
        clicks = pygame.mouse.get_pressed()

        if keys[pygame.K_w]:
            self.moving = self.speed
        elif keys[pygame.K_s]:
            self.moving = -self.speed
        else:
            self.moving = 0
        
        if keys[pygame.K_a]:
            self.side_moving = self.speed
        elif keys[pygame.K_d]:
            self.side_moving = -self.speed
        else:
            self.side_moving = 0
        
        if keys[pygame.K_LEFT]:
            self.direction = self.direction.rotate(-0.1)
        if keys[pygame.K_RIGHT]:
            self.direction = self.direction.rotate(0.1)
        if keys[pygame.K_n]:
            self.hp -= 1
        
        self.direction = self.direction.rotate(dx*self.sensitivity)
        if keys[pygame.K_l]:
            self.up_direction += 0.1
        if keys[pygame.K_k]:
            self.up_direction += 1
        self.up_direction -= dy*self.up_sensitivity
        self.up_direction = max(-self.up_direction_cap, min(self.up_direction, self.up_direction_cap))
        #print(self.up_direction)

        self.side_direction = self.direction.copy()
        self.side_direction = self.side_direction.rotate(-90)
        #print(self.direction, self.side_direction)

        for i in range (2):
            self.cords[i] += self.direction[i] * self.moving
            self.rect.center = self.cords
            
            if pygame.sprite.spritecollide(self, self.obstacle_sprites, False):
                self.cords[i] -= self.direction[i] * self.moving
            
            self.cords[i] += self.side_direction[i] * self.side_moving
            self.rect.center = self.cords
            
            if pygame.sprite.spritecollide(self, self.obstacle_sprites, False):
                self.cords[i] -= self.side_direction[i] * self.side_moving
                self.rect.center = self.cords
        
        
        if clicks[0]:
            if self.shot == False:
                self.shot = True
                #print("l clcik")
                self.b = Bullet(self, self.groups)
        else:
            self.shot = False
        
        #print(self.cords)
        
        self.restrict()
    
    def update(self, dx, dy):
        self.move(dx, dy)