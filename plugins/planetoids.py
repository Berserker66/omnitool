config = {
    "name": "Planetoids",  # plugin name
    "type": "generator",  #plugin type
    "description": ["Planetoids & Terra"]  #description
}
import sys

if __name__ == "__main__":
    sys.path.extend(["."])
    import os

    os.chdir("..")
    del (os)
from math import cos, sin, pi
from collections import defaultdict
from random import *
import pygame

from omnitool.loadbar import Bar
from omnitool.database import itemlist, names, tiles, ntiles
from omnitool.tinterface import *

from .planetoids_lib import terragui
from .planetoids_lib.tree import make_tree
from .planetoids_lib.terradata import *


class Generator():
    def __init__(self):
        itemlist["Life Crystal"] = 1
        itemlist["Fallen Star"] = 10
        itemlist["Wood"] = 100
        itemlist['Swiftness Potion'] = 5
        itemlist['Battle Potion'] = 5
        itemlist['Shine Potion'] = 5
        itemlist['Gravitation Potion'] = 5
        itemlist['Water Walking Potion'] = 5
        itemlist['Invisibility Potion'] = 5
        itemlist['Night Owl Potion'] = 5
        itemlist['Magic Power Potion'] = 5
        itemlist['Thorns Potion'] = 5
        itemlist['Mana Regeneration Potion'] = 5
        itemlist['Archery Potion'] = 5
        itemlist['Hunter Potion'] = 5
        itemlist['Restoration Potion'] = 5
        itemlist['Lesser Healing Potion'] = 5
        itemlist['Featherfall Potion'] = 5
        itemlist['Obsidian Skin Potion'] = 5
        itemlist['Spelunker Potion'] = 5
        itemlist['Ironskin Potion'] = 5
        itemlist['Gold Bar'] = 10
        itemlist['Meteorite Bar'] = 10
        itemlist['Silver Bar'] = 10
        itemlist['Iron Bar'] = 10
        itemlist['Copper Bar'] = 10
        itemlist["Meteorite"] = 30

    def run(self):
        # print ("Welcome to the Planetoids & Terra World Generator V12")
        is_exe = hasattr(sys, "frozen")
        terramode = False
        if is_exe:
            import os

            path = os.path.dirname((sys.executable))
            sys.path = [path] + sys.path

        def draw_chasm(sur, pos, rmin, rmax, amin, amax):
            points = [
                (int(pos[0] + rmin * cos(amin)), int(pos[1] + rmin * sin(amin))),
                (int(pos[0] + rmin * cos((amin + amax) / 2)), int(pos[1] + rmin * sin((amin + amax) / 2))),
                (int(pos[0] + rmin * cos(amax)), int(pos[1] + rmin * sin(amax))),
                (int(pos[0] + rmax * cos(amax)), int(pos[1] + rmax * sin(amax))),
                (int(pos[0] + rmax * cos((amin + amax) / 2)), int(pos[1] + rmax * sin((amin + amax) / 2))),
                (int(pos[0] + rmax * cos(amin)), int(pos[1] + rmax * sin(amin)))]
            pygame.draw.polygon(sur, (233, 233, 233), points)
            steps = 70
            pygame.draw.circle(sur, (23, 23, 23), points[-1], 8)
            pygame.draw.circle(sur, (23, 23, 23), points[3], 8)
            orb = randint(steps // 2, steps)
            for x in range(steps + 1):

                x = float(x)
                cpos = (int(points[0][0] * x / steps + points[-1][0] * (steps - x) / steps),
                        int(points[0][1] * x / steps + points[-1][1] * (steps - x) / steps))
                ra = randint(4, 8)  #
                #pygame.draw.circle(sur, (32,32,32), cpos, ra, 4) #vines
                pygame.draw.circle(sur, (23, 23, 23), cpos, ra, 2)  #grass
                pygame.draw.circle(sur, (25, 25, 25), cpos, ra)  #ebonstone

                cpos2 = (int(points[2][0] * x / steps + points[3][0] * (steps - x) / steps),
                         int(points[2][1] * x / steps + points[3][1] * (steps - x) / steps))
                ra = randint(4, 8)
                #pygame.draw.circle(sur, (32,32,32), cpos2, ra, 4) #vines
                pygame.draw.circle(sur, (23, 23, 23), cpos2, ra, 2)  #grass
                pygame.draw.circle(sur, (25, 25, 25), cpos2, ra)  #ebonstone

                if x == orb:
                    cpos = (cpos[0] + cpos2[0]) // 2, (cpos[1] + cpos2[1]) // 2
                    pygame.draw.circle(sur, (25, 25, 25), cpos, 3)  #ebonstone
                    sur.blit(multis["shadoworb"], (cpos[0] - 1, cpos[1] - 1))

            return sur


        d = terragui.run(None)
        if not d == False:
            name, mode, starttype, sun, atlantis, merch, loot, hard, mirrored, pre = d
            sizetype = mode[0]
            terramode = mode[1]
        else:
            hard = 0
            name = "Planetoids"
            ## ask the user what kind of world he/she wants.
            print("Select world type")
            print("Terra mode only available on large and square")
            print("1: planetoids")
            print("2: terra & planetoids; implies large world size")
            print("3: terra; implies square world size")
            valid = [1, 2, 3]
            terramode = 0
            while terramode not in valid:
                try:
                    terramode = int(input("World type:"))
                except:
                    pass
                if terramode not in valid:
                    print("Please put in 1,2, or 3 and then hit enter, cant be that hard, right?")
            print("")
            terramode -= 1
            if not terramode:
                print("Select world size")
                print("1: small  (4200 x 1200)")
                print("2: medium (6300 x 1800)")
                print("3: large  (8400 x 2400)")
                print("4: square (2400 x 2400)")
                valid = [1, 2, 3, 4]
                sizetype = 0
                while sizetype not in valid:
                    try:
                        sizetype = int(raw_input("World size:"))
                    except:
                        pass
                    if sizetype not in valid:
                        print("Please put in 1,2,3 or 4 and then hit enter, cant be that hard, right?")
                print("")

            valid = [1, 2, 3, 4]
            print("Select start condition")
            print("1: Day (Standard Terraria)")
            print("2: Morning")
            print("3: Night")
            print("4: Bloodmoon")
            starttype = 0
            while starttype not in valid:
                try:
                    starttype = int(raw_input("Start condition:"))
                except:
                    pass
                if starttype not in valid:
                    print("Please input 1,2,3 or 4, then hit enter.")
            print("")
            valid = [1, 2, 3, 4]
            print("Select extra difficulty, you may select multiple by entering multiple numbers.")
            print("By entering nothing you play normal")
            print("1: Darkness! I dont need a puny sun!")
            print("2: Less loot! I want to keep exploring!")
            print("3: Atlantis, I want to conquer the world from my sunken planet!")
            print("4: No merchant at the start, I want to earn him!")
            dif = input("Difficulty:")

            if "1" in dif:
                sun = False
            else:
                sun = True
            if "2" in dif:
                loot = True
            else:
                loot = False
            if "3" in dif:
                atlantis = True
            else:
                atlantis = False
            if "4" in dif:
                merch = False
            else:
                merchant = True

        loadingbar = Bar(caption = "Planetoids: startup")
        sizetype -= 1
        starttype -= 1
        #people dont like to start counting at 0, so its decremented afterwards

        #for people used to python this part of code should be obvious
        #otherwise: [1,2,3][0] returns 1, as that is at part 1
        #this is a cpu intense way of doing it, but its the less typing
        #execution time at this point is also pretty much unimportant
        is_day = [1, 1, 0, 0][starttype]
        is_blood = [0, 0, 0, 1][starttype]
        time = [13000.0, 0.0, 0.0, 0.0][starttype]
        size = [(4200, 1200), (6300, 1800), (8400, 2400), (2400, 2400)][sizetype]
        if terramode:
            border = 200
            spawn = (size[0] // 2, border)
            superradius = 1200 - border
        else:
            spawn = [(2100, 200), (3150, 300), (4200, 400), (1200, 200)][sizetype]

        if not sun:  #if no sun
            ground = [-1200.0, -1800.0, -2400.0, -2400.0][sizetype]
            rock = [385.0, 385.0, 385.0, 385.0][sizetype]
        else:
            ground = [385.0, 385.0, 385.0, 385.0][sizetype]
            rock = [487.0, 703.0, 907.0, 907.0][sizetype]

        if sizetype == 3:
            #square world has almost the same amount of tiles as small
            # so in the following code it will be regarded as a small world.
            sizetype = 0
        elif sizetype == 2 and terramode:  #large world - terra = contents of medium planetoids
            sizetype = 1

        chestcount = [200, 400, 800][sizetype]
        #I would prefer [500,1000,1500] chests
        #but terraria only allows 1000 chests as well as 1000 signs, never forget that limit

        large_planets = [25, 50, 100][sizetype]
        dungeon_planets = [5, 10, 20][sizetype]
        small_planets = [250, 500, 1000][sizetype]
        stone_planets = [25, 50, 100][sizetype]
        #header data
        header = {'spawn': spawn, 'groundlevel': ground, 'is_bloodmoon': is_blood,
                  'dungeon_xy': spawn, 'worldrect': (0, size[0] * 16, 0, size[1] * 16),
                  'is_meteor_spawned': 0, 'gob_inv_time': 0, 'rocklevel': rock,
                  'gob_inv_x': 0.0, 'is_day': is_day, 'shadow_orbs_broken': 0,
                  'width': size[0], 'version': 39, 'gob_inv_type': 0,
                  'bosses_slain': (0, 0, 0), "npcs_saved": (0, 0, 0), "special_slain": (0, 0, 0),
                  'gob_inv_size': 0, 'height': size[1],
                  'ID': randint(10, 10000000), 'moonphase': 0, 'name': name, "hardmode": int(hard),
                  "altars_broken": 0,
                  'is_a_shadow_orb_broken': 0, 'time': time}
        chestfactor = 1
        if sizetype == 0:
            for item, amount in itemdata.items():
                itemdata[item] = sum(divmod(amount, 2))
            for item, amount in goldlockitemdata.items():
                goldlockitemdata[item] = sum(divmod(amount, 2))
            for item, amount in shadowlockitemdata.items():
                shadowlockitemdata[item] = sum(divmod(amount, 2))
            chestfactor /= 2
        elif sizetype == 2:
            for item in itemdata:
                itemdata[item] = itemdata[item] * 2
            for item, amount in goldlockitemdata.items():
                goldlockitemdata[item] = amount*2
            for item, amount in shadowlockitemdata.items():
                shadowlockitemdata[item] = amount*2
            chestfactor *= 2
        if mirrored:
            for item in itemdata:
                itemdata[item] = itemdata[item] // 2 + itemdata[item] % 2
            for item, amount in goldlockitemdata.items():
                goldlockitemdata[item] = sum(divmod(amount, 2))
            for item, amount in shadowlockitemdata.items():
                shadowlockitemdata[item] = sum(divmod(amount, 2))
            chestcount //= 2
            chestfactor /= 2
        if loot:
            for item in itemdata:
                itemdata[item] = itemdata[item] // 2 + itemdata[item] % 2
            for item, amount in goldlockitemdata.items():
                goldlockitemdata[item] = sum(divmod(amount, 2))
            for item, amount in shadowlockitemdata.items():
                shadowlockitemdata[item] = sum(divmod(amount, 2))
            chestfactor /= 2

        itemtotal = 0
        for item in itemdata:
            itemtotal += itemdata[item]
        target = itemtotal // chestcount

        loadingbar.set_progress(5, "Planetoids: generating base content")
        #initialize a texture to hold all tile data
        #could have used an array as well, like numpy, but I am more familiarized with pygame than numpy
        surface = pygame.surface.Surface(size)
        if atlantis:  #if waterworld
            surface.fill((254, 0, 255))
            pygame.draw.rect(surface, (54, 54, 54), ((0, size[0]), (-1 + size[1] - size[1] // 6, size[1] // 6)))
            pygame.draw.rect(surface, (255, 255, 255), ((0, size[0]), (size[1] - size[1] // 6, size[1] // 6)))
        else:
            surface.fill((255, 255, 255))


        def on_radius(rad):
            pos = size[0] // 2, size[1] // 2
            angle = random() * 2 * pi
            return (int(pos[0] + rad * cos(angle)),
                    int(pos[1] + rad * sin(angle)))

        def terrapick(radius):  #picks randomly items for a chest
            fradius = float(radius)
            current = 0
            content = []
            types = [choice((accessoires, weapons)), choice((other, potions))]
            for typ in types:
                while 1:
                    item = choice(list(typ.keys()))
                    #print item, fradius/superradius
                    if typ[item] > fradius / superradius:
                        break
                content.append((randint(1, itemlist[item]), item))
            for x in range(randint(*healthperchest)):
                content.append((1, "Life Crystal"))
            stars = randint(*starsperchest)
            if stars:
                content.append((stars, "Fallen Star"))
            content.append((1, "Acorn"))

            for x in range(20 - len(content)):  #chests always have 20 slots
                content.append((0, None))

            return (on_radius(radius), content)

        def pad_chest(content):
            for x in range(20 - len(content)):  #chests always have 20 slots
                content.append((0, None))
            return content

        def pick(items, targetnumber):  #picks randomly items for a chest planetoids
            current = 0
            content = []
            while targetnumber > current:
                item = choice(tuple(items.keys()))
                if item in itemlist:
                    amount = randint(1, min(itemlist[item], items[item], targetnumber - current))
                else:
                    amount = randint(1, min(3, items[item], targetnumber - current))
                items[item] -= amount
                if items[item] < 1:
                    del (items[item])
                content.append((amount, item))
                current += amount
                if len(content) > 19:
                    break

            return pad_chest(content), current, items

        multis = get_multis()

        goldlockedsurf = multis["goldlockchest"]
        shadowlockedsurf = multis["shadowlockchest"]
        chestnames = ("woodchest",
                         "goldchest",
                         "shadowchest",
                         "barrelchest",
                         "canchest",
                         "ebonwoodchest",
                         "mahoganywoodchest",
                         "bonechest",
                         "ivychest",
                         "icechest",
                         "livingwoodchest",
                         "skychest",
                         "shadewoodchest",
                         "webbedchest",)

        chestsurflist = {}
        for entry in chestnames:
            chestsurflist[entry] = multis[entry]

        loadingbar.set_progress(10, "Planetoids: filling chests")

        chests = []
        if terramode:
            rad = superradius // 50
            step = (float(superradius) - superradius // 16 - 30) / terrachestcount
            while len(chests) < terrachestcount:
                rad += step
                pos, content = terrapick(rad)
                chests.append((pos, content, choice(chestnames)))

        chestcontents = []

        while itemtotal > 0:  # fill those chests with something useful.. or not, angel statue ftw.
            i, c, itemdatabase = pick(itemdata, min(target, itemtotal))
            chestcontents.append(i)
            itemtotal -= c

        def fill_special_chests(itemsperchest, chestcontents, extra_items = ()):

            items = []
            for item,amount in chestcontents.items():
                items.extend([item]*amount)
            shuffle(items)
            while items:
                ch = items[:itemsperchest]
                items = items[itemsperchest:]
                content = [(1, item) for item in ch]
                content.extend([(amount, item) for item, amount in extra_items])
                yield pad_chest(content)

        goldchests = []
        shadowchests = []
        special_chest_contents = {"goldlockchest" : goldchests,
                                  "shadowlockchest" : shadowchests,
                                  "blockedjunglechest" : [pad_chest([(1, "Piranha Gun")])],
                                  "blockedcorruptionchest" : [pad_chest([(1, "Scourge of the Corruptor")])],
                                  "blockedcrimsonchest" : [pad_chest([(1, "Vampire Knives")])],
                                  "blockedhallowedchest" : [pad_chest([(1, "Rainbow Gun")])],
                                  "blockedicechest" : [pad_chest([(1, "Staff of the Frost Hydra")])],
                                  }
        [goldchests.append(content) for content in fill_special_chests(itemspergoldchest, goldlockitemdata, goldlockextra)]
        [shadowchests.append(content) for content in fill_special_chests(itemspershadowchest, shadowlockitemdata, shadowlockextra)]
        special_chests = []
        for chestmulti, chs in special_chest_contents.items():
            for ch in chs:
                special_chests.append((chestmulti, ch))


        center_pos = complex(header["spawn"][0], header["spawn"][1] + 50)  #mid of spawn planet

        shadoworbpos = []

        def make_planet(c, rmin=20, rmax=50, surround=None, value = False):  # function to literally draw the planets onto the world
            r = randint(rmin, rmax)

            if terramode:
                if randint(0, 1) or mirrored:
                    pos = (randint(50, size[0] // 2 - border // 2 - superradius), randint(50, size[1] - 50))
                else:
                    pos = (randint(size[0] // 2 + border // 2 + superradius, size[0] - 50), randint(50, size[1] - 50))
            else:

                if mirrored:
                    pos = (randint(50, size[0] // 2 - 50), randint(50, size[1] - 50))
                    while abs(complex(pos[0], pos[1]) - center_pos) < r + 200:
                        pos = (randint(50, size[0] // 2 - 50), randint(50, size[1] - 50))
                else:
                    pos = (randint(50, size[0] - 50), randint(50, size[1] - 50))
                    while abs(complex(pos[0], pos[1]) - center_pos) < r + 200:
                        pos = (randint(50, size[0] - 50), randint(50, size[1] - 50))

            if c == 25:#ebonstone
                dire = random() * 2 * pi
                radius = randint(10, r)
                shadoworbpos.append((int(pos[0] + radius  * cos(dire)), int(pos[1]+ radius * sin(dire))))

            # a few special planets.. like glass, jungle donuts etc.
            if c == 59:
                pygame.draw.circle(surface, (c, c, c), pos, r)
                pygame.draw.circle(surface, (60, 60, 60), pos, r, 1)  #jungle grass
                pygame.draw.circle(surface, (255, 255, 255), pos, r - 30)
                pygame.draw.circle(surface, (60, 60, 60), pos, r - 30, 1)  #jungle grass
                for _ in range(10):
                    draw_valuable(r-25, r-5,pos,(211,211,211),randint(3,7))
            elif c == 54:
                pygame.draw.circle(surface, (c, c, c), pos, r)
                pygame.draw.circle(surface, (254, randint(0, 1), 255), pos, r - 2)
            elif c == 53:
                pygame.draw.circle(surface, (40, 40, 40), (pos[0], pos[1] + 1), r)
                pygame.draw.circle(surface, (c, c, c), pos, r)

            elif c == 0:
                pygame.draw.circle(surface, (c, c, c), pos, r)
                pygame.draw.circle(surface, (2, 2, 2), pos, r, 1)
                pygame.draw.circle(surface, (30, 30, 30), pos, r - 3, 1)
                if value:
                    draw_valuable(r-2, r,pos,choice(valuable),randint(3,7))
            elif c == -1:
                c = dungeon_map[surround]
                pygame.draw.circle(surface, (surround, surround, surround), pos, r + 7)
                pygame.draw.circle(surface, (252, c, 0), pos, r)
                if value:
                    draw_valuable(min(10, r), r,pos,choice(valuable),randint(3,7))
            else:
                if surround != None:
                    pygame.draw.circle(surface, (surround, surround, surround), pos, r + 7)
                pygame.draw.circle(surface, (c, c, c), pos, r)
                if value:
                    draw_valuable(min(10, r), r,pos,choice(valuable),randint(3,7))
            return (pos[0] - 1, pos[1] - 1)

        def make_hub_planet():

            r = randint(75, 125)
            if terramode:
                if randint(0, 1):
                    pos = (randint(50, size[0] // 2 - border // 2 - superradius), randint(50, size[1] - 50))
                else:
                    pos = (randint(size[0] // 2 + border // 2 + superradius, size[0] - 50), randint(50, size[1] - 50))
            else:
                if mirrored:
                    pos = (randint(50, size[0] // 2 - 50), randint(50, size[1] - 50))
                    while abs(complex(pos[0], pos[1]) - center_pos) < r + 200:
                        pos = (randint(50, size[0] // 2 - 50), randint(50, size[1] - 50))
                else:
                    pos = (randint(50, size[0] - 50), randint(50, size[1] - 50))
                    while abs(complex(pos[0], pos[1]) - center_pos) < r + 200:
                        pos = (randint(50, size[0] - 50), randint(50, size[1] - 50))

            valuables = (r // 25) ** 2
            pygame.draw.circle(surface, (0, 0, 0), pos, r)  #dirt
            pygame.draw.circle(surface, (1, 1, 1), pos, r // 3)  #stone
            pygame.draw.circle(surface, (2, 2, 2), pos, r, 2)  #grassring
            pygame.draw.circle(surface, (30, 30, 30), pos, r - 3, 2)  #woodring
            for x in range(valuables * 5):
                rad = randint(1, 10)
                npos = get_randrad(pos, r - 10 - rad)
                pygame.draw.circle(surface, (252, 2, 252), npos, rad)  #air
            for x in range(valuables):
                rad = randint(4, 7)
                npos = get_randrad(pos, r - 5 - rad)
                pygame.draw.circle(surface, choice(valuable), npos, rad)

            return pos

        def get_randrad(pos, radius):
            radius = random() * radius
            angle = random() * 2 * pi
            return (int(pos[0] + radius * cos(angle)),
                    int(pos[1] + radius * sin(angle)))

        def get_randradrange(pos, minradius, maxradius):
            radius = randint(minradius, maxradius)
            angle = random() * 2 * pi
            return (int(pos[0] + radius * cos(angle)),
                    int(pos[1] + radius * sin(angle)))

        def draw_valuable(min_radius, max_radius, planetpos, material, size):
            r = random() * 2 * pi
            radius = randint(min_radius, max_radius)
            pos = (
            int(planetpos[0] + radius  * cos(r)), int(planetpos[1]+ radius * sin(r)))
            pygame.draw.circle(surface, material, pos, size)

        def make_terra(surface, size):
            pos = (size[0] // 2, size[1] // 2)
            r = superradius
            valuables = (r // 25) ** 2

            pygame.draw.circle(surface, (0, 0, 0), pos, r)  #dirt
            pygame.draw.circle(surface, (30, 30, 30), pos, 3 * r // 4, r // 100)  #wood
            pygame.draw.circle(surface, (1, 1, 1), pos, r // 2)  #stone
            pygame.draw.circle(surface, (59, 59, 59), pos, r // 5)  #jungle
            pygame.draw.circle(surface, (2, 2, 2), pos, r, 2)  #grassring

            for name, minradius, maxradius, amount, size in planetdata:
                minradius = int(r * minradius)
                maxradius = int(r * maxradius)
                for x in range(int(amount * valuables)):
                    npos = get_randradrange(pos, minradius, maxradius)
                    c = ntiles[name]
                    usize = randint(size[0], size[1])
                    if usize > 1:
                        pygame.draw.circle(surface, (c, c, c), npos, usize)  #air
                    else:
                        surface.set_at(npos, (c, c, c))

            #caverns
            for x in range(int(caverns * valuables)):
                npos = get_randradrange(pos, r * 0.25, r * 0.75)
                pygame.draw.circle(surface, (255, 255, 255), npos, randint(*cavernsize))
            for x in range(int(dirtcaverns * valuables)):
                npos = get_randradrange(pos, r * 0.75, r * 0.9)
                pygame.draw.circle(surface, (252, 2, 255), npos, randint(*dirtcavernsize))
            #liquids
            for x in range(int(water * valuables)):
                npos = get_randradrange(pos, r // 3, r * 0.9)
                pygame.draw.circle(surface, (254, 0, 255), npos, randint(watersize[0], watersize[1]))
            for x in range(int(lava * valuables)):
                npos = get_randradrange(pos, r // 4, r // 3)
                pygame.draw.circle(surface, (254, 1, 255), npos, randint(lavasize[0], lavasize[1]))
            for x in range(chasms):
                if x == 0:
                    a = random() * pi + pi
                    while abs(a - 1.5 * pi) < 0.2 * pi:
                        a = random() * pi + pi
                else:
                    a = random() * pi * 2
                    while abs(a - 1.5 * pi) < 0.2 * pi:
                        a = random() * pi + pi
                #corruption
                deep = randint(chasmdeepness[0], chasmdeepness[1]) * 0.01 * r
                surface = draw_chasm(surface, pos, deep, r + 5, a, a + chasmthickness)
                #pygame.image.save(surface, "mask2.png")

            ##jungle
            for x in range(int(valuables * jcircle)):
                npos = get_randradrange(pos, 5, r // 5)
                pygame.draw.circle(surface, (255, 255, 255), npos, randint(*jcirclesize))
                #pygame.draw.circle(surface, (60,60,60), npos, randint(*jcirclesize), 1)
            for x in range(int(valuables * jrect)):
                rect = pygame.rect.Rect((0, 0), (randint(*jrectsize), randint(*jrectsize)))
                rect.center = get_randradrange(pos, 5, r // 4)
                pygame.draw.rect(surface, (254, 1, 255), rect)
            for x in range(int(valuables * jdot)):
                npos = get_randradrange(pos, 5, r // 5)
                surface.set_at(npos, (48, 48, 48))
            for x in range(int(valuables * jarc)):
                npos = get_randradrange(pos, r // 10, r // 5)
                pygame.draw.circle(surface, (60, 60, 60), npos, randint(*jarcsize), 1)
            ##trees
            for x in range(trees):
                a = random() * pi + pi
                npos = (int(pos[0] + r * cos(a)),
                        int(pos[1] + r * sin(a)))
                while npos[1] > border + 100:
                    a = random() * pi + pi
                    npos = (int(pos[0] + r * cos(a)),
                            int(pos[1] + r * sin(a)))
                h = randint(5, 25)
                surface.blit(make_tree(h), (npos[0] - 1, npos[1] - h - 1))
                s = pygame.surface.Surface((5, 2))
                s.fill((2, 2, 2))
                surface.blit(s, (npos[0] - 2, npos[1] - 1))

            ##altars
            for x in range(altar_count):
                npos = get_randradrange(pos, r // 5, r // 2)
                surface.blit(multis["altar"], npos)

        loadingbar.set_progress(20, "Planetoids: drawing some circles")

        chestpos = []
        if mirrored:
            stone_planets //= 2
            large_planets //= 2
            small_planets //= 2
            mul = 3
        else:
            mul = 5
        if not terramode or sizetype == 1:
            for x in range(stone_planets):
                chestpos.append(make_hub_planet())
            for x in range(large_planets):
                chestpos.append(make_planet(*choice(data1), value=True))
            for x in range(0, (sizetype + 1) * mul):
                for d in data1:
                    chestpos.append(make_planet(*d))
            for x in range(dungeon_planets):
                chestpos.append(make_planet(*choice(data3)))
            for x in range(0, (sizetype + 1) * mul):
                for d in data2:
                    chestpos.append(make_planet(*d))

            for x in range(small_planets):
                chestpos.append(make_planet(*choice(data2)))

        if mirrored:
            mirror = surface.subsurface(0, 0, size[0] // 2, size[1])
            mirror = pygame.transform.flip(mirror, 1, 0)
            surface.blit(mirror, (size[0] // 2, 0))


        if terramode:
            if atlantis:
                pygame.draw.circle(surface, (255, 255, 255), (header["spawn"][0], header["spawn"][1]), 50)
                pygame.draw.circle(surface, (54, 54, 54), (header["spawn"][0], header["spawn"][1]), 50, 2)

            make_terra(surface, size)


        else:  #spawnplanet
            items = [(50, "Torch"), (25, "Acorn"), (5, "Daybloom Seeds"), (5, "Moonglow Seeds"),
                     (5, "Blinkroot Seeds"), (5, "Waterleaf Seeds"), (5, "Fireblossom Seeds"),
                     (5, "Deathweed Seeds"), (5, "Shiverthorn Seeds"), (1, "Life Crystal"), (2, "Mana Crystal"), (50, "Book"),
                     (200, "Cobweb"), (5, "Mushroom Grass Seeds"), (1, "Snow Globe"), (10, "Mud Block"),
                     (250, "Dirt Block"), (250, "Dirt Block"),
                     (1, "Shiny Red Balloon"),
                    ]

            for x in range(20 - len(items)):
                items.append((0, None))
            # draw the spawn planet
            radius = 100
            center = header["spawn"][0], header["spawn"][1] + 50
            if atlantis:
                pygame.draw.circle(surface, (255, 255, 255), center, radius + 50)
                pygame.draw.circle(surface, (54, 54, 54), center, radius + 50, 2)
            pygame.draw.circle(surface, (52, 52, 52), center, radius)
            pygame.draw.circle(surface, (2, 2, 2), center, radius)
            pygame.draw.circle(surface, (0, 0, 0), center, radius - 2)
            pygame.draw.circle(surface, (1, 1, 1), center, radius // 2)
            pygame.draw.circle(surface, (30, 30, 30), center, radius // 4)

            for _ in range(3):#sand
                draw_valuable(20, 40, center, (53,53,53), 7)

            for _ in range(2):#clay
                draw_valuable(20,50, center, (40,40,40), 7)

            for _ in range(2):#iron
                draw_valuable(20,30, center, (6,6,6), 4)

            for _ in range(3):#copper
                draw_valuable(20, 30, center, (7,7,7), 5)

            chests.append(((header["spawn"][0] - 1, header["spawn"][1] + 49), items, choice(chestnames)))

            header["spawn"] = header["spawn"][0], header["spawn"][1] - radius + 50

            surface.blit(make_tree(25), (header["spawn"][0] + 1, header["spawn"][1] - 25))
        surface.blit(multis["altar"], (header["spawn"][0] - 2, header["spawn"][1] - 2))

        #draw the lower border of the world. Falling into the void was fun in minecraft,
        #not su much here, as it will just make "splat"
        pygame.draw.rect(surface, (57, 57, 57), ((0, size[1] - 100), (size[0], 100)))
        pygame.draw.rect(surface, (254, 1, 255), ((0, size[1] - 150), (size[0], 50)))

        #not pure terra mode
        if terramode != 2:
            #ocean planetoids
            pygame.draw.circle(surface, (53, 53, 53), (0, 500), 500)
            pygame.draw.circle(surface, (54, 54, 54), (0, 500), 500, 1)
            pygame.draw.circle(surface, (253, 0, 255), (0, 301), 300)

            pygame.draw.circle(surface, (53, 53, 53), (size[0], 500), 500)
            pygame.draw.circle(surface, (54, 54, 54), (size[0], 500), 500, 1)
            pygame.draw.circle(surface, (253, 0, 255), (size[0], 301), 300)

            a = len(chestcontents)
            if sizetype == 0:b = max_altar_planet//2
            elif sizetype == 2:b = max_altar_planet*2
            elif sizetype == 1:b = max_altar_planet
            else:
                raise IndexError("Invalid world size")

            if mirrored:
                double = chestcontents[:]
                for pos in chestpos:
                    pos = size[0] - pos[0], pos[1]
                    tile = surface.get_at(pos)[0]
                    if tile == 25 or tile == 23:
                        surface.blit(multis["shadoworb"], pos)  #place shadoworb into corruption
                    elif tile == 58:  #hellfurnace into hellstone
                        surface.blit(multis["hellfurnace"], pos)
                    elif b:
                        b -= 1
                        surface.blit(multis["altar"], pos)
                    elif a:
                        chests.append((pos, chestcontents.pop(), choice(chestnames)))  #place chests
                        a -= 1

                    else:
                        print("Warning, could not place all content!")
                        break  # we usually have more planets than chests, so lets get out of here
                chestcontents = double
            a = len(chestcontents)
            b = max_altar_planet
            for pos in chestpos:
                tile = surface.get_at(pos)[0]
                if tile == 25 or tile == 23:
                    surface.blit(multis["shadoworb"], pos)  #place shadoworb into corruption
                elif tile == 58:  #hellfurnace into hellstone
                    surface.blit(multis["hellfurnace"], pos)
                elif special_chests:
                    multi, content = special_chests.pop()
                    chests.append((pos, content, multi))
                elif b:
                    b -= 1
                    surface.blit(multis["altar"], pos)
                elif a:
                    chests.append((pos, chestcontents.pop(), choice(chestnames)))  #place chests
                    a -= 1
                else:
                    break  # we usually have more planets than chests, so lets get out of here

            if a:
                print("------------------Warning: {} unallocated chests------------------".format(a))
                import time

                time.sleep(1)

        loadingbar.set_progress(30, "Planetoids: hiding goodies")
        for shadoworb in shadoworbpos:
            surface.blit(multis["shadoworb"], shadoworb)
        for chest in chests:
            #draw the chests into the world texture
            surface.blit(multis[chest[2]], chest[0])
            # below is to make sure every chest stands on something, so they dont glitch
            d = surface.get_at((chest[0][0], chest[0][1] + 2))[0]
            if d > 250 or d == 51:
                surface.set_at((chest[0][0], chest[0][1] + 2), (0, 0, 0))
            d = surface.get_at((chest[0][0] + 1, chest[0][1] + 2))[0]
            if d > 250 or d == 51:
                surface.set_at((chest[0][0] + 1, chest[0][1] + 2), (0, 0, 0))

        # save the "source" of the world. Helped plenty with debugging.
        #pygame.image.save(surface, "mask.png")

        for x in range(1000 - len(chests)):  #fill in nonechests, as terraria always has 1000 chests
            chests.append(None)

        self.header = header

        z = header["width"] * header["height"]  #tileamount
        total = z

        #list of tiles : walls
        walls = defaultdict(lambda: None, {0: 2,
                                           25: 3,
                                           9: 11,
                                           8: 10,
                                           7: 12,
                                           30: 4,
                                           58: 13,
                                           21: 2,
                                           31: 3,
                                           51: 62,#cobweb gets spider nest wall
                                           40: 6,
                                           })

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

        loadingbar.set_progress(50, "Planetoids: writing tile data")
        self.tiles = write_tiles(surface, header, walls, True, callback = loadingbar)

        self.chests = chests

        self.signs = [None] * 1000

        self.names = names
        self.npcs = [('Guide', (header["spawn"][0] * 16, (header["spawn"][1] - 3) * 16), 1,
                      (header["spawn"][0], header["spawn"][1] - 3)),
                     ('Old Man', (header["spawn"][0] * 16 - 16, (header["spawn"][1] - 3) * 16), 1,
                      (header["spawn"][0], header["spawn"][1] - 3))]
        if merch: self.npcs.append(
            ('Merchant', (header["spawn"][0] * 16 - 16, (header["spawn"][1] - 3) * 16), 1,
             (header["spawn"][0], header["spawn"][1] - 3)))
        self.loadingbar = loadingbar



if __name__ == "__main__":
    gen = Generator()
    gen.run()
