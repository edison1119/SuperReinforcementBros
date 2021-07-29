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
r = 38
blue = pygame.transform.scale(bluepic, (r, r))

framerate = 30


# classes
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # image
        self.image = blue

        # initial value & rect
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 150
        self.xvel = 0
        self.yvel = 0
        self.run = False
        self.g = r * 67.82 / framerate ** 2
        self.jumph = r * 17.36 / framerate

        # movement state
        self.right = False
        self.left = False
        self.run = False
        self.jump = False
        self.ground = False
        self.onplatform = False
        self.jumphold = False
        self.jumptimer = 0
        self.runtimer = 0
        self.stop = True
        if self.rect.x > 1000:
            self.rect.x = -20

    def nextframe(self, c):
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
        if event.key == K_e and (self.right or self.left):
            self.run = True
            self.stop=False
        if event.key == K_RIGHT or event.key == K_d:
            self.right = True
            self.stop = False
        if event.key == K_LEFT or event.key == K_a:
            self.left = True
            self.stop = False
        if event.key == K_w or event.key == K_UP:
            if not self.jump:
                self.jump = True
                self.jumphold = True
                self.jumptimer = 0

    def unpressbutton(self, event):
        if event.key == K_RIGHT or event.key == K_d:
            self.right = False

        if event.key == K_LEFT or event.key == K_a:
            self.left = False

        if event.key == K_w or event.key == K_UP:
            self.jumphold = False

    def update(self):
        # movement
        print(self.run, self.runtimer)
        if not self.right and not self.left:
            self.stop = True
        if self.stop:
            self.runtimer += 1
        else:
            self.runtimer = 0
        if self.runtimer >= 5:
            self.run = False
        if self.ground:
            self.g = r * 55.88 / framerate ** 2
        self.jumptimer += 1
        if self.jumptimer == 5 and self.jump:
            if self.jumphold:
                self.yvel = r * -15.21 / framerate
                self.g = r * 34.79 / framerate ** 2
            else:
                self.yvel = r * -17.36 / framerate
                self.g = r * 67.82 / framerate ** 2
        if self.right:
            if self.run:
                self.xvel = 9.1 * 38 / framerate
            else:
                self.xvel = 3.7 * 38 / framerate
        elif self.left:
            if self.run:
                self.xvel = -9.1 * 38 / framerate
            else:
                self.xvel = -3.7 * 38 / framerate
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
            if self.jumptimer > 5:
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


class Object(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        # image
        self.image = image

        # initial value & rect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
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
            player.unpressbutton(event)
        if event.type == QUIT:
            running = False
            pygame.quit()
            exit()
    screen.fill((0, 0, 0))
    player.update()
