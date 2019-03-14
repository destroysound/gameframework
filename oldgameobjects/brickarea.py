
import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *


class brickarea(pygame.sprite.Sprite):
    def __init__(self, x, y, rect):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.brickimage, temp = load_image('unbreakable.png')
        self.rect = rect
        self.breakable = False
        self.image = pygame.Surface((rect.width, rect.height))
        for j in range(0, int(rect.height/16)+1):
            for i in range(0, int(rect.width/16)+1):
                self.image.blit(self.brickimage,(i*16, j*16)) 
        self.move(x, y)
    
    def scroll(self, scrollx, scrolly):
        self.move(self.rect.left+scrollx, self.rect.top+scrolly)

    def move(self, x, y):
        self.rect.left = x
        self.rect.top = y
