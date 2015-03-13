from tinterface import World

tiles = []
from tlib import *
import sys
import time

z = 0
x = 0

# sys.argv.append("world1.wld")
if len(sys.argv) < 2:
    print
    "No World supplied, shutting down in 5 seconds"
    time.sleep(5)
else:
    origin = sys.argv[1]
    world = World(origin)
    header = world.header

    for tile in world.tiles:
        if tile[2] >= 0:
            tile = (tile[0], tile[1], 255, tile[3])
        tiles.append(tile)

        ##    if tile[0] == 0:
        ##        ntile = (1, tile[1], tile[2], tile[3])
        ##    elif tile[0] == 2:
        ##        if random()>0.01:
        ##            ntile = (1, tile[1], tile[2], tile[3])
        ##        else:
        ##            ntile = tile
        ##    elif tile[2] > 0:
        ##        ntile = (tile[0], tile[1], -tile[2], tile[3])
        ##    else:
        ##        ntile = tile
        z += 1

        if not z % (100 * world.header["height"]):
            print
            "%6.2f%% done reading content" % (z * 100.0 / (world.header["width"] * world.header["height"]))
            x += 1
world.make_split()
from binarysplit import join

y = z
with open("1.part", "wb") as a:
    for t in tiles:
        set_tile(a, t)
        if not z % (world.header["height"] * 100):
            print
            "%6.2f%% done writing content" % ((y - z) * 100.0 / (world.header["width"] * world.header["height"]))
        z -= 1
print("done writing tiles")
join("world7.wld")
print
"done"

