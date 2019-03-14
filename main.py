import os, pygame, sys

from pgu import engine

from math import sqrt
from random import randint
import pygame.mixer

from titlescreen import *
from editscreen import *

from pygame.locals import *

def main():
    pygame.mixer.pre_init(44100,-16,2, 1024 * 3)
    mixer = pygame.mixer
    mixer.init(44100)
    mixer.set_num_channels(10)
#    mixer.music.load(os.path.join('./choons/', 'ethergrind.xm'))
#    mixer.music.play(-1)
    sounds = [None] * 15
    sounds[0] = mixer.Sound(os.path.join('./sounds/', 'logo.wav'))
    sounds[1] = mixer.Sound(os.path.join('./sounds/', 'break.wav'))
    sounds[2] = mixer.Sound(os.path.join('./sounds/', 'golds.wav'))
    sounds[3] = mixer.Sound(os.path.join('./sounds/', 'hitground.wav'))
    sounds[4] = mixer.Sound(os.path.join('./sounds/', 'jump.wav'))
    sounds[5] = mixer.Sound(os.path.join('./sounds/', 'pickup.wav'))
    sounds[6] = mixer.Sound(os.path.join('./sounds/', 'throw.wav'))
    sounds[7] = mixer.Sound(os.path.join('./sounds/', 'tite.wav'))
    sounds[8] = mixer.Sound(os.path.join('./sounds/', 'smush.wav'))
    sounds[9] = mixer.Sound(os.path.join('./sounds/', 'cryingoutloud.wav'))
    sounds[10] = mixer.Sound(os.path.join('./sounds/', 'cartblow.wav'))
    sounds[11] = mixer.Sound(os.path.join('./sounds/', 'turnon.wav'))
    screen = pygame.display.set_mode((640, 480))
#    pygame.display.set_caption("::ethergrind::")
    pygame.mouse.set_visible(False);
    pygame.font.init()
    game = engine.Game()
    flags = 0
    nextfile = False
    editor = False
    filename = ""
    for arg in sys.argv:
        if (nextfile):
            filename = arg
            nextfile = False
            editor = True
        elif (arg == "-f"):
            flags = pygame.fullscreen
        elif (arg == "-e"):
            nextfile = True
    if (editor):
        pygame.display.set_caption("xml level editor")
        game.run(editscreen(game, sounds, mixer, filename), screen)
    else:
        pygame.display.set_caption("Super Bean Kid")
        game.run(titlescreen(game, sounds, mixer), screen)

if __name__ == '__main__': main()
