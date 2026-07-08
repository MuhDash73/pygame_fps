import pygame
from settings import *
from debug import debug
from game import Game
import os


class Main():
    def __init__(self):

        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.width, self.height = pygame.display.get_window_size()
        pygame.display.set_caption("game")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.fullscreen = False
        self.mouse_locked = False

        self.FPS_list = []
        self.FPS = FPS
        #print("FPS:", self.FPS)a
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mouse_locked = True
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    self.centre = pygame.display.get_window_size()[0]//2, pygame.display.get_window_size()[1]//2
                    pygame.mouse.set_pos(self.centre)
                    pygame.mouse.get_rel()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                  self.mouse_locked = False
                  pygame.mouse.set_visible(True)
                  pygame.event.set_grab(False)


                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                        os.environ['SDL_VIDEO_CENTERED'] = '1'
                    else:
                        os.environ['SDL_VIDEO_CENTERED'] = '1'
                        self.width, self.height = pygame.display.get_window_size()
                        self.screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0], pygame.RESIZABLE)
                    self.fullscreen = not self.fullscreen
                    self.game.display = pygame.display.get_surface()

            if self.mouse_locked:
                self.centre = pygame.display.get_window_size()[0]//2, pygame.display.get_window_size()[1]//2
                dx, dy = pygame.mouse.get_rel()
                pygame.mouse.set_pos(self.centre)
            else:
                dx, dy = (0,0)

            self.game.run(dx, dy)
            '''
            try:

                debug((
                    int(self.clock.get_fps()),
                    self.game.raycaster.FOV,
                    self.game.player.direction
                    #self.game.seenenemy.v_cords,
                    #self.game.seenenemy.enemy.v_cords_1,
                    #self.game.seenenemy.enemy.cords.distance_to(self.game.player.cords)
                    ))
                    
            except Exception as e:
                debug(e)
            pygame.display.update()
            #print(self.clock.get_fps())
            self.clock.tick(self.FPS)

            '''
            if self.clock.get_fps() > 30:
                self.FPS_list.append(self.clock.get_fps())
            try:
                print("average FPS:", sum(self.FPS_list) / len(self.FPS_list))
            except:
                pass
            '''



if __name__ == "__main__":
    main = Main()
    main.run()


'''
make bulklet go up or down
6, 300
6 pixels up = 300 pixels away
300/6 = 50
150 pixels away = 12 pixels up
75 = 24
div by 0
[0.944089, 0.329691]
'''