from pygame.constants import *
import pygame


def get_movement(keys, player):
    if keys[K_w]:
        y = 2
    elif keys[K_s]:
        y = -2
    else:
        y = 0
    if keys[K_a]:
        x = 2
    elif keys[K_d]:
        x = -2
    else:
        x = 0
    rel = (x * 2, y * 2)
    return rel


def get_dirty(rel, dirty, res):
    if rel[0] > 0:
        dirty.append(pygame.rect.Rect(0, 0, rel[0], res[1]))
    elif rel[0] < 0:
        dirty.append(pygame.rect.Rect(res[0] + rel[0], 0, -rel[0], res[1]))
    if rel[1] > 0:
        dirty.append(pygame.rect.Rect(0, 0, res[0], rel[1]))
    elif rel[1] < 0:
        dirty.append(pygame.rect.Rect(0, res[1] + rel[1], res[0], -rel[1]))

    return dirty
