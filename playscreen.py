import os, pygame

from math import sqrt
from random import randint
from string import Template

from util import *
from pygame.locals import *
from pygame.surfarray import *
import pygame.mixer
from numpy import zeros

from player import *

import xml.dom.minidom
from xml.dom.minidom import Node

import copy

from pgu import engine, gui, text, timer

##::
class playscreen(engine.State):
    ##
    ##The init method should load data, etc.  The __init__ method
    ##should do nothing but record the parameters.  If the init method
    ##returns a value, it becomes the new state.
    ##::
    def __init__(self, game, sounds, mixer, level, score):
        self.sounds = sounds
        self.mixer = mixer
        self.game = game
        self.level = level
        self.score = score
        engine.State.__init__(self, game)
    def init(self):
        self.accumulator = zeros((320, 240, 3))
        self.screensurf = pygame.Surface((320, 240)) 
        #self.mixer.music.load(os.path.join('./choons/', str(self.level) + ".mp3"))
        #self.mixer.music.play(-1)
        self.font = pygame.font.Font("./fonts/MMMM8.TTF", 16)
        self.timer = timer.Timer(45)
        self.fpsframe = 0
        self.player = player(0, 0)
        self.playergroup = pygame.sprite.OrderedUpdates(())
        self.playergroup.add(self.player)
        self.loadlevel("map" + str(self.level) + ".xml")
        self.speedometer = timer.Speedometer()
        self.stagetimer = 100
        self.playedwarning = False
        self.resumedwarning = False
        self.levelover = False
    def loadlevel(self, filename):
        doc = xml.dom.minidom.parse("maps/" + filename)
        for level in doc.getElementsByTagName("level"):
            levelname = level.getElementsByTagName("name");
            for i in levelname:
                for j in i.childNodes:
                    if j.nodeType == Node.TEXT_NODE:
                        self.levelname = j.nodeValue
            leveldata = level.getElementsByTagName("leveldata");
            for level in leveldata:
                for node in level.childNodes:    
                    if node.nodeType == Node.ELEMENT_NODE:
                        if (node.nodeName == "player"):
                            playerx = int(node.getAttribute("x"))
                            playery = int(node.getAttribute("y"))
        (scrollx, scrolly, oldx, oldy) = self.player.move(playerx, playery)
    ##
    ##The paint method is called once.  If you call repaint(), it
    ##will be called again.
    ##::
    def paint(self,s): 
        pygame.display.flip()
    ##
    ##Every time an event occurs, event is called.  If the event method
    ##returns a value, it will become the new state.
    ##::
    def event(self,e):
        return
    ##
    ##Loop is called once a frame.  It should contain all the
    ##logic.  If the loop method returns a value it will become the
    ##new state.
    ##::
    def loop(self):
        if (self.fpsframe > 45):
            print("frames per second: " + str(self.speedometer.fps))
            self.fpsframe = 0
        else:
            self.fpsframe += 1            
        self.timer.tick()
        self.speedometer.tick()
    ##
    ##Update is called once a frame.  It should update the display.
    ##::
    def update(self,screen):
        self.screensurf.fill((255,255,255))
        self.playergroup.draw(self.screensurf)
        pygame.transform.scale(self.screensurf, (640, 480), screen)
        #self.drawmenutext(screen, (2, 35), (255, 255, 255), "FPS: " + str(self.speedometer.fps))
        pygame.display.flip() #better to do updates        
    ##
    def drawmenutext(self, screen, position, color, string):
        x, y = position
        screen.blit(self.font.render(string, False, color), (x+1, y+1))
        screen.blit(self.font.render(string, False, (0,0,0)), position)

