"""Higher level interface to Terraria data, based on the low level interface tlib"""
import sys
import io
import os
import tempfile
import appdirs

from pathlib import Path
from itertools import count, chain

from .database import multitiles, multitilestrides
from .tlib import *


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

    def set_multi_2x2(tid, f):
        stride = multitilestrides[tid]
        surf = pygame.surface.Surface((2, 2))
        surf.set_at((0, 0), (tid, f * 2, 0))
        surf.set_at((0, 1), (tid, f * 2, 1))
        surf.set_at((1, 0), (tid, 1 + f * 2, 0))
        surf.set_at((1, 1), (tid, 1 + f * 2, 1))
        return surf
    def set_multi_generic(x,y, tid, x_entry, y_entry):
        stride = multitilestrides[tid]
        surf = pygame.surface.Surface((x, y))
        for xi in range(x):
            for yi in range(y):
                surf.set_at((xi,yi), (tid, x*x_entry+xi, y*y_entry+yi))
        return surf
    types = {"goldchest": set_multi_2x2(21, 1),
             "woodchest": set_multi_2x2(21, 0),
             "goldlockchest": set_multi_2x2(21, 2),
             "shadowchest": set_multi_2x2(21, 3),
             "shadowlockchest": set_multi_2x2(21, 4),
             "barrelchest": set_multi_2x2(21, 5),
             "canchest": set_multi_2x2(21, 6),
             "ebonwoodchest" : set_multi_2x2(21, 7),
             "mahoganywoodchest" : set_multi_2x2(21, 8),
             "bonechest" : set_multi_2x2(21, 9),
             "ivychest" : set_multi_2x2(21, 10),
             "icechest" : set_multi_2x2(21, 11),
             "livingwoodchest" : set_multi_2x2(21, 12),
             "skychest" : set_multi_2x2(21, 13),
             "shadewoodchest" : set_multi_2x2(21, 14),
             "webbedchest" : set_multi_2x2(21, 15),
             "lihzahrdchest" : set_multi_2x2(21, 16),
             "waterchest" : set_multi_2x2(21, 17),
             "bjunglechest" : set_multi_2x2(21, 18),
             "bcorruptionchest" : set_multi_2x2(21, 19),
             "bcrimsonchest" : set_multi_2x2(21, 20),
             "bhallowedchest" : set_multi_2x2(21, 21),
             "bicechest" : set_multi_2x2(21, 22),
             "blockedjunglechest" : set_multi_2x2(21, 23),
             "blockedcorruptionchest" : set_multi_2x2(21, 24),
             "blockedcrimsonchest" : set_multi_2x2(21, 25),
             "blockedhallowedchest" : set_multi_2x2(21, 26),
             "blockedicechest" : set_multi_2x2(21, 27),
             "shadoworb" : set_multi_2x2(31, 0),

             }

    # make demonaltar
    types["altar"] = set_multi_generic(3,2,26,0,0)
    # make hellfurnace

    types["hellfurnace"] = set_multi_generic(3,2,77,0,0)
    return types


def get_myterraria():
    import os

    if os.name == "nt":
        # get the my documents folder in windows. on other OS it will fail somewhere
        import ctypes

        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(300)
        dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)

        p = Path(buf.value) / "My Games" / "Terraria"
    else:
        p = appdirs.user_data_dir('Terraria')
    return Path(p)


def get_steamdir():
    if os.name == "nt":
        import winreg
        opened = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Valve\Steam")
        path = winreg.QueryValueEx(opened, "SteamPath")[0]
    else:
        path = Path(os.path.expanduser('~')) / ".steam" / "steam"

    return Path(path)

cloud_warning_flag = 0
def get_remote_terraria_dirs(sub_dir=""):
    global cloud_warning_flag
    userdatadir = get_steamdir() / 'userdata'
    if (userdatadir).is_dir():
        for p in (userdatadir).iterdir():
            r = p / '105600' / 'remote'
            yield r / sub_dir  # (r / "") -> r

    elif not cloud_warning_flag:
        print("Could not get online worlds from {}.".format(userdatadir))
        cloud_warning_flag = 1


def get_worlds(source = "vanilla"):
    """Get World files from a certain folder,
    source locations:
    'N' #not implemented
    'vanilla'
    'tApi' #not implemented
    """
    local = get_myterraria() / "Worlds"
    remotes = [remote.iterdir() for remote in get_remote_terraria_dirs('worlds') if remote.is_dir()]
    for item in chain(local.iterdir(), *remotes):
        if item.is_file() and item.suffix == ".wld":
            yield item


def get_players():
    local = get_myterraria() / "Players"
    remotes = [remote.iterdir() for remote in get_remote_terraria_dirs('players') if remote.is_dir()]
    for item in chain(local.iterdir(), *remotes):
        if item.is_file() and item.suffix == ".plr":
            yield item


def get_next_world(name=None):
    if name:
        p = get_myterraria() / "Worlds" / "{}.wld".format(name)
        if not p.is_file():
            return p
    # fall back to calling it worldX.wld if the specific name already exists
    for x in count(1):
        p = get_myterraria() / "Worlds" / "world{}.wld".format(x)
        if not p.is_file():
            return p


def write_tiles(surface, header, walls={}, report=False, overwrite_no_mt = set(),callback = None):
    import pygame
    total = header["width"] * header["height"]

    short = 100.0 / total
    cache = {}
    a = tempfile.SpooledTemporaryFile(10000000)
    y = 0
    wordzero = set_ushort(0)
    pxarray = pygame.PixelArray(surface)
    # with open(n , "wb") as a:#write the tile data
    for x in range(header["width"]):
        y = 0
        while y < header["height"]:
            c = pxarray[x, y]
            amount = 0
            while y < header["height"] - 1 - amount and c == pxarray[x, y + 1 + amount]:
                amount += 1

            c = pygame.Color(c)[1:]
            if c in cache:
                a.write(cache[c])
            else:
                tiledata = io.BytesIO()
                if c[0] == 255:
                    set_tile_no_amount(tiledata, (None, None, 0, None))
                elif c[0] == 254:  #liquid
                    if c[1]:  #if lava
                        set_tile_no_amount(tiledata, (None, None, -c[2], None))
                    else:
                        set_tile_no_amount(tiledata, (None, None, c[2], None))
                elif c[0] == 253:  #liquid
                    if c[1]:  #if lava
                        set_tile_no_amount(tiledata, (None, 1, -c[2], None))
                    else:
                        set_tile_no_amount(tiledata, (None, 1, c[2], None))
                elif c[0] == 252:#just Wall
                    set_tile_no_amount(tiledata, (None, c[1], 0, None))
                elif c[0] > 230:  #only have a wall
                    set_tile_no_amount(tiledata, (None, c[0] - 230, 0, None))
                elif c[0] in multitiles and c[0] not in overwrite_no_mt:  #if it has multitiledata.. i hate those
                    stride = multitilestrides[c[0]]
                    set_tile_no_amount(tiledata, (c[0], walls[c[0]], 0, (c[1]*stride, c[2]*stride)))
                elif c[0] in walls:  #put down background walls if we want them
                    set_tile_no_amount(tiledata, (c[0], walls[c[0]], 0, None), c[0] in overwrite_no_mt)
                else:  #or just write a nice normal tile
                    set_tile_no_amount(tiledata, (c[0], None, 0, None))
                value = tiledata.getvalue()
                a.write(value)
                cache[c] = value

            if amount:
                y += amount
                a.write(set_ushort(amount - 1))
            else:
                y += 1
                a.write(wordzero)

        if report and x % 100 == 0:
            progress = (((x * header["height"] + y)) * short)
            st = "%6.2f%% done writing tiles" % progress
            if callback:callback.set_progress(50+progress/2)
            print(st)
    if report: print("done writing tiles        ")
    return a
