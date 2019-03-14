import os, pygame, sys
sys.path.append('/usr/lib/python%s/site-packages/oldxml' % sys.version[:3])

from math import sqrt
from random import randint
from string import Template

from util import *
from mousecursor import *
from pygame.locals import * 
from pointtag import *
from regiontag import *
import pygame.mixer

from pgu import engine, gui, text

import xml.dom.minidom
from xml.dom.minidom import Node

MODE_REGION = 1
MODE_POINT = 2
MODE_DELETE = 3
MODE_ATTRIBUTES = 4


##A state may subclass engine.State.
##::
class editscreen(engine.State):
    ##
    ##The init method should load data, etc.  The __init__ method
    ##should do nothing but record the parameters.  If the init method
    ##returns a value, it becomes the new state.
    ##::
    def __init__(self, game, sounds, mixer, filename):
        self.sounds = sounds
        self.mixer = mixer
        self.filename = filename
        engine.State.__init__(self, game)
    def init(self):
        self.font = pygame.font.Font("./fonts/freesansbold.ttf", 12)
        self.fontshown = False
        self.cursor = mousecursor()
        self.cursorgroup = pygame.sprite.OrderedUpdates((self.cursor))
        self.backimage = pygame.Surface((640, 480))
        itemimage = pygame.Surface((16, 16))
        itemimage.fill((255,255,255))
        for j in range(0, int(self.backimage.get_height()/16)+1):
            for i in range(0, int(self.backimage.get_width()/16)+1):
                self.backimage.blit(itemimage,(i*16, j*16)) 
        self.paletteimage = pygame.Surface((640, 480))
        i = 0
        j = 0
        for (key, image) in IMAGE_FILES.items():
            if (REGION_NODES.count(key)):
                tempimage,temp = load_image(image)
                self.paletteimage.blit(tempimage, (i*32, j*16))
                i += 1
                if (i > 20):
                    i = 0
                    j += 1
        self.tagedit = False
        self.tagname = 'brick'
        self.paletteedit = False
        self.fontshown = True
        self.attributeedit = False
        self.attributetag = None
        self.attributekey = ""
        self.attributevalue = ""
        self.attributeeditkey = False
        self.attributeeditvalue = False
        self.hidepointlayer = False
        self.attributenumber = None
        self.scrolloffsetx = 0
        self.scrolloffsety = 0
        self.editmode = MODE_POINT
        self.regiondrawing = False
        self.movingup = False
        self.movingdown = False
        self.movingleft = False
        self.movingright = False
        self.pointtags = []
        self.regiontags = []
        self.pointtaggroup = pygame.sprite.OrderedUpdates(self.pointtags)
        self.regiontaggroup = pygame.sprite.OrderedUpdates(self.regiontags)
        self.levelname = ""
        if (self.filename):
            self.loadlevel(self.filename)
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
                        if (REGION_NODES.count(node.nodeName)):
                            x = int(node.getAttribute("x"))
                            y = int(node.getAttribute("y"))
                            width = int(node.getAttribute("width"))
                            height = int(node.getAttribute("height"))
                            regionrect = pygame.Rect((x,y,width,height))
                            attributes = {}
                            for attr in node.attributes.keys():
                                if (attr != "x" and attr != "y" and attr != "width" and attr != "height"):
                                    attributes[attr] = node.getAttribute(attr)
                            self.regiontags.append(regiontag(regionrect, node.nodeName, IMAGE_FILES[node.nodeName], self.font,attributes, self.fontshown))
                            self.regiontaggroup.add(self.regiontags[-1])
                        elif (POINT_NODES.count(node.nodeName)):
                            x = int(node.getAttribute("x"))
                            y = int(node.getAttribute("y"))
                            attributes = {}
                            for attr in node.attributes.keys():
                                if (attr != "x" and attr != "y"):
                                    attributes[attr] = node.getAttribute(attr)
                            self.pointtags.append(pointtag(x, y, node.nodeName, IMAGE_FILES[node.nodeName], self.font,attributes, self.fontshown))  
                            self.pointtaggroup.add(self.pointtags[-1])
    def savelevel(self, filename):
        doc = xml.dom.minidom.Document()
        level = doc.createElement("level")
        doc.appendChild(level)
        name = doc.createElement("name")
        nametext = doc.createTextNode(self.levelname)
        name.appendChild(nametext)
        level.appendChild(name)
        leveldata = doc.createElement("leveldata")
        level.appendChild(leveldata)
        for i in self.pointtags:
            pointtag = doc.createElement(i.tagname)
            pointtag.setAttribute("x", str(i.rect.left))
            pointtag.setAttribute("y", str(i.rect.top))
            for (key, value) in i.attributes.items():
                pointtag.setAttribute(key, value)
            leveldata.appendChild(pointtag)    
        for i in self.regiontags:
            pointtag = doc.createElement(i.tagname)
            pointtag.setAttribute("x", str(i.rect.left))
            pointtag.setAttribute("y", str(i.rect.top))
            pointtag.setAttribute("width", str(i.rect.width))
            pointtag.setAttribute("height", str(i.rect.height))
            for (key, value) in i.attributes.items():
                pointtag.setAttribute(key, value)
            leveldata.appendChild(pointtag)    
        file_object = open("maps/" + filename, "w")
        printed = doc.toprettyxml(indent='  ')
        file_object.write(printed)
        file_object.close
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
        if e.type is KEYDOWN and not self.regiondrawing:
            if (self.tagedit):
                if e.key == K_RETURN:
                    self.tagedit = False
                elif (e.key == K_BACKSPACE):
                    self.tagname = self.tagname[:len(self.tagname)-1]
                elif (e.key >= 32 and e.key <= 125):
                    self.tagname = self.tagname + chr(e.key)
            elif (self.paletteedit):
                if e.key == K_RETURN:
                    self.paletteedit = False
            elif (self.attributeeditkey):
                if e.key == K_RETURN:
                    self.attributeeditkey = False
                    self.attributeeditvalue = True
                elif (e.key == K_DELETE):
                    self.attributeeditkey = False
                    self.attributeeditvalue = False
                    del self.attributetag.attributes[self.attributekey]
                elif (e.key == K_BACKSPACE):
                    self.attributekey = self.attributekey[:len(self.attributekey)-1]
                elif (e.key >= 32 and e.key <= 125):
                    self.attributekey = self.attributekey + chr(e.key)
            elif (self.attributeeditvalue):
                if e.key == K_RETURN:
                    self.attributeeditvalue = False
                    self.attributetag.attributes[self.attributekey] = self.attributevalue
                elif (e.key == K_BACKSPACE):
                    self.attributevalue = self.attributevalue[:len(self.attributevalue)-1]
                elif (e.key == K_SLASH):
                    self.attributevalue = self.attributevalue + "?"
                elif (e.key >= 32 and e.key <= 125):
                    if (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                        self.attributevalue = self.attributevalue + upper(chr(e.key))
                    else:
                        self.attributevalue = self.attributevalue + chr(e.key)
            elif (self.attributeedit):
                if (e.key == K_RETURN):
                    self.attributeedit = False
                    self.attributetag = None
            else:
                if e.key == K_t:
                    self.tagedit = True
                    self.tagname = ""
                elif e.key == K_l:
                    for i in self.regiontags:
                        i.togglefont()
                    for i in self.pointtags:
                        i.togglefont()
                    self.fontshown = not(self.fontshown)
                elif e.key == K_F2:
                    self.hidepointlayer = not(self.hidepointlayer)
                elif e.key == K_TAB:
                    self.paletteedit = True
                elif e.key == K_m:
                    self.editmode += 1
                    if (self.editmode > MODE_ATTRIBUTES):
                        self.editmode = MODE_REGION
                elif e.key == K_s:
                    self.savelevel(self.filename)
                elif e.key == K_UP:
                    self.movingup = True
                    self.movingdown = False
                elif e.key == K_DOWN:
                    self.movingdown = True
                    self.movingup = False
                elif e.key == K_LEFT:
                    self.movingleft = True
                    self.movingright = False
                elif e.key == K_RIGHT:
                    self.movingright = True
                    self.movingleft = False
                elif e.key == K_ESCAPE:
                    self.savelevel(self.filename)
                    return engine.Quit(self.game)
        elif e.type is KEYUP:
            if e.key == K_UP:
                self.movingup = False
            elif e.key == K_DOWN:
                self.movingdown = False
            elif e.key == K_LEFT:
                self.movingleft = False
            elif e.key == K_RIGHT:
                self.movingright = False
        elif e.type == MOUSEBUTTONDOWN:
            button1, button2, button3 = pygame.mouse.get_pressed(); 
            if button1:
                if (self.regiondrawing):
                    self.regiondrawing = False
                    (rectleft, recttop) = self.regionstart
                    (rectright, rectbottom) = pygame.mouse.get_pos()
                    rectright = int(rectright/16)*16
                    rectbottom = int(rectbottom/16)*16
                    regionrect = pygame.Rect((rectleft, recttop, -rectleft+rectright, -recttop+rectbottom))
                    if (-recttop+rectbottom != 0 and -rectleft+rectright != 0):
                        self.regiontags.append(regiontag(regionrect, self.tagname, IMAGE_FILES[self.tagname], self.font, {}, self.fontshown))
                        self.regiontaggroup.add(self.regiontags[-1])
                elif (self.paletteedit):
                    self.paletteedit = False
                    x, y = pygame.mouse.get_pos()
                    index = int(x/32)+16*int(y/16)
                    i = 0
                    for key, value in IMAGE_FILES.items():
                        if (REGION_NODES.count(key)):
                            if (i == index):
                                self.tagname = key
                            i += 1
                elif (self.editmode == MODE_REGION):
                    self.regiondrawing = True
                    x, y = pygame.mouse.get_pos()
                    self.regionstart = (int(x/16)*16, int(y/16)*16)
                elif (self.editmode == MODE_POINT):
                    x, y = pygame.mouse.get_pos()
                    self.pointtags.append(pointtag(int(x/16)*16, int(y/16)*16, self.tagname, IMAGE_FILES[self.tagname], self.font, {}, self.fontshown))  
                    self.pointtaggroup.add(self.pointtags[-1])
                elif (self.editmode == MODE_DELETE):
                    self.delete()
                elif (self.attributeedit):
                    (x, y) = pygame.mouse.get_pos()
                    self.attributenumber = int(y/16)
                    self.attributeeditkey = True
                    self.attributeeditvalue = False
                    i = 0
                    foundkey = False
                    for key in self.attributetag.attributes.keys():
                        if (i == self.attributenumber):
                            self.attributekey = key
                            self.attributevalue = self.attributetag.attributes[key]
                            foundkey = True
                        i += 1
                    if (not(foundkey)):
                        self.attributekey = ""
                        self.attributevalue = ""
                elif (self.editmode == MODE_ATTRIBUTES):
                    self.showattributes()
    def delete(self):
        foundobject = False
        for i in self.pointtags:
            if (not(foundobject) and self.cursor.click(i)):
                self.pointtags.remove(i)
                self.pointtaggroup.remove(i)
                del i
                foundobject = True
        if (not(foundobject)):
            for i in self.regiontags:
                if (not(foundobject) and self.cursor.click(i)):
                    self.regiontags.remove(i)
                    self.regiontaggroup.remove(i)
                    del i
                    foundobject = True
    def showattributes(self):
        foundobject = False
        for i in self.pointtags:
            if (not(foundobject) and self.cursor.click(i)):
                self.attributetag = i
                self.attributeedit = True
                foundobject = True
        if (not(foundobject)):
            for i in self.regiontags:
                if (not(foundobject) and self.cursor.click(i)):
                    self.attributetag = i
                    self.attributeedit = True
                    foundobject = True
    def move(self):
        scrollx = 0
        scrolly = 0
        if (self.movingright):
            scrollx -= 16
        elif (self.movingleft):
            scrollx += 16
        if (self.movingup):
            scrolly += 16
        elif (self.movingdown):
            scrolly -= 16
        self.scrolloffsetx -= scrollx
        self.scrolloffsety -= scrolly
        for i in self.pointtags:
            i.scroll(scrollx, scrolly)
        for i in self.regiontags:
            i.scroll(scrollx, scrolly)
    ##
    ##Loop is called once a frame.  It should contain all the
    ##logic.  If the loop method returns a value it will become the
    ##new state.
    ##::
    def loop(self):
        self.move()
        self.cursor.update()
    ##
    ##Update is called once a frame.  It should update the display.
    ##::
    def update(self,screen):
        if (not(self.paletteedit)): 
            tempx = self.scrolloffsetx%640
            tempy = self.scrolloffsety%480
            screen.blit(self.backimage, (-tempx, -tempy))
            screen.blit(self.backimage, (640-tempx, -tempy))
            screen.blit(self.backimage, (-tempx, 480-tempy))
            screen.blit(self.backimage, (640-tempx, 480-tempy))
            self.regiontaggroup.draw(screen)
            if (not(self.hidepointlayer)):
                self.pointtaggroup.draw(screen)
            else:
                self.drawmenutext(screen, (300, 0), (255, 255, 255), "Objects layer hidden")
        else:
            screen.blit(self.paletteimage, (0, 0)) 
        if (self.attributeedit):
            if (self.attributeeditkey):
                self.drawmenutext(screen, (0, 0), (255, 255, 255), "Key: " + self.attributekey)
            elif (self.attributeeditvalue):
                self.drawmenutext(screen, (0, 0), (255, 255, 255), "Value: " + self.attributevalue)
            else:
                i = 0
                for (key, value) in self.attributetag.attributes.items():
                    self.drawmenutext(screen, (0, 16*i), (255, 255, 255), key + " -> " + value)
                    i += 1
        elif not(self.paletteedit):
            if (self.regiondrawing):
                (rectleft, recttop) = self.regionstart
                (rectright, rectbottom) = pygame.mouse.get_pos()
                rectright = int(rectright/16)*16
                rectbottom = int(rectbottom/16)*16
                regionrect = pygame.Rect((rectleft, recttop, -rectleft+rectright, -recttop+rectbottom))
                pygame.draw.rect(screen, (255, 100, 100), regionrect)
                
            if (self.tagedit):
                self.drawmenutext(screen, (0,0), (100,100,100), "Name of tag to place:" + self.tagname)
            else:
                self.drawmenutext(screen, (0,464), (100,100,100), "Tag: " + self.tagname)
            if (self.editmode == MODE_REGION):
                self.drawmenutext(screen, (550,0), (100,100,100), "Mode: Region")    
            elif (self.editmode == MODE_POINT):
                self.drawmenutext(screen, (550,0), (100,100,100), "Mode: Point")    
            elif (self.editmode == MODE_DELETE):
                self.drawmenutext(screen, (550,0), (100,100,100), "Mode: Delete")    
            elif (self.editmode == MODE_ATTRIBUTES):
                self.drawmenutext(screen, (550,0), (100,100,100), "Mode: Attributes")    
            (mousex, mousey) = pygame.mouse.get_pos() 
            if (not(self.regiondrawing)):
                self.drawmenutext(screen, (450,464), (100,100,100), "(" + str(mousex+self.scrolloffsetx) + ", " + str(mousey+self.scrolloffsety) + ")") 
            else:
                (rectleft, recttop) = self.regionstart
                self.drawmenutext(screen, (450,464), (100,100,100), "(" + str(rectleft+self.scrolloffsetx) + ", " + str(recttop+self.scrolloffsety) + ")-(" + str(mousex+self.scrolloffsetx) + ", " + str(mousey+self.scrolloffsety) + ")") 
        self.cursorgroup.draw(screen)
        pygame.display.flip() #better to do updates
    ##

    def drawmenutext(self, screen, position, color, string):
        x, y = position
        text.writewrap(screen,self.font,pygame.Rect(x+1,y+1,640,30),(0,0,0),    string)
        text.writewrap(screen,self.font,pygame.Rect(x,y,640,30),color,string)

