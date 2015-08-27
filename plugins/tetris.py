#! python3

config ={
    "name" : "Tetris", #plugin name
    "type" : "program", #plugin type
    "description" : ["Minimalist Tetris"] #description
     }
state = None
from pygame.constants import *
left = [K_LEFT, K_a]
right = [K_RIGHT,K_d]
down = [K_DOWN, K_d]
all_down = [K_SPACE, ]
rotate = [K_UP, K_w]
from random import choice
from itertools import product
import pygame
try:
    from plugins.tetris_lib import TetrisConfig
except:
    from tetris_lib import TetrisConfig

pygame.init()
fps = pygame.time.Clock()


def expand(x,y):
    return x,y,state.squaresize,state.squaresize

def draw(screen):
    screen.fill((20,20,20))
    s = state.squaresize
    for x,row in enumerate(state.grid):
        for y,space in enumerate(row):
            if space.filled:
                screen.fill(space.filled, (x*s, y*s, s,s))
    state.current.draw(screen)
                       
def overlap(mask, mask2, offset):
    pass
    

class Piece():
    def __init__(self, color, masks):
        self.color = color
        self.masks = masks
        self.index = 0
        self.mask = masks[self.index]
        self.size = self.mask.get_size()
        self.pos = config["width"]//2-self.size[0]//2, 0
        self.projection = 0

    def draw(self,screen):
        for x,y in product(range(self.size[0]),range(self.size[1])):
            if self.mask.get_at((x,y)):
                pos = (x+self.pos[0])*state.squaresize,(y+self.pos[1])*state.squaresize
                screen.fill(self.color, expand(*pos))
                
                ppos = (x+self.pos[0])*state.squaresize,(y+self.projection)*state.squaresize
                pygame.draw.circle(screen, self.color, (ppos[0]+state.squaresize//2, ppos[1]+state.squaresize//2), state.squaresize//2)
                #screen.fill(self.color, expand(*ppos))
            
    def check(self, offset):
        return state.mask.overlap(self.mask, offset)
    
    def on_move_horizontal(self):
        projected_y = self.pos[1]
        while not self.check((self.pos[0], projected_y)):
            projected_y +=1
            if projected_y+self.size[1] > config["height"]:
                #projected_y -= 1
                break
            
        self.projection = projected_y-1
    
    def drop(self):
        
        if self.check((self.pos[0], self.pos[1]+1)):
            state.assimilate_Piece()
            if self.pos[1]<= 1:state.__init__(config)
            return True
        self.pos = self.pos[0],self.pos[1]+1
        if self.pos[1]+self.size[1] > config["height"]:
            self.pos = self.pos[0],self.pos[1]-1
            state.assimilate_Piece()
            return True
        
    def rotate(self):
        self.index +=1
        if self.index > len(self.masks)-1: self.index = 0
        self.mask = self.masks[self.index]
        self.size = self.mask.get_size()
        if self.pos[0]+self.size[0] > config["width"]:
            self.pos = config["width"]-self.size[0],self.pos[1]
            
        self.on_move_horizontal()

    def move_down(self, dt):
        self.drop()
        state.current_fall = state.fallspeed
        
    def move_left(self, dt):
        if self.check((self.pos[0]-1, self.pos[1])):
            return
        self.pos = max(0,self.pos[0]-1), self.pos[1]
        self.on_move_horizontal()
        
    def move_right(self, dt):
        if self.check((self.pos[0]+1, self.pos[1])):
            return
        self.pos = min(self.pos[0]+1, config["width"]-self.size[0]), self.pos[1]
        self.on_move_horizontal()
        
    def move_all_down(self, dt):
        while not self.drop():pass


class Space():
    def __init__(self):
        self.filled = None #None or Color it's filled with


class Gamestate():
    def __init__(self,configdict):
        for k,v in configdict.items():
            setattr(self, k, v)
        self.grid = [[Space() for _ in range(self.height)] for _ in range(self.width)]
        self.mask = pygame.Mask((self.width,self.height))
        self.current_inc = self.fallspeed_increment 
        self.current_fall = self.fallspeed
        self.parse_pieces()
        self.pick_Piece(init = True)
    
    def check_lines(self, to_check):
        ys = set()
        for y in to_check:
            if all([self.mask.get_at((x,y)) for x in range(self.width)]):
                ys.add(y)

        if ys:
            [self.move_line_down(y) for y in ys]
            self.regen_mask()
        
    def remove_line(self,y):
        for x in range(self.width):
            self.grid[x][y].filled = None
            
    def move_line_down(self, level):
        for x in range(self.width):
            for y in range(level,0,-1):
                self.grid[x][y] = self.grid[x][y-1]
                
            
    def regen_mask(self):
        for x,y in product(range(self.width),range(self.height)):
            self.mask.set_at((x,y), bool(self.grid[x][y].filled))
        
        
        
    def assimilate_Piece(self):
        p = self.current
        w,h = p.size
        px,py = p.pos
        ys = set()
        for x,y in product(range(w), range(h)):#
            
            if p.mask.get_at((x,y)):
                nx = x+px
                ny = y+py
                self.grid[nx][ny].filled = p.color
                self.mask.set_at((nx,ny), True)
                ys.add(ny)
        self.check_lines(ys)
        self.pick_Piece()
    
    def cache_rotations(self, mask):
        def rotate(x, y):
            return -y, x
        masks = [mask]
        for i in range(3):
            newmask = pygame.Mask((mask.get_size()[1],mask.get_size()[0]))
            for x,y in product(range(mask.get_size()[0]), range(mask.get_size()[1])):
                truth = mask.get_at((x,y))
                loc = (mask.get_size()[1]-y-1, x)
                newmask.set_at(loc, truth)

            mask = newmask
            masks.append(newmask)
        return masks
    
    def parse_pieces(self):
        self.masks = []
        for p in self.pieces:
            x_max = len(p)
            y_max = max([len(r) for r in p])
            mask = pygame.Mask((x_max, y_max))
            for x, row in enumerate(p):
                for y, truth in enumerate(row):
                    if truth:mask.set_at((x,y), True)
            self.masks.append(self.cache_rotations(mask))
            
    def pick_Piece(self, init = False):
        self.current = Piece(choice(self.colors), choice(self.masks))
        if not init:
            self.current.on_move_horizontal()
        
    def update(self, dt):
        self.current_inc -= dt
        while self.current_inc <= 0:
            self.current_inc += self.fallspeed_increment
            self.fallspeed = max(1, self.fallspeed - 1)
        self.current_fall -= dt
        while self.current_fall <= 0:
            self.current_fall += self.fallspeed
            self.drop()
            
    def drop(self):
        self.current.drop()

import os

join = os.path.join
import sys
try:
    from shared import appdata as ot
except:
    if sys.platform.startswith("win"):
        appdata = os.environ["APPDATA"]
        ot = join(appdata, "Omnitool")
    else:
        appdata = os.environ["HOME"]
        ot = join(appdata, "Omnitool")
    dirs = [ot]
    for d in dirs:
        if not os.path.isdir(d):os.mkdir(d)
    appdata = ot
    
conf = join(appdata, "tetrisconfig.txt")


class Program():
    def __init__(self):
        pass
    
    def run(self):
        global config, state, mainscreen
        config = TetrisConfig(conf).config
        state = Gamestate(config)
        state.current.on_move_horizontal()
        mainscreen = pygame.display.set_mode((state.squaresize*state.width, state.squaresize*state.height))
        pygame.display.set_caption("Tetris")
        

        while 1:
            dt = fps.tick(120)
            state.update(dt)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key in down:
                        state.current.move_down(dt)
                    elif event.key in left:
                        state.current.move_left(dt)
                    elif event.key in right:
                        state.current.move_right(dt)
                    elif event.key in all_down:
                        state.current.move_all_down(dt)
                    elif event.key in rotate:
                        state.current.rotate()
                        
            draw(mainscreen)
            pygame.display.flip()

if __name__ == "__main__":
    Program.run(None)
