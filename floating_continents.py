"""
As I continue working on other world gens, I will likely pull code out of here into more general libs
especially chest code will be affected
"""

# imports in no particular order
from math import sqrt, cos, sin, pi
from random import *

import pygame
import numpy

from tinterface import World
import database as db
from tlib import *
from binarysplit import join


## ask the user what kind of world he/she wants.
print("Select world size")
print("1: small  (4200 x 1200)")
print("2: medium (6300 x 1800)")
print("3: large  (8400 x 2400)")
print("4: square (2400 x 2400)")
valid = [1, 2, 3, 4]
sizetype = 0
while sizetype not in valid:
    try:
        sizetype = int(input("World size:"))
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
        starttype = int(input("Start condition:"))
    except:
        pass
    if starttype not in valid:
        print("Please put in 1,2,3 or 4 and then hit enter, cant be that hard, right?")
print("")
valid = [1, 2, 3, 4]
print("Select extra difficulty, you may select multiple by entering multiple numbers.")
print("By entering nothing you play normal")
print("1: Darkness! I dont need a puny sun!")
print("2: Less loot! I want to keep exploring!")
print("3: Atlantis, I want to conquer the world from my sunken planet!")
dif = input("Difficulty:")

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
spawn = [(2100, 180), (3150, 300), (4200, 400), (1200, 200)][sizetype]

if sizetype == 3:
    #square world has almost the same amount of tiles as small
    # so in the following code it will be regarded as a small world.
    sizetype = 0
if "1" in dif:  #if no sun
    ground = [-1200.4, -1800.4, -2400.4][sizetype]
else:
    ground = [300.4, 460.4, 610.4][sizetype]
if "1" in dif:  #if no sun
    rock = [0.4, 0.4, 0.4][sizetype]
else:
    rock = [400.4, 650.4, 1050.4][sizetype]

chestcount = [400, 600, 800][sizetype]
#I would prefer [500,1000,1500] chests
#but terraria only allows 1000 chests as well as 1000 signs, never forget that limit

large_planets = [0, 50, 100][sizetype]
dungeon_planets = [5, 10, 20][sizetype]
small_planets = [700, 1000, 1300][sizetype]


#header data
header = {'spawn': spawn, 'groundlevel': ground, 'is_bloodmoon': is_blood,
          'dungeon_xy': spawn, 'worldrect': (0, size[0] * 16, 0, size[1] * 16),
          'is_meteor_spawned': 0, 'gob_inv_time': 0, 'rocklevel': rock,
          'gob_inv_x': 0.0, 'is_day': is_day, 'shadow_orbs_broken': 0,
          'width': size[0], 'version': 12, 'gob_inv_type': 0,
          'bosses_slain': (0, 0, 1), 'gob_inv_size': 0, 'height': size[1],
          'ID': 1394008879, 'moonphase': 0, 'name': 'Planetoids',
          'is_a_shadow_orb_broken': 0, 'time': time, "npcs_saved" : (0,0,0)}

#initialize a texture to hold all tile data
#could have used an array as well, like numpy, but I am more familiarized with pygame than numpy
surface = pygame.surface.Surface(size)
if "3" in dif:  #if waterworld
    surface.fill((254, 0, 255))
    pygame.draw.rect(surface, (54, 54, 54), ((0, size[0]), (-1 + size[1] - size[1] // 6, size[1] // 6)))
    pygame.draw.rect(surface, (255, 255, 255), ((0, size[0]), (size[1] - size[1] // 6, size[1] // 6)))
else:
    surface.fill((255, 255, 255))

#list of all items that will land in chests along with their amount
#original chestitem list was extracted from a normal fresh terraria world, and then modified
itemdata = {'Swiftness Potion': 10, 'Cloud in a Bottle': 50,
            'Lucky Horseshoe': 5, 'Gold Bar': 500, 'Shiny Red Balloon': 5,
            'Wooden Arrow': 1000, 'Meteorite Bar': 200, 'Throwing Knife': 5000,
            'Wooden Boomerang': 5, 'Flipper': 10, 'Blowpipe': 5, 'Dynamite': 500,
            'Band of Regeneration': 100, 'Flaming Arrow': 3000, 'Starfury': 3,
            'Aqua Scepter': 3, 'Battle Potion': 50, 'Hellfire Arrow': 5000,
            'Shine Potion': 50, 'Trident': 7, 'Gills potion': 50,
            'Silver Bar': 600, 'Gravitation Potion': 300,
            'Regeneration Potion': 50, 'Water Walking Potion': 50,
            'Invisibility Potion': 50, 'Magic Mirror': 100,
            'Magic Power Potion': 50, 'Glowstick': 5000, 'Healing Potion': 1000,
            'Enchanted Boomerang': 100, 'Handgun': 5, 'Blue Moon': 5,
            'Staff of Regrowth': 3, 'Night Owl Potion': 50, 'Angel Statue': 50,
            'Thorns Potion': 50, 'Mana Regeneration Potion': 50,
            'Archery Potion': 50, 'Feral Claws': 10, 'Gold Coin': 300,
            'Hunter Potion': 50, 'Bottle': 300, 'Silver Bullet': 500,
            'Iron Bar': 700, 'Dark Lance': 2, 'Breathing Reed': 10,
            'Grenade': 100, 'Aglet': 10, 'Restoration Potion': 300,
            'Magic Missile': 5, 'Hermes Boots': 50, 'Muramasa': 3,
            'Bomb': 300, 'Spear': 15, 'Lesser Healing Potion': 200,
            'Silver Coin': 5000, 'Torch': 3000, 'Anklet of the Wind': 5,
            'Cobalt Shield': 5, 'Featherfall Potion': 50, "Jester's Arrow": 2000,
            'Shuriken': 10000, 'Copper Bar': 1000, 'Obsidian Skin Potion': 50,
            'Spelunker Potion': 50, 'Lesser Restoration Potion': 100,
            'Ironskin Potion': 50, "Life Crystal": 50, "Mana Crystal": 150}

#multiply item amounts depending on world size
#there are more chests to be filled after all
#and larger worlds have less chests than they should have
#so we overfill medium/large chests
if sizetype == 0:
    for item in itemdata:
        itemdata[item] = itemdata[item] // 2  + itemdata[item] % 2
elif sizetype == 2:
    for item in itemdata:
        itemdata[item] = itemdata[item] * 2
if "2" in dif:
    for item in itemdata:
        itemdata[item] = itemdata[item] // 2 + itemdata[item] % 2
# list of items that dont stack beyond 1.. if you stack more than that they still work fine
# but I dont like people screaming haxors
no_stack = ["Lucky Horseshoe", 'Cloud in a Bottle', 'Shiny Red Balloon', 'Wooden Boomerang',
            'Flipper', 'Blowpipe', 'Band of Regeneration', 'Starfury', 'Aqua Scepter',
            'Trident', 'Enchanted Boomerang', 'Handgun', 'Blue Moon', 'Staff of Regrowth',
            'Angel Statue', 'Feral Claws', 'Dark Lance', 'Breathing Reed', 'Aglet',
            'Magic Missile', 'Hermes Boots', 'Muramasa', 'Spear', 'Anklet of the Wind',
            'Cobalt Shield', "Life Crystal", "Mana Crystal"]

#count amount of items to be placed
itemtotal = 0
for item in itemdata:
    itemtotal += itemdata[item]

print(str(len(itemdata)) + " different items loaded for chests")

target = itemtotal // chestcount  #target amount of items per chest


def pick(items, targetnumber):  #picks randomly items for a chest planetoids
    current = 0
    content = []
    while targetnumber > current:
        item = choice(tuple(items.keys()))
        if item in db.itemlist:
            amount = randint(1, min(db.itemlist[item], items[item], targetnumber - current))
        else:
            amount = randint(1, min(3, items[item], targetnumber - current))
        items[item] -= amount
        if items[item] < 1:
            del (items[item])
        content.append((amount, item))
        current += amount
        if len(content) > 19:
            break
    for x in range(20 - len(content)):  #chests always have 20 slots
        content.append((0, None))
    return content, current, items


chestcontents = []

while itemtotal > 0:  # fill those chests with something useful.. or not, angel statue ftw.
    i, c, itemdatabase = pick(itemdata, min(target, itemtotal))
    chestcontents.append(i)
    print(c)
    itemtotal -= c

print (str(len(chestcontents)) + " chests filled")  # give the user a sign of life every once a while
import time

s = time.clock()


def find_rects(size, amount):
    rects = []
    while len(rects) < amount:
        new = pygame.Rect(
            ((randint(0, size[0] - 100), randint(0, size[1] - 100)), (randint(100, 700), randint(100, 200))))
        col = False
        for rect in rects:
            if rect.colliderect(new):
                col = True
        if not col:
            rects.append(new)
    return rects


chestpos = []

areas = find_rects(size, 100)
print (time.clock() - s)
print (areas)
for area in areas:
    #pygame.draw.rect(surface, (0,0,0), area)
    pygame.draw.ellipse(surface, (0, 0, 0), area, 0)
    pygame.draw.ellipse(surface, (2, 2, 2), area, 1)
    pygame.draw.line(surface, (2, 2, 2),
                     (area.x, -1 + area.y + area.h // 2),
                     (-1 + area.x + area.w, -1 + area.y + area.h // 2),
                     3)
    pygame.draw.rect(surface, (255, 255, 255), area.inflate(4, -area.h // 2).move(0, -area.h // 4))
#raise AssertionError("")


chests = []
# contents of the spawn chest
items = [(5, "Torch"), (10, "Acorn"), (1, "Daybloom Seeds"), (1, "Moonglow Seeds"),
         (1, "Blinkroot Seeds"), (1, "Waterleaf Seeds"), (1, "Fireblossom Seeds"),
         (1, "Life Crystal"), (1, "Mana Crystal")]
for x in range(20 - len(items)):
    items.append((0, None))
# draw the spawn planet
pygame.draw.circle(surface, (255, 255, 255), (header["spawn"][0], header["spawn"][1] + 50), 60)
if "3" in dif:
    pygame.draw.circle(surface, (54, 54, 54), (header["spawn"][0], header["spawn"][1] + 50), 60, 1)
pygame.draw.circle(surface, (52, 52, 52), (header["spawn"][0], header["spawn"][1] + 55), 50)
pygame.draw.circle(surface, (2, 2, 2), (header["spawn"][0], header["spawn"][1] + 50), 50)
pygame.draw.circle(surface, (1, 1, 1), (header["spawn"][0], header["spawn"][1] + 50), 25)
pos = (
int(header["spawn"][0] + 30 * cos(random() * 2 * pi)), int(header["spawn"][1] + 50 + 30 * sin(2 * random() * pi)))
pygame.draw.circle(surface, (40, 40, 40), pos, 4)
pos = (
int(header["spawn"][0] + 20 * cos(random() * 2 * pi)), int(header["spawn"][1] + 50 + 20 * sin(2 * random() * pi)))
pygame.draw.circle(surface, (6, 6, 6), pos, 3)
pygame.draw.circle(surface, (30, 30, 30), (header["spawn"][0], header["spawn"][1] + 50), 15)
chests.append(((header["spawn"][0] - 1, header["spawn"][1] + 49), items))
#make a chestimage
chestsurf = pygame.surface.Surface((2, 2))
chestsurf.set_at((0, 0), (21, 0, 0))
chestsurf.set_at((0, 1), (21, 0, 18))
chestsurf.set_at((1, 0), (21, 18, 0))
chestsurf.set_at((1, 1), (21, 18, 18))
# make shadow orb
orbsurf = pygame.surface.Surface((2, 2))
orbsurf.set_at((0, 0), (31, 0, 0))
orbsurf.set_at((0, 1), (31, 0, 18))
orbsurf.set_at((1, 0), (31, 18, 0))
orbsurf.set_at((1, 1), (31, 18, 18))
# make altar
shadowsurf = pygame.surface.Surface((3, 2))
shadowsurf.set_at((0, 0), (26, 0, 0))
shadowsurf.set_at((0, 1), (26, 0, 18))
shadowsurf.set_at((1, 0), (26, 18, 0))
shadowsurf.set_at((1, 1), (26, 18, 18))
shadowsurf.set_at((2, 0), (26, 36, 0))
shadowsurf.set_at((2, 1), (26, 36, 18))
# make hellfurnace
hellsurf = pygame.surface.Surface((3, 2))
hellsurf.set_at((0, 0), (77, 0, 0))
hellsurf.set_at((0, 1), (77, 0, 18))
hellsurf.set_at((1, 0), (77, 18, 0))
hellsurf.set_at((1, 1), (77, 18, 18))
hellsurf.set_at((2, 0), (77, 36, 0))
hellsurf.set_at((2, 1), (77, 36, 18))
#plunk down an altar onto the spawn
surface.blit(shadowsurf, (header["spawn"][0] - 1, header["spawn"][1] - 2))
a = len(chestcontents)
for pos in chestpos:
    if surface.get_at(pos)[0] == 25:
        surface.blit(orbsurf, pos)  #place shadoworb into corruption
    elif surface.get_at(pos)[0] == 58:
        surface.blit(hellsurf, pos)
    elif a:
        chests.append((pos, chestcontents.pop()))  #place chests
        a -= 1
    else:
        break  # we usually have more planets than chests, so lets get out of here

#draw the lower border of the world. Falling into the void was fun in minecraft,
#not su much here, as it will just make "splat"
pygame.draw.rect(surface, (57, 57, 57), ((0, size[1] - 20), (size[0], 50)))
pygame.draw.rect(surface, (254, 1, 255), ((0, size[1] - 23), (size[0], 3)))

for chest in chests:
    #draw the chests into the world texture
    surface.blit(chestsurf, chest[0])
    # below is to make sure every chest stands on something, so they dont glitch
    if surface.get_at((chest[0][0], chest[0][1] + 2))[0] > 250:
        surface.set_at((chest[0][0], chest[0][1] + 2), (0, 0, 0))
    if surface.get_at((chest[0][0] + 1, chest[0][1] + 2))[0] > 250:
        surface.set_at((chest[0][0] + 1, chest[0][1] + 2), (0, 0, 0))

# save the "source" of the world. Helped plenty with debugging.
pygame.image.save(surface, "mask.png")

for x in range(1000 - len(chests)):  #fill in nonechests, as terraria always has 1000 chests
    chests.append(None)
#world.make_split()
print ("World fully generated")  #give another lifesign
header["groundlevel"] = header["groundlevel"] + 500  #push down backgrounds a bit, they are annoying
header["rocklevel"] = header["rocklevel"] + 500
with open("0.part", "wb") as f:  #write the header
    set_header(f, header)
print("done writing header")  #sounds cool

z = header["width"] * header["height"]  #tileamount
total = z  #yeah redundancy is cool

#list of tiles : walls
walls = {0: 2,
         1: 1,
         25: 3,
         9: 11,
         8: 10,
         7: 12,
         30: 4,
         58: 13,
         21: 2,
         31: 3,
         26: 0,
         77: 0,
         }

with open("1.part", "wb") as a:  #write the tile data
    for x in range(size[0]):
        for y in range(size[1]):
            c = surface.get_at((x, y))
            c0 = c[0]
            if c0 == 255:
                set_tile(a, (None, None, 0, None))
            elif c0 == 254:  #liquid
                if c[1]:  #if lava
                    set_tile(a, (None, None, -c[2], None))
                else:
                    set_tile(a, (None, None, c[2], None))
            elif c0 in db.multitiles:  #if it has multitiledata.. i hate those
                set_tile(a, (c0, walls[c0], 0, (c[1], c[2])))
            elif c0 in walls:  #put down background walls if we ewant them
                set_tile(a, (c0, walls[c0], 0, None))
            elif c0 > 230:  #only have a wall
                set_tile(a, (None, c0 - 230, 0, None))
            else:  #or just write a nice normal tile
                set_tile(a, (c0, None, 0, None))
            if z % (header["height"] * 10) == 0:  #give lifesigns
                print
                "%6.2f%% done writing tiles" % ((total - z) * 100.0 / (header["width"] * header["height"]))
            z -= 1
print("done writing tiles")
with open("2.part", "wb") as a:  #write chestdata
    set_chests(a, chests)
print ("done writing chests")
with open("3.part", "wb") as f:
    for sign in [None] * 1000:
        set_sign(f, sign)
print("done writing signs")
with open("4.part", "wb") as f:
    set_npc(f, (
    'Guide', (header["spawn"][0] * 16, (header["spawn"][1] - 3) * 16), 1, (header["spawn"][0], header["spawn"][1] - 3)))
    set_npc(f, None)
print("done writing npcs")
with open("5.part", "wb") as f:
    set_trail(f, (1, header["name"], header["ID"]))
print("done writing trail")
name = "world1.wld"
join(name)  #this just puts all the binary parts into one world file
print ("done joining world " + name)  #yay!
print ("A world has been created!")
