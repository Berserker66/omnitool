from __future__ import with_statement
import time
import pygame
import numpy
from tinterface import *
minimap_limits = 400,300



# from blendmapper import *

def load(tiles=None, walls=None, colors=None, wallcolors=None):
    if os.path.exists("content.lzma"):
        import zipfile
        ZF = zipfile.ZipFile("content.lzma", "r", zipfile.ZIP_LZMA)
        import io
        def load_content(imagename):
            return pygame.image.load(io.BytesIO(ZF.read(imagename)), "png")
    else:
        def load_content(imagename):
            return pygame.image.load(os.path.join("tImages", imagename))
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
        npc_tex[name] = load_content(bind[name])

    tex = [pink] * 65537
    x = 0
    while 1:
        try:
            tex[x] = load_content("Tiles_" + str(x) + ".png")#.convert_alpha()
        except pygame.error:
            break
        except KeyError:
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
            walltex[x] = load_content("Wall_" + str(x) + ".png")
        except pygame.error:
            break
        except KeyError:
            break
        x += 1
    if walls is not None:
        for w in wallcolors:
            if not walltex[w]:
                print(w)
                s = pygame.surface.Surface((500, 500))
                s.fill(wallcolors[w])
                walltex[w] = s

    air = load_content("Background_0.png")
    gborder =load_content("Background_1.png")
    rborder = load_content("Background_4.png")
    gfill = load_content("Background_2.png")
    rfill = load_content("Background_3.png")

    return tex, walltex, npc_tex, air, gborder, rborder, gfill, rfill



def run(header, path, mapping, data):
    header, pos = data
    pygame.init()
    pygame.display.init()

    try:
        imageloc = os.path.join(get_myterraria(), "WorldImages", os.path.basename(path).split(".")[0]+".png")
        mapimage = pygame.image.load(imageloc)
        mi_size = mapimage.get_size()
        mi_scale = 1
        if mi_size[0] > minimap_limits[0]:
            mi_scale = 1/(mi_size[0]/minimap_limits[0])
        if mi_size[1] > minimap_limits[1]:
            mi_scale = min(1/(mi_size[1]/minimap_limits[1]), mi_scale)
            print("Scaling minimap with factor "+str(mi_scale))
        if mi_scale != 1:
            mapimage = pygame.transform.rotozoom(mapimage, 0, mi_scale)
        mi_size = mapimage.get_size()

    except:
        print("Cannot load minimap:")
        import traceback
        traceback.print_exc()
        mapimage = None

    start = time.clock()
    f = open(path, "rb")
    f.seek(pos)
    get = get_tile_buffered_12_masked if header["version"] > 100 else get_tile_buffered
    pygame.display.set_caption("Loading World..")
    loadbar_width = minimap_limits[0]
    if mapimage:
        if mi_size[0] > 200:loadbar_width = mi_size[0]
        surface = pygame.display.set_mode((loadbar_width, 20+mi_size[1]))
        pygame.display.update(surface.blit(mapimage, (0, 20)))
    else:
        surface = pygame.display.set_mode((loadbar_width, 20))
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
            nw = int(minimap_limits[0] * xi / w)
            if nw != rect.w:
                rect.w = nw
                pygame.draw.rect(surface, (200, 200, 200), rect)
                pygame.display.update(tup)

                for event in pygame.event.get():
                    if event.type == 12:
                        pygame.quit()
                        import sys
                        sys.exit()

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

    blendmap = numpy.ones((header["width"], header["height"], 2), dtype=numpy.uint16)
    wblendmap = numpy.ones((header["width"], header["height"], 2), dtype=numpy.uint16)

    mid = time.clock()
    print("World loaded: %5f seconds" % (mid - start))

    tex, walltex, npc_tex, air, gborder, rborder, gfill, rfill = load()
    print("Textures loaded: %5f seconds" % (time.clock() - mid))

    spawn = header["spawn"]
    clock = pygame.time.Clock()
    pos = [spawn[0] * 16 - 256, spawn[1] * 16 - 256]

    pygame.display.set_caption("Terraria World Render")
    if mapping:
        res = [1600, 1600]
        area = [1600, 1600]
        os.chdir("..")
    else:
        res = [1024, 768]
        dis = pygame.display.set_mode(res, pygame.RESIZABLE)
    s = pygame.surface.Surface(res)
    def relmove(rel):
        nonlocal s
        nonlocal pos
        nonlocal dirty
        pos[0] -= rel[0]
        pos[1] -= rel[1]

        s.blit(s, rel)
        if abs(rel[0]) > res[0] or abs(rel[1])> res[1]:
            dirty = [pygame.rect.Rect(0, 0, res[0], res[1])]
        else:
            if rel[0] > 0:
                dirty.append(pygame.rect.Rect(0, 0, rel[0], res[1]))
            elif rel[0] < 0:
                dirty.append(pygame.rect.Rect(res[0] + rel[0], 0, -rel[0], res[1]))
            if rel[1] > 0:
                dirty.append(pygame.rect.Rect(0, 0, res[0], rel[1]))
            elif rel[1] < 0:
                dirty.append(pygame.rect.Rect(0, res[1] + rel[1], res[0], -rel[1]))
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
    movemode = None
    #movemodes:
    MAP = 2
    CURSOR = 1
    while 1:

        events = pygame.event.get()
        for event in events:
            if event.type == 12:
                pygame.quit()
                import sys

                sys.exit()
            elif event.type == 16:
                res = event.size
                dis = pygame.display.set_mode(res, pygame.RESIZABLE)
                s = pygame.surface.Surface(res)
                dirty.append(pygame.rect.Rect(0, 0, res[0], res[1]))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mapimage and event.button == 1:
                    if event.pos[0]>(res[0]-mi_size[0]) and event.pos[1] < mi_size[1]:
                        movemode = MAP
                    else:
                        movemode = CURSOR
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    movemode = None
        if not mapping:
            rel = pygame.mouse.get_rel()
            if pygame.mouse.get_pressed()[0] and movemode:
                if movemode == CURSOR:
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

                    relmove(rel)
                else:
                    mpos = pygame.mouse.get_pos()
                    mpos = (mpos[0]-res[0]+mi_size[0])*16/mi_scale,mpos[1]*16/mi_scale
                    rel = (pos[0]-mpos[0], pos[1]-mpos[1])
                    if any(rel):relmove(rel)

        for rect in dirty:
            try:
                b = render_lib.render(pygame.surface.Surface(rect.size),
                                      (pos[0] + rect.x, pos[1] + rect.y),
                                      header, tiles, blendmap, wblendmap, rmap)
            except IndexError:
                print("Out of bounds rendering attempt.")
            else:
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

                res[0] = -mx * area[0] + wi
            if (my + 1) * area[1] > he and not (my * area[1] > he):

                res[1] = -my * area[1] + he

            dirty = [pygame.rect.Rect(0, 0, res[0], res[1])]
            if s.get_size() != res: s = pygame.surface.Surface(res)
            res = [area[0], area[1]]
            pos = [mx * res[0], my * res[1]]

        else:
            dirty = []
            dis.blit(s, (0,0))
            if mapimage:
                dis.blit(mapimage, (res[0]-mi_size[0], 1))
                #draw minimap viewport borders:
                bpos = pos[0]//16, pos[1]//16
                topleft = bpos[0]*mi_scale+res[0]-mi_size[0], bpos[1]*mi_scale
                viewsize = (mi_scale*res[0])//16, (res[1]*mi_scale)//16
                pygame.gfxdraw.rectangle(dis, (topleft, viewsize), (127,30,30, 127))

        pygame.display.update()
        clock.tick(100)


if __name__ == "__main__":
    path, worlds = get_worlds(False)
    b = {}
    x = 0
    for w in worlds:
        with open(os.path.join(path, w), "rb") as f:
            header = get_header(f)[0]
            b[w] = header, f.tell()
        name = header["name"]

        print(x, ":", name)
        x += 1

    x = input("World Number:")
    world = worlds[int(x) - 1]
    if "super" in sys.argv:
        image = True
    else:
        image = False
    run(os.path.join(path, world), image, b[world])
