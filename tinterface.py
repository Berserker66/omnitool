import sys
import os
import tempfile

from tlib import *


is_exe = hasattr(sys, "frozen")


class Tiles():
    def __init__(self, path, pos, w, h):
        self.path = path
        self.w = w
        self.pos = pos
        self.endpos = None
        self.h = h

    def __len__(self):
        return self.w * self.h

    def __iter__(self):
        with open(self.path, "rb") as f:
            f.seek(self.pos)
            for xi in range(self.w):
                for yi in range(self.h):
                    yield get_tile(f)
            self.endpos = f.tell()


class Chests():
    def __init__(self, path, pos):
        self.path = path
        self.pos = pos
        self.endpos = None

    def __len__(self):
        return 1000

    def __iter__(self):
        with open(self.path, "rb") as f:
            f.seek(self.pos)
            for x in range(1000):
                yield get_chest(f)
            self.endpos = f.tell()


class Signs():
    def __init__(self, path, pos):
        self.path = path
        self.pos = pos
        self.endpos = None

    def __len__(self):
        return 1000

    def __iter__(self):
        with open(self.path, "rb") as f:
            f.seek(self.pos)
            for x in range(1000):
                s = get_sign(f)
                # print s[0][0] == "\x01"
                #print s[0][0]
                yield s
            self.endpos = f.tell()


class NPCs():
    def __init__(self, path, pos):
        self.path = path
        self.pos = pos
        self.endpos = None
        for x in self:
            pass

    def __len__(self):
        return self.len

    def __iter__(self):
        with open(self.path, "rb") as f:
            f.seek(self.pos)
            i = 0
            while 1:
                npc = get_npc(f)
                if npc:
                    i += 1
                    yield npc

                else:
                    self.endpos = f.tell()
                    break
        self.len = i


class Trail():
    def __init__(self, path, pos):
        self.path = path
        self.pos = pos

    def get(self):
        with open(self.path, "rb") as f:
            return get_byte(f), get_string(f), get_int(f)  # (1,name, ID)


class World():
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as f:
            self.header = get_header(f)[0]
            self.tilepos = f.tell()
        self.tiles = Tiles(path, self.tilepos, self.header["width"], self.header["height"])

    def ready_chests(self):
        if self.tiles.endpos != None:
            self.chestpos = self.tiles.endpos
        else:
            for x in self.tiles:
                pass
            self.chestpos = self.tiles.endpos
        self.chests = Chests(self.path, self.chestpos)

    def ready_signs(self):
        if self.tiles.endpos != None:
            self.chestpos = self.tiles.endpos

        else:
            for x in self.tiles:
                pass
            self.chestpos = self.tiles.endpos
        if not hasattr(self, "chests"):
            self.chests = Chests(self.path, self.chestpos)
        if self.chests.endpos != None:
            self.signpos = self.chests.endpos
        else:
            for x in self.chests:
                pass
            self.signpos = self.chests.endpos
        self.signs = Signs(self.path, self.signpos)

    def ready_npcs(self):
        if self.tiles.endpos != None:
            self.chestpos = self.tiles.endpos

        else:
            for x in self.tiles:
                pass
            self.chestpos = self.tiles.endpos
        if not hasattr(self, "chests"):
            self.chests = Chests(self.path, self.chestpos)
        if self.chests.endpos != None:
            self.signpos = self.chests.endpos
        else:
            for x in self.chests:
                pass
            self.signpos = self.chests.endpos
        if not hasattr(self, "signs"):
            self.signs = Signs(self.path, self.signpos)
        if self.signs.endpos != None:
            self.npcpos = self.signs.endpos
        else:
            for x in self.signs:
                pass
            self.npcpos = self.signs.endpos
        self.npcs = NPCs(self.path, self.npcpos)

    def make_split(self):
        self.ready_npcs()
        import binarysplit as bs  # aka bullshit

        bs.split(self.path, [self.tilepos, self.chestpos, self.signpos, self.npcpos, self.npcs.endpos])


def get_content(f, layers=5):  # not done yet
    with open(f, "rb") as f:
        header = get_header(f)[0]
        if layers > 1:
            tiles = get_tiles(f, header["width"], header["height"])
        else:
            return (header,)
    return header, tiles


def get_multis():
    import pygame

    def set_multi_18(tid, f):
        surf = pygame.surface.Surface((2, 2))
        surf.set_at((0, 0), (tid, f * 36, 0))
        surf.set_at((0, 1), (tid, f * 36, 18))
        surf.set_at((1, 0), (tid, 18 + f * 36, 0))
        surf.set_at((1, 1), (tid, 18 + f * 36, 18))
        return surf

    types = {"goldchest": set_multi_18(21, 1),
             "woodchest": set_multi_18(21, 0),
             "goldlockchest": set_multi_18(21, 2),
             "shadowchest": set_multi_18(21, 3),
             "shadowlockchest": set_multi_18(21, 4),
             "barrelchest": set_multi_18(21, 5),
             "canchest": set_multi_18(21, 6),
             #beyond 6*18 cant be mapped yet
             #"ebonwoodchest" : set_multi_18(21, 7),
             #"mahoganywoodchest" : set_multi_18(21, 8),
             #"bonechest" : set_multi_18(21, 9),
             #"ivychest" : set_multi_18(21, 10),
             #"icechest" : set_multi_18(21, 11),
             #"livingwoodchest" : set_multi_18(21, 12),
             #"skychest" : set_multi_18(21, 13),
             #"shadewoodchest" : set_multi_18(21, 14),
             #"webbedchest" : set_multi_18(21, 15),
             #"lihzahrdchest" : set_multi_18(21, 16),
             #"waterchest" : set_multi_18(21, 17),
             #"bjunglechest" : set_multi_18(21, 18),
             #"bcorruptionchest" : set_multi_18(21, 19),
             #"bcrimsonchest" : set_multi_18(21, 20),
             #"bhallowedchest" : set_multi_18(21, 21),
             #"bicechest" : set_multi_18(21, 22),
             "shadoworb" : set_multi_18(31, 0),

             }

    # make altar
    shadowsurf = pygame.surface.Surface((3, 2))
    shadowsurf.set_at((0, 0), (26, 0, 0))
    shadowsurf.set_at((0, 1), (26, 0, 18))
    shadowsurf.set_at((1, 0), (26, 18, 0))
    shadowsurf.set_at((1, 1), (26, 18, 18))
    shadowsurf.set_at((2, 0), (26, 36, 0))
    shadowsurf.set_at((2, 1), (26, 36, 18))
    types["altar"] = shadowsurf
    # make hellfurnace
    hellsurf = pygame.surface.Surface((3, 2))
    hellsurf.set_at((0, 0), (77, 0, 0))
    hellsurf.set_at((0, 1), (77, 0, 18))
    hellsurf.set_at((1, 0), (77, 18, 0))
    hellsurf.set_at((1, 1), (77, 18, 18))
    hellsurf.set_at((2, 0), (77, 36, 0))
    hellsurf.set_at((2, 1), (77, 36, 18))
    types["hellfurnace"] = hellsurf
    return types


def get_myterraria():
    import os

    try:
        # get the my documents folder in windows. on other OS it will fail somewhere
        import ctypes

        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(300)
        dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)

        p = os.path.join(buf.value, "My Games", "Terraria")
    except:
        p = os.path.expanduser("~/My Games/Terraria")
    return p


def get_worlds(tconfig=False):
    worlds = []
    try:
        # get the my documents folder in windows. on other OS it will fail somewhere
        import ctypes

        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(300)
        dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)

        if tconfig:
            p = os.path.join(buf.value, "My Games", "Terraria", "Worlds", "tConfig")
        else:
            p = os.path.join(buf.value, "My Games", "Terraria", "Worlds")
    except:
        if tconfig:
            p = os.path.expanduser("~/My Games/Terraria/Worlds/tConfig")
        else:
            p = os.path.expanduser("~/My Games/Terraria/Worlds")
    if tconfig:
        for item in os.listdir(p):
            if item[-3:] == "zip":
                worlds.append(item)
    else:
        for item in os.listdir(p):
            if item[-3:] == "wld":
                worlds.append(item)
    return p, worlds


def get_players():
    players = []
    try:
        # get the my documents folder in windows. on other OS it will fail somewhere
        import ctypes

        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(300)
        dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)

        p = os.path.join(buf.value, "My Games", "Terraria", "Players")
    except:
        p = os.path.expanduser("~/My Games/Terraria/Players")

    for item in os.listdir(p):
        if item[-3:] == "plr":
            players.append(item)
    return p, players


def get_next_world(cmod=False):
    path, worlds = get_worlds(cmod)
    # if len(worlds) > 4:
    #    x = 1
    #    while 1:
    #        if not os.path.isfile("world%d.wld" % x):break
    #        else:x += 1
    #    return "world%d.wld" % x
    #else:
    x = 1
    while 1:
        if not os.path.isfile(os.path.join(path, "world%d.wld" % x)):
            break
        else:
            x += 1
    return os.path.join(path, "world%d.wld" % x)


def write_tiles(surface, header, walls={}, report=False):
    total = header["width"] * header["height"]
    part = header["height"] * 50
    short = 100.0 / total

    a = tempfile.SpooledTemporaryFile(10000000)
    y = 0
    wordzero = set_ushort(0)
    # with open(n , "wb") as a:#write the tile data
    for x in range(header["width"]):
        y = 0
        while y < header["height"]:
            c = surface.get_at((x, y))
            amount = 0
            while y < header["height"] - 1 - amount and c == surface.get_at((x, y + 1 + amount)):
                amount += 1

            if c[0] == 255:
                set_tile_no_amount(a, (None, None, 0, None))
            elif c[0] == 254:  #liquid
                if c[1]:  #if lava
                    set_tile_no_amount(a, (None, None, -c[2], None))
                else:
                    set_tile_no_amount(a, (None, None, c[2], None))
            elif c[0] == 253:  #liquid
                if c[1]:  #if lava
                    set_tile_no_amount(a, (None, 1, -c[2], None))
                else:
                    set_tile_no_amount(a, (None, 1, c[2], None))
            elif c[0] == 252:
                set_tile_no_amount(a, (None, c[1], 0, None))
            elif c[0] in db.multitiles:  #if it has multitiledata.. i hate those
                set_tile_no_amount(a, (c[0], walls[c[0]], 0, (c[1], c[2])))
            elif c[0] in walls:  #put down background walls if we want them
                set_tile_no_amount(a, (c[0], walls[c[0]], 0, None))
            elif c[0] > 230:  #only have a wall
                set_tile_no_amount(a, (None, c[0] - 230, 0, None))
            else:  #or just write a nice normal tile
                set_tile_no_amount(a, (c[0], None, 0, None))
            if amount:
                y += amount
                #a.seek(-2, 1)
                a.write(set_ushort(amount - 1))
            else:
                y += 1
                a.write(wordzero)
                #print (amount)
        if report:
            if x % 100 == 0:
                st = "%6.2f%% done writing tiles" % (((x * header["height"] + y)) * short)
                if is_exe:
                    sys.stdout.write(st + "\b" * 26)
                else:
                    print(st)
    if report: print("done writing tiles        ")
    return a
