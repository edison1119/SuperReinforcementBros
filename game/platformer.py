# import statement

import time
import pygame
from pygame.locals import *

pygame.init()

# screen setup
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('platformer')
# picture import
bluepic = pygame.image.load('blue.png')
blue = pygame.transform.scale(bluepic, (38, 38))

framerate=30
# classes
class Player(pygame.sprite.Sprite):
    # 初次召喚角色時必定執行的部分
    def __init__(self):
        # 召喚角色時一起設定好sprite的屬性
        pygame.sprite.Sprite.__init__(self)
        # 屬性image
        self.image = blue
        # 屬性rect 最最最重要就這個啦~~~~~
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 150
        self.xvel = 0
        self.yvel = 0
        self.g = 38*67.82/ framerate**2
        self.jumph = 38*17.36/framerate
        self.right = False
        self.left = False
        self.wasright = False
        self.wasleft = False
        self.jump = False
        self.ground = False
        self.onplatform = False
        self.jumphold = False
        if self.rect.x > 1000:
            self.rect.x = -20

    def pressbutton(self, event):
        if event.key == K_RIGHT or event.key == K_d:
            self.right = True
        if event.key == K_LEFT or event.key == K_a:
            self.left = True
        if event.key == K_w or event.key == K_UP:
            if self.jump == False:
                self.jump = True
                self.yvel = -self.jumph
                self.jumphold = True

    def unpressbutton(self):
        if event.key == K_RIGHT or event.key == K_d:
            self.right = False
        if event.key == K_LEFT or event.key == K_a:
            self.left = False
        if event.key == K_w or event.key == K_UP:
            self.jumphold = False

    def update(self):
        # speed up
        if self.right == True:
            if self.xvel < 10:
                if self.xvel < 0:
                    self.xvel = self.xvel + 1.2
                else:
                    self.xvel = self.xvel + 0.6
        if self.left == True:
            if self.xvel > -10:
                if self.xvel > 0:
                    self.xvel = self.xvel - 1.2
                else:
                    self.xvel = self.xvel - 0.6
        # xvel process
        if -0.3 < self.xvel < 0.3:
            self.xvel = 0
        elif self.xvel > 0.3:
            self.xvel = self.xvel - 0.3
        elif self.xvel < -0.3:
            self.xvel = self.xvel + 0.3
        self.rect.x = self.rect.x + self.xvel

        # yvel process
        self.rect.y = self.rect.y + self.yvel
        if self.ground == False:
            self.yvel = self.yvel + self.g
            # if over adding
            # if self.yvel >30:
            #    self.yvel = 30
        # grounding detecting
        if self.rect.y > 500 or self.onplatform == True:
            self.rect.y = 500
            self.ground = True
            self.yvel = 0
            self.jump = False
        elif self.rect.y < 500 and self.onplatform == False:
            self.ground = False

        if self.rect.x > 1020:
            self.rect.x = -20
        if self.rect.x < -20:
            self.rect.x = 1020

        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.flip()


player = Player()
run = True
Clock = pygame.time.Clock()
while run:
    Clock.tick(framerate)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            player.pressbutton(event)
        if event.type == KEYUP:
            player.unpressbutton()
        if event.type == QUIT:
            running = False
            pygame.quit()
            exit()
    screen.fill((0, 0, 0))
    player.update()
