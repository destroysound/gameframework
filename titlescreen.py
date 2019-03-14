import os, pygame

from math import sqrt
from random import randint
from string import Template

from util import *
from pygame.locals import * 
from playscreen import *
import pygame.mixer

from pgu import engine, gui, text

##A state may subclass engine.State.
##::
class titlescreen(engine.State):
    ##
    ##The init method should load data, etc.  The __init__ method
    ##should do nothing but record the parameters.  If the init method
    ##returns a value, it becomes the new state.
    ##::
    def __init__(self, game, sounds, mixer):
        self.sounds = sounds
        self.mixer = mixer
        engine.State.__init__(self, game)
    def init(self):
        #if not(self.mixer.music.get_busy()):
            #self.mixer.music.load(os.path.join('./jams/', 'liquid.xm'))
            #self.mixer.music.play(-1)
        self.font = pygame.font.Font("./fonts/MMMM8.TTF", 16)
        self.accumulator = zeros((320, 240, 3))
        self.screensurf = pygame.Surface((320, 240)) 
        self.title, temp = load_image("title.png")
        self.timer = timer.Timer(45)

    ##Theopaint method is called once.  If you call repaint(), it
    ##will be called again.
    ##::
    def paint(self,s): 
        pygame.display.flip()
    ##
    ##Every time an event occurs, event is called.  If the event method
    ##returns a value, it will become the new state.
    ##::
    def event(self,e):
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                return engine.Quit(self.game)
            if e.key == K_SPACE or e.key == K_RETURN:
                return playscreen(self.game, self.sounds, self.mixer, 1, 0)
    ##
    ##Loop is called once a frame.  It should contain all the
    ##logic.  If the loop method returns a value it will become the
    ##new state.
    ##::
    def loop(self):
        self.timer.tick()
    ##
    ##Update is called once a frame.  It should update the display.
    ##::
    def update(self,screen):
        self.screensurf.fill((255, 255, 255))
        self.screensurf.blit(self.title, (160-self.title.get_width()/2,8))
        self.drawmenutext(self.screensurf, (95, 150), (88, 88, 88), "Irrationally exuberant happy funtime game!")
        self.drawmenutext(self.screensurf, (95, 165), (88, 88, 88), "Jump About! X! Or (Space)!")
        self.drawmenutext(self.screensurf, (140, 180), (88, 88, 88), "Throw Radishes! Z! Or (Left Alt)!")
        self.drawmenutext(self.screensurf, (110, 195), (88, 88, 88), "Collect Gold!")
        self.drawmenutext(self.screensurf, (125, 210), (88, 88, 88), "Avoid Baddies!")
        self.drawmenutext(self.screensurf, (80, 225), (88, 88, 88), "Press Spacebar To Begin!!")
        pygame.transform.scale(self.screensurf, (640, 480), screen)
        pygame.display.flip() #better to do updates
    ##
    def drawmenutext(self, screen, position, color, string):
        x, y = position
        rendered = self.font.render(string, False, color)
        screen.blit(rendered, (161-rendered.get_width()/2, y+1))
        screen.blit(self.font.render(string, False, (0,0,0)),(160-rendered.get_width()/2, y))

