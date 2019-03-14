
import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *


class spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('spikes.png', -1)
        if (flipped):
            self.image = pygame.transform.flip(self.image, True, True)
        self.move(x, y)
    
    def scroll(self, scrollx, scrolly):
        self.move(self.rect.left+scrollx, self.rect.top+scrolly)

    def move(self, x, y):
        self.rect.left = x
        self.rect.top = y
