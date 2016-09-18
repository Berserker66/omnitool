#! python3.4-32

import sys
import os
import multiprocessing

import zlib
import pickle

from importlib import import_module
from urllib.request import urlretrieve

from .shared import cachepath, appdata, __version__
from .loadbar import Bar
from . import render

__author__ = "Fabian Dill"
__credits__ = ["Ijwu", "7UR7L3", "Fabian Dill"]
__maintainer__ = "Fabian Dill"
os.environ["PYGAME_FREETYPE"] = "1"

if not os.path.isdir(appdata):
    os.mkdir(appdata)

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
elif cache["version"] < __version__:
    print("Newer Omnitool version, resetting world image cache.")
    cache["version"] = __version__
    cache["worlds"] = {}

from .Language import load_language

lang = load_language(cache['lang'])

if False:
    from .Language import english as lang  # IDE hook

shared.lang = lang
shared.cache = cache
shared.cores = multiprocessing.cpu_count()

import pygame
from pgu import gui
from .tinterface import *
from .colorlib import walldata, data as colorlib_data
from .tlib import *
import threading
import time
from .pgu_override import MyTheme, MyApp

theme = shared.theme = MyTheme(themename)
import subprocess
import shutil
import sys
import webbrowser

if sys.platform.startswith("win"):
    from ctypes import windll

import struct
import tempfile
import json

bit = struct.calcsize("P") * 8

cache_lock = threading.Lock()


def save_cache():
    cache_lock.acquire()
    d = zlib.compress(pickle.dumps(cache), 9)
    with open(shared.cachepath, "wb") as f:
        f.write(d)
    cache_lock.release()


if len(sys.argv) > 1:  # user wants something
    def savequit():
        import time
        time.sleep(3)
        save_cache()
        pygame.quit()
        sys.exit()


    if sys.argv[1].split("\\")[-1] == "TEditXna.exe":  # install tedit
        cache["tedit"] = sys.argv[1]
        print("Learned TEdit path: " + sys.argv[1])
        savequit()

    elif sys.argv[1].split("\\")[-1] == "Terrafirma.exe":  # install tedit
        cache["terrafirma"] = sys.argv[1]
        print("Learned terrafirma path: " + sys.argv[1])
        savequit()

myterraria = get_myterraria()  # mygames-terraria path
images = myterraria / "WorldImages"

processes = []

if not images.is_dir():
    images.mkdir(parents=True)
try:
    (myterraria / "Worlds").mkdir()
except:
    pass

shutdown = False


def exit_prog(p):
    global shutdown
    shutdown = True
    pygame.quit()
    import sys
    sys.exit()


shared.exit_prog = exit_prog


def nothing(p):
    pass


class GenButton(gui.Button):
    def __init__(self, name, gen, width=100, disabled=False):
        gui.Button.__init__(self, name, width=width)

        self.connect(gui.CLICK, start_proc, bind[gen], True)
        self.disabled = disabled
        self.blur()


last_gen_start = 0


def start_proc(func, delay=False):
    global last_gen_start
    if delay:
        now = time.time()
        if now - last_gen_start < 0.1:
            return
        last_gen_start = time.time()
    if func[1].__class__.__name__ == "list":
        p = multiprocessing.Process(target=func[0], name=func[1][0],
                                    args=(func[1][1],))
    else:
        p = multiprocessing.Process(target=func[0], name=func[1])  # , args = (to_self,))
    p.start()
    processes.append(p)


class Language(gui.Dialog):
    def __init__(self, n=None):
        main = gui.Table()
        gui.Dialog.__init__(self, gui.Label("Language"), main)

        liste = gui.List(200, 150)
        langs = ["german", "english", "portuguese", "czech",
                 "spanish", "french", "norwegian", "japanese",
                 "danish", "italian", "hungarian", "russian"]
        langnames = [lang.capitalize() for lang in langs]
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
        themes = "themes"
        for dire in os.listdir(themes):
            liste.add(str(dire), value=dire)
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
        main.td(gui.Label(lang.world_columns), col=1, row=3)
        main.tr()
        main.td(self.columns, col=1, row=4)
        main.tr()
        main.td(gui.Label(lang.mk_backups), col=1, row=5)
        main.tr()
        main.td(backupswitch, col=1, row=6)

        self.open()

    def close(self, w=None):
        cache["theme"] = self.liste.value
        if cache["thumbsize"] != self.sizelist.value:
            change = True
        else:
            change = False
        cache["thumbsize"] = self.sizelist.value
        cache["do_backup"] = self.backup.value
        cache["columns"] = self.columns.value
        save_cache()
        gui.Dialog.close(self, w)
        display_worlds(change)


class Button(gui.Button):
    def __init__(self, name, func, args, width=200):
        gui.Button.__init__(self, name, width=width)
        self.connect(gui.CLICK, func, args)


def open_image(world):
    webbrowser.open(str(world.imagepath))


def open_tedit(world):
    subprocess.Popen((cache["tedit"], str(world.path)), cwd=os.path.split(cache["tedit"])[0])


def regen_map(world):
    if not world.get_worldview():
        print("No changes found in world file, rendering skipped.")


def runrender(world, mapping):
    if mapping:
        megaimage_dir = images / Path(str(world.name))
        args = (render.run, megaimage_dir / "index.html",
                world.header, world.path, True, (world.header, world.pos), megaimage_dir)
        p = multiprocessing.Process(target=relay.run_with_browser, name="WorldRender (mapping)", args=args)
    else:
        args = (world.header, world.path, False, (world.header, world.pos))
        p = multiprocessing.Process(target=render.run, name="WorldRender", args=args)
    p.start()
    processes.append(p)


class WorldInteraction(gui.Dialog):
    def __init__(self, world):
        main = gui.Table()
        gui.Dialog.__init__(self, gui.Label(lang.wa_worldactionmenu.format(world.name)), main)

        imgopen = Button(lang.wa_imageopen, self.bundle, (open_image, world))
        renderopen = Button(lang.wa_renderopen, self.bundle, (runrender, world, False))
        updatemap = Button(lang.wa_update, self.bundle, (regen_map, world))
        superimg = Button(lang.wa_super, self.bundle, (runrender, world, True))
        main.td(imgopen)
        main.tr()
        main.td(renderopen)
        main.tr()
        main.td(superimg)
        if "tedit" in cache and os.path.exists(cache["tedit"]):
            editopen = Button(lang.wa_teditopen, self.bundle, (open_tedit, world))
            main.tr()
            main.td(editopen)
        main.tr()
        main.td(updatemap)
        self.open()

    def close(self, w=None):
        gui.Dialog.close(self, w)

    def bundle(self, args):
        self.close()
        args[0](*args[1:])


class World():
    aircolor = pygame.Color(200, 200, 255)
    groundcolor = pygame.Color(150, 75, 0)
    rockcolor = pygame.Color(50, 50, 50)

    def __init__(self, path):
        self.mapperrunning = threading.Event()
        self.path = path
        self.imagepath = images / self.path.with_suffix(".png").name
        with self.path.open("rb") as f:
            self.header, self.multiparts, self.sectiondata = get_header(f)
            if self.sectiondata:
                self.pos = self.sectiondata["sections"][1]
                if f.tell() != self.pos:
                    print("Warning: Header for world",self.header["name"].decode(),"of different size than expected, errors may occur.")
            else:
                self.pos = f.tell()

        self.name = self.header["name"].decode()
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
        self.raw.fill(self.aircolor)
        self.thumbsize = thumbsize

        if thumbsize:
            self.get_thumb()
            self.image = gui.Image(self.thumb)

            self.image.connect(gui.CLICK,
                               WorldInteraction,
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

    def check_change(self):
        if not self.mapperrunning.is_set():
            redraw = False
            try:
                strpath = str(self.path)
                if strpath in cache["worlds"] and self.path.stat().st_mtime > cache["worlds"][strpath]["time"]:
                    redraw = True
            except FileNotFoundError:  # world happened to be removed between checks
                pass
            else:  # why is there no elif on try?
                if redraw:
                    self.raw.fill(self.aircolor)
                    self.get_worldview()

    def get_worldview(self):
        self.mapperrunning.set()  # make sure Redrawer knows, that aquisition of this image is in progress
        needed = False
        try:
            if str(self.path) in cache["worlds"]:
                worldcache = cache["worlds"][str(self.path)]
                if self.path.stat().st_mtime == worldcache["time"]:
                    i = proxyload(images / self.path.with_suffix('.png').name)
                else:
                    raise IOError("Image is outdated")
            else:
                cache["worlds"][str(self.path)] = {"time": 0}
                raise IOError("Image does not exist")

        except IOError:
            needed = True
        else:
            self.raw.blit(i, (0, 0))
            self.update_thumb()

        save_cache()
        if needed:
            size = self.raw.get_size()
            levels = self.header["groundlevel"], self.header["rocklevel"]
            pygame.draw.rect(self.raw, self.groundcolor,
                             ((0, levels[0]),
                              (size[0], size[1] - levels[0])))

            pygame.draw.rect(self.raw, self.rockcolor,
                             ((0, levels[1]),
                              (size[0], size[1] - levels[1])))
            self.update_thumb()
            t = PLoader(self)
            t.name = "Vanilla-Mapper-%s" % self.header["name"]
            t.start()
        else:
            self.mapperrunning.clear()
        return needed

def gen_slices(queue, imgpath, path, start, size, levels, version, multiparts, interval=32):
    get_tile = select_tile_getter(version)

    with path.open("rb") as f:
        f.seek(start)
        xworld, yworld = size  # read world size from header cache
        s = pygame.surface.Surface(size, depth=24)
        s.fill((200, 200, 255))
        pygame.draw.rect(s, (150, 75, 0),
                         ((0, levels[0]),
                          (size[0], size[1] - levels[0])))

        pygame.draw.rect(s, (50, 50, 50),
                         ((0, levels[1]),
                          (size[0], size[1] - levels[1])))
        buffer = pygame.PixelArray(s)
        xstart = 0
        while xstart < xworld:
            w = min(interval, -xstart + xworld)
            for xi in range(xstart, xstart + w):  # for each slice
                yi = 0
                while yi < yworld:  # get the tiles
                    (tile, wall, liquid, multi, wire), b = get_tile(f)
                    color = None
                    if not liquid:  # liquid == 0 means no liquid
                        # there could be a liquid and a tile, like a chest and water,
                        # but I can only set one color to a pixel anyway, so I priotise the tile
                        if tile == None:
                            if wall:
                                if wall in colorlib.walldata:
                                    color = colorlib.walldata[wall]
                                else:
                                    color = (wall, wall, wall)

                        elif tile in colorlib.data:
                            color = colorlib.data[tile]  # if colorlib has a color use it
                        else:
                            tile = min(255, tile)
                            color = (tile, tile, tile)  # make a grey otherwise
                    elif liquid > 512:
                        color = (245, 219, 27)
                    elif liquid > 256:
                        color = (150, 35, 17)

                    else:  # 0>x>256 is water, the higher x is the more water is there
                        color = (19, 86, 134)
                    if color:
                        buffer[xi, yi:yi + b] = color
                    yi += b
            sub = buffer[xstart:xstart + w, ::].make_surface()
            queue.put([w, pygame.image.tostring(sub, "RGB")])
            xstart += w
    del (buffer)
    queue.close()
    pygame.image.save(s, imgpath)


class PLoader(threading.Thread):
    def __init__(self, world):
        threading.Thread.__init__(self)
        self.world = world

    def run(self):
        world = self.world
        wx, wy = size = (world.header["width"], world.header["height"])
        levels = world.header["groundlevel"], world.header["rocklevel"]
        xi = 0
        version = world.header["version"]

        pos = world.pos
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=relay.launch_gen_slices, args=(
        queue, str(self.world.imagepath), world.path, pos, size, levels, version, world.multiparts))
        p.start()
        while xi < wx:

            x, imgdata = queue.get()

            surface = pygame.image.fromstring(imgdata, (x, wy), "RGB")
            while world.raw.get_locked():  # if window is beeing rezized, keep waiting
                time.sleep(0.1)
            world.raw.blit(surface, (xi, 0))
            world.update_thumb()
            world.image.repaint()
            xi += x

        p.join()  # wait until the image file is saved
        cache["worlds"][str(world.path)]["time"] = world.path.stat().st_mtime
        save_cache()
        world.mapperrunning.clear()


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
            # print ("alive")
            dead = []
            for p in processes:
                # print (p.exitcode, p.is_alive())
                # print (p)
                if not p.is_alive(): dead.append(p)
            for d in dead:
                d.join()
                processes.remove(d)
            time.sleep(1)
        sys.exit()


class Backupper(threading.Thread):
    """Thread handling background backups - quits when everything is backed up"""

    def __init__(self):
        threading.Thread.__init__(self)

    def backup(self, path, dest):
        t = path.stat().st_mtime
        if path not in cache["backup"] or t != cache["backup"]:
            s = time.strftime("%SS_%MM_%HH_%dD_%b_%YY.", time.localtime(t))
            shutil.copy(str(path), str(dest / (s + path.name)))
            cache["backup"][str(path)] = t

    def run(self):
        dest = myterraria / "WorldsBackup"
        if not dest.is_dir():
            dest.mkdir()

        # source = os.path.join("C:\program files (x86)\\steamapps\common\Terraria")
        worlds = list(get_worlds())
        for path in worlds:
            self.backup(path, dest)
        if len(worlds) == 0:
            print("BackUpper has found no worlds")

        dest = myterraria / "PlayersBackup"
        if not dest.is_dir():
            dest.mkdir()
        try:
            players = get_players()
            for path in players:
                self.backup(path, dest)
        except FileNotFoundError:
            print("BackUpper has found no player files")

        print("Backups made")
        sys.exit()
        save_cache()


class Redrawer(threading.Thread):
    """Thread that waits for changes in the world folder and triggers a menu redraw when necessary"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "Redrawer"
        self.daemon = True

    def run(self):
        global worlds
        new = []
        dropped = []
        while 1:
            time.sleep(1)
            if dropped:
                worlds = list(filter(lambda world: world.path not in dropped, worlds))
            for world in worlds:
                world.check_change()
            if new:
                for name in new:
                    get_world(name, worlds)
            if new or dropped:
                print("World File Change Detected!")
                app.queue.append((display_worlds,))

            names = set(get_worlds())
            new = names - set(worldnames)
            dropped = set(worldnames) - names
            if new:
                worldnames.extend(new)
            if dropped:
                for w in dropped:
                    worldnames.remove(w)


class Updater(threading.Thread):
    ziploc = os.path.join(appdata, "tImages.zip")
    verloc = os.path.join(appdata, "tImages.json")

    def __init__(self, update):
        threading.Thread.__init__(self)
        self.name = "Updater"
        self.update = update

    def run(self):
        import urllib.request
        import json
        f = urllib.request.urlopen("http://dl.dropbox.com/u/44766482/ot_updater/ot_version.json").read()
        js = json.loads(f.decode())
        verint = js["omnitool"]
        if verint > __version__:
            from .version import Version
            text = gui.Label("Version " + Version(verint).__repr__() + lang.available, color=(255, 0, 0))
            self.update.td(text, align=-1)
            text2 = gui.Label(lang.changelog, color=(100, 100, 255))
            self.update.td(text2, align=1)

            text2.connect(gui.CLICK,
                          webbrowser.open,
                          "http://adf.ly/686481/omnitool-github-releases")

            text.connect(gui.CLICK,
                         webbrowser.open,
                         "http://adf.ly/686481/omnitool-github-releases")


        if  not os.path.exists("tImages.zip") or self.check_texture_version(js["tImages"]):  # newer version available
            args = (r"http://dl.dropbox.com/u/44766482/ot_updater/tImages.zip",
                    str(self.ziploc),
                    "Texture Download",
                    False)
            p = multiprocessing.Process(target=remote_retrieve, name="tImages Retriever", args=args)
            p.start()
            p.join()

            import json
            with open(self.verloc, "w") as f:
                json.dump({"version": js["tImages"]}, f)
        print("Updater done")
        sys.exit()

    def check_texture_version(self, remote_texture_version):
        if os.path.exists(self.ziploc) and os.path.exists(self.verloc):
            import json
            with open(self.verloc) as f:
                js = json.load(f)
            if js["version"] >= remote_texture_version:
                return False

        return True


def remote_retrieve(source, target, name, abortable=True):
    """
    Retrieves remote file, showing a pygame progressbar for progress.
    As there can only be one pygame window per process, it is recommended to run this as a subprocess.
    :param source: URL source of file
    :param target: local target location
    :param name: caption of pygame window
    :return:
    """
    bar = Bar(caption=name, abortable=abortable)

    def reporthook(blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
        else:  # total size is unknown
            percent = 0
        bar.set_progress(percent, name + " {:d}%".format(int(percent)))

    urlretrieve(source, target, reporthook)


def proxyload(path):
    with path.open("rb") as f:
        d = pygame.image.load(f, path.suffix[1:])
    return d


if "directlaunch" in sys.argv:
    if cache["do_backup"]:
        b = Backupper()
        b.name = "Backup"
        b.daemon = False
        b.start()
    webbrowser.open("steam://rungameid/105600")
    sys.exit()


def get_world(world, worlds):
    try:
        w = World(world)
    except Exception as e:
        print("Error loading world %s:" % world)
        import traceback

        traceback.print_exc()
    else:
        worlds.append(w)


def open_dir(direc):
    direc = str(direc)
    if sys.platform == 'win32':
        subprocess.Popen(['explorer', direc], shell=True)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', direc])
    else:
        try:
            subprocess.Popen(['xdg-open', direc])
        except OSError:
            pass


plugins_ = []


def get_plugins():
    if "." not in sys.path:
        sys.path = ["."] + sys.path  # use plugins in the folder, instead of library.zip - if accidentally included
    for file in os.listdir("plugins"):
        if file[-3:] == ".py" and file != "plugins.py" and file != "__init__.py":
            try:
                plugin = import_module('plugins.' + file[:-3], package="omnitool")
            except:
                import traceback

                print("Error importing plugin %s:" % file[:-3])
                traceback.print_exc()
            else:
                name, ptype = plugin.config["name"], plugin.config["type"]
                plugins_.append((file[:-3], name, ptype))
    return plugins_


def plug_save(Plug):
    if hasattr(Plug, "loadingbar"):
        # we have a loadingbar to attend to
        loadcallback = Plug.loadingbar
    else:
        loadcallback = None
    f = tempfile.SpooledTemporaryFile(10000000)  # 10 megabyte ram file
    set_header(f, Plug.header)
    try:
        Plug.tiles[0]
    except:
        Plug.tiles.seek(0)
        f.write(Plug.tiles.read())
    else:
        set_tiles(f, Plug.tiles, Plug.header, True, loadcallback)
    set_chests(f, Plug.chests)
    set_signs(f, Plug.signs)
    [set_npc(f, npc) for npc in Plug.npcs]
    set_npc(f, None)
    set_npc_names(f, Plug.names)
    set_trail(f, (1, Plug.header["name"], Plug.header["ID"]))
    with get_next_world(Plug.header["name"]).open("wb") as g:
        f.seek(0)
        g.write(f.read())


def launch_plugin(plug):
    import importlib
    if "." not in sys.path:
        sys.path = ["."] + sys.path  # use plugins in the folder, instead of library.zip - if accidentally included
    Plugin = importlib.import_module("plugins." + plug[0], "omnitool")

    if plug[2] == "receiver":
        worlds = list(get_worlds())
        from . import plugingui

        w = plugingui.run(worlds, Plugin, "rec")
        if w:
            with w.open("rb") as f:
                Plug = Plugin.Receiver()
                f.buffer = [0]
                header = get_header(f)[0]
                print("sending header")
                if Plug.rec_header(header) != False:
                    get_tile = iter_get_tile(select_tile_getter(header["version"]))(f)
                    tiles = []
                    for xi in range(header["width"]):  # for each slice
                        tiles.append([next(get_tile) for _ in range(header["height"])])
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
        worlds = list(get_worlds())
        import plugingui

        w1, w2 = plugingui.run(worlds, Plugin, "trans")
        with w2.open("rb") as f:
            Plug = Plugin.Transplant()
            f.buffer = [0]
            header = get_header(f)[0]
            Plug.rec_header(header)
            get_tile = iter_get_tile(select_tile_getter(header["version"]))(f)
            tiles = []
            for xi in range(header["width"]):  # for each slice
                tiles.append([next(get_tile) for _ in range(header["height"])])
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

        with w1.open("rb") as f:
            # Plug = Plugin.Transplant()
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
        worlds = list(get_worlds())
        from .plugingui import run as run_plugingui

        w = run_plugingui(worlds, Plugin, "mod")
        with w.open("rb") as f:
            Plug = Plugin.Modifier()
            f.buffer = [0]
            header = get_header(f)[0]
            Plug.rec_header(header)
            get_tile = iter_get_tile(select_tile_getter(header["version"]))(f)
            tiles = []
            for xi in range(header["width"]):  # for each slice
                tiles.append([next(get_tile) for _ in range(header["height"])])
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


from .relay import launch_plugin as relay_launch_plugin


def run():
    global app
    global worldnames
    global worlds
    global display_worlds

    try:
        loc = myterraria / "Game Launcher" / "omnitool.gli3"
        data = {
            "appAuthor": __author__ + " (Berserker66)",
            "appName": "Omnitool",
            "appPath": os.path.abspath(sys.argv[0]),
            "appVersion": __version__.__repr__()
        }
        with loc.open("wt") as f:
            f.write(json.dumps(data, indent=4))
    except:
        import traceback

        print("Could not register to GameLauncher 3. Maybe it just isn't installed. Exception:")
        traceback.print_exc()

    try:
        worldnames = list(get_worlds())
    except FileNotFoundError:
        worldnames = []
        print("Omnitool has found no worlds")

    use_override = True
    if use_override:
        app = MyApp(theme=theme)
    else:
        import pgu
        app = pgu.gui.App(theme=theme)
    worlds = []
    ts = [threading.Thread(target=get_world, args=(world, worlds)) for world in worldnames]
    tuple(t.start() for t in ts)
    pad = 10
    x = 0

    data = [
        ("Omnitool/" + lang.settings, Settings, None),
        ("Omnitool/" + "Language", Language, None),
        ("Omnitool/" + lang.report_issue, webbrowser.open, "https://github.com/Berserker66/omnitool/issues"),
        ("Omnitool/" + lang.exit, exit_prog, None),
        (lang.start + "/" + lang.terraria, webbrowser.open, "steam://rungameid/105600"),

    ]

    if "tedit" in cache and os.path.exists(cache["tedit"]):
        def run_tedit(n):
            subprocess.Popen(cache["tedit"], cwd=os.path.split(cache["tedit"])[0])

        data.append((lang.start + "/TEdit", run_tedit, None))
    if "terrafirma" in cache:
        if os.path.exists(cache["terrafirma"]):
            def run_terrafirma(n):
                subprocess.Popen(cache["terrafirma"], cwd=os.path.split(cache["terrafirma"])[0])

            data.append((lang.start + "/Terrafirma", run_terrafirma, None))
    data.extend([
        (lang.open + "/" + lang.imagefolder, open_dir, images),
        (lang.open + "/" + lang.backupfolder, open_dir, myterraria / "WorldsBackup"),
        (lang.open + "/" + lang.themes, open_dir, Path.cwd() / "themes"),
        (lang.visit + "/" + lang.donate, webbrowser.open,
         r"https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JBZM8LFAGDK4N"),
        (lang.visit + "/Patreon", webbrowser.open,
         r"https://www.patreon.com/Berserker55"),
        (lang.visit + "/" + lang.homepage, webbrowser.open,
         r"http://forums.terraria.org/index.php?threads/omnitool-world-creation-mapping-backups-and-more.14664/"),
        (lang.visit + "/" + lang.wiki, webbrowser.open, "http://terraria.gamepedia.com/Terraria_Wiki"),
        (lang.visit + "/GameLauncher GUI", webbrowser.open,
         "http://forums.terraria.org/index.php?threads/game-launcher-3-2-1-5.1061/"),
    ])
    forbidden = ["flatworld", "planetoids", "worldify", "arena"]
    for plug in plugins_:
        if plug[0] not in forbidden and plug[2] != "injector":
            data.append(("Plugins/%s" % plug[1], start_proc, (relay_launch_plugin, [plug[1], plug])))
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
    width = 190
    worldify = GenButton(lang.worldify, IMAGE, width=width)
    planetoids = GenButton(lang.planetoids, PLANET, width=width)
    dungeon = GenButton(lang.arena, DUNGEON, width=width)
    flat = GenButton(lang.flat, FLAT, width=width)

    tuple(t.join() for t in ts)
    expected_h = 170 * len(worlds) // cache["columns"] + 100
    pygame.display.init()
    available_h = max([res[1] for res in pygame.display.list_modes()])
    if expected_h > available_h:
        print("GUI expected to be higher than monitor height, adding columns")
        cache["columns"] = max(cache["columns"] + 1, 1 + (170 * len(worlds)) // (available_h - 100))
    del (ts)
    newworldtable = gui.Table()
    newworldtable.td(gui.Spacer(10, 10))
    newworldtable.td(gui.Label(lang.new), align=-1)
    newworldtable.tr()
    newworldtable.td(gui.Spacer(10, 10))
    newworldtable.td(worldify)
    newworldtable.td(gui.Spacer(10, 10))
    newworldtable.td(planetoids)
    newworldtable.td(gui.Spacer(10, 10))
    newworldtable.td(dungeon)
    newworldtable.td(gui.Spacer(10, 10))
    newworldtable.td(flat)
    newworldtable.tr()
    newworldtable.td(gui.Spacer(10, 10))
    main.td(newworldtable, colspan=6)
    main.tr()
    worldtable = gui.Table()
    main.td(worldtable, colspan=6)

    def display_worlds(optionchange=False):
        worldtable.clear()
        x = 0
        for w in worlds:
            if x % cache["columns"] == 0:
                worldtable.tr()
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

            worldtable.td(gui.Spacer(pad, 1))
            worldtable.td(wtab)

            x += 1
        if x % cache["columns"] == 0:
            worldtable.tr()

        worldtable.td(gui.Spacer(12, 12))
        if app.widget:
            print("Window Reset!")
            app.resize()
            app.repaint()
            size = pygame.display.get_surface().get_size()
            data = {"size": size, "w": size[0], "h": size[1], "reload": True if optionchange else False}

            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, data))

    display_worlds()
    print("GUI Matrix created, initializing..")
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption("Terraria Omnitool V%s | %d Bit" % (__version__.__repr__(), bit))

    def make_resize(worlds, app, main):
        def resize(self, ev):
            if app.first and not app.zoomed:
                app.first = False
            else:
                padding = 50
                if hasattr(ev, "reload") and ev.reload == True:
                    thumb_w, thumb_h = cache["thumbsize"]
                    for w in worlds:
                        w.override_thumb((thumb_w, thumb_h))
                        w.info.style.width = thumb_w
                        w.thumbsize = (thumb_w, thumb_h)
                else:
                    thumb_w = max((ev.w - padding) // cache["columns"], 420)
                    thumb_h = int(thumb_w / 3.5)

                    for w in worlds:
                        w.override_thumb((thumb_w, thumb_h))
                        w.info.style.width = thumb_w
                        w.thumbsize = (thumb_w, thumb_h)

                app.rect.size = main.rect.size = main.w, main.h = main.resize()
                if sys.platform.startswith("win"):
                    if windll.user32.IsZoomed(pygame.display.get_wm_info()['window']):
                        s = pygame.display.set_mode(ev.size, pygame.RESIZABLE)
                        app.rect.size = pygame.display.get_surface().get_size()
                        app.zoomed = True
                    else:
                        s = pygame.display.set_mode((main.w, main.h), pygame.RESIZABLE)
                        app.zoomed = False
                else:
                    s = pygame.display.set_mode((main.w, main.h), pygame.RESIZABLE)
                    app.zoomed = False

                app.screen = s
                app.first = True

        return resize

    app.on_resize = make_resize(worlds, app, main)
    app.init(main, None)

    main.rect.h = max(main.rect.height, 250)
    if cache["thumbsize"]:
        pygame.display.set_mode((main.rect.size[0] - 2, main.rect.size[1] - 2), pygame.SWSURFACE | pygame.RESIZABLE)
    else:
        pygame.display.set_mode(main.rect.size, pygame.SWSURFACE)
    info = Info()
    info.name = "Info"
    info.daemon = False

    updater = Updater(update)
    updater.daemon = False

    if cache["do_backup"]:
        b = Backupper()
        b.name = "Backup"
        b.start()
    redrawer = Redrawer()
    redrawer.start()
    info.start()
    updater.start()
    app.run(main)


PLANET = 1
DUNGEON = 2
FLAT = 3
IMAGE = 4

from .relay import run_plat, run_arena, run_flat, run_world

bind = {1: (run_plat, "Planetoids"),
        2: (run_arena, "Arena"),
        3: (run_flat, "Flatworld"),
        4: (run_world, "Worldify")}
