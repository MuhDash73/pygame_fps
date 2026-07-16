import pygame
from settings import *
from debug import debug
from player import Player
from enemy import *
from support import *
from tile import Tile
from raycaster import Raycaster
from bullet import Bullet
from other_visible_sprites import *

class Game():
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.state = "start_menu"
        self.win = None
        
        self.visible_sprites_start = pygame.sprite.Group()
        StartMenu("Assets/Title screens/StartMenu.png", self.visible_sprites_start)

        self.player = Player()
        self.other_updatable_sprites = pygame.sprite.Group()
        self.entity_sprites = pygame.sprite.Group()
        self.visible_sprites_playing = pygame.sprite.Group()
        self.visible_sprites_playing_test = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.raycastables = []
        self.create_map()
        self.create_other_visible_sprites()

        self.visible_sprites_end = pygame.sprite.Group()
    
    def create_other_visible_sprites(self):
        temp_imag = pygame.surface.Surface((20,20))
        temp_imag_center = 9
        pygame.draw.line(temp_imag, (255, 255, 255), (0,temp_imag_center), (20,temp_imag_center), 2)
        pygame.draw.line(temp_imag, (255, 255, 255), (temp_imag_center,0), (temp_imag_center,20), 2)
        temp_imag.set_colorkey((0, 0, 0))
        self.crosshair = Crosshair(temp_imag, CENTER[0], CENTER[1], [self.visible_sprites_playing])

    def create_map(self):
        layouts = {
            "map" : import_csv_layout("Assets/map/map.csv")
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                temp_list = []
                for col_index, col in enumerate(row):
                    if col != "-1" or style == "map":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "map":
                            if col == "0":
                                self.tile = Tile((x,y),[self.obstacle_sprites, self.visible_sprites_playing_test])
                                self.obstacle_sprites.add(self.tile)
                                temp_list.append(1)
                                #print("added tile")
                            elif col == "1":
                                self.player.start(x, y, self.obstacle_sprites, [self.visible_sprites_playing_test], self.raycastables, self.entity_sprites)
                                self.raycaster = Raycaster(self.player, self.raycastables)
                                self.healthbar = HealthBar(self.player, [self.visible_sprites_playing])
                                temp_list.append(0)
                                #print("added player")
                            elif col == "3":
                                for i in range(5):
                                    self.latest_enemy = Enemy(x + i*5, y, self.obstacle_sprites, self.player, [self.visible_sprites_playing_test, self.other_updatable_sprites, self.entity_sprites, self.enemies])
                                    self.seenenemy = SeenEnemy(self.latest_enemy, [self.other_updatable_sprites], self.player)
                                    self.latest_enemy.add_seenenemy(self.seenenemy)
                                temp_list.append(0)
                            elif col == "-1":
                                temp_list.append(0)
                #print(temp_list)
                self.raycastables.append(temp_list)
        #print(self.raycastables)


    def scale(self):
        self.display = pygame.display.get_surface()
        self.scaled_surface = pygame.transform.scale(self.surface, self.display.get_size())
        self.display.blit(self.scaled_surface, (0, 0))


    def run(self, dx, dy):
        self.surface.fill("#000000")
        keys = pygame.key.get_pressed()
        if self.state == "start_menu":
            self.visible_sprites_start.draw(self.surface)
            if keys[pygame.K_SPACE]:
                self.state = "playing"

        elif self.state == "playing":
            self.player.update(dx, dy)
            self.other_updatable_sprites.update(self.raycaster)
            self.raycaster.draw_rays(self.surface)
            self.visible_sprites_playing.draw(self.surface)
            self.raycaster.raycast()
            #self.visible_sprites_playing_test.draw(self.surface)
            if self.enemies.sprites() == []:
                self.state = "end_screen"
                EndScreen("Assets/Title screens/WinScreen.png", self.visible_sprites_end)
            if self.player.hp <= 0:
                self.state = "end_screen"
                EndScreen("Assets/Title screens/LoseScreen.png", self.visible_sprites_end)

        elif self.state == "end_screen":
            self.visible_sprites_end.draw(self.surface)

        self.scale()