
import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *


class radish(pygame.sprite.Sprite):
    def __init__(self, x, y, facing, playervel):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.loadedimage = []
        self.imagerect = []
        for i in range(4):
            tempimage, temprect = load_image('radish.png', -1)
            tempimage = pygame.transform.rotate(tempimage, i*90)
            self.loadedimage.append(tempimage)
            self.imagerect.append(temprect)
        self.rect = pygame.Rect(0, 0, 8, 8)
        self.tosscount = 0
        self.facing = facing
        self.yvelocity = 10
        self.loadimage(0)
        if (not(self.facing)):
            self.velocity = 2
        else:
            self.velocity = -2
        self.velocity += playervel
        self.move(x, y)
        self.flying = True

    def land(self):
        self.flying = False

    def stop(self):
       self.velocity = 0
       self.yvelocity = 0 

    def updatepos(self):
        self.yvelocity -= 1
        if (self.yvelocity < -5):
            self.yvelocity = -5
        return self.move(self.rect.left+self.velocity, self.rect.top-self.yvelocity)
    
    def scroll(self, scrollx, scrolly):
        self.move(self.rect.left+scrollx, self.rect.top+scrolly)

    def move(self, x, y):
        oldx = self.rect.left
        oldy = self.rect.top
        self.rect.left = x
        self.rect.top = y
        return oldx, oldy

    def loadimage(self, imagenumber):
        self.image = self.loadedimage[imagenumber]
        self.currimage = imagenumber
