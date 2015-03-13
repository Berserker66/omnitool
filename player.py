import pygame

from vec2d import *


class Player():
    def __init__(self, pos, cpos, color=(255, 0, 0)):
        self.image = pygame.image.load("placeholder.png")
        self.color = color
        self.pos = Vec2d(pos)
        self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
        self.lastrect = self.rect
        self.rect.topleft = self.pos - cpos

        self.falling = 0

    def update(self, rel, tiles):
        tile_pos = tuple(self.pos // 20)
        tx, ty = tile_pos
        topleft = tiles[tile_pos]
        topright = tiles[tx + 1, ty]

        middleleft = tiles[tx, ty + 1]
        middleright = tiles[tx + 1, ty + 1]

        bottomleft = tiles[tx, ty + 2]
        bottomright = tiles[tx + 1, ty + 2]
        print(rel, bottomleft, topleft)
        x = 0
        if rel[0] > 0:  # left
            if topleft[0] == None and middleleft[0] == None:
                x = rel[0]
        elif rel[0] < 0:
            if topright[0] == None and middleright[0] == None:
                x = rel[0]

        # y = rel[1]
        y = 0
        if bottomleft[0] == None and bottomright[0] == None:  #we are in the air
            y = -self.falling
            self.falling += 1

        elif rel[1] > 0 and self.falling == 0:
            y = rel[1] * 10
        else:
            self.falling = 0
            y = self.pos.y - 1 - tile_pos[1] * 20
            print("standing")
            #y = self.pos.y-self.rect.top

        self.pos.x -= x
        self.pos.y -= y

        return x, y

    def render(self, cpos, s):
        s.blit(self.image, self.pos - cpos)
        # pygame.draw.circle(s,self.color, self.pos-cpos-(18,18), 18)
        #pygame.draw.rect(s, (0,255,0), self.rect)
        
        
