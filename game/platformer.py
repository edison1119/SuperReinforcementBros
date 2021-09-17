#  created at 2021 17

# import statement

import time
import pygame
from pygame.locals import *

pygame.init()

# screen setup
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('platformer')
# picture import
bluepic = pygame.image.load('blue.bmp')
brickpic = pygame.image.load('brick.bmp')
r = 38
brickpic = pygame.transform.scale(brickpic, (r, r))
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
        self.onplatform = False
        self.jumphold = False
        self.jumptimer = 0
        self.runtimer = 0
        self.stop = True
        self.jumpable = True
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
            self.stop = False
        if event.key == K_RIGHT or event.key == K_d:
            self.right = True
            self.stop = False
        if event.key == K_LEFT or event.key == K_a:
            self.left = True
            self.stop = False
        if event.key == K_w or event.key == K_UP:
            if not self.jump and self.jumpable:
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
        print('onplat:', self.onplatform, 'jable:', self.jumpable, 'Jtimer:', self.jumptimer)
        if not self.right and not self.left:
            self.stop = True
        if self.stop:
            self.runtimer += 1
        else:
            self.runtimer = 0
        if self.runtimer >= 5:
            self.run = False

        self.jumptimer += 1

        #gravity check
        if self.jumptimer == 5 and self.jump:
            if self.jumphold:
                self.yvel = r * -15.21 / framerate
                self.g = r * 34.79 / framerate ** 2
            else:
                self.yvel = r * -17.36 / framerate
                self.g = r * 67.82 / framerate ** 2
            self.jump = False

        # directional movement, running
        if self.right:
            if self.run:
                self.xvel = 9.1 * r / framerate
            else:
                self.xvel = 3.7 * r / framerate
        elif self.left:
            if self.run:
                self.xvel = -9.1 * r / framerate
            else:
                self.xvel = -3.7 * r / framerate
        else:
            self.xvel = 0
        # xvel process
        self.rect.x = self.rect.x + self.xvel
        # yvel process
        print('yvel', self.yvel)
        self.rect.y = self.rect.y + self.yvel

        # ground detecting
        for brick in brickgroup:
            relx = brick.rect.x-self.rect.x
            rely = brick.rect.y-self.rect.y
            if not self.onplatform and self.yvel > 0 and abs(rely - r) <= self.yvel + .01 and abs(relx) <= r:
                self.rect.y = brick.rect.y - r - 0.001
                self.onplatform = True
                self.yvel = 0
                self.jumpable = True

        # for brick in brickgroup:
        #    if self.onplatform== False and self.ground == False and self.yvel > 0 and abs(brick.rect.y -self.rect.y-r)<=self.yvel and abs(brick.rect.x - self.rect.x)<= r :
        #        self.rect.y = brick.rect.y-r
        #        self.onplatform = True
        #        self.ground = True
        #        self.yvel = 0
        #        print('a')
        #        break
        if self.rect.y > 500:
            self.rect.y = 500
            self.jumpable = True
            self.onplatform = True
            self.yvel = 0
        elif self.rect.y < 500 and not self.onplatform:
            self.jumpable = False

        if not self.onplatform:
            self.yvel = self.yvel + self.g
            # if over adding
            # if self.yvel >30:
            #    self.yvel = 30
        else:
            self.g = r * 55.88 / framerate ** 2
        if self.rect.x > 1020:
            self.rect.x = -20
        elif self.rect.x < -20:
            self.rect.x = 1020

        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.onplatform = False


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


class Brick(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def update(self):
        super(Brick, self).update()


brickgroup = pygame.sprite.Group()
brick = Brick(400, 400, brickpic)
brickgroup.add(brick)
player = Player()
run = True
Clock = pygame.time.Clock()
while run:
    Clock.tick(framerate)
    print(Clock.get_fps())
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
    brickgroup.update()
    player.update()
    pygame.display.update()
