import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *

class regiontag(pygame.sprite.Sprite):
    def __init__(self, regionrect, tagname, imagefile, font, attributes, fontshown):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        fontsurf = font.render(tagname, False, (255,255,255)) 
        width = regionrect.width
        height = regionrect.height
        if (width < 0):
            x = regionrect.left + width
        else:
            x = regionrect.left
        if (height < 0):
            y = regionrect.top + height
        else:   
            y = regionrect.top
        self.image = pygame.Surface((abs(width), abs(height)))
        self.rect = pygame.Rect((0,0,abs(width),abs(height)))
        itemimage, temp = load_image(imagefile)
        for j in range(0, int(self.rect.height/16)+1):
            for i in range(0, int(self.rect.width/16)+1):
                self.image.blit(itemimage,(i*16, j*16)) 
        self.image.blit(fontsurf, (0,0))
        self.itemimage = itemimage
        self.fontsurf = fontsurf
        self.fontshown = True
        if (not(fontshown)):
            self.togglefont()
        self.move(x, y)
        self.attributes = attributes
        self.tagname = tagname

    def togglefont(self):
        if (self.fontshown):
            self.fontshown = False
            for j in range(0, int(self.rect.height/16)+1):
                for i in range(0, int(self.rect.width/16)+1):
                    self.image.blit(self.itemimage,(i*16, j*16)) 
        else:
            self.fontshown = True
            for j in range(0, int(self.rect.height/16)+1):
                for i in range(0, int(self.rect.width/16)+1):
                    self.image.blit(self.itemimage,(i*16, j*16)) 
            self.image.blit(self.fontsurf, (0,0))


    def scroll(self, x, y):
        self.move(self.rect.left+x, self.rect.top+y)

    def move(self, x, y):
        self.rect.left = x
        self.rect.top = y

