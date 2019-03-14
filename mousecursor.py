import os, pygame

from pygame.locals import *

from util import *

class mousecursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('cursor.png', -1)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

    def click(self, target):
        x, y = self.rect.topleft;
        hitbox = pygame.Rect(x+1, y+1, 1, 1)
        return hitbox.colliderect(target.rect)
