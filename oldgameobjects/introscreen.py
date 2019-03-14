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
class introscreen(engine.State):
    ##
    ##The init method should load data, etc.  The __init__ method
    ##should do nothing but record the parameters.  If the init method
    ##returns a value, it becomes the new state.
    ##::
    def __init__(self, game, sounds, mixer, begin):
        self.sounds = sounds
        self.mixer = mixer
        self.begin = begin
        engine.State.__init__(self, game)
    def init(self):
        #if not(self.mixer.music.get_busy()):
            #self.mixer.music.load(os.path.join('./jams/', 'liquid.xm'))
            #self.mixer.music.play(-1)
        self.font = pygame.font.Font("./fonts/MMMM8.TTF", 16)
        self.accumulator = zeros((320, 240, 3))
        self.screensurf = pygame.Surface((320, 240)) 
        self.mixer.music.stop()
        self.timer = timer.Timer(45)
        self.beginbuffer='''Bean Kid's grandmother lives in a small village of beans and children.$$$$$$$
One day, Bean Kid's grandmother became very ill.$$$$$$$
Bean in the case of the poor does not have enough money to save the life of her grandmother.$$$$$$$$
However...$$$$$$
Cavern Bean Kid knows just outside of town.$$$$$$
There is a legend, and a bags of golds in this cave.$$$$$$
However, The Turnip Ruffians is a group of living in cave.$$$$$$$
Go! Bean Kid! For grandmother!$$$$$$
'''
        self.endbuffer='''Bean Kid have collected enough golds for her grandmother.$$$$$$
Kid Bean from his grandmother's illness is not fear death.$$$$$$
A great job, Kid Bean!$$$$
The victory of the day!$$$$
But for now, why is any more golds in the cave?$$$$'''
        if (self.begin):
            self.textbuffer = self.beginbuffer
        else:
            self.textbuffer = self.endbuffer
        self.displaybuffer = ""
        self.bufferindex = 0
        self.buffercount = 0
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
        if (len(self.displaybuffer) > 1):
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
        self.buffercount += 1
        if (self.bufferindex < len(self.textbuffer) and self.buffercount > 7):
            self.buffercount = 0
            character = self.textbuffer[self.bufferindex]
            if (character == "$"):
                k = 1 #wait a frame
            else:
                self.sounds[1].play()
                self.displaybuffer = self.displaybuffer + self.textbuffer[self.bufferindex]
            self.bufferindex += 1
        self.timer.tick()
    ##
    ##Update is called once a frame.  It should update the display.
    ##::
    def update(self,screen):
        self.screensurf.fill((255, 255, 255))
        self.drawmenutext(self.screensurf, (95, 150), (88, 88, 88), self.displaybuffer)
        pygame.transform.scale(self.screensurf, (640, 480), screen)
        pygame.display.flip() #better to do updates
    ##
    def drawmenutext(self, screen, position, color, string):
        x, y = position
        text.writewrap(screen,self.font,pygame.Rect(20,20,280,160),color,string)
        text.writewrap(screen,self.font,pygame.Rect(20,20,280,160),(0,0,0),string)

