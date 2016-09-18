from __future__ import with_statement
import time
import pygame
import numpy
import zlib
from . import googlemapindex
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from .Resources.header import imgheader
from . import render_lib
from .loadbar import Bar
from .shared import cores
import collections

from .tinterface import *

minimap_limits = 0.4, 0.2
defaultres = [1024, 768]


def load(tiles=None, walls=None, colors=None, wallcolors=None):
    from .shared import appdata
    shared = os.path.join(appdata, "tImages.zip")
    ziploc = None
    if os.path.exists("tImages.zip"):
        ziploc = "tImages.zip"
    elif os.path.exists(shared):
        ziploc = shared
    if ziploc:
        from .Resources import ResourceManager
        manager = ResourceManager(ziploc)

        def load_content(imagename):
            base, _ = os.path.splitext(imagename)
            return manager.get_pygame_image(base + ".img")
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
            tex[x] = load_content("Tiles_" + str(x) + ".png")  # .convert_alpha()
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
    gborder = load_content("Background_1.png")
    rborder = load_content("Background_4.png")
    gfill = load_content("Background_2.png")
    rfill = load_content("Background_3.png")
    return tex, walltex, npc_tex, air, gborder, rborder, gfill, rfill


def adjust_minimap(target_rel_size, resolution, base_image):
    mi_size = base_image.get_size()
    mi_scale = 1
    scaled_limits = [x * y for x, y in zip(minimap_limits, resolution)]
    if mi_size[0] > scaled_limits[0]:
        mi_scale = 1 / (mi_size[0] / scaled_limits[0])
    if mi_size[1] > scaled_limits[1]:
        mi_scale = min(1 / (mi_size[1] / scaled_limits[1]), mi_scale)
    if mi_scale != 1:
        print("Scaling minimap with factor " + str(mi_scale))
        mapimage = pygame.transform.rotozoom(base_image, 0, mi_scale)

    return mapimage, mi_scale


def run(path, mapping, data = None, mappingfolder=None):
    if data:header, pos = data
    else:
        with path.open("rb") as f:
            header, _, sectiondata = get_header(f)
            if sectiondata:
                pos = sectiondata["sections"][1]
            else:
                pos = f.tell()

    pygame.init()
    pygame.display.init()
    threadpool = ThreadPoolExecutor(cores)
    texture_loader = threadpool.submit(load)
    try:
        imageloc = get_myterraria() / "WorldImages" / path.with_suffix('.png').name
        base_image = pygame.image.load(str(imageloc))
        mapimage, mi_scale = adjust_minimap(minimap_limits, defaultres, base_image)
        mi_size = mapimage.get_size()

    except:
        print("Cannot load minimap:")
        import traceback
        traceback.print_exc()
        mapimage = None

    start = time.clock()
    f = path.open("rb")
    f.seek(pos)
    get = get_tile_buffered_12_masked if header["version"] > 100 else get_tile_buffered
    pygame.display.set_caption("Loading World..")
    loadbar_width = 200
    if mapimage:
        if mi_size[0] > 200: loadbar_width = mi_size[0]
        surface = pygame.display.set_mode((loadbar_width, 20 + mi_size[1]))
        pygame.display.update(surface.blit(mapimage, (0, 20)))
    else:
        surface = pygame.display.set_mode((loadbar_width, 20))
    skip = False
    if not skip:
        print("loading and converting world data")

        rect = pygame.Rect(0, 0, 0, 20)
        tup = (rect,)
        tiles = numpy.empty((header["width"], header["height"]), dtype=tuple)
        w, h = header["width"], header["height"]
        for xi in range(w):  # for each slice
            yi = 0
            while yi < h:  # get the tiles
                data, b = get(f)
                tiles[xi, yi:yi + b] = (data,) * b
                yi += b
            if xi % 16 == 0:
                rect.w = int(xi * loadbar_width / w)
                pygame.draw.rect(surface, (200, 200, 200), rect)
                pygame.display.update(tup)

                for event in pygame.event.get():
                    if event.type == 12:
                        pygame.quit()
                        import sys
                        sys.exit()

        npcs = []

    f.close()

    rmap = numpy.random.randint(3, size=(header["width"], header["height"]))

    blendmap = numpy.ones((header["width"], header["height"], 2), dtype=numpy.uint16)
    wblendmap = numpy.ones((header["width"], header["height"], 2), dtype=numpy.uint16)

    mid = time.clock()
    print("World loaded: %5f seconds" % (mid - start))

    tex, walltex, npc_tex, air, gborder, rborder, gfill, rfill = texture_loader.result()

    spawn = header["spawn"]
    clock = pygame.time.Clock()
    pos = [spawn[0] * 16 - 256, spawn[1] * 16 - 256]

    pygame.display.set_caption("Terraria World Render: {}".format(header["name"].decode()))
    if mapping:
        res = [1600, 1600]
        area = [1600, 1600]
        os.chdir("..")
    else:
        res = list(defaultres)
        dis = pygame.display.set_mode(res, pygame.RESIZABLE)
    s = pygame.surface.Surface(res)

    def relmove(rel):
        nonlocal s
        nonlocal pos
        nonlocal dirty
        pos[0] -= rel[0]
        pos[1] -= rel[1]

        s.blit(s, rel)
        if abs(rel[0]) > res[0] or abs(rel[1]) > res[1]:
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
        tempfiles = {}
        if mappingfolder == None:
            mappingfolder = Path("superimage")
        print("Mapping into folder",mappingfolder)
        tilefolder = mappingfolder / "tiles"
        for folder in (mappingfolder, tilefolder):
            if not folder.is_dir():
                folder.mkdir()

        mx = 0
        my = 0
        index = (mappingfolder / "index.html").open("wt")
        index.write(googlemapindex.index)
        index.write(header["name"].decode())
        index.write(googlemapindex.index2)
        index.close()
        pos = [mx * res[0], my * res[1]]
        caption = "Rendering {}".format(header["name"].decode())
        loadingbar = Bar(caption=caption)
        plates_x, plates_y = header["width"] * 16 // area[0], header["height"] * 16 // area[1]
        plates_done = 0
        plates = plates_x * plates_y
    dirty = [pygame.rect.Rect(0, 0, res[0], res[1])]

    render_lib.walltex = walltex
    render_lib.tex = tex
    render_lib.gborder = gborder
    render_lib.gfill = gfill
    render_lib.rborder = rborder
    render_lib.rfill = rfill
    wi, he = header["width"] * 16 - 64, header["height"] * 16 - 64
    movemode = None
    # movemodes:
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
                mapimage, mi_scale = adjust_minimap(minimap_limits, res, base_image)
                mi_size = mapimage.get_size()
                dirty.append(pygame.rect.Rect(0, 0, res[0], res[1]))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mapimage and event.button == 1:
                    if event.pos[0] > (res[0] - mi_size[0]) and event.pos[1] < mi_size[1]:
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
                    mpos = (mpos[0] - res[0] + mi_size[0]) * 16 / mi_scale, mpos[1] * 16 / mi_scale
                    rel = (pos[0] - mpos[0], pos[1] - mpos[1])
                    if any(rel): relmove(rel)

        if len(dirty):
            for rect in dirty:
                try:
                    b = render_lib.render(pygame.surface.Surface(rect.size),
                                          (pos[0] + rect.x, pos[1] + rect.y),
                                          header, tiles, blendmap, wblendmap, rmap)
                except IndexError:
                    print("Out of bounds rendering attempt.")
                else:
                    s.blit(b, rect.topleft)
            rect = pygame.rect.Rect(pos, res)
            for npc in npcs:
                if rect.collidepoint(npc[1]):
                    try:
                        target = (-pos[0] + npc[1][0], -pos[1] + npc[1][1] - 12)
                        s.blit(npc_tex[npc[0]], target, area=(0, 0, 40, 56))
                    except:
                        print("Warning: NPC of ID %d could not be rendered" % npc[0])

        if mapping:

            progtext = "%2dX|%2dY of %dX|%dY" % (mx, my, plates_x - 1, plates_y - 1)
            loadingbar.set_progress(100 * plates_done / plates, caption + " " + progtext)
            lasttask = threadpool.submit(store_surface, s, tempfiles, mx, my)

            mx += 1
            if mx * area[0] >= wi:
                # index.write("</tr><tr>")
                my += 1
                mx = 0
                if my * area[1] >= he:
                    lasttask.result()

                    splice_gmaps(threadpool, tilefolder, tempfiles, header["name"].decode())
                    pygame.quit()
                    return

            if (mx + 1) * area[0] > wi and not (mx * area[0] > wi):
                res[0] = -mx * area[0] + wi
            if (my + 1) * area[1] > he and not (my * area[1] > he):
                res[1] = -my * area[1] + he
            dirty = [pygame.rect.Rect(0, 0, res[0], res[1])]
            if s.get_size() != res: s = pygame.surface.Surface(res)
            res = [area[0], area[1]]
            pos = [mx * res[0], my * res[1]]
            plates_done += 1
            lasttask.result()
        else:
            dirty = []
            dis.blit(s, (0, 0))
            if mapimage:
                dis.blit(mapimage, (res[0] - mi_size[0], 0))
                # draw minimap viewport borders:
                bpos = pos[0] // 16, pos[1] // 16
                topleft = bpos[0] * mi_scale + res[0] - mi_size[0], bpos[1] * mi_scale
                viewsize = (mi_scale * res[0]) // 16, (res[1] * mi_scale) // 16
                pygame.gfxdraw.rectangle(dis, (topleft, viewsize), (127, 30, 30, 127))

            pygame.display.update()
        clock.tick(100)


def store_surface(surface: pygame.Surface, tempfiles: dict, mx: int, my: int):
    tfp = tempfile.SpooledTemporaryFile()
    string = zlib.compress(pygame.image.tostring(surface, "RGB"))
    data = imgheader.pack(1, *surface.get_size()) + string
    tfp.write(data)
    tempfiles[(mx, my)] = tfp


def generate_plate_coords(side: int, tempfiles: dict):
    mapping = collections.defaultdict(set)
    for x, y in tempfiles:
        outside_xy = x // side, y // side
        mapping[outside_xy].add((x, y))
    return mapping


def unpack(tempfiles, x, y, loc):
    tfp = tempfiles[(x, y)]
    tfp.seek(0)
    data = tfp.read()
    tfp.close()
    _, width, height = imgheader.unpack(data[:imgheader.size])
    imgdata = zlib.decompress(data[imgheader.size:])
    return imgdata, (width, height), loc


def render_plate(data, tilefolder, current_area, side, fname):
    temp = pygame.image.frombuffer(data, current_area, "RGB")
    targetsurf = pygame.transform.smoothscale(temp, (side, side))
    pygame.image.save(targetsurf, str(tilefolder / fname))


def splice_gmaps(threadpool, tilefolder, tempfiles, name):
    processpool = ProcessPoolExecutor()
    caption = "Rendering Zoom Layers {}".format(name)
    loadingbar = Bar(caption=caption)
    loadingbar.set_progress(0, caption)
    pygame.display.update()

    side = 1600
    zoom_levels = 4
    factor = 2 ** (zoom_levels - 1)
    masterside = side * factor
    plates = generate_plate_coords(factor, tempfiles)

    master_surface = pygame.Surface((masterside, masterside))

    done = 0
    total = len(tempfiles) + len(plates) * sum((4 ** x for x in range(zoom_levels)))
    fraction = 100 / total

    def render_base_to_master(task):
        imgdata, size, location = task.result()
        tempsurf = pygame.image.frombuffer(imgdata, size, "RGB")
        master_surface.blit(tempsurf, location)

    tasks = []
    for masterpos, pieces in plates.items():
        master_surface.fill((132, 170, 248))

        for x, y in pieces:
            task = processpool.submit(unpack, tempfiles, x, y, ((x % factor) * side, (y % factor) * side))
            tasks.append(threadpool.submit(render_base_to_master, task))
            tasks.append(task)
        current_area = masterside

        for task in tasks:
            task.result()
            done += 0.5
            loadingbar.set_progress(done * fraction, caption + " %4d of %4d" % (done, total))
        for z in range(zoom_levels):
            tasks = []
            pieces = masterside // current_area
            x_off = masterpos[0] * pieces
            y_off = masterpos[1] * pieces
            for xp in range(pieces):
                for yp in range(pieces):
                    temp = pygame.Surface.subsurface(master_surface,
                                                     (xp * current_area, yp * current_area, current_area, current_area))
                    filename = "screen_{}_{}_{}.png".format(z + 1, x_off + xp, y_off + yp)
                    data = pygame.image.tostring(temp, "RGB")
                    tasks.append(processpool.submit(render_plate, data, tilefolder, temp.get_size(), side, filename))

            for task in tasks:
                task.result()
                done += 1
                loadingbar.set_progress(done * fraction, caption + " %4d of %4d" % (done, total))
            current_area //= 2

if __name__ == "__main__":
    worlds = list(get_worlds(False))
    b = {}
    x = 0
    for w in worlds:
        with w.open("rb") as f:
            header = get_header(f)[0]
            b[w] = header, f.tell()
        name = header["name"].decode()

        print(x, ":", name)
        x += 1

    x = input("World Number:")
    world = worlds[int(x)]
    run(world, True)
