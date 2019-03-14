
import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *


class tite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('stalagtite.png', -1)
        self.originaly = y
        self.move(x, y)
        self.tick = 0
        self.alive = True
        self.movingup = False
        self.movingdown = False
        self.movingtick = 0
    
    def scroll(self, scrollx, scrolly):
        self.originaly += scrolly
        self.move(self.rect.left+scrollx, self.rect.top+scrolly)

    def kill(self):
        self.alive = False

    def updatepos(self, player):
        if (((player.rect.top > self.rect.top and
            self.rect.right + 6 > player.rect.left and
            player.rect.right + 6 > self.rect.left)
            or self.movingdown) and not(self.movingup)):
            self.movingdown = True
            return self.move(self.rect.left, self.rect.top+3)
        elif (self.rect.top > self.originaly):
            self.movingdown = False
            self.movingup = True
            self.movingtick += 1
            if (self.movingtick > 2):
                self.movingtick = 0
                return self.move(self.rect.left, self.rect.top-1)
        else:
            self.movingup = False
        self.movingdown = False
        return (self.rect.left, self.rect.top)

    def move(self, x, y):
        oldx = self.rect.left
        oldy = self.rect.top
        self.rect.left = x
        self.rect.top = y
        return (oldx, oldy)
