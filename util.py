import os, pygame

from math import sqrt
from string import Template

from pygame.locals import *
import pygame.surfarray

POINT_NODES = ["player", "brick", "turnip", "stalagtite", "stalagmite",
               "spikes", "unbreakable", "revspikes", "radish", "golds"]

REGION_NODES = ["brickarea"]

IMAGE_FILES = {
               "player" : "beankid1.png",
               "brick" : "brick.png",
               "brickarea": "unbreakable.png",
               "turnip" : "turnip.png",
               "stalagtite" : "stalagtite.png",
               "stalagmite" : "stalagmites.png",
               "spikes" : "spikes.png",
               "revspikes" : "spikes.png",
               "unbreakable" : "unbreakable.png",
               "radish" : "radish.png",
               "golds" : "golds.png",
              }


def colorize(pic, color):
    picarray  = pygame.surfarray.array3d(pic)
    for i in range(len(picarray)):
       for j in range(len(picarray[i])):
            for k in range(3):
                if (picarray[i][j][k] != 0 and picarray[i][j][k] != 255):
                    num = picarray[i][j][k] + color[k]
                    if num < 0:
                        num = 0
                    elif num >  255:
                        num = 255
                    picarray[i][j][k] = num
    return pygame.surfarray.make_surface(picarray)

def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    
    pygame.display.quit()
    pygame.display.init()
    
    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)

    pygame.mouse.set_visible(0) 
    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
    
    return screen

def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname)
    except message:
        print('Cannot load image:', fullname)
        raise(SystemExit, message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

