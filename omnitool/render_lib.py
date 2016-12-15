import pygame
import pygame.gfxdraw

from . import database as db
from .blendmapper import *


def render(s, pos, header, tiles, blendmap, wblendmap, rmap):
    res = s.get_size()
    s.fill((132, 170, 248))
    left = pos[0] // 16  # +10
    w = res[0] // 16 + 2
    right = left + w
    if right > header["width"]:
        #out of bounds to the right
        right = header["width"]-1
        w = right-left
    top = pos[1] // 16  # +10
    h = res[1] // 16 + 2
    bottom = top + h
    if bottom > header["height"]:
        #out of bounds to the bottom
        bottom = header["height"]-1
        h = bottom-top
    xp = pos[0] % 16
    yp = pos[1] % 16
    xb = pos[0] % 96  # for background

    if bottom > header["groundlevel"]:
        if top - 1 < header["groundlevel"]:  # if top over ground
            px = 0
            y = int(header["groundlevel"] - top - 1) * 16 - yp
            while px < (5 + w) * 16:
                s.blit(gborder, (px - xb, y))
                px += 96
        px = 0
        while px < (5 + w) * 16:
            y = int(header["groundlevel"] - top) * 16 - yp
            yrock = int(header["rocklevel"] - top) * 16 - yp
            while y < min((5 + h) * 16, yrock):
                s.blit(gfill, (px - xb, y))  # ground fill
                y += 96
            s.blit(rborder, (px - xb, yrock - 16))

            y = int(header["rocklevel"] - top) * 16 - yp
            while y < (5 + h) * 16:
                s.blit(rfill, (px - xb, y))
                y += 96
            px += 96
    torender = tiles[left: right, top:bottom]
    x = 0
    for sli in torender:  # walls
        y = 0
        lx = left + x
        for t in sli:

            if t[1]:
                ly = top + y
                tpos = (x * 16 - xp - 8, y * 16 - yp - 8)
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
                tpos = (x * 16 - xp, y * 16 - yp)
                if t[0] in db.multitiles:
                    s.blit(tex[t[0]], tpos, area=(t[3], (16, 16)))
                else:
                    ly = top + y
                    if blendmap[lx, ly][0] == 1:
                        get_tile_detail(tiles, blendmap, rmap, lx, ly)
                    s.blit(tex[t[0]], tpos, area=(blendmap[lx, ly], (16, 16)))
            if t[2]:
                if t[2] > 512:
                    pygame.gfxdraw.box(s,
                                       ((x * 16 - xp, y * 16 - yp),
                                        (16, 16)),
                                       (255, 255, 127, 150))
                elif t[2] > 256:
                    pygame.gfxdraw.box(s,
                                       ((x * 16 - xp, y * 16 - yp),
                                        (16, 16)),
                                       (200, 0, 0, 150))
                else:
                    pygame.gfxdraw.box(s,
                                       ((x * 16 - xp, y * 16 - yp),
                                        (16, 16)),
                                       (0, 50, 255, 100))

            y += 1
        x += 1
    return s


class Chestinfo():
    def __init__(chest, pos):
        self.chest = chest
        self.pos = pos  # worldcoord

#    def render(tilepos,
