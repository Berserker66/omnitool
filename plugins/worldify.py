config = {
    "name": "Worldify",  # plugin name
    "type": "generator",  #plugin type
    "description": ["Image -> World"]  #description
}
# ref id: 5
import sys
import os

if __name__ == "__main__":
    sys.path.extend(["."])

    os.chdir("..")
import pygame
import database as db
import colorlib
from tlib import *
from time import sleep
import tempfile
import colorsys
from pgu_override import MyFileDialog


class Generator():
    def __init__(self):
        pass


    def run(self):
        from omnitool import themename, Theme, lang, exit_prog, Quitbutton, temp, __version__
        #pygame.quit()
        if hasattr(sys, "frozen"):
            os.chdir(os.path.dirname(sys.executable))
        from pgu import gui

        nogui = False
        pygame.display.init()
        pygame.display.set_caption("Worldify")

        try:
            blue = Theme(themename)
        except Exception as e:
            print("Error initialising GUI, proceeding without it")
            print(str(e))
            nogui = True
        else:
            nogui = False

        if len(sys.argv) < 2:
            if nogui:
                noimage = True
                print("No Image supplied, please drag and drop an image onto the program")
                sleep(3)
                sys.exit(1000)
            else:

                def open_file_browser(arg):
                    d = gui.FileDialog()
                    d.connect(gui.CHANGE, handle_file_browser_closed, d)
                    d.open()

                app = gui.Desktop(theme=blue)
                app.connect(gui.QUIT, exit_prog, None)
                app.connect(gui.CLOSE, exit_prog, None)
                main = MyFileDialog()
                main.connect(gui.CLOSE, app.quit, main)
                main.connect(gui.CHANGE, app.quit, main)
                main.open()
                app.run(main)
                pygame.display.quit()
                imagepath = main.value
        else:
            imagepath = sys.argv[1]
            noimage = False

        local = os.listdir(os.getcwd())
        if "db.txt" in local:
            print("Found external database, starting parsing..")
            from plugins.worldify_lib import jsonparse

            jsonparse.load()
            print("Database injection successful")
            ext = True
        else:
            ext = False
        pygame.display.init()
        pygame.display.set_caption("Worldify")
        colors = colorlib.data
        #bad = [4,49, 53, 32, 62, 52, 80, 19]#torch, blue candle, sand, corruption vines, wooden platform

        for tile in colors:
            if tile in db.multitiles or tile > 255:
                colorlib.bad.append(tile)
        colors[None] = (250, 250, 250)  #air
        for b in colorlib.bad:
            if b in colors: del (colors[b])
        rcolors = {}
        for color in colors:
            rcolors[tuple(colors[color])] = color
            #print ("%-25s %s" % ((db.tiles[color], colors[color])))
        try:
            surface = pygame.image.load(imagepath)
        except:
            import traceback

            print("Unable to load image, please try using png or bmp files")
            print("Error:")
            print(traceback.format_exc())
            sleep(3)
            sys.exit(1000)

        w, h = surface.get_size()
        preview = surface.copy()
        scale = min(280.0 / w, 210.0 / h)
        try:
            preview = pygame.transform.smoothscale(surface, (int(w * scale), int(h * scale)))
        except:
            surface = surface.convert(32, 0)
            preview = pygame.transform.smoothscale(surface, (int(w * scale), int(h * scale)))
        print("Image loaded with %d x %d pixels" % (w, h))
        while w < 240 or h < 150:
            surface = pygame.transform.smoothscale(surface, (w * 2, h * 2))
            w, h = surface.get_size()
            print("Image enlarged to %d x %d pixels" % (w, h))
        if w > 8400 or h > 2400:
            print("Warning: Terraria can only load worlds up to a size of 8400 x 2400")
            print("Program will continue in 3 seconds anyway")
            sleep(3)
            oversize = True
        else:
            oversize = False

        ###GUI###
        name = "ImageWorld OT-V" + str(__version__)
        func = "RGB"
        weight = (1, 1, 1)
        if not nogui:

            app = gui.Desktop(theme=blue)
            app.connect(gui.QUIT, exit_prog, None)
            c = gui.Table()

            def change(method, button):
                if method.value == "RGB":
                    button.value = lang.w_start
                else:
                    button.value = lang.w_cont
                button.chsize()

            c.td(gui.Image(preview), colspan=2)
            c.tr()
            if oversize:
                dbstr = gui.Label("Warning: Image too large")
                c.td(dbstr, colspan=2)
                c.tr()
            if ext:
                dbstr = gui.Label("External database loaded")
            else:
                dbstr = gui.Label("No external database found")
            c.td(dbstr, colspan=2)
            c.tr()

            namefield = gui.Input(name, width=200)
            c.td(gui.Label(lang.w_name))
            c.td(namefield)
            c.tr()
            method = gui.Select(width=214)
            method.add(lang.w_rgb, "RGB")
            method.add(lang.w_hsv, "HSV")
            method.value = lang.w_rgb
            e = Quitbutton(app)
            method.connect(gui.CHANGE, change, method, e)
            c.td(gui.Label(lang.w_method))
            c.td(method)
            c.tr()
            c.td(gui.Spacer(1, 25), colspan=2)
            c.tr()

            c.td(e, colspan=2)
            app.run(c)
            name = namefield.value
            func = method.value
            pygame.display.quit()

            if func == "HSV":
                pygame.display.init()
                pygame.display.set_caption("Worldify")

                def update(slider, label):
                    label.set_text(str(slider.value) + "X")

                app = gui.Desktop(theme=blue)
                app.connect(gui.QUIT, exit_prog, None)
                c = gui.Table(width=250)
                c.td(gui.Label(lang.w_priority, size=40), colspan=3)
                c.tr()
                H = gui.HSlider(value=1, min=0, max=9, size=20, height=16, width=120)
                S = gui.HSlider(value=1, min=0, max=9, size=20, height=16, width=120)
                V = gui.HSlider(value=1, min=0, max=9, size=20, height=16, width=120)
                c.td(gui.Label(lang.w_hue))
                c.td(H)
                hl = gui.Label("1X")
                H.connect(gui.CHANGE, update, H, hl)
                c.td(hl)
                c.tr()
                c.td(gui.Label(lang.w_saturation))
                c.td(S)
                sl = gui.Label("1X")
                S.connect(gui.CHANGE, update, S, sl)
                c.td(sl)
                c.tr()
                c.td(gui.Label(lang.w_brightness))
                c.td(V)
                vl = gui.Label("1X")
                V.connect(gui.CHANGE, update, V, vl)
                c.td(vl)
                c.tr()
                e = Quitbutton(app)
                c.td(e, colspan=3)
                app.run(c)
                pygame.display.quit()
                weight = H.value, S.value, V.value

        ###GUI END###

        self.header = {'spawn': (w // 2, h // 2), 'groundlevel': h + 0.4, 'is_bloodmoon': 0,
                       'dungeon_xy': (w, h), 'worldrect': (0, w * 16, 0, h * 16),
                       'is_meteor_spawned': 0, 'gob_inv_time': 0, 'rocklevel': h + 100.4,
                       'gob_inv_x': 0.0, 'is_day': 1, 'shadow_orbs_broken': 0,
                       'width': w, 'version': 39, 'gob_inv_type': 0,
                       'bosses_slain': (0, 0, 0), "npcs_saved": (0, 0, 0), "special_slain": (0, 0, 0),
                       'gob_inv_size': 0, 'height': h,
                       'ID': 1394008880, 'moonphase': 0, 'name': name,
                       'is_a_shadow_orb_broken': 0, 'time': 13500,
                       "hardmode": 0, "altars_broken": 0, }

        import time

        def rgba(a, surface, rcolors, weight=None, bg=1.0):
            w10 = w // 20
            total = z = w
            acolors = {}
            for color in rcolors:
                nc = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
                #print nc
                acolors[nc] = rcolors[color]
            #print acolors
            for x in range(w):
                for y in range(h):
                    color = surface.get_at((x, y))
                    p = 1 - color[3] / 255.0
                    b = (bg * color[3] / 255.0)
                    color = ((p * (color[0] / 255.0)) + b * color[3] / 255.0,
                             (p * (color[1] / 255.0)) + b * color[3] / 255.0,
                             (p * (color[2] / 255.0)) + b * color[3] / 255.0)
                    cdif = 100000
                    #color = int(color[0]*255),int(color[1]*255),int(color[2]*255)
                    for c in acolors:

                        dif = (c[0] - color[0]) * (c[0] - color[0]) + (c[1] - color[1]) * (c[1] - color[1]) + (c[2] -
                                                                                                               color[
                                                                                                                   2]) * (
                                                                                                              c[2] -
                                                                                                              color[2])
                        if dif < cdif:
                            cdif = dif
                            hit = acolors[c]
                            #print dif
                    set_tile(a, (hit, None, 0, None))
                if z % w10 == 1:  #give lifesigns
                    print("%6.2f%% done writing tiles") % ((total - z) * 100.0 / w)
                z -= 1

        def rgb(a, surface, rcolors, weight=None):
            w10 = w // 20
            total = z = w
            for x in range(w):
                for y in range(h):
                    color = surface.get_at((x, y))
                    cdif = 100000
                    #hit = None
                    for c in rcolors:
                        dif = (c[0] - color[0]) * (c[0] - color[0]) + (c[1] - color[1]) * (c[1] - color[1]) + (c[2] -
                                                                                                               color[
                                                                                                                   2]) * (
                                                                                                              c[2] -
                                                                                                              color[2])
                        if dif < cdif:
                            cdif = dif
                            hit = rcolors[c]
                    set_tile(a, (hit, None, 0, None))
                if z % w10 == 1:  #give lifesigns
                    n = ((total - z) * 100.0) / w
                    print("%6.2f%% done writing tiles" % n)
                z -= 1

        def hsv(a, surface, rcolors, weight=(2, 3, 1)):
            #hue saturation value/brightness


            hcolors = {}
            for color in rcolors:
                nc = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
                hcolors[nc] = rcolors[color]
            w10 = w // 20
            total = z = w
            #print hcolors
            for x in range(w):
                for y in range(h):
                    color = surface.get_at((x, y))
                    color = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
                    #print color
                    cdif = 100
                    for c in hcolors:
                        p1 = min(weight[0] * (c[0] - color[0]) * (c[0] - color[0]),
                                 weight[0] * (c[0] + 1 - color[0]) * (c[0] + 1 - color[0]),
                                 weight[0] * (c[0] - 1 - color[0]) * (c[0] - 1 - color[0]))

                        dif = p1 + weight[1] * (c[1] - color[1]) * (c[1] - color[1]) + weight[2] * (c[2] - color[2]) * (
                        c[2] - color[2])
                        #print dif, cdif
                        if dif < cdif:
                            cdif = dif
                            hit = hcolors[c]
                    set_tile(a, (hit, None, 0, None))
                    #print hit, dif
                if z % w10 == 1:  #give lifesigns
                    n = ((total - z) * 100.0) / w
                    print("%6.2f%% done writing tiles" % n)
                z -= 1

        start = time.clock()
        self.tiles = tempfile.TemporaryFile()

        if func == "RGB":
            print("Finding closest match via euclidian RGB distance")
            rgb(self.tiles, surface, rcolors)
        else:
            print("Finding closest match via weighted HSV difference")
            hsv(self.tiles, surface, rcolors, weight)
        t = time.clock() - start
        n = (t, t / (w * h))
        print("%5f seconds taken, that is %0.10f seconds per pixel" % n)
        self.chests = [None] * 1000
        self.signs = [None] * 1000
        self.names = db.names
        self.npcs = [('Guide', (self.header["spawn"][0] * 16, (self.header["spawn"][1] - 3) * 16), 1,
                      (self.header["spawn"][0], self.header["spawn"][1] - 3))]


if __name__ == "__main__":
    gen = Generator()
    gen.run()
