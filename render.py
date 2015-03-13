from __future__ import with_statement
import os
import pickle
from random import choice
import time
import sys
import json
import zipfile

import pygame
import numpy

from tlib import *
from tinterface import *
import database as db

# from blendmapper import *

def load(tiles=None, walls=None, colors=None, wallcolors=None):
    npc_tex = {}
    pink = pygame.surface.Surface((500, 500))
    pink.fill((255, 0, 255))
    bind = {"Merchant": "NPC_17.png",
            "Nurse": "NPC_18.png",
            "Arms Dealer": "NPC_19.png",
            "Dryad": "NPC_20.png",
            "Guide": "NPC_22.png",
            "Old Man": "NPC_37.png",
            "Demolitionist": "NPC_38.png",
            "Clothier": "NPC_54.png",
            "Wizard": "NPC_108.png",
            "Mechanic": "NPC_124.png",
            "Goblin Tinkerer": "NPC_107.png",

            }
    for name in bind:
        npc_tex[name] = pygame.image.load(os.path.join("tImages", bind[name]))

    tex = [pink] * 65537
    x = 0
    while 1:
        try:
            tex[x] = pygame.image.load(
                os.path.join("tImages",
                             "Tiles_" + str(x) + ".png")).convert_alpha()
        except pygame.error:
            break
        x += 1
    if tiles is not None:
        for t in range(x - 1, len(tiles) + 1):
            if t in colors:
                s = pygame.surface.Surface((500, 500))
                s.fill(colors[t])
                tex[t] = s

    walltex = [pink] * 65537
    x = 1
    while 1:
        try:
            walltex[x] = pygame.image.load(
                os.path.join("tImages",
                             "Wall_" + str(x) + ".png")).convert_alpha()
        except pygame.error:
            break
        x += 1
    if walls is not None:
        for w in wallcolors:
            if not walltex[w]:
                print(w)
                s = pygame.surface.Surface((500, 500))
                s.fill(wallcolors[w])
                walltex[w] = s
                #x -= 1
                #while 1:
                #for w in range(x-1, len(walls)+1):

                #    if w in wallcolors:
                #        s = pygame.surface.Surface((500,500))
                #        s.fill(wallcolors[w])
                #        walltex[w] = s
                #    else: break
                #    x += 1
    return tex, walltex, npc_tex


def run(header, path, mapping, data, txt=None):
    header, pos = data
    pygame.init()
    pygame.display.init()

    #
    start = time.clock()
    f = open(path, "rb")
    f.seek(pos)
    get = get_tile_buffered_12_masked if header["version"] > 100 else get_tile_buffered
    pygame.display.set_caption("Loading World..")
    surface = pygame.display.set_mode((300, 20))
    skip = False
    if not skip:
        print("loading and converting world data")

        b = [0]
        rect = pygame.Rect(0, 0, 0, 20)
        nw = 0
        tup = (rect,)
        tiles = numpy.empty((header["width"], header["height"]), dtype=tuple)
        w, h = header["width"], header["height"]
        for xi in range(w):  # for each slice
            yi = 0
            while yi < h:  # get the tiles
                data, b = get(f)
                tiles[xi, yi:yi+b] = (data,)*b
                yi+=b
            nw = int(300.0 * xi / w)
            if nw != rect.w:
                rect.w = nw
                pygame.draw.rect(surface, (200, 200, 200), rect)
                pygame.display.update(tup)
                pygame.event.pump()

                #chests = [get_chest(f) for x in range(1000)]
                #signs = [get_sign(f) for x in range(1000)]
                #print (chests)
        npcs = []
        #while 1:
        #    npc = get_npc(f)
        #    if not npc: break
        #    else: npcs.append(npc)
        #names = get_npc_names(f)
        #print (names, npcs)
        #trail = get_trail(f)
        #if trail[0] and trail[1] == header["name"] and trail[2] == header["ID"]:
        #    print ("World Signature test passed")
        #else:
        #    print ("World Signature test failed, information possibly corrupted")
    f.close()

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

    tex, walltex, npc_tex = load()
    air = pygame.image.load(os.path.join("tImages", "Background_0.png")).convert()
    gborder = pygame.image.load(os.path.join("tImages", "Background_1.png")).convert_alpha()
    rborder = pygame.image.load(os.path.join("tImages", "Background_4.png")).convert_alpha()
    gfill = pygame.image.load(os.path.join("tImages", "Background_2.png")).convert()
    rfill = pygame.image.load(os.path.join("tImages", "Background_3.png")).convert()
    print("Textures loaded: %5f seconds" % (time.clock() - mid))

    #airbg = pygame.surface.Surface(
    spawn = header["spawn"]
    clock = pygame.time.Clock()
    pos = [spawn[0] * 16 - 256, spawn[1] * 16 - 256]

    #contain = pygame.surface.Surface(res)
    pygame.display.set_caption("Terraria World Render")
    if mapping:
        res = [1600, 1600]
        area = [1600, 1600]
        s = pygame.surface.Surface(res)
        os.chdir("..")
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
    dirty = [pygame.rect.Rect(0, 0, res[0], res[1])]
    import render_lib

    render_lib.walltex = walltex
    render_lib.tex = tex
    render_lib.gborder = gborder
    render_lib.gfill = gfill
    render_lib.rborder = rborder
    render_lib.rfill = rfill
    wi, he = header["width"] * 16 - 64, header["height"] * 16 - 64
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
        if not mapping:
            rel = pygame.mouse.get_rel()
            if pygame.mouse.get_pressed()[0]:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    rel = rel[0] * 10, rel[1] * 10
                if -rel[0] + pos[0] < 0:
                    rel = pos[0], rel[1]
                elif -rel[0] + pos[0] + res[0] > header["width"] * 16 - 64:
                    rel = header["width"] * 16 - 64 - pos[0] - res[0], rel[1]
                if -rel[1] + pos[1] < 0:
                    rel = rel[0], pos[1]
                elif -rel[1] + pos[1] + res[1] > header["height"] * 16 - 64:
                    rel = rel[0], header["height"] * 16 - 64 - pos[1] - res[1]

                pos[0] -= rel[0]
                pos[1] -= rel[1]
                #print (rel[0] > res[0] and rel[1] > res[1])
                s.blit(s, rel)

                if rel[0] > 0:
                    dirty.append(pygame.rect.Rect(0, 0, rel[0], res[1]))
                if rel[0] < 0:
                    dirty.append(pygame.rect.Rect(res[0] + rel[0], 0, -rel[0], res[1]))
                if rel[1] > 0:
                    dirty.append(pygame.rect.Rect(0, 0, res[0], rel[1]))
                if rel[1] < 0:
                    dirty.append(pygame.rect.Rect(0, res[1] + rel[1], res[0], -rel[1]))
                    #for rect in dirty:
                    #    pygame.draw.rect(s, (0,0,0), rect)

        for rect in dirty:
            b = render_lib.render(pygame.surface.Surface(rect.size),
                                  (pos[0] + rect.x, pos[1] + rect.y),
                                  header, tiles, blendmap, wblendmap, rmap)
            s.blit(b, rect.topleft)
        if len(dirty):
            rect = pygame.rect.Rect(pos, res)
            for npc in npcs:
                if rect.collidepoint(npc[1]):
                    try:
                        target = (-pos[0] + npc[1][0], -pos[1] + npc[1][1] - 12)
                        s.blit(npc_tex[npc[0]], target, area=(0, 0, 40, 56))
                    except:
                        print("Warning: NPC of ID %d could not be rendered" % npc[0])

        if mapping:


            print("%2dX|%2dY of %dX|%dY" % (
            mx, my, header["width"] * 16 // area[0] - 1, header["height"] * 16 // area[1] - 1))
            pygame.image.save(s, os.path.join("superimage", "tiles", "screen_%d_%d.png" % (mx, my)))
            index.write('<td><img src="' + str("tiles/screen_%d_%d.png" % (mx, my)) + '"></td>')
            r = True
            mx += 1
            if mx * area[0] >= wi:
                index.write("</tr><tr>")
                my += 1
                mx = 0
                if my * area[1] >= he:
                    index.write("</table></html>")
                    index.close()
                    pygame.quit()
                    import sys

                    sys.exit()

            if (mx + 1) * area[0] > wi and not (mx * area[0] > wi):
                #print (mx*area[0], header["width"]*16)
                res[0] = -mx * area[0] + wi
            if (my + 1) * area[1] > he and not (my * area[1] > he):
                #print (my*area[1], header["height"]*16)
                res[1] = -my * area[1] + he
            #print (res)
            dirty = [pygame.rect.Rect(0, 0, res[0], res[1])]
            if s.get_size() != res: s = pygame.surface.Surface(res)
            res = [area[0], area[1]]
            pos = [mx * res[0], my * res[1]]
        else:
            dirty = []
        pygame.display.update()

        clock.tick(100)


if __name__ == "__main__":
    print("Select mode:")
    print("1 : Vanilla (Terraria 1.1.2)")
    print("2 : tConfig")
    mode = int(input("Mode:")) - 1
    x = 1
    b = {}
    if mode == 0:
        path, worlds = get_worlds(False)

        for w in worlds:
            with open(os.path.join(path, w), "rb") as f:
                header = get_header(f)[0]
                b[w] = header, f.tell()
            name = header["name"]

            print(x, ":", name)
            x += 1
    elif mode == 1:
        path, worlds = get_worlds(True)
        for w in worlds:
            with zipfile.ZipFile(os.path.join(path, w)) as z:
                txt = json.loads(z.read("world.txt").decode())

            header = txt["header"]
            name = header["name"]
            b[w] = header, 0
            print(x, ":", name)
            x += 1
    else:
        print("Invalid mode")
        sys.exit()
    x = input("World Number:")
    world = worlds[int(x) - 1]
    if "super" in sys.argv:
        image = True
    else:
        image = False
    run(os.path.join(path, world), image, mode, b[world], txt if mode else None)
