import pygame
import random
from math import *
from settings import *
from debug import debug
import  bisect

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacle_sprites, player, groups):
        super().__init__(groups)
        self.image = pygame.Surface((1,1))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = (x,y))
        self.x = x
        self.y = y
        self.cords = pygame.math.Vector2(self.x, self.y)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 0.9
        self.obstacle_sprites = obstacle_sprites
        self.player = player
        self.hp = 1
        self.immune = False
        self.alive = True
    
    def add_seenenemy(self, seenenemy):
        self.seenenemy = seenenemy
        self.bottom = -self.seenenemy.rect.height//2 - self.seenenemy.ground
        self.top = self.seenenemy.rect.height//2 - self.seenenemy.ground
    
    def move(self):
        self.look_at_player()

        for i in range (2):
            self.cords[i] += self.direction[i] * self.speed
            self.rect.center = self.cords
            
            if pygame.sprite.spritecollide(self, self.obstacle_sprites, False):
                self.cords[i] -= self.direction[i] * self.speed

        #print(self.cords, self.rect.center)
    
    def look_at_player(self):
        direction_to_player = self.player.cords - self.cords
        self.direction = direction_to_player.normalize()
    
    def go_into_raycastable_position(self):
        player_dir = self.player.direction.as_polar()[1]
        new_player_dir = player_dir + 90
        self.v_cords_1 = self.cords - self.player.cords
        if -1 < self.v_cords_1.x < 1:
            self.v_cords_1.x = 0
        if not (-1 < self.v_cords_1.y < 1):
            v_cords_2 = pygame.math.Vector2()
            v_cords_2.y = (self.v_cords_1.x * cos(radians(player_dir))) + (self.v_cords_1.y * sin(radians(player_dir)))
            v_cords_2.x = -(self.v_cords_1.x * sin(radians(player_dir))) + (self.v_cords_1.y * cos(radians(player_dir)))
            return v_cords_2
        else:
            return None

    def restrict(self):
        if self.cords.x < 0:
            self.cords.x = 0
        elif self.cords.x > WIDTH - self.rect.width:
            self.cords.x = WIDTH - self.rect.width
        
        if self.cords.y < 0:
            self.cords.y = 0
        elif self.cords.y > HEIGHT - self.rect.height:
            self.cords.y = HEIGHT - self.rect.height
        
    def damage_player(self):
        if self.rect.colliderect(self.player.rect):
            self.player.hp -= 1
            #print(self.player.hp)
    
    def update(self, *others):
        self.immune = False
        self.move()
        self.damage_player()




class SeenEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy, groups, player):
        super().__init__(groups)
        self.type = random.choice(["normal", "high", "low"])
        self.type = "high"
        list = enemy_heights[self.type]
        self.width = list[0]
        self.height = list[1]
        self.image = pygame.Surface(list[2])
        self.ground = list[3]
        self.image.fill("red")
        self.player = player
        self.rect = self.image.get_rect(center = (0,0))
        self.enemy = enemy
    
    def update(self, raycaster):
        if self.enemy.alive == False:
            self.image.fill("#41A044")
        v_cords = self.enemy.go_into_raycastable_position()
        self.v_cords = v_cords
        self.rect.bottomright = (0,0)

        self.distance = self.enemy.cords.distance_to(self.player.cords)
        if self.distance > 1:
            try:
                self.percent = (10*(raycaster.DV/self.v_cords.y))/100
                self.image = pygame.transform.scale(self.image, (int(self.width*self.percent), int(self.height*self.percent)))
            except:
                self.image = pygame.transform.scale(self.image, (1, 1))

        if v_cords is not None:
            if v_cords.y > 0:
                if abs(v_cords.y) < 0.0001:
                    safe_y = 0.0001 if v_cords.y >= 0 else -0.0001
                else:
                    safe_y = v_cords.y

                center_x = WIDTH // 2 + v_cords.x * (raycaster.DV / safe_y)
                center_y = raycaster.middle_y + (self.ground * self.percent)
                center_x = max(-99999, min(99999, center_x))
                center_y = max(-99999, min(99999, center_y))

                self.rect = self.image.get_rect(center=(int(center_x), int(center_y + (self.player.up_direction))))
                temp_result = [item[0] for item in raycaster.result]
                try:
                    index = bisect.bisect_right(temp_result, v_cords.y)
                except:
                    print(temp_result, v_cords.y)
                raycaster.result.insert(index, (v_cords.y, False, self, None))