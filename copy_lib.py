import pygame

import database as db
from blendmapper import *


def render(s, pos, header, tiles, blendmap, wblendmap, rmap):
    res = s.get_size()
    s.fill((132, 170, 248))
    left = pos[0] // 20  # +10
    w = res[0] // 20 + 2
    right = left + w
    top = pos[1] // 20  # +10
    h = res[1] // 20 + 2
    bottom = top + h
    xp = pos[0] % 20
    yp = pos[1] % 20

    torender = tiles[left: right, top:bottom]
    x = 0
    for sli in torender:  # walls
        y = 0
        lx = left + x
        for t in sli:

            if t[1]:
                ly = top + y
                tpos = (x * 20 - xp - 10, y * 20 - yp - 10)
                if wblendmap[lx, ly][0] == 1:
                    get_wall(tiles, wblendmap, rmap, lx, ly)
                s.blit(walltex[t[1]], tpos, area=(wblendmap[lx, ly], (32, 32)))

            y += 1
        x += 1
    x = 0
    for sli in torender:  # tiles
        y = 0
        lx = left + x
        for t in sli:
            if t[0] != None:
                tpos = (x * 20 - xp, y * 20 - yp)
                if t[0] in db.multitiles:
                    s.blit(tex[t[0]], tpos, area=(t[3], (20, 20)))
                else:
                    ly = top + y
                    if blendmap[lx, ly][0] == 1:
                        get_tile_detail(tiles, blendmap, rmap, lx, ly)
                        blendmap[lx, ly][0] = blendmap[lx, ly][0] // 18 * 20
                        blendmap[lx, ly][1] = blendmap[lx, ly][1] // 18 * 20
                    s.blit(tex[t[0]], tpos, area=(blendmap[lx, ly], (20, 20)))

            if t[2] > 0:
                pygame.gfxdraw.box(s,
                                   ((x * 20 - xp, y * 20 - yp),
                                    (20, 20)),
                                   (0, 50, 255, 100))
            elif t[2] < 0:
                pygame.gfxdraw.box(s,
                                   ((x * 20 - xp, y * 20 - yp),
                                    (20, 20)),
                                   (200, 0, 0, 150))
            y += 1
        x += 1
    return s


class Chestinfo():
    def __init__(chest, pos):
        self.chest = chest
        self.pos = pos  # worldcoord

#    def render(tilepos,
