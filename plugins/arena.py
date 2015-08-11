# ref ID: 7
config = {
    "name": "Dungeon Arena",  #plugin name
    "type": "generator",  #plugin type
    "description": ["Dungeon Arena"]  #description
}

import sys
from collections import defaultdict

if __name__ == "__main__":
    sys.path.extend(["."])
    import os

    os.chdir("..")
    del (os)

from pgu import gui
from math import sqrt, cos, sin, pi
from random import *
import pygame
from os.path import join as osjoin

from omnitool.database import version, tiles, names
from omnitool.tlib import *
from omnitool.tinterface import *
from omnitool.binarysplit import join, cleanup

from .arena_lib.arenaitems import items as arenaitems


class Generator():
    def __init__(self):
        pass

    def run(self):

        from omnitool.shared import lang, theme, exit_prog, __version__
        from omnitool.pgu_override import Quitbutton

        torch_chances = [lang.at_full, lang.at_blue, lang.at_red, lang.at_green,
                         lang.at_pink, lang.at_white, lang.at_yellow, lang.at_purple,
                         lang.at_lime]

        name = 'Dungeon Arena'
        if hasattr(sys, "frozen"):
            import os

            os.chdir(os.path.dirname(sys.executable))


        def update(slider, label):
            label.set_text(str(slider.value))

        def update_per(slider, label):
            label.set_text(str(slider.value) + "%")

        def update_2(slider, label):
            label.set_text(str(slider.value * slider.value))

        pygame.display.init()
        pygame.display.set_caption(name)


        def weighted(liste):
            n = uniform(0, 1)
            for item, weight in liste:
                if n < weight:
                    break
                n = n - weight
            return item


        app = gui.Desktop(theme=theme)

        app.connect(gui.QUIT, exit_prog, None)
        main = gui.Table()

        main.td(gui.Label(lang.a_name), align=-1)
        nameinput = gui.Input("Dungeon Arena OT-V" + str(__version__), width=200)
        main.td(nameinput, colspan=2)

        main.tr()
        main.td(gui.Spacer(1, 12))
        main.tr()

        rooms = gui.HSlider(value=15, min=3, max=31, size=20, height=16, width=150)
        roomstext = gui.Label(str(15 * 15))
        rooms.connect(gui.CHANGE, update_2, rooms, roomstext)
        main.td(gui.Label(lang.a_rooms), align=-1)
        main.td(rooms, align=-1)
        main.td(roomstext)

        main.tr()

        roomsize = gui.HSlider(value=12, min=9, max=36, size=20, height=16, width=150)
        roomsizetext = gui.Label("12")
        roomsize.connect(gui.CHANGE, update, roomsize, roomsizetext)
        main.td(gui.Label(lang.a_sidelen), align=-1)
        main.td(roomsize, align=-1)
        main.td(roomsizetext)

        main.tr()

        corridor = gui.HSlider(value=6, min=3, max=9, size=20, height=16, width=150)
        corridortext = gui.Label("6")
        corridor.connect(gui.CHANGE, update, corridor, corridortext)
        main.td(gui.Label(lang.a_corlen), align=-1)
        main.td(corridor, align=-1)
        main.td(corridortext)

        main.tr()
        main.td(gui.Spacer(1, 12))
        main.tr()

        chestcount = gui.HSlider(value=100, min=0, max=100, size=20, height=16, width=150)
        chesttext = gui.Label("100%")
        chestcount.connect(gui.CHANGE, update_per, chestcount, chesttext)
        main.td(gui.Label(lang.a_chest), align=-1)
        main.td(chestcount, align=-1)
        main.td(chesttext)

        main.tr()

        itemcount = gui.HSlider(value=1, min=0, max=20, size=20, height=16, width=150)
        itemtext = gui.Label("1")
        itemcount.connect(gui.CHANGE, update, itemcount, itemtext)
        main.td(gui.Label(lang.a_itemchest), align=-1)
        main.td(itemcount, align=-1)
        main.td(itemtext)

        main.tr()
        main.td(gui.Spacer(1, 12))
        main.tr()

        torchcount = gui.HSlider(value=100, min=0, max=100, size=20, height=16, width=150)
        torchtext = gui.Label("100%")
        torchcount.connect(gui.CHANGE, update_per, torchcount, torchtext)
        main.td(gui.Label(lang.a_light), align=-1)
        main.td(torchcount, align=-1)
        main.td(torchtext)

        main.tr()
        main.td(gui.Spacer(1, 12))
        main.tr()
        torch_sel = []
        main.td(gui.Label(lang.at_chances), align=-1)
        main.tr()
        for t in torch_chances:
            torchsel = gui.HSlider(value=1, min=0, max=10, size=20, height=16, width=150)
            torcht = gui.Label("1")
            torchsel.connect(gui.CHANGE, update, torchsel, torcht)
            main.td(gui.Label(t), align=-1)
            main.td(torchsel, align=-1)
            main.td(torcht)
            torch_sel.append(torchsel)
            main.tr()

        main.tr()
        main.td(gui.Spacer(1, 12))
        main.tr()

        main.td(gui.Label(lang.a_chances), colspan=2, align=-1)
        main.td(gui.Spacer(50, 1))

        main.tr()

        standardcount = gui.HSlider(value=1, min=0, max=10, size=20, height=16, width=150)
        standardtext = gui.Label("1")
        standardcount.connect(gui.CHANGE, update, standardcount, standardtext)
        main.td(gui.Label(lang.a_standard), align=-1)
        main.td(standardcount, align=-1)
        main.td(standardtext)

        main.tr()

        crosscount = gui.HSlider(value=1, min=0, max=10, size=20, height=16, width=150)
        crosstext = gui.Label("1")
        crosscount.connect(gui.CHANGE, update, crosscount, crosstext)
        main.td(gui.Label(lang.a_cross), align=-1)
        main.td(crosscount, align=-1)
        main.td(crosstext)

        main.tr()
        main.td(gui.Spacer(1, 12))
        main.tr()
        main.td(Quitbutton(app, lang.pt_start), colspan=3)

        app.run(main)
        pygame.display.quit()

        selection = [("cross", crosscount.value),
                     ("standard", standardcount.value)]
        torch_selection = []
        x = 0
        for v in torch_sel:
            torch_selection.append((x, v.value))
            x += 1
        weight = 0

        for item, w in selection:
            weight += w

        if not weight:
            print("UserError: No rooms to place.")
            import time

            time.sleep(10)
        t_weight = 0
        for item, w in torch_selection:
            t_weight += w

        if not t_weight:
            print("UserError: No torches to place. To have no lighting ONLY set the lighting slider to zero.")
            import time

            time.sleep(10)

        for x in range(len(torch_selection)):
            torch_selection[x] = (torch_selection[x][0], torch_selection[x][1] / float(t_weight))
        for x in range(len(selection)):
            selection[x] = (selection[x][0], selection[x][1] / float(weight))
        name = nameinput.value
        chest_mode = itemcount.value
        s = roomsize.value
        chestchance = chestcount.value
        roomwidth = s
        roomheight = s
        rooms = rooms.value
        border = 250
        corridor = corridor.value
        torches = torchcount.value
        size = (rooms * roomwidth + (rooms - 1) * corridor + border * 2,
                rooms * roomheight + (rooms - 1) * corridor + border * 2)
        dtile = choice([41, 43, 44])
        dwall = choice([7, 8, 9])
        if not rooms % 2:
            spawn = (roomwidth // 2 + size[0] // 2, roomheight // 2 + size[1] // 2)
        else:
            spawn = (size[0] // 2, size[1] // 2)
        print("Starting Generation")
        header = {'spawn': spawn, 'groundlevel': -10.0, 'is_bloodmoon': 0,
                  'dungeon_xy': spawn, 'worldrect': (0, size[0] * 16, 0, size[1] * 16),
                  'is_meteor_spawned': 0, 'gob_inv_time': 0, 'rocklevel': size[1] // 2 + 0.4,
                  'gob_inv_x': 0.0, 'is_day': 1, 'shadow_orbs_broken': 0,
                  'width': size[0], 'version': version, 'gob_inv_type': 0,
                  'bosses_slain': (0, 0, 1), "npcs_saved": (0, 0, 0), "special_slain": (0, 0, 0), 'gob_inv_size': 0,
                  'height': size[1],
                  'ID': 1394008880, 'moonphase': 0, "hardmode": 0,
                  'name': name, "altars_broken": 0,
                  'is_a_shadow_orb_broken': 0, 'time': 13500}

        is_exe = hasattr(sys, "frozen")
        surface = pygame.surface.Surface(size)
        surface.fill((254, 1, 255))
        pygame.draw.rect(surface, (dtile, dtile, dtile),
                         ((border - corridor, border - corridor),
                          (size[0] - border * 2 + corridor * 2, size[1] - border * 2 + corridor * 2)))
        plat = (19, 0, 0)

        chests = []
        # contents of the spawn chest

        multis = get_multis()

        chestsurflist = (multis["woodchest"],
                         multis["goldchest"],
                         multis["shadowchest"],
                         multis["barrelchest"],
                         multis["canchest"])

        for x in range(rooms):  #horizontal
            pygame.draw.rect(surface, (252, dwall, 0),
                             ((border + corridor, border + roomheight // 2 - 2 + x * (roomheight + corridor)),
                              ((rooms - 1) * (roomwidth + corridor), 4)))

        for x in range(rooms):  #vertical
            pygame.draw.rect(surface, (252, dwall, 0),
                             ((border + roomwidth // 2 - 2 + x * (roomheight + corridor), border + corridor),
                              (4, (rooms - 1) * (roomheight + corridor))))
        for x in range(rooms):
            for y in range(rooms):
                rtype = weighted(selection)
                ltype = weighted(torch_selection)
                #print(ltype)
                if rtype == "standard":
                    pos = (border + x * (roomwidth + corridor), border + y * (roomwidth + corridor))
                    pygame.draw.rect(surface, (252, dwall, 0),
                                     (pos, (roomwidth, roomheight)))
                    if torches > randint(0, 100):
                        surface.set_at(pos, (4, 0, ltype))
                        surface.set_at((pos[0] + roomwidth - 1, pos[1]), (4, 0, ltype))
                        surface.set_at((pos[0], pos[1] + roomheight - 1), (4, 0, ltype))
                        surface.set_at((pos[0] + roomwidth - 1, pos[1] + roomheight - 1), (4, 0, ltype))

                    #platforms on ground with corridor
                    pygame.draw.line(surface, plat, (pos[0], pos[1] + roomheight // 2 + 2),
                                     (pos[0] + roomwidth - 1, pos[1] + roomheight // 2 + 2))
                    #over corridor
                    pygame.draw.line(surface, plat, (pos[0], pos[1] + roomheight // 2 - 3),
                                     (pos[0] + roomwidth - 1, pos[1] + roomheight // 2 - 3))
                    if y > 0:  #lowest platform
                        pygame.draw.line(surface, plat, (pos[0] + roomwidth // 2 - 2, pos[1] - 1),
                                         (pos[0] + roomwidth // 2 + 1, pos[1] - 1))
                    if y < rooms:  #high platform
                        pygame.draw.line(surface, plat, (pos[0] + roomwidth // 2 - 2, pos[1] + roomheight),
                                         (pos[0] + roomwidth // 2 + 1, pos[1] + roomheight))

                elif rtype == "cross":
                    pos = (border + x * (roomwidth + corridor), border + y * (roomwidth + corridor))
                    if torches > randint(0, 100):
                        surface.set_at(pos, (4, 0, ltype))
                        surface.set_at((pos[0] + roomwidth - 1, pos[1]), (4, 0, ltype))
                        surface.set_at((pos[0], pos[1] + roomheight - 1), (4, 0, ltype))
                        surface.set_at((pos[0] + roomwidth - 1, pos[1] + roomheight - 1), (4, 0, ltype))

                    #platforms on ground with corridor
                    pygame.draw.line(surface, plat,
                                     (pos[0] + roomwidth // 2 - 2, pos[1] + roomheight // 2 + 2),
                                     (pos[0] + roomwidth // 2 + 1, pos[1] + roomheight // 2 + 2))
                    #over corridor
                    pygame.draw.line(surface, plat,
                                     (pos[0] + roomwidth // 2 - 2, pos[1] + roomheight // 2 - 3),
                                     (pos[0] + roomwidth // 2 + 1, pos[1] + roomheight // 2 - 3))
                    if y > 0:  #lowest platform
                        pygame.draw.line(surface, plat,
                                         (pos[0] + roomwidth // 2 - 2, pos[1] - 1),
                                         (pos[0] + roomwidth // 2 + 1, pos[1] - 1))
                    if y < rooms:  #high platform
                        pygame.draw.line(surface, plat,
                                         (pos[0] + roomwidth // 2 - 2, pos[1] + roomheight),
                                         (pos[0] + roomwidth // 2 + 1, pos[1] + roomheight))

                else:
                    print(rtype)
                    raise AssertionError("")
                if chest_mode and chestchance > randint(0, 100):
                    content = []
                    for spam in range(chest_mode):
                        item = choice(list(arenaitems.keys()))
                        content.append((arenaitems[item], item, 0))

                    for i in range(20 - len(content)):  #chests always have 20 slots
                        content.append((0, None))
                    chests.append(((pos[0] + roomwidth // 2 - 1, pos[1] + roomheight // 2), content))

        for chest in chests:
            #draw the chests into the world texture
            surface.blit(choice(chestsurflist), chest[0])
            #surface.blit(multis["shadoworb"], chest[0])
            # below is to make sure every chest stands on something, so they dont glitch
            d = surface.get_at((chest[0][0], chest[0][1] + 2))[0]
            if d > 250 or d == 51:
                surface.set_at((chest[0][0], chest[0][1] + 2), (0, 0, 0))
            d = surface.get_at((chest[0][0] + 1, chest[0][1] + 2))[0]
            if d > 250 or d == 51:
                surface.set_at((chest[0][0] + 1, chest[0][1] + 2), (0, 0, 0))
            assert chest[0][0] < header["width"] and chest[0][0] > 0
            assert chest[0][1] < header["height"] and chest[0][1] > 0

        for x in range(1000 - len(chests)):  #fill in nonechests, as terraria always has 1000 chests
            chests.append(None)


        z = header["width"] * header["height"]  #tileamount
        walls = defaultdict(lambda:None, {21: dwall,
                 31: dwall,
                 dtile: dwall,
                 4: dwall,
                 19: dwall})

        def count(checks):
            c = {}
            for t_id in checks:
                c[t_id] = 0
            for x in range(size[0]):
                for y in range(size[1]):
                    tid = surface.get_at((x, y))[0]
                    if tid in c:
                        c[tid] += 1
            for tid in c:
                amount = c[tid]
                print("%-10s : %d" % (tiles[tid], amount))

        self.header = header
        #wooden platforms used to not be multitiles, so overwrite that
        self.tiles = write_tiles(surface, header, walls, True, overwrite_no_mt = {19})

        self.chests = chests
        self.signs = [None] * 1000

        self.npcs = [('Guide', (header["spawn"][0] * 16, (header["spawn"][1] - 3) * 16), 1,
                      (header["spawn"][0], header["spawn"][1] - 3))]
        self.names = names


if __name__ == "__main__":
    gen = Generator()
    gen.run()
