
import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *


class decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(filename, -1)
        self.move(x, y)
    
    def scroll(self, scrollx, scrolly):
        self.move(self.rect.left+scrollx, self.rect.top+scrolly)

    def move(self, x, y):
        self.rect.left = x
        self.rect.top = y
