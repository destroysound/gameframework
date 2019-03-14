
import os, pygame

from math import sqrt
from random import randint
from string import Template
from math import degrees, sqrt, sin, cos, atan2

from util import *

from pygame.locals import *

NUMBEANS = 8

class player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.loadedimage = []
        self.imagerect = []
        for i in range(NUMBEANS):
            temp = Template('beankid' + '$number' + '.png')
            tempimage, temprect = load_image(temp.substitute(number=i+1), -1)
            self.loadedimage.append(tempimage)
            self.imagerect.append(temprect)
        self.mirrorsprites()
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.holding = False
        self.facing = 0
        self.loadimage(0)
        self.idlecount = 0
        self.idleframe = 0
        self.movecount = 0
        self.moveframe = 0
        self.jumpvelocity = 0
        self.jumping = 0
        self.jumpcounter = 0
        self.velocity = 0
        self.move(x, y)
        self.velocityaccum = 0;
        self.alive = True

    def kill(self):
        self.alive = False
        self.loadimage(3)

    def runleft(self):
        if (self.jumping):
            self.velocity -= 1
        else:
            self.velocity -= .2
        if (self.velocity < -3):
            self.velocity = -3
        if (self.facing==0):
            self.facing = 1
            self.loadimage(self.moveframe)
        self.movecount += 1
        if (self.movecount > 3):
            if (self.moveframe):
                self.moveframe = 0
            else:
                self.moveframe = 1
            self.loadimage(self.moveframe)
            self.movecount = 0
    
    def runright(self):
        if (self.jumping):
            self.velocity += 1
        else:
            self.velocity += .2
        if (self.velocity > 3):
            self.velocity = 3
        if (self.facing==1):
            self.facing = 0
            self.loadimage(self.moveframe)
        self.movecount += 1
        if (self.movecount > 3):
            if (self.moveframe):
                self.moveframe = 0
            else:
                self.moveframe = 1
            self.loadimage(self.moveframe)
            self.movecount = 0

    def idle(self):
        if (self.velocity >= .3):
            self.velocity -= .3
        elif (self.velocity <= -.3):
            self.velocity += .3
        else:
            self.velocity = 0
        self.loadimage(0)
        self.moveframe = 0

    def jump(self):
        if (not(self.jumping)):
            self.jumping=True
            self.jumpcounter = 0
        if (self.jumpvelocity >= 0 and self.jumpcounter < 20):
            self.jumpvelocity += 5.0
            if (self.jumpvelocity > 5.0):
                self.jumpvelocity = 5.0

    def updatepos(self):
        self.velocityaccum += self.velocity
        if (self.velocityaccum > 1):
            self.velocityaccum -= self.velocity
            return self.move(self.rect.left+int(self.velocity), self.rect.top)
        elif (self.velocityaccum < 1):
            self.velocityaccum -= self.velocity
            return self.move(self.rect.left+int(self.velocity), self.rect.top)
        return (0, 0, self.rect.left, self.rect.top)

    def updateypos(self):
        self.jumpvelocity = self.jumpvelocity - 1
        if (self.jumpvelocity < -5.0):
            self.jumpvelocity = -5.0
        if (self.jumping):
            self.loadimage(2)
            self.jumpcounter += 1
        return self.move(self.rect.left, self.rect.top-self.jumpvelocity)

    def removeyvel(self):
        self.jumpvelocity = 0

    def stopjumping(self):
        self.jumping=False
        self.jumpcounter = 0
        self.jumpvelocity = 0

    def move(self, x, y):
        scrollx = 0
        scrolly = 0
        if (self.alive):
            if (x > 220):
                scrollx = 220-x
                x = 220
            elif (x < 100):
                scrollx = 100-x
                x=100
            if (y > 140):
                scrolly = 140-y
                y = 140
            elif (y < 100):
                scrolly = 100-y
                y=100
        oldx = self.rect.left
        oldy = self.rect.top
        self.rect.left = x
        self.rect.top = y
        return (scrollx, scrolly, oldx, oldy)

    def mirrorsprites(self):
        for i in range(NUMBEANS):
            tempimage = pygame.transform.flip(self.loadedimage[i], True, False)
            self.loadedimage.append(tempimage)
            
    def loadimage(self, imagenumber):
        if (self.holding and imagenumber != 4):
            imagenumber = imagenumber + 4
        self.image = self.loadedimage[imagenumber+NUMBEANS*self.facing]
        self.currimage = imagenumber
