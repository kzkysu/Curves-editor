import pygame
from pygame.locals import *

class point:
    def __init__(self,x,y,color="black"):

        self.x = x
        self.y = y
        self.z = 0.0
        self.size = 3

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(color)