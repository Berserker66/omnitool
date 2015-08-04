from random import *

import pygame


def make_tree(height=randint(5, 30), trunk=(1, 1)):
    s = pygame.surface.Surface((3, height))
    s.fill((255, 255, 255))
    if trunk[0]:
        s.set_at((0, height - 1), (5, 2, 6 + randint(0, 2)))
        if not trunk[1]: s.set_at((1, height - 1), (5, 3, 6 + randint(0, 2)))
    if trunk[1]:
        s.set_at((2, height - 1), (5, 1, 6 + randint(0, 2)))
        if trunk[0]:
            s.set_at((1, height - 1), (5, 4, 6 + randint(0, 2)))
        else:
            s.set_at((1, height - 1), (5, 0, 6 + randint(0, 2)))
    elif not trunk[0]:
        raise Exception("too small trunk, tree.py")
    for level in range(height - 1):
        s.set_at((1, level), (5, 0, randint(0, 2)))
    return s
    
            
    
    
