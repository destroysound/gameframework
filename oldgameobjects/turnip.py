
import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *


class turnip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.normalimage, self.rect = load_image('turnip.png', -1)
        self.flippedimage = pygame.transform.flip(self.normalimage, True, False)
        self.smushedimage, temp = load_image('smushedturnip.png', -1)
        self.image = self.normalimage
        self.move(x, y)
        self.tick = 0
        self.flipped = False
        self.facing = False
        self.yvel = 0
        self.alive = True
        self.moonwalking = False
    
    def scroll(self, scrollx, scrolly):
        self.move(self.rect.left+scrollx, self.rect.top+scrolly)

    def kill(self):
        self.image = self.smushedimage
        self.alive = False

    def resetyvel(self):
        self.yvel = 0

    def updateypos(self):
        self.yvel += 1
        if (self.yvel > 5):
            self.yvel = 5
        return self.move(self.rect.left, self.rect.top+self.yvel)

    def updatexpos(self):
        self.tick += 1
        if (self.tick > 5):
            if (self.flipped):
                self.flipped = False
                self.image = self.normalimage
            else:
                self.flipped = True
                self.image = self.flippedimage
            self.tick = 0
        if (self.facing):
            return self.move(self.rect.left+1, self.rect.top)
        else:
            return self.move(self.rect.left-1, self.rect.top)

    def move(self, x, y):
        oldx = self.rect.left
        oldy = self.rect.top
        self.rect.left = x
        self.rect.top = y
        return (oldx, oldy)
