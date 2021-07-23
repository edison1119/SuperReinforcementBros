# import statement

import time
import pygame
from pygame.locals import *

pygame.init()

# screen setup
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('platformer')
# picture import
bluepic = pygame.image.load('Blue.bmp')
r=38
blue = pygame.transform.scale(bluepic, (r, r))

framerate=30
# classes
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #image
        self.image = blue

        #initial value & rect
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 150
        self.xvel = 0
        self.yvel = 0
        self.run = False
        self.g = r*67.82/ framerate**2
        self.jumph = r*17.36/framerate


        #movement state
        self.right = False
        self.left = False
        self.run= False
        self.jump = False
        self.ground = False
        self.onplatform = False
        self.jumphold = False
        self.jumptimer=0

        if self.rect.x > 1000:
            self.rect.x = -20

    def nextframe(self,c):
        """
        0: No movement
        1: jump
        2: squat / pipe
        3: left
        4: right
        5: right + jump
        6: right + sprint (fireball)
        7: 5 + 6
        """

    def pressbutton(self, event):
        if event.key == KMOD_CTRL:
            self.run = True
        if event.key == K_RIGHT or event.key == K_d:
            self.right = True

        if event.key == K_LEFT or event.key == K_a:
            self.left = True

        if event.key == K_w or event.key == K_UP:
            if self.jump == False:
                self.jump = True
                self.jumphold = True
                self.jumptimer=0
    def unpressbutton(self):
        if event.key == K_RIGHT or event.key == K_d:
            self.right = False
            self.run = False
        if event.key == K_LEFT or event.key == K_a:
            self.left = False
            self.run=False
        if event.key == K_w or event.key == K_UP:
            self.jumphold = False

    def update(self):
        # movement
        print(self.jump,self.yvel)
        if self.ground == True:
            self.g= r*55.88/ framerate**2
        self.jumptimer +=1
        if self.jumptimer ==5 and self.jump:
            if self.jumphold == True:
                self.yvel = r * -15.21/framerate
                self.g=r*34.79/ framerate**2
            else:
                self.yvel = r * -17.36/framerate
                self.g = r * 67.82 / framerate ** 2
        if self.right == True:
            if self.run == True:
                self.xvel=9.1*38/framerate
            else:
                self.xvel=3.7*38/framerate
        elif self.left == True:
            if self.run == True:
                self.xvel=-9.1*38/framerate
            else:
                self.xvel=-3.7*38/framerate
        else:
            self.xvel = 0
        # xvel process
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
            if self.jumptimer >5:
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
