from __future__ import with_statement
import os
import pickle
from random import *
import time
import sys

import pygame

from tlib import *
from tinterface import *
import omnitool
import database as db


sys.path.insert(0, ".")
import numpy

sys.path.remove(sys.path[0])
from player import Player
from control import *
# from blendmapper import *
def load():
    tex = []
    x = 0
    while 1:
        try:
            tex.append(pygame.image.load(
                os.path.join("ownimages",
                             "Tiles_" + str(x) + ".png")).convert_alpha())
        except pygame.error:
            break
        x += 1
    walltex = [None]
    x = 1
    while 1:
        try:
            walltex.append(pygame.image.load(
                os.path.join("ownimages",
                             "Wall_" + str(x) + ".png")).convert_alpha())
        except pygame.error:
            break
        x += 1
    return tex, walltex


def run():
    mapping = False
    pygame.init()
    pygame.display.init()

    #
    start = time.clock()

    header = {"width": 500, "height": 500,
              "spawn": (250, 250), "groundlevel": 500,
              "rocklevel": 1000}

    tiles = numpy.empty((header["width"], header["height"]), dtype=tuple)
    w, h = 500, 500

    for x in range(w):
        i = randint(250, 260)
        for y in range(h):
            if y > i:
                tiles[x, y] = (0, None, 0)
            else:
                tiles[x, y] = (None, None, 0)

    npcs = []
    signs = []
    chests = []
    rmap = numpy.random.randint(3, size=(header["width"], header["height"]))
    #blendmap, wblendmap = calc(header, tiles,rmap)
    blendmap = numpy.ones((header["width"], header["height"], 2), dtype=numpy.uint16)
    wblendmap = numpy.ones((header["width"], header["height"], 2), dtype=numpy.uint16)
    #with open("blend.pic", "wb") as f:
    #    pickle.dump((blendmap, wblendmap), f)
    #with open("blend.pic", "rb") as f:
    #    blendmap, wblendmap = pickle.load(f)
    mid = time.clock()
    print("World loaded: %5f seconds" % (mid - start))
    pygame.display.set_caption("Undead Window")
    pygame.display.set_mode((100, 100))
    tex, walltex = load()
    print("Textures loaded: %5f seconds" % (time.clock() - mid))

    #airbg = pygame.surface.Surface(
    spawn = header["spawn"]
    clock = pygame.time.Clock()


    #contain = pygame.surface.Surface(res)
    pygame.display.set_caption("Terraria World Render")
    res = [1024, 768]
    s = pygame.display.set_mode(res, pygame.RESIZABLE)
    pos = [spawn[0] * 20 - res[0] // 2, spawn[1] * 20 - res[1] // 2]
    passed = 0
    print("initializing render loop...")

    dirty = [pygame.rect.Rect(0, 0, res[0], res[1])]
    import copy_lib as render_lib

    render_lib.walltex = walltex
    render_lib.tex = tex

    wi, he = header["width"] * 20 - 80, header["height"] * 20 - 80
    player = Player((spawn[0] * 20, spawn[1] * 20), pos)
    for rect in dirty:
        b = render_lib.render(pygame.surface.Surface(rect.size),
                              (pos[0] + rect.x, pos[1] + rect.y),
                              header, tiles, blendmap, wblendmap, rmap)
        s.blit(b, rect.topleft)
    while 1:

        events = pygame.event.get()
        for event in events:
            if event.type == 12:
                pygame.quit()
                import sys

                sys.exit()
            elif event.type == 16:
                res = event.size
                s = pygame.display.set_mode(res, pygame.RESIZABLE)
                dirty.append(pygame.rect.Rect(0, 0, res[0], res[1]))
        keys = pygame.key.get_pressed()
        prel = get_movement(keys, player)

        rel = player.update(prel, tiles)

        dirty = get_dirty(rel, dirty, res)
        if len(dirty):
            dirty.append(player.rect.move(rel))
            s.blit(s, rel)
            pos[0] -= rel[0]
            pos[1] -= rel[1]

        for rect in dirty:
            b = render_lib.render(pygame.surface.Surface(rect.size),
                                  (pos[0] + rect.x, pos[1] + rect.y),
                                  header, tiles, blendmap, wblendmap, rmap)
            s.blit(b, rect.topleft)

        player.render(pos, s)
        #raise AssertionError()
        pygame.display.update()
        dirty = []

        passed = (clock.tick(50))


if __name__ == "__main__":
    run()
