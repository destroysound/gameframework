import os, pygame

from math import sqrt, degrees, atan2, sin, cos
from random import randint
from string import Template

from util import *

from pygame.locals import *

class particle():
    def __init__(self, x, y, xvel, yvel, size, age, lifespan, color, bitmap):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.size = size
        self.age = age
        self.lifespan = lifespan
        self.color = color
        if (bitmap):
            self.bitmapped = True
            self.image = pygame.image.load("./img/" + bitmap)
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
            self.image.set_alpha(randint(5, 10), RLEACCEL)
        else:
            self.bitmapped = False

    def update(self):
        self.x += self.xvel
        self.y += self.yvel
        self.age += 1

    def scroll(self, scrollx, scrolly):
        self.x += scrollx
        self.y += scrolly


class particleeffects(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = pygame.surface.Surface((320, 240))
        self.image.set_colorkey((255, 255, 255))
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect(0, 0, 320, 240)
        self.particles = []

    def varycolor(self, color, amount):
        colorvary = randint(0, 2)
        if (colorvary == 0):
            r = 0
            g = 0
            b = 0
        elif (colorvary == 1):
            r = 88
            g = 88
            b = 88
        else:
            r = 186
            g = 186
            b = 186
        return (r, g, b)


    def makeexplosion(self, originx, originy, color, rect, power):
        for i in range(randint(40, 50)):
            x = randint(rect.left, rect.left + rect.width)
            y = randint(rect.top, rect.top + rect.height)
            bitmap = False
            distancex = float(x - originx)
            if distancex == 0:
                distancex = 1.0
            distancey = float(y - originy)
            if distancey == 0:
                distancey = 1.0
            xvel = power/distancex
            yvel = power/distancey
            lifespan = randint(30, 50)
            size = randint(1, 2)
            color = self.varycolor(color, 100) 
            self.particles.append(particle(x, y, xvel, yvel, size, 0, lifespan, color, bitmap))

    def scroll(self, scrollx, scrolly):
        for i in self.particles:
            i.scroll(scrollx, scrolly)
            
    def update(self):
        self.image.fill((255, 255, 255))
        for i in self.particles:
            i.update()
            if (i.age > i.lifespan) or (i.x > 320) or (i.x < 0) or (i.y > 240) or (i.y < 0):
                self.particles.remove(i)
                del i
            else:
                if (i.bitmapped):
                   self.image.blit(i.image, (i.x, i.y))
                else:
                    pygame.draw.circle(self.image, i.color, (int(i.x), int(i.y)), int(i.size))
                             
