import sys
import time

from tlib import *
from binarysplit import *
from tinterface import World

# sys.argv.append("world2.wld")
from database import npclist
#npclist = ["Guide", "Merchant", "Nurse", "Dryad", "Clothier", "Demolitionist", "Arms Dealer", "Old Man"]
def run(worldpath=None):
    if hasattr(sys, "frozen"):
        os.chdir(os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding())))
    if len(sys.argv) < 2 and worldpath == None:
        print("No World supplied, shutting down in 5 seconds")
        time.sleep(5)
    else:
        if len(sys.argv) < 2:
            world = World(worldpath)
        else:
            world = World(sys.argv[1])
        print("Reading world data, this may take a while")
        world.ready_npcs()
        print("Data prepared")
        npcs = []
        print("Following NPCs found:")
        for npc in world.npcs:
            npcs.append(npc)
            if npc[2]:
                print("%s without a home") % (npc[0])
            else:
                print("%s with a home") % (npc[0])
        world.make_split()
        while 1:
            print("")
            print("Select a NPC to add")
            x = 1
            print("0: Save & Exit")
            for npc in npclist:
                print("%d: %s") % (x, npc)
                x += 1
            pick = x
            while pick >= x or pick < 0:
                try:
                    pick = int(raw_input("NPC:"))
                except:
                    pass
                if pick >= x or pick < 0:
                    print("Please put in a number and then hit enter, cant be that hard, right?")
            i = pick
            if pick == 0:
                print("Writing world data")
                with open("4.part", "wb") as f:
                    for npc in npcs:
                        set_npc(f, npc)
                    set_npc(f, None)
                join("worldx.wld")
                cleanup()
                print("Done")
                time.sleep(5)
                break
            else:
                pick = 0
                print("There are %d remaining slots for npcs") % (1000 - len(npcs))
                print('How many of "%s" do you want to add?') % (npclist[i - 1])
                while pick < 1:
                    try:
                        pick = int(raw_input("NPC:"))
                    except:
                        print("Error occured when parsing input, please try again writing ONE number")
                    if pick > 1000 - len(npcs):
                        print("You cant add that many npcs, Terraria cant take it, have pity.")
                        pick = 0
                for x in range(pick):
                    npcs.append((
                    npclist[i - 1], (world.header["spawn"][0] * 16, (world.header["spawn"][1] - 3) * 16), 1,
                    (world.header["spawn"][0], world.header["spawn"][1] - 3)))
                print("%d %s added to 'to do' list") % (pick, npclist[i - 1])


if __name__ == "__main__":
    run()
