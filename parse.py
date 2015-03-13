import json
import time
import sys

from tinterface import World
from tlib import *


start = time.clock()
method = 0
checklevel = 1
if "checklevel" in sys.argv:
    pos = sys.argv.index("checklevel")
    checklevel = sys.argv[pos + 1]

# sys.argv.append("world2.txt")
if len(sys.argv) > 1:
    argvtype = sys.argv[1][-3:]
    if argvtype == "wld":
        print("parsing world->json")
        path = sys.argv[1]
        jpath = path[:-3] + "txt"
    elif argvtype == "txt":
        print("parsing json->world")
        jpath = sys.argv[1]
        path = sys.argv[1][:-3] + "wld"
        method = 1
    else:
        import time

        print("Unrecognized file extension, only accepting wld or txt")
        time.sleep(10)

else:
    import time

    print("Nothing supplied")
    time.sleep(10)
if method:
    with open(jpath, "rt") as f:
        data = json.load(f)
    print("Checklevel: %d" % checklevel)
    if checklevel:
        try:
            data["tiles"]
        except:
            print("Warning: tiles not found")
        try:
            data["header"]
        except:
            print("Warning: header not found")
        try:
            data["signs"]
        except:
            print("Warning: signs not found")
        try:
            data["chests"]
        except:
            print("Warning: chests not found")
        try:
            data["npcs"]
        except:
            print("Warning: npcs not found")
        if not data["header"]["width"] * data["header"]["width"] == len(data["tiles"]):
            print("Warning: tile amount not equal to defined amount in header")
        if len(data["chests"]):
            print("Warning: not 1000 Chestslots")
        if len(data["npcs"]) > 1000:
            print("Warning: more than 1000 NPCs")
        if len(data["signs"]) > 1000:
            print("Warning: more than 1000 signs")
        if checklevel > 1:
            def check_tile(tile):
                return not ((tile[0] == None or
                             tile[0].__class__.__name__ == "int") and
                            (tile[1] == None or
                             tile[1].__class__.__name__ == "int") and
                            tile[2].__class__.__name__ == "int" and
                            (tile[3] == None or tile[3].__class.__name__ == "tuple"))

            def check_sense(tile):
                if tile[0] != None:
                    if tile[0] < 0:
                        print("Negative tile_id")
                        return True
                    elif tile[0] > 255:
                        print("tile_id greater than a byte")
                        return True
                if tile[1] != None:
                    if tile[1] < 0:
                        print("Negative wall_id")
                        return True
                    elif tile[1] > 255:
                        print("wall_id greater than a byte")
                        return True
                if tile[2] > 255:
                    print("liquid cant be greater than 255")
                    return True
                elif tile[2] < -255:
                    print("liquid cant be smaller than -255")
                    return True
                return False

            for tile, x in zip(data["tiles"], range(len(data["tiles"]))):
                if check_tile(tile) or check_sense(tile):
                    print("Invalid tile #%d" % x)
    with open("0.part", "wb") as f:  #write the header
        set_header(f, data["header"])
    print("done writing header")
    with open("1.part", "wb") as f:
        for tile in data["tiles"]:
            set_tile(f, tile)
    with open("2.part", "wb") as a:
        set_chests_uni(a, data["chests"])
    print
    "done writing chests"
    with open("3.part", "wb") as f:
        for sign in data["signs"]:
            set_sign(f, sign)
    print
    "done writing signs"
    with open("4.part", "wb") as f:
        for npc in data["npcs"]:
            set_npc(f, npc)
        set_npc(f, None)
    print
    "done writing npcs"
    with open("5.part", "wb") as f:
        set_trail(f, (1, data["header"]["name"], data["header"]["ID"]))
    print
    "done writing trail"
    name = "world1.wld"
    from binarysplit import join

    join(name, True)  #this just puts all the binary parts into one world file
    print
    "done joining world " + name  #yay!
    print
    "A world has been created!"

else:
    print("parsing header")
    world = World(path)
    print("parsing tiles")
    tiles = []
    for tile in world.tiles:
        tiles.append(tile)
    print("parsing chests")
    chests = []
    world.ready_chests()
    for chest in world.chests:
        chests.append(chest)
    print("parsing signs")
    world.ready_signs()
    signs = []
    for sign in world.signs:
        signs.append(sign)
    print("parsing npcs")
    world.ready_npcs()
    npcs = []
    for npc in world.npcs:
        npcs.append(npc)
    print("saving")
    data = {"header": world.header,
            "tiles": tiles,
            "chests": chests,
            "signs": signs,
            "npcs": npcs}

    with open(jpath, "wt") as f:
        json.dump(data, f)

print("took %3.3f seconds" % (time.clock() - start))
