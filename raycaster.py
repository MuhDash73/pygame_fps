import pygame
from settings import *
from debug import debug
from math import *
import bisect

class Raycaster(pygame.sprite.Sprite):
    def __init__(self, player, raycastables):
        super().__init__()
        self.player = player
        self.raycastables = raycastables
        self.result = []
        self.FOV = 90
        self.min_fov = 30
        self.max_fov = 120
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.middle_y = HEIGHT//2
        self.res = 1
        self.DV = (WIDTH/2)/tan(radians(self.FOV/2))

    def raycast(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.FOV -= 1
        elif keys[pygame.K_DOWN]:
            self.FOV += 1
        
        self.FOV = max(self.min_fov, min(self.max_fov, self.FOV))
        self.DV = (WIDTH/2)/tan(radians(self.FOV/2))
        self.result = []
        player_angle = self.player.direction.angle_to(pygame.math.Vector2(-1, 0))
        map_height = len(self.raycastables)
        map_width = len(self.raycastables[0])
        pos_x, pos_y = self.player.cords
        temp_x = (self.res/2)+(WIDTH/2)
        range_amount = int(WIDTH//self.res)

        for ray in range(range_amount):
            radian_offset = atan(temp_x / self.DV)
            deg_offset = degrees(radian_offset)
            ray_dir = self.player.direction.rotate(-deg_offset)
            dir_x, dir_y = ray_dir.x, ray_dir.y
            map_x = int(pos_x // TILESIZE)
            map_y = int(pos_y // TILESIZE)
            delta_dist_x = abs(1 / dir_x) if dir_x != 0 else 1e30
            delta_dist_y = abs(1 / dir_y) if dir_y != 0 else 1e30

            if dir_x < 0:
                step_x = -1
                side_dist_x = (pos_x / TILESIZE - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - pos_x / TILESIZE) * delta_dist_x
            if dir_y < 0:
                step_y = -1
                side_dist_y = (pos_y / TILESIZE - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1.0 - pos_y / TILESIZE) * delta_dist_y
            hit = False
            side = 0

            while not hit:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1
                if map_x < 0 or map_x >= map_width or map_y < 0 or map_y >= map_height:
                    break
                if self.raycastables[map_y][map_x] == 1:
                    hit = True

            if hit:
                if side == 0:
                    perp_wall_dist = (map_x - pos_x / TILESIZE + (1 - step_x) / 2) / dir_x
                else:
                    perp_wall_dist = (map_y - pos_y / TILESIZE + (1 - step_y) / 2) / dir_y
                ray_length = perp_wall_dist * TILESIZE
                ray_length *= abs(cos(radian_offset))
                index = bisect.bisect_right(self.result, (ray_length, side, ray))
                self.result.insert(index, (ray_length, True, side, ray))
            else:
                self.result.insert(0, (self.middle_y, True, 0, ray))
            #if deg_offset == 0.07161968708944808:
                #print(ray_length)
            #print("deg", deg_offset)

            temp_x -= self.res


    def draw_rays(self, surface):
        slice_width = self.res 

        self.result = reversed(self.result)
        
        for ray_info in self.result:
            ray_length, is__ray, side, index = ray_info
            if is__ray:
                if ray_length >= 1e30:
                    continue
                if ray_length <= 0:
                    ray_length = 1e-6
                wall_height = int((self.DV*10) / ray_length)
                if wall_height > HEIGHT * 2:
                    wall_height = HEIGHT * 2
                y_start = self.middle_y - (wall_height // 2)
                y_start += self.player.up_direction
                x_pos = index * slice_width
                if side == 0:
                    pygame.draw.rect(surface, (20, 40, 100), (int(x_pos), int(y_start), int(slice_width) + 1, int(wall_height)))
                elif side == 1:
                    try:
                        pygame.draw.rect(surface, (40, 70, 170), (int(x_pos), int(y_start), int(slice_width) + 1, int(wall_height)))
                    except:
                        print("Error drawing rect:", x_pos, y_start, slice_width, wall_height)
            else:
                '''
                ray_length is distance to entity
                side is the sprite class
                index is None
                '''
                
                surface.blit(side.image, side.rect)