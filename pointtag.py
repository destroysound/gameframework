import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *

class pointtag(pygame.sprite.Sprite):
    def __init__(self, x, y, tagname, imagefile, font, attributes, fontshown):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        fontsurf = font.render(tagname, False, (255,255,255)) 
        fontsurf.set_colorkey((0, 0, 0), RLEACCEL)
        itemimage, temp = load_image(imagefile, -1)
        if (fontsurf.get_width() > itemimage.get_width()):
            width = fontsurf.get_width()
        else:
            width = itemimage.get_width()
        self.image = pygame.Surface((itemimage.get_width(), fontsurf.get_height()+itemimage.get_height()))
        self.image.fill((248, 248, 248))
        self.image.set_colorkey((248, 248, 248), RLEACCEL)
        self.rect = pygame.Rect((0,0,itemimage.get_width(),itemimage.get_height()))
        self.image.blit(itemimage, (0,0))
        self.image.blit(fontsurf, (0,itemimage.get_height()))
        self.itemimage = itemimage
        self.fontsurf = fontsurf
        self.fontshown = True
        if (not(fontshown)):
            self.togglefont()
        self.move(x, y)
        self.attributes = attributes
        self.tagname = tagname
    
    def togglefont(self):
        self.image.fill((248, 248, 248))
        if (self.fontshown):
            self.fontshown = False
            self.image.blit(self.itemimage, (0,0))
        else:
            self.fontshown = True
            self.image.blit(self.itemimage, (0,0))
            self.image.blit(self.fontsurf, (0,self.itemimage.get_height()))

    def move(self, x, y):
        self.rect.left = x
        self.rect.top = y
    
    def scroll(self, x, y):
        self.move(self.rect.left+x, self.rect.top+y)

