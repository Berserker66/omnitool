from __future__ import with_statement
import os
import pickle
from random import choice
import time
import sys

import pygame

from tlib import *
from tinterface import *
import omnitool
import database as db


try:
    import numpy
except:
    sys.path.insert(0, ".")
    import numpy
from blendmapper import *


def get_tiles(x, y, f):
    tiles = []
    for xi in range(x):  # for each slice
        row = []
        tiles.append(row)
        for yi in range(y):  # get the tiles
            row.append(get_tile(f))
    return tiles


def load():
    tex = []
    x = 0
    while 1:
        try:
            tex.append(pygame.image.load(
                os.path.join("tImages",
                             "Tiles_" + str(x) + ".png")).convert_alpha())
        except pygame.error:
            break
        x += 1
    walltex = [pygame.surface.Surface((1, 1))]
    x = 1
    while 1:
        try:
            walltex.append(pygame.image.load(
                os.path.join("tImages",
                             "Wall_" + str(x) + ".png")).convert_alpha())
        except pygame.error:
            break
        x += 1
    return tex, walltex


def run(path, mapping=False):
    pygame.init()
    pygame.display.init()

    #
    start = time.clock()
    print("loading and converting world data")

    # with open(path, "rb") as f:
    #    header = get_header(f)
    #    tiles = numpy.empty((header["width"], header["height"]), dtype =  tuple)
    #    for xi in range(header["width"]):# for each slice
    #        for yi in range(header["height"]): # get the tiles
    #            tiles[xi, yi] = get_tile(f)
    #with open("tiles.pic", "wb") as f:
    #    pickle.dump((header, tiles), f)

    with open("tiles.pic", "rb") as f:
        header, tiles = pickle.load(f)
    print("Finding Tile Frames")
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
    air = pygame.image.load(os.path.join("tImages", "Background_0.png")).convert()
    gborder = pygame.image.load(os.path.join("tImages", "Background_1.png")).convert_alpha()
    rborder = pygame.image.load(os.path.join("tImages", "Background_4.png")).convert_alpha()
    gfill = pygame.image.load(os.path.join("tImages", "Background_2.png")).convert()
    rfill = pygame.image.load(os.path.join("tImages", "Background_3.png")).convert()
    print("Textures loaded: %5f seconds" % (time.clock() - mid))

    #airbg = pygame.surface.Surface(
    spawn = header["spawn"]
    clock = pygame.time.Clock()
    pos = [spawn[0] * 16, spawn[1] * 16 - 256]
    r = True

    #contain = pygame.surface.Surface(res)
    pygame.display.set_caption("Terraria World Render")
    opengl = True
    if mapping:
        res = [1600, 1600]
        area = [1600, 1600]
        s = pygame.surface.Surface(res)
    else:
        if opengl:
            from HWBind import Display
            import renderogl as ogl

            t_tex = [ogl.Texture(x) for x in tex]
            w_tex = [ogl.Texture(x) for x in walltex]
            res = [1024, 768]
            display = Display()
            display.set_mode(res[0], res[1])
        else:
            res = [1024, 768]
            s = pygame.display.set_mode(res, pygame.RESIZABLE)
    print("initializing render loop...")
    if mapping:
        try:
            os.mkdir("superimage")
        except:
            pass
        try:
            os.mkdir(os.path.join("superimage", "tiles"))
        except:
            pass
        mx = 0
        my = 0
        index = open(os.path.join("superimage", "index.html"), "wt")
        index.write('<html><table border="0" cellspacing="0" cellpadding="0"><tr>')
        pos = [mx * res[0], my * res[1]]
    while 1:

        events = pygame.event.get()
        for event in events:
            if event.type == 12:
                pygame.quit()
                import sys

                sys.exit()
            elif event.type == 16:
                res = event.size
                r = True
                s = pygame.display.set_mode(res, pygame.RESIZABLE)
        if not mapping:
            rel = pygame.mouse.get_rel()
            if pygame.mouse.get_pressed()[0]:
                pos[0] -= rel[0]
                pos[1] -= rel[1]
                r = 2

        if r:
            #s.fill((132,170,248))
            display.fill()
            print("Render")
            left = pos[0] // 16
            w = res[0] // 16 + 2
            right = left + w
            top = pos[1] // 16
            h = res[1] // 16 + 2
            bottom = top + h
            xp = pos[0] % 16
            yp = pos[1] % 16
            xb = pos[0] % 96  #for background
            yb = pos[1] % 96  #for background
            if not mapping:
                px = 0
                while px < w * 16:
                    #s.blit(air, (px,0))
                    px += 48

            if bottom > header["groundlevel"]:
                if top - 1 < header["groundlevel"]:  #if top over ground
                    px = 0
                    y = int(header["groundlevel"] - top - 1) * 16 - yp
                    while px < (4 + w) * 16:
                        #s.blit(gborder, (px-xb,y))
                        px += 96
                px = 0
                while px < (4 + w) * 16:
                    y = int(header["groundlevel"] - top) * 16 - yp
                    yrock = int(header["rocklevel"] - top) * 16 - yp
                    while y < min((4 + h) * 16, yrock):
                        #s.blit(gfill, (px-xb,y))#ground fill
                        y += 96
                    #s.blit(rborder, (px-xb,yrock-16))

                    y = int(header["rocklevel"] - top) * 16 - yp
                    while y < (4 + h) * 16:
                        #s.blit(rfill, (px-xb,y))
                        y += 96
                    px += 96
            torender = tiles[left: right, top:bottom]
            x = 0
            for sli in torender:  #walls
                y = 0
                lx = left + x
                for t in sli:

                    if t[1]:
                        ly = top + y
                        tpos = (x * 16 - xp - 24, y * 16 - yp - 24)
                        if wblendmap[lx, ly][0] == 1:
                            get(tiles, blendmap, wblendmap, rmap, lx, ly)
                            #s.blit(walltex[t[1]], tpos, area = (wblendmap[lx, ly], (32,32)))
                    y += 1
                x += 1
            x = 0
            for sli in torender:  #tiles
                y = 0
                lx = left + x
                for t in sli:

                    if t[0] != None:

                        tpos = (x * 16 - xp - 16, y * 16 - yp - 16)
                        if t[0] in db.multitiles:
                            ogl.render_tile(display, t_tex[t[0]], tpos, *t[3])
                            #s.blit(tex[t[0]], tpos, area = (t[3], (16,16)))
                        else:
                            ly = top + y
                            if blendmap[lx, ly][0] == 1:
                                get(tiles, blendmap, wblendmap, rmap, lx, ly)
                            ogl.render_tile(display, t_tex[t[0]], tpos,
                                            *blendmap[lx, ly])
                            #s.blit(tex[t[0]], tpos, area = (blendmap[lx, ly], (16,16)))
                    y += 1
                x += 1
            x = 0
            for sli in torender:  #liquids
                y = 0
                for t in sli:

                    if t[2] > 0:
                        tpos = (x * 16 - xp - 16, y * 16 - yp - 16)
                        #pygame.gfxdraw.box(s,
                        #                   (tpos,
                        #                    (16,16)),
                        #                   (0,50,255, 100))
                    elif t[2] < 0:
                        tpos = (x * 16 - xp - 16, y * 16 - yp - 16)
                        #pygame.gfxdraw.box(s,
                        #                   (tpos,
                        #                   (16,16)),
                        #                   (200,0,0, 150))
                    y += 1
                x += 1
            r -= 1
        if mapping:
            print("%2dX|%2dY of %dX|%dY" % (
            mx, my, header["width"] * 16 // area[0] - 1, header["height"] * 16 // area[1] - 1))
            pygame.image.save(s, os.path.join("superimage", "tiles", "screen_%d_%d.png" % (mx, my)))
            index.write('<td><img src="' + str("tiles/screen_%d_%d.png" % (mx, my)) + '"></td>')
            r = True
            mx += 1
            if mx * area[0] >= header["width"] * 16:
                index.write("</tr><tr>")
                my += 1
                mx = 0
                if my * area[1] >= header["height"] * 16:
                    index.write("</table></html>")
                    index.close()
                    pygame.quit()
                    import sys

                    sys.exit()

            if (mx + 1) * area[0] > header["width"] * 16 and not (mx * area[0] > header["width"] * 16):
                print(mx * area[0], header["width"] * 16)
                res[0] = -mx * area[0] + header["width"] * 16
            if (my + 1) * area[1] > header["height"] * 16 and not (my * area[1] > header["height"] * 16):
                print(my * area[1], header["height"] * 16)
                res[1] = -my * area[1] + header["height"] * 16

            if s.get_size() != res: s = pygame.surface.Surface(res)
            res = [area[0], area[1]]
            pos = [mx * res[0], my * res[1]]
        #raise AssertionError()
        display.flip()
        clock.tick(60)


if __name__ == "__main__":
    path, worlds = get_worlds()
    x = 1
    for w in worlds:
        with open(os.path.join(path, w), "rb") as f:
            name = get_header(f)[0]["name"].decode()
        print(x, ":", name)
        x += 1
    x = input("World Number:")
    world = worlds[int(x) - 1]
    if "super" in sys.argv:
        image = True
    else:
        image = False
    run(os.path.join(path, world), image)
