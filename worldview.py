from __future__ import with_statement
import time
import sys
from multiprocessing import *

from tlib import get_tile_buffered
from tinterface import get_header, get_pointers


is_exe = hasattr(sys, "frozen")
try:
    import pygame._view
except ImportError:
    pass
try:
    import pygame
except:
    raise RuntimeError("Failed to import pygame, please install it - pygame.org")
import colorlib
import database as db


def make_map(path, outputpath=None, mark=False, name=None):
    images = {}
    render = {}
    if mark:
        mark = [12, 26, 31]
    else:
        mark = []
    for tile in mark:
        try:
            images[tile] = (pygame.image.load(str(tile) + ".png"))
        except Exception as e:
            print("Could not load image for tile ID %d") % (tile)
            raise e
        render[tile] = []
    if len(mark):
        chests = []
        chestsizes = []
        for x in range(6):
            chests.append((pygame.image.load("21_" + str(x * 36) + ".png")))
            chestsizes.append(chests[-1].get_size())

        mark.append(21)
        render[21] = []
    start = time.clock()
    with open(path, "rb") as f:
        b = [0]
        header = get_header(f)[0]  # read header with tlib.get_header and also reach tile data in f
        x, y = header["width"], header["height"]  #read world size from header cache
        s = pygame.surface.Surface((x, y))  #create a software surface to save tile colors in
        s.fill((200, 200, 255))
        levels = header["groundlevel"], header["rocklevel"]
        pygame.draw.rect(s, (150, 75, 0),
                         ((0, levels[0]),
                          (x, y - levels[0])))

        pygame.draw.rect(s, (50, 50, 50),
                         ((0, levels[1]),
                          (x, y - levels[1])))
        for xi in range(x):  # for each slice
            for yi in range(y):  # get the tiles
                #tiles start from the upper left corner, then go downwards
                # when a slice is complete its starts with the next slice

                tile, b = get_tile_buffered(f, b)  #tlib.get_tile

                tile, wall, liquid, multi, wire = tile
                """ debug stuff, please ignore"""
                ##                if tile:
                ##
                ##                    if tile == 255:
                ##                        print xi,yi
                ##                        pygame.image.save(s, path[:-3]+"png")
                ##                        i += 1
                ##                        if i > 2:
                ##                            raise AssertionError()
                ##                    try:
                ##                        db.tiles[tile]
                ##                    except:
                ##                        print tile, xi, yi
                ##                        #raise AssertionError()
                """ debug stuff end"""
                if not liquid:  #liquid == 0 means no liquid
                    # there could be a liquid and a tile, like a chest and water,
                    #but I can only set one color to a pixel anyway, so I priotise the tile
                    if tile == None:
                        if wall:
                            if wall in colorlib.walldata:
                                s.set_at((xi, yi), colorlib.walldata[wall])
                            else:
                                print(wall)
                                s.set_at((xi, yi), (wall, wall, wall))

                                #s.set_at((xi,yi), (255,255,255))#if no tile present, set it white

                    elif tile in colorlib.data:
                        s.set_at((xi, yi), colorlib.data[tile])  #if colorlib has a color use it
                    else:
                        s.set_at((xi, yi), (tile, tile, tile))  #make a grey
                elif liquid > 0:  #0>x>256 is water, the higher x is the more water is there
                    s.set_at((xi, yi), (19, 86, 134))
                else:  #lava is -256>x>0
                    s.set_at((xi, yi), (150, 35, 17))
                if tile in mark:
                    if multi == None:
                        render[tile].append((xi, yi, multi))
                    elif multi[0] % 36 == 0 and multi[1] == 0:
                        render[tile].append((xi, yi, multi))
            if xi % 100 == 0:  # every ten slices print the progress
                if name == None:
                    print("done %5d of %5d\r" % (xi, x))
                else:
                    print("done %5d of %5d, of %s" % (xi, x, name))

    for tile in render:
        for pos in render[tile]:


            if tile == 21:
                if pos[2][0] % 36 == 0 and pos[2][1] == 0:
                    kind = pos[2][0] // 36
                    try:
                        s.blit(chests[kind], (pos[0] - chestsizes[kind][0] // 2, pos[1] - chestsizes[kind][1] // 2))
                    except IndexError:
                        kind = 0
                        s.blit(chests[kind], (pos[0] - chestsizes[kind][0] // 2, pos[1] - chestsizes[kind][1] // 2))
            else:
                i = images[tile]
                size = i.get_size()
                s.blit(i, (pos[0] - size[0] // 2, pos[1] - size[1] // 2))
    try:
        if outputpath == None:
            pa = path[:-3] + "png"
        else:
            pa = outputpath[:-3] + "png"
        pygame.image.save(s, pa)
    except:  # if pygame was not build with additional image types, we go with with bmp which is guaranteed to exist
        if outputpath == None:
            pa = path[:-3] + "bmp"
        else:
            pa = outputpath[:-3] + "bmp"
        pygame.image.save(s, pa)  # save the map and exit
    if name:
        print("completed mapping " + name)
    else:
        print("Completed mapping a World! ")
    return pa


if __name__ == "__main__":
    freeze_support()
    # sys.argv.append("mark")# remove the # if you dont want to specify mark via command line

    if "mark" in sys.argv:
        mark = True
    else:
        mark = False

    make = None
    #make = "world1.wld"
    if make:
        make_map(make)
    done = False
    for world in sys.argv[1:]:
        if world[-3:] == "wld":
            make_map(sys.argv[1])
            done = True

    if done:
        pass
    else:
        import os

        try:
            # get the my documents folder in windows. on other OS it will fail somewhere
            import ctypes

            dll = ctypes.windll.shell32
            buf = ctypes.create_unicode_buffer(300)
            dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)

            p = os.path.join(buf.value, "My Games", "Terraria", "Worlds")
        except:
            p = os.path.expanduser("~/My Games/Terraria/Worlds")
        processes = []
        for item in os.listdir(p):
            if item[-3:] == "wld":

                if "drop_low" in sys.argv:
                    pos = os.path.join("..", item)
                else:
                    pos = item
                pro = Process(target=make_map, name=item,
                              args=(os.path.join(p, item), pos, mark, item, False))
                pro.start()
                processes.append(pro)
        while len(processes) > 0:

            dead = []
            for p in processes:
                #print (p)
                if not p.is_alive(): dead.append(p)
            for d in dead:
                d.join()
                processes.remove(d)
            time.sleep(1)
        print("All tasks done")
        time.sleep(5)
