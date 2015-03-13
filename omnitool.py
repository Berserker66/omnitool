#! python3.4-32
if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
__version__ = 17
import sys
import os

if "APPDATA" in os.environ:
    appdata = os.path.join(os.environ["APPDATA"], "Omnitool")
else:
    appdata = os.path.join(os.environ["HOME"], "Omnitool")
temp = os.path.join(appdata, "temp")
cachepath = os.path.join(appdata, "cache.dill")
for p in (appdata, temp):
    if not os.path.isdir(p):
        os.mkdir(p)

import zlib
import pickle

try:
    with open(cachepath, "rb") as f:
        cache = pickle.loads(zlib.decompress(f.read()))
except IOError as e:
    print("Unable to load cache (" + e.__class__.__name__ + "), creating new cache")

    cache = {"worlds": {}, "backup": {}}
    with open(cachepath, "wb") as f:
        f.write(zlib.compress(pickle.dumps(cache, 2), 9))
except Exception as e:
    print("Unable to load cache (" + e.__class__.__name__ + "), creating new cache")

    cache = {"worlds": {}, "backup": {}}
    with open(cachepath, "wb") as f:
        f.write(zlib.compress(pickle.dumps(cache, 2), 9))

if "reset" in sys.argv:
    cache = {"worlds": {}}
    sys.argv.remove("reset")
if "theme" in cache:
    themename = cache["theme"]
else:
    themename = "Blue"
if "thumbsize" in cache:
    thumbsize = cache["thumbsize"]
else:
    thumbsize = (420.0, 120.0)
    cache["thumbsize"] = (420, 120)
if "backup" not in cache:
    cache["backup"] = {}
if "do_backup" not in cache:
    cache["do_backup"] = True
if "columns" not in cache:
    cache["columns"] = 3
if "lang" not in cache:
    cache["lang"] = "english"
if "version" not in cache:
    cache["version"] = __version__
    cache["worlds"] = {}
if os.path.isfile("custom.py"):
    sys.path.append(".")
    exec("import custom as lang")
    sys.path.remove(".")
else:
    command = "import Language." + cache["lang"] + " as lang"
    exec(command)

if __name__ == "__main__":

    global processes
    processes = []


    # print (sys.argv)
    if not '--multiprocessing-fork' in sys.argv:

        try:
            import splashlib

            splashlib.splash((512, 512), os.path.join("themes", themename, "splash.png"))
        except Exception as e:
            print("SplashWarning: " + str(e))
    else:
        pass
import pygame


# for python 2/3 compatibility
try:
    import pygame._view
except ImportError:
    pass
#print (os.environ['SDL_VIDEODRIVER'])
if sys.platform.startswith("win"):
    os.environ['SDL_VIDEODRIVER'] = "windib"
from pgu import gui
from tinterface import *
from tinterface import World as tWorld
import colorlib
from tlib import *
import tlib  #multiprocessing issues when frozen
import threading
import time
import pgu_override
import pgu.gui.surface as pgusur

import subprocess
import shutil
import sys
import npcadd
import webbrowser

if sys.platform.startswith("win"):
    from ctypes import windll
import struct
import tempfile
import zipfile
import json
from itertools import product

bit = struct.calcsize("P") * 8

outdated = False


def myupdate(self, s):
    updates = []

    if self.myfocus: self.toupdate[self.myfocus] = self.myfocus

    for w in self.topaint:
        if w is self.mywindow:
            continue
        else:
            sub = pgusur.subsurface(s, w.rect)
            #if (hasattr(w, "_container_bkgr")):
            #    sub.blit(w._container_bkgr,(0,0))
            w.paint(sub)
            updates.append(pygame.rect.Rect(w.rect))
    while 1:
        try:
            for w in self.toupdate:
                if w is self.mywindow:
                    continue
                else:
                    us = w.update(pgusur.subsurface(s, w.rect))
                if us:
                    for u in us:
                        updates.append(pygame.rect.Rect(u.x + w.rect.x, u.y + w.rect.y, u.w, u.h))
            break
        except RuntimeError:
            pass
    for w in self.topaint:
        if w is self.mywindow:
            w.paint(self.top_surface(s, w))
            updates.append(pygame.rect.Rect(w.rect))
        else:
            continue

    for w in self.toupdate:
        if w is self.mywindow:
            us = w.update(self.top_surface(s, w))
        else:
            continue
        if us:
            for u in us:
                updates.append(pygame.rect.Rect(u.x + w.rect.x, u.y + w.rect.y, u.w, u.h))

    self.topaint = {}
    self.toupdate = {}

    return updates


gui.container.Container.update = myupdate

#for exe bundling
t = False
if t:
    from Language import english, german, portuguese, czech, french, spanish, japanese, norwegian, danish

cache_lock = threading.Lock()


def save_cache():
    cache_lock.acquire()
    #print (cache)
    d = zlib.compress(pickle.dumps(cache), 9)
    with open(cachepath, "wb") as f:
        f.write(d)
    cache_lock.release()


cmod = False
if len(sys.argv) > 1:  #user wants something
    if sys.argv[1].split("\\")[-1] == "TEdit.exe":  #install tedit
        cache["tedit"] = sys.argv[1]
        print("Learned TEdit path: " + sys.argv[1])
        save_cache()
        pygame.quit()
        sys.exit()
    elif sys.argv[1].split("\\")[-1] == "Terrafirma.exe":  #install tedit
        cache["terrafirma"] = sys.argv[1]
        print("Learned terrafirma path: " + sys.argv[1])
        save_cache()
        pygame.quit()
        sys.exit()
myterraria = get_myterraria()  #mygames-terraria path
images = os.path.join(myterraria, "WorldImages")
if __name__ == "__main__":
    try:
        import render
    except:
        if not '--multiprocessing-fork' in sys.argv:
            print("WorldRender extension not available:")
            import traceback

            traceback.print_exc()
        render_ext = False
    else:
        render_ext = True


def runrender(world):
    args = (world.header, world.file, False, (world.header, world.pos), None)
    p = multiprocessing.Process(target=render.run, name="WorldRender", args=args)
    p.start()
    processes.append(p)


if not os.path.exists(images):
    os.makedirs(images)
try:
    os.mkdir(os.path.join(myterraria, "Worlds"))
except:
    pass


class Theme(gui.Theme):
    def __init__(self, name):
        try:
            gui.Theme.__init__(self, os.path.join("themes", name))
        except:
            print("Warning: Unable to load selected theme")
            themes = os.listdir("themes")
            for name in themes:
                try:
                    gui.Theme.__init__(self, os.path.join("themes", name))
                except:
                    pass
                else:
                    break


shutdown = False


def exit_prog(p):
    global shutdown
    shutdown = True
    pygame.quit()
    import sys

    sys.exit()


def nothing(p):
    pass


class GenButton(gui.Button):
    def __init__(self, name, gen, width=100, disabled=False):
        gui.Button.__init__(self, name, width=width)

        self.connect(gui.CLICK, start_proc, bind[gen])
        self.disabled = disabled
        self.blur()


def start_proc(func):
    #print(func)
    if func[1].__class__.__name__ == "list":
        p = multiprocessing.Process(target=func[0], name=func[1][0],
                                    args=(func[1][1],))
    else:
        p = multiprocessing.Process(target=func[0], name=func[1])  #, args = (to_self,))
    p.start()
    processes.append(p)


class Button(gui.Button):
    def __init__(self, name, func, world_id, width=100):
        gui.Button.__init__(self, name, width=width)
        self.connect(gui.CLICK, func, world_id)


class Language(gui.Dialog):
    def __init__(self, n=None):
        main = gui.Table()
        gui.Dialog.__init__(self, gui.Label("Language"), main)

        liste = gui.List(200, 100)
        langs = languages = ["german", "english", "portuguese", "czech",
                             "spanish", "french", "norwegian", "japanese", "danish"]
        langnames = languages = ["German", "English", "Portuguese (BR)", "Czech",
                                 "Spanish", "French", "Norwegian", "Japanese", "Danish"]
        for name, dire in zip(langnames, langs):
            liste.add(name, value=dire)
        self.liste = liste
        self.liste.value = cache["lang"]
        main.td(self.liste)

        self.open()

    def close(self, w=None):
        cache["lang"] = self.liste.value
        save_cache()
        gui.Dialog.close(self, w)


class Settings(gui.Dialog):
    def __init__(self, n=None):

        main = gui.Table()
        gui.Dialog.__init__(self, gui.Label(lang.settings), main)

        liste = gui.List(200, 114)
        liste.value = themename
        themes = os.listdir("themes")
        for dire in themes:
            liste.add(dire, value=dire)
        self.liste = liste

        liste = gui.Select()
        liste.value = cache["columns"]
        for x in (1, 2, 3, 4, 5):
            liste.add(str(x), value=x)
        self.columns = liste

        backupswitch = gui.Switch()
        backupswitch.value = cache["do_backup"]
        self.backup = backupswitch
        sizelist = gui.Select(value=thumbsize)
        sizelist.add(lang.none, 0)
        sizelist.add(lang.small, (420.0, 120.0))
        sizelist.add(lang.medium, (630.0, 180.0))
        sizelist.add(lang.large, (840.0, 240.0))
        sizelist.add(lang.very_large, (1260.0, 360.0))
        self.sizelist = sizelist
        main.td(gui.Label(lang.warning, color=(127, 0, 0)), colspan=2)
        main.tr()
        main.td(gui.Label(lang.theme_select))
        main.td(gui.Label(lang.thumbsize))
        main.tr()
        main.td(self.liste, rowspan=5)
        main.td(sizelist)
        main.tr()
        #main.td(gui.Spacer(1,1))
        main.td(gui.Label(lang.world_columns), col=1, row=3)
        main.tr()
        main.td(self.columns, col=1, row=4)
        main.tr()
        main.td(gui.Label(lang.mk_backups), col=1, row=5)
        main.tr()

        #main.td(gui.Spacer(1,1))
        main.td(backupswitch, col=1, row=6)

        self.open()

    def close(self, w=None):
        cache["theme"] = self.liste.value
        cache["thumbsize"] = self.sizelist.value
        cache["do_backup"] = self.backup.value
        cache["columns"] = self.columns.value
        save_cache()
        gui.Dialog.close(self, w)


class World():
    def __init__(self, path, filename):
        self.file = os.path.join(path, filename)
        self.filename = filename
        self.path = path
        with open(self.file, "rb") as f:
            self.header, self.multiparts = get_header(f)
            self.pos = f.tell()


        self.size = gui.Label(str(self.header["width"]) + "X" + str(self.header["height"]) + " tiles")
        self.label = gui.Label(self.header["name"])

        if thumbsize:
            self.info = gui.Table(width=thumbsize[0])
        else:
            self.info = gui.Table(width=420)
        self.info.td(self.label, align=-1)
        if self.header["hardmode"]:
            self.info.td(gui.Label("Hardmode", color=(250, 0, 0)), align=0)
        self.info.td(self.size, align=1)
        self.raw = pygame.surface.Surface((self.header["width"], self.header["height"]))
        self.raw.fill((100, 100, 100))
        self.thumbsize = thumbsize
        ##buttons
        self.save = Button("Save Image", nothing, self)
        self.npcs = Button("Edit NPCs", nothing, self)
        self.chests = Button("Edit Chests", nothing, self)
        self.save.disabled = True
        self.save.blur()
        self.npcs.disabled = True
        self.npcs.blur()
        self.chests.disabled = True
        self.chests.blur()
        if thumbsize:
            self.get_thumb()
            self.image = gui.Image(self.thumb)
            if render_ext:
                self.image.connect(gui.CLICK,
                                   runrender,
                                   self)

            self.get_worldview()

    def get_thumb(self, size=thumbsize):
        i_size = self.raw.get_size()
        scale = min(size[0] / i_size[0], size[1] / i_size[1])
        self.thumb = pygame.transform.rotozoom(self.raw, 0, scale)

    def update_thumb(self, size=None):
        if size == None:
            size = self.thumbsize
        i_size = self.raw.get_size()
        scale = min(size[0] / i_size[0], size[1] / i_size[1])
        i = pygame.transform.rotozoom(self.raw, 0, scale)
        self.thumb.blit(i, (0, 0))

    def override_thumb(self, size=thumbsize):
        i_size = self.raw.get_size()
        scale = min(size[0] / i_size[0], size[1] / i_size[1])
        self.thumb = pygame.transform.rotozoom(self.raw, 0, scale)
        self.image.change_image(self.thumb)

    def get_worldview(self):
        needed = False
        #i =proxyload(os.path.join(appdata,self.filename[:-3]+"png"))
        try:
            #raise AssertionError()
            if self.filename in cache["worlds"]:
                self.cache = cache["worlds"][self.filename]
                if os.path.getmtime(self.file) == self.cache["time"]:
                    i = proxyload(os.path.join(images, self.filename[:-3] + "png"))
                    #print ("Loaded Image for "+self.filename)
                else:
                    #print ("Image is outdated for "+self.filename)
                    raise IOError("Image is outdated")

            else:
                cache["worlds"][self.filename] = {"time": 0}
                self.cache = cache["worlds"][self.filename]
                #print ("Image does not exist for "+self.filename)
                raise IOError("Image does not exist")

        except:
            #print ("Can not load image for "+self.filename)
            needed = True
        else:
            self.raw.blit(i, (0, 0))
            self.update_thumb()
            self.save.disabled = False
            self.save.blur()
            self.npcs.disabled = False
            self.npcs.blur()
            self.chests.disabled = False
            self.chests.blur()
        save_cache()
        if needed:
            self.update_thumb()
            if False:  #stupid code, but here so I don't forget how to thread it
                t = Loader(self)
                first = False
            else:
                t = PLoader(self)
                t.name = "Vanilla-Mapper-%s" % self.header["name"]
            t.start()


def gen_slice(path, start, size, levels, version, queue=None):
    #import tlib
    if version > 100:
        get_tile = tlib.get_tile_buffered_iter_12_masked
    else:
        get_tile = tlib.get_tile_buffered_iter_12 if version >= 68 else tlib.get_tile_buffered_iter
    with open(path, "rb") as f:
        b = [0]
        f.seek(start)
        x, y = size  #read world size from header cache
        #s = pygame.surface.Surface((x,y)) #create a software surface to save tile colors in
        s = pygame.surface.Surface(size, depth=24)
        s.fill((200, 200, 255))
        pygame.draw.rect(s, (150, 75, 0),
                         ((0, levels[0]),
                          (size[0], size[1] - levels[0])))

        pygame.draw.rect(s, (50, 50, 50),
                         ((0, levels[1]),
                          (size[0], size[1] - levels[1])))
        for (xi, yi), (tile, wall, liquid, multi, wire) in zip(product(range(x), range(y)), get_tile(f, x * y)):

            #tiles start from the upper left corner, then go downwards
            # when a slice is complete its starts with the next slice

            #print(tile, wall, liquid, multi)
            if not liquid:  #liquid == 0 means no liquid
                # there could be a liquid and a tile, like a chest and water,
                #but I can only set one color to a pixel anyway, so I priotise the tile
                if tile == None:
                    if wall:
                        if wall in colorlib.walldata:
                            s.set_at((xi, yi), colorlib.walldata[wall])
                        else:
                            s.set_at((xi, yi), (wall, wall, wall))
                            #s.set_at((xi,yi), (255,255,255))#if no tile present, set it white

                elif tile in colorlib.data:
                    s.set_at((xi, yi), colorlib.data[tile])  #if colorlib has a color use it
                else:
                    tile = min(255, tile)
                    s.set_at((xi, yi), (tile, tile, tile))  #make a grey
            elif liquid > 512:
                s.set_at((xi, yi), (245, 219, 27))
            elif liquid > 256:
                s.set_at((xi, yi), (150, 35, 17))

            else:  #0>x>256 is water, the higher x is the more water is there
                s.set_at((xi, yi), (19, 86, 134))

                #pygame.image.saves, "image.png")
                #raise AssertionError()

        pos = f.tell()
        f.seek(start)
    if queue:
        queue.put((pygame.image.tostring(s, "RGB"), pos))
    else:
        return (pygame.image.tostring(s, "RGB"), pos)

processing = threading.Lock()


class PLoader(threading.Thread):
    def __init__(loader, world):
        threading.Thread.__init__(loader)
        loader.world = world

    def run(loader):
        import omnitool

        w = 50
        self = loader.world
        size = (self.header["width"], self.header["height"])
        #queue = multiprocessing.Queue()
        with processing:
            pool = multiprocessing.Pool(1)

        path = os.path.join(self.path, self.filename)

        levels = self.header["groundlevel"], self.header["rocklevel"]
        xi = 0
        version = self.header["version"]
        hw = self.header["width"]
        pos = self.pos

        while xi < hw:
            w = min(w, -xi + hw)
            p, pos = pool.apply(omnitool.gen_slice, ((path, pos, (w, self.header["height"]), levels, version)))
            p = pygame.image.fromstring(p, (w, self.header["height"]), "RGB")
            while self.raw.get_locked():  #if window is beeing rezized, keep waiting
                time.sleep(0.1)
            self.raw.blit(p, (xi, 0))
            self.update_thumb()
            self.image.repaint()
            xi += w
        pool.close()
        self.update_thumb()
        self.image.repaint()
        #pygame.image.save(self.raw, os.path.join(appdata,self.filename[:-3]+"png"))
        #shutil.copyfile(os.path.join(appdata,self.filename[:-3]+"png"),
        #                os.path.join(images,self.filename[:-3]+"png"))
        pygame.image.save(self.raw, os.path.join(images, self.filename[:-3] + "png"))

        self.cache["time"] = os.path.getmtime(self.file)
        save_cache()
        sys.exit()


class Loader(threading.Thread):
    def __init__(loader, world):
        threading.Thread.__init__(loader)
        loader.world = world

    def run(loader):
        self = loader.world
        with open(os.path.join(self.path, self.filename), "rb") as f:
            b = [0]
            #header = get_header(f)#read header with tlib.get_header and also reach tile data in f
            f.seek(self.pos)
            x, y = self.header["width"], self.header["height"]  #read world size from header cache
            #s = pygame.surface.Surface((x,y)) #create a software surface to save tile colors in
            s = self.raw
            s.fill((200, 200, 255))
            pygame.draw.rect(s, (150, 75, 0),
                             ((0, self.header["groundlevel"]),
                              (self.header["width"], self.header["height"] - self.header["groundlevel"])))

            pygame.draw.rect(s, (50, 50, 50),
                             ((0, self.header["rocklevel"]),
                              (self.header["width"], self.header["height"] - self.header["rocklevel"])))
            for xi in range(x):  # for each slice
                for yi in range(y):  # get the tiles
                    #tiles start from the upper left corner, then go downwards
                    # when a slice is complete its starts with the next slice

                    tile = get_tile_buffered(f, b)
                    tile, wall, liquid, multi, wire = tile

                    if not liquid:  #liquid == 0 means no liquid
                        # there could be a liquid and a tile, like a chest and water,
                        #but I can only set one color to a pixel anyway, so I priotise the tile
                        if tile == None:
                            if wall:
                                if wall in colorlib.walldata:
                                    s.set_at((xi, yi), colorlib.walldata[wall])
                                else:
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
                if xi % 50 == 0:  # every x slices show the progress
                    self.update_thumb()
                    self.image.repaint()

        self.update_thumb()
        self.image.repaint()
        pygame.image.save(s, os.path.join(appdata, self.filename[:-3] + "png"))
        shutil.copyfile(os.path.join(appdata, self.filename[:-3] + "png"),
                        os.path.join(images, self.filename[:-3] + "png"))
        self.cache["time"] = os.path.getmtime(self.file)
        save_cache()
        sys.exit()


def full_split(root):
    split = list(os.path.split(root))
    rsplit = [split[1]]
    while split[1] != "":
        split = os.path.split(split[0])
        rsplit.append(split[1])
    rsplit = rsplit[:-1]
    rsplit.append(split[0])
    rsplit.reverse()
    return rsplit


class Info(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global shutdown
        import time

        while 1:
            if shutdown: sys.exit()
            threads = threading.enumerate()
            x = len(threads)
            unneeded = ("SockThread", "Info")
            dead = False
            for thread in threads:
                if thread.name == "MainThread":
                    if not (thread.is_alive()): dead = True
                elif (thread.name) not in unneeded:

                    x -= 1
            if x <= 2 and dead and len(processes) == 0:
                if not shutdown:
                    print("All important threads have exited, full shutdown in 15 seconds")
                    time.sleep(15)
                sys.exit()
            #print ("alive")
            dead = []
            for p in processes:
                #print (p.exitcode, p.is_alive())
                #print (p)
                if not p.is_alive(): dead.append(p)
            for d in dead:
                d.join()
                processes.remove(d)
            time.sleep(1)
        sys.exit()


class Backupper(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dest = os.path.join(myterraria, "WorldsBackup")
        if not os.path.exists(dest):
            os.mkdir(dest)

        #source = os.path.join("C:\program files (x86)\\steamapps\common\Terraria")
        try:
            worlds = get_worlds()
        except:
            worlds = [None, []]
            print("BackUpper has found no worlds")
        for f in worlds[1]:
            path = (os.path.join(worlds[0], f))
            if f in cache["backup"]:
                t = os.path.getmtime(path)
                if t != cache["backup"]:
                    s = time.strftime("%SS_%MM_%HH_%dD_%b_%YY.", time.localtime(t))
                    shutil.copy(path, os.path.join(dest, s + f))
                    cache["backup"][f] = t
            else:
                t = os.path.getmtime(path)
                s = time.strftime("%SS_%MM_%HH_%dD_%b_%YY.", time.localtime(t))
                shutil.copy(path, os.path.join(dest, s + f))
                cache["backup"][f] = t

        dest = os.path.join(myterraria, "PlayersBackup")
        if not os.path.exists(dest):
            os.mkdir(dest)
        try:
            players = get_players()
        except:
            players = [None, []]
            print("BackUpper has found no player files")
        for f in players[1]:
            path = (os.path.join(players[0], f))
            if f in cache["backup"]:
                t = os.path.getmtime(path)
                if t != cache["backup"]:
                    s = time.strftime("%SS_%MM_%HH_%dD_%b_%YY.", time.localtime(t))
                    shutil.copy(path, os.path.join(dest, s + f))
                    cache["backup"][f] = t
            else:
                t = os.path.getmtime(path)
                s = time.strftime("%SS_%MM_%HH_%dD_%b_%YY.", time.localtime(t))
                shutil.copy(path, os.path.join(dest, s + f))
                cache["backup"][f] = t

        print("Backups made")
        sys.exit()
        save_cache()


def launch_terraria(arg=""):
    dest = os.path.join(appdata, "Terraria")
    source = get_t_path()
    if source == False:
        webbrowser.open(
            "http://www.terrariaonline.com/threads/omnitool-world-mapping-backups-creation-and-more-released.61654/page-19#post-1501847")
        raise RuntimeError("Terraria not found, opening a guide to set path")
    source = source.lower()
    dest = dest.lower()
    if os.path.isdir(dest):
        print("checking Terraria for changes")
        for root, dirs, files in os.walk(source):
            rsplit = full_split(root)
            ssplit = full_split(source)
            #print (rsplit, ssplit)
            for name in ssplit:
                rsplit.remove(name)
            d = (os.path.join(dest, *rsplit))
            s = (os.path.join(source, *rsplit))
            for direc in dirs:
                if not os.path.isdir(os.path.join(d, direc)):
                    os.mkdir(os.path.join(d, direc))
            for file in files:
                so = os.path.join(s, file)
                de = os.path.join(d, file)
                if not os.path.isfile(de):
                    shutil.copy2(so, de)
                elif abs(os.path.getmtime(so) - os.path.getmtime(de)) > 1:
                    shutil.copy2(so, de)

    else:
        print("Copying Terraria to isolated location")
        shutil.copytree(source, dest)

    print("impersonating steam")
    shutil.copy("steam_api.dll", dest)
    print("launching Terraria")
    subprocess.Popen(os.path.join(dest, "Terraria.exe") + arg,
                     cwd=dest)


class Updater(threading.Thread):
    def __init__(self, update):
        threading.Thread.__init__(self)
        self.update = update

    def run(self):
        import urllib.request

        f = urllib.request.urlopen("http://dl.dropbox.com/u/44766482/ot_version.txt").read()
        if int(f.decode("utf-8")) > __version__:
            text = gui.Label("Version " + f.decode("utf-8") + lang.available, color=(255, 0, 0))
            self.update.td(text, align=-1)
            #self.update.tr()
            text2 = gui.Label(lang.changelog, color=(100, 100, 255))
            self.update.td(text2, align=1)

            text2.connect(gui.CLICK,
                          webbrowser.open,
                          "http://www.terrariaonline.com/threads/omnitool-world-mapping-backups-creation-and-more.61654/#post-1155423")

            text.connect(gui.CLICK,
                         webbrowser.open,
                         "http://www.terrariaonline.com/threads/omnitool-world-mapping-backups-creation-and-more.61654/")
        print("Update notifier done")
        sys.exit()


def proxyload(file):
    #print ("proxy loading")
    ext = file.split(".")[-1]
    with open(file, "rb") as f:
        d = pygame.image.load(f, ext)
    return d


def get_t_path(verbal=False):
    done = False
    source = False
    if os.path.exists("path.txt"):
        with open("path.txt") as f:
            for path in f.readlines():
                path = path.rstrip("\n")
                if not os.path.isdir(path):
                    if verbal: print("Terraria not found at %s" % path)
                else:
                    if verbal: print("Terraria found at %s" % path)
                    done = True
                    source = path
                    break
    if not done:
        if os.path.isdir("Terraria"):
            source = "Terraria"
            if verbal: print("Terraria found in Omnitool")
        else:
            source = False
    if not done:
        try:
            try:
                import winreg
            except:
                import _winreg as winreg

            opened = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Valve\Steam")
            x = (winreg.QueryValueEx(opened, "SteamPath"))[0]
            x = os.path.join(x, "SteamApps", "common", "terraria")
            if os.path.isdir(x):
                source = x
                if verbal: print("Terraria found at %s" % x)
                done = True
        except:
            pass
    if not done:
        paths = [":\program files (x86)\steam\steamapps\common\Terraria",
                 ":\program files\steam\steamapps\common\Terraria",
                 ":\steam\steamapps\common\Terraria",
                 ":\Terraria"]
        for c in ["C", "D", "E", "F"]:
            if done: break
            for p in paths:

                path = c + p
                if not os.path.isdir(path):
                    if verbal: print("Terraria not found at %s" % path)
                else:
                    if verbal: print("Terraria found at %s" % path)
                    source = path
                    done = True
                    break
    return source


if "directlaunch" in sys.argv:
    if cache["do_backup"]:
        b = Backupper()
        b.name = "Backup"
        b.daemon = False
        b.start()
    launch_terraria()
    sys.exit()


def get_world(path, world, worlds):
    try:
        w = World(path, world)
    except Exception as e:
        print("Error loading world %s:" % world)
        import traceback

        traceback.print_exc()
    else:
        worlds.append(w)


def run():
    try:
        loc = os.path.join(myterraria, "Game Launcher", "omnitool.gli3")
        data = {
            "appAuthor": "Berserker55",
            "appName": "Omnitool",
            "appPath": os.path.abspath(sys.argv[0]),
            "appVersion": __version__
        }
        with open(loc, "wt") as f:
            f.write(json.dumps(data, indent=4))
    except:
        import traceback

        print("Could not register to GameLauncher 3. Maybe it just isn't installed. Exception:")
        traceback.print_exc()

    try:
        path, worldnames = get_worlds()
    except:
        path, worldnames = [None, []]
        print("Omnitool has found no worlds")

    theme = Theme(themename)
    app = pgu_override.MyApp(theme=theme)
    worlds = []
    ts = [threading.Thread(target=get_world, args=(path, world, worlds)) for world in worldnames]
    tuple(t.start() for t in ts)
    source = get_t_path(True)
    pad = 10
    x = 0

    data = [
        ("Omnitool/" + lang.settings, Settings, None),
        ("Omnitool/" + "Language", Language, None),
        ("Omnitool/" + lang.exit, exit_prog, None),
        (lang.start + "/" + lang.terraria, os.system, "start steam://rungameid/105600"),

    ]

    if source:
        import omnitool

        data.append((lang.start + "/" + lang.steamfree, start_proc, (omnitool.launch_terraria, "Launch", "")))
        for file in os.listdir(source):
            if file[-4:] == ".gli":
                with open(os.path.join(source, file), "rt") as f:
                    name, ghash = f.readline().strip(), f.readline().strip()
                data.append((lang.start + "/" + name, start_proc, (launch_terraria, ["Launch", " " + ghash])))

    if "tedit" in cache:
        if os.path.exists(cache["tedit"]):
            def run_tedit(n):
                subprocess.Popen(cache["tedit"], cwd=os.path.split(cache["tedit"])[0])

            data.append((lang.start + "/TEdit", run_tedit, None))
    if "terrafirma" in cache:
        if os.path.exists(cache["terrafirma"]):
            def run_terrafirma(n):
                subprocess.Popen(cache["terrafirma"], cwd=os.path.split(cache["terrafirma"])[0])

            data.append((lang.start + "/Terrafirma", run_terrafirma, None))
    data.extend([
        (lang.open + "/" + lang.imagefolder, subprocess.Popen, "explorer " + images),
        (lang.open + "/" + lang.backupfolder, subprocess.Popen, "explorer " + os.path.join(myterraria, "WorldsBackup")),
        (lang.open + "/" + lang.themes, subprocess.Popen, "explorer " + os.path.join(os.getcwd(), "themes")),
        (lang.visit + "/" + lang.donate, webbrowser.open,
         "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JBZM8LFAGDK4N"),
        (lang.visit + "/" + lang.homepage, webbrowser.open,
         "http://www.terrariaonline.com/threads/omnitool-world-mapping-backups-creation-and-more-released.61654/"),
        (lang.visit + "/" + lang.TO, webbrowser.open, "http://www.terrariaonline.com"),
        (lang.visit + "/" + lang.wiki, webbrowser.open, "http://wiki.terrariaonline.com/Terraria_Wiki"),
        (lang.visit + "/GameLauncher GUI", webbrowser.open,
         "http://www.terrariaonline.com/threads/terraria-game-launcher-gui.64759/"),
    ])
    forbidden = ["flatworld", "planetoids", "worldify", "arena"]
    for plug in plugins:
        if plug[0] not in forbidden and plug[2] != "injector":
            data.append(("Plugins/%s" % plug[1], start_proc, (relay.launch_plugin, [plug[1], plug])))
    os.environ["SDL_VIDEO_WINDOW_POS"] = "20,50"

    app.connect(gui.QUIT, exit_prog, None)
    main = gui.Table()

    menu = gui.Menus(data)
    main.td(gui.Spacer(pad, pad))
    main.td(menu, colspan=5, align=-1)
    main.td(gui.Spacer(pad, pad))
    main.tr()
    update = gui.Table()
    update.td(gui.Label(""))
    main.td(update, col=1, colspan=5, align=-1)

    main.tr()
    if len(worldnames) > 5:
        print("Warning: You have more than five worlds, Terraria will not be able to list all!")
    newtable = gui.Table()
    width = 190
    worldify = GenButton(lang.worldify, IMAGE, width=width)
    planetoids = GenButton(lang.planetoids, PLANET, width=width)
    dungeon = GenButton(lang.arena, DUNGEON, width=width)
    flat = GenButton(lang.flat, FLAT, width=width)
    #start = time.clock()
    tuple(t.join() for t in ts)
    expected_h = 170 * len(worlds) // cache["columns"] + 100
    pygame.display.init()
    available_h = max([res[1] for res in pygame.display.list_modes()])
    if expected_h > available_h:
        print("GUI expected to be higher than monitor height, adding columns")
        #print((170*len(worlds)),(expected_h-100))
        cache["columns"] = max(cache["columns"] + 1, 1 + (170 * len(worlds)) // (available_h - 100))
    del (ts)
    #print(time.clock()-start)
    for w in worlds:
        if x % cache["columns"] == 0:
            main.tr()
        wtab = gui.Table()
        wtab.td(w.info, colspan=2)
        wtab.tr()
        if thumbsize:
            wtab.td(w.image, colspan=2)
        else:
            wtab.td(gui.Spacer(1, 20))
        wtab.tr()
        wtab.td(gui.Spacer(pad, pad))
        wtab.tr()

        wtab.td(gui.Spacer(420, 25), colspan=2)
        wtab.tr()

        main.td(gui.Spacer(pad, 1))
        main.td(wtab)
        #main.td(gui.Spacer(pad,1))

        x += 1
    if x % cache["columns"] == 0:
        main.tr()
    newtable.td(gui.Label(lang.new), align=-1)
    newtable.tr()
    newtable.td(gui.Spacer(1, 10), colspan=3)
    newtable.tr()
    newtable.td(worldify)
    newtable.td(gui.Spacer(12, 12))
    newtable.td(planetoids)
    newtable.tr()
    newtable.td(gui.Spacer(1, 10), colspan=3)
    newtable.tr()
    newtable.td(dungeon)
    newtable.td(gui.Spacer(12, 12))
    newtable.td(flat)
    main.td(newtable, colspan=3)
    main.tr()
    main.td(gui.Spacer(12, 12))
    print("GUI Matrix created, initializing..")
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption("Terraria Omnitool V%d | %d Bit" % (__version__, bit))

    def make_resize(worlds, app, main):
        def resize(self, ev):
            if app.first and not app.zoomed:
                app.first = False
            else:
                padding = 50
                thumb_w = max((ev.w - padding) // cache["columns"], 420)
                thumb_h = int(thumb_w / 3.5)

                for w in worlds:
                    w.override_thumb((thumb_w, thumb_h))
                    w.info.style.width = thumb_w
                    w.thumbsize = (thumb_w, thumb_h)

                app.rect.size = main.rect.size = main.w, main.h = main.resize()
                if sys.platform.startswith("win"):
                    if windll.user32.IsZoomed(pygame.display.get_wm_info()['window']):
                        s = pygame.display.set_mode(ev.size, pygame.SWSURFACE | pygame.RESIZABLE)
                        app.zoomed = True
                    else:
                        s = pygame.display.set_mode((main.w, main.h), pygame.SWSURFACE | pygame.RESIZABLE)
                        app.zoomed = False
                app.screen = s
                app.first = True

        return resize


    app.init(main, None)
    app.on_resize = make_resize(worlds, app, main)
    main.rect.h = max(main.rect.height, 250)
    if cache["thumbsize"]:
        pygame.display.set_mode((main.rect.size[0] - 2, main.rect.size[1] - 2), pygame.SWSURFACE | pygame.RESIZABLE)
    else:
        pygame.display.set_mode(main.rect.size, pygame.SWSURFACE)
    info = Info()
    info.name = "Info"
    info.daemon = False

    updater = Updater(update)
    updater.name = "Updater"
    updater.daemon = False

    if cache["do_backup"]:
        b = Backupper()
        b.name = "Backup"
        b.daemon = False
        b.start()
    info.start()
    updater.start()
    app.run(main)


plugins = []


def get_plugins():
    for file in os.listdir("plugins"):
        if file[-3:] == ".py" and file != "plugins.py" and file != "__init__.py":
            s = "import plugins.%s as %s" % (file[:-3], file[:-3])
            try:
                exec(s)
            except:
                import traceback

                print("Error importing plugin %s:" % file[:-3])
                traceback.print_exc()
            else:
                config = eval(file[:-3] + ".config")
                name, ptype = config["name"], config["type"]
                plugins.append((file[:-3], name, ptype))


def plug_save(Plug):  #

    f = tempfile.SpooledTemporaryFile(10000000)  #10 megabyte ram file
    set_header(f, Plug.header)
    try:
        Plug.tiles[0]
    except:
        Plug.tiles.seek(0)
        f.write(Plug.tiles.read())
    else:
        set_tiles(f, Plug.tiles, Plug.header, True)
    set_chests(f, Plug.chests)
    set_signs(f, Plug.signs)
    [set_npc(f, npc) for npc in Plug.npcs]
    set_npc(f, None)
    set_npc_names(f, Plug.names)
    set_trail(f, (1, Plug.header["name"], Plug.header["ID"]))
    with open(get_next_world(), "wb") as g:
        f.seek(0)
        g.write(f.read())


def launch_plugin(plug):
    import importlib

    Plugin = importlib.__import__("plugins." + plug[0], fromlist=[plug[0]])
    if plug[2] == "receiver":
        #print(dir(Plugin))
        p, worlds = get_worlds()
        import plugingui

        w = plugingui.run(p, worlds, Plugin, "rec")
        if w:
            path = os.path.join(p, w)
            with open(path, "rb") as f:
                Plug = Plugin.Receiver()
                f.buffer = [0]
                header = get_header(f)[0]
                print("sending header")
                if Plug.rec_header(header) != False:
                    tiles = []
                    for xi in range(header["width"]):  # for each slice
                        tiles.append([get_tile(f) for tile in range(header["height"])])
                    print("sending tiles")
                    if Plug.rec_tiles(tiles) != False:
                        if Plug.rec_chests(chests=[get_chest(f) for x in range(1000)]) != False:
                            if Plug.rec_signs(signs=[get_sign(f) for x in range(1000)]) != False:
                                npcs = []
                                while 1:
                                    npc = get_npc(f)
                                    if not npc:
                                        break
                                    else:
                                        npcs.append(npc)
                                names = get_npc_names(f)
                                trail = get_trail(f)
                                if trail[1] != header["name"] or trail[2] != header["ID"]:
                                    print("Warning, World signature test not passed")
                                Plug.rec_npcs(npcs, names)
                                Plug.run()
        else:
            print("No world selected, aborting execution")
    elif plug[2] == "generator":
        Plug = Plugin.Generator()
        Plug.run()
        plug_save(Plug)

    elif plug[2] == "program":

        Plug = Plugin.Program()
        Plug.run()
    elif plug[2] == "transplant":

        p, worlds = get_worlds()
        import plugingui

        w = plugingui.run(p, worlds, Plugin, "trans")
        path = os.path.join(p, w[1])
        with open(path, "rb") as f:
            Plug = Plugin.Transplant()
            f.buffer = [0]
            header = get_header(f)[0]
            Plug.rec_header(header)
            tiles = []
            for xi in range(header["width"]):  # for each slice
                tiles.append([get_tile(f) for tile in range(header["height"])])
            Plug.rec_tiles(tiles)
            Plug.rec_chests(chests=[get_chest(f) for x in range(1000)])
            Plug.rec_signs(signs=[get_sign(f) for x in range(1000)])
            npcs = []
            while 1:
                npc = get_npc(f)
                if not npc:
                    break
                else:
                    npcs.append(npc)
            names = get_npc_names(f)
            trail = get_trail(f)
            if trail[1] != header["name"] or trail[2] != header["ID"]:
                print("Warning, World signature test not passed")
            Plug.rec_npcs(npcs, names)
            Plug.run()

        path = os.path.join(p, w[0])
        with open(path, "rb") as f:
            #Plug = Plugin.Transplant()
            f.buffer = [0]
            header = get_header(f)[0]
            if Plug.rec_header(header) != False:
                tiles = []
                for xi in range(header["width"]):  # for each slice
                    tiles.append([get_tile(f) for tile in range(header["height"])])
                if Plug.rec_tiles(tiles) != False:
                    if Plug.rec_chests(chests=[get_chest(f) for x in range(1000)]) != False:
                        if Plug.rec_signs(signs=[get_sign(f) for x in range(1000)]) != False:
                            npcs = []
                            while 1:
                                npc = get_npc(f)
                                if not npc:
                                    break
                                else:
                                    npcs.append(npc)
                            names = get_npc_names(f)
                            trail = get_trail(f)
                            if trail[1] != header["name"] or trail[2] != header["ID"]:
                                print("Warning, World signature test not passed")
                            Plug.rec_npcs(npcs, names)
                            Plug.run()
        plug_save(Plug)
    elif plug[2] == "modifier":
        p, worlds = get_worlds()
        import plugingui

        w = plugingui.run(p, worlds, Plugin, "mod")
        path = os.path.join(p, w)
        with open(path, "rb") as f:
            Plug = Plugin.Modifier()
            f.buffer = [0]
            header = get_header(f)[0]
            Plug.rec_header(header)
            tiles = []
            for xi in range(header["width"]):  # for each slice
                tiles.append([get_tile(f) for tile in range(header["height"])])
            Plug.rec_tiles(tiles)
            Plug.rec_chests(chests=[get_chest(f) for x in range(1000)])
            Plug.rec_signs(signs=[get_sign(f) for x in range(1000)])
            npcs = []
            while 1:
                npc = get_npc(f)
                if not npc:
                    break
                else:
                    npcs.append(npc)
            names = get_npc_names(f)
            trail = get_trail(f)
            if trail[1] != header["name"] or trail[2] != header["ID"]:
                print("Warning, World signature test not passed")
            Plug.rec_npcs(npcs, names)
            Plug.run()

        plug_save(Plug)

    else:
        print("Unrecognized plugin type, aborting execution")
    print()
    print(plug[1] + " is done")
    sys.exit()


PLANET = 1
DUNGEON = 2
FLAT = 3
IMAGE = 4
import relay

bind = {1: (relay.run_plat, "Planetoids"),
        2: (relay.run_arena, "Arena"),
        3: (relay.run_flat, "Flatworld"),
        4: (relay.run_world, "Worldify")}


class Quitbutton(gui.Button):
    def __init__(self, app, value=lang.pt_start):
        gui.Button.__init__(self, value, width=300, height=40)
        try:
            self.connect(gui.CLICK, app.quit, None)
        except AttributeError:
            self.connect(gui.CLICK, app.close, None)


if __name__ == "__main__":

    get_plugins()
    p = False
    for arg in sys.argv:
        if arg.startswith("plugin:"):
            p = True
            name = arg[7:]
            for ps in plugins:
                if ps[0] == name:
                    print("Launching plugin %s" % ps[1])
                    pygame.quit()
                    start_proc((relay.launch_plugin, [ps[1], ps]))
                    sys.exit()
            print("Plugin not found")

    if not p:
        run()
        
