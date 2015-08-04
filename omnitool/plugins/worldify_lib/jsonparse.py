import json

import database as db
import colorlib


json_db_version = 2

##def get_standard_config():
##    
##    planetoids = {}
##    maper = {}
##    render = {}
##    npc = {"NPCs" : ["Guide", "Merchant", "Nurse", "Dryad", "Clothier", "Demolitionist", "Arms Dealer", "Old Man"]}
##    worldify = {"worldname" : "ImageWorld"}
##    options = {"worldify" : worldify,
##               "planetoids" : planetoids,
##               "mapper" : mapper,
##               "npc" : npc}
##    return options
##def loadoptions(path = "config.txt"):
##    local = os.listdir(os.getcwd())
##    if "config.txt" in local:
##        with open(path, "r") as f:
##            options = json.load(f,encoding = "ascii")
##            
##    else:
##        options = get_standard_config()
##        saveoptions(options)
##    return options
##    
##def saveoptions(options = get_standard_config(), path = "config.txt"):
##    with open("config.txt", "wt") as f:
##        json.dump(options,f,encoding = "ascii", sort_keys=True, indent=4)
def dump():
    database = {}
    for c, t in zip(colorlib.data, db.tiles):
        if c in db.multitiles:
            b = None
        else:
            b = not c in colorlib.bad
        database[t] = colorlib.data[c], b
    # s = json.dumps(database,encoding = "ascii", sort_keys=True, indent=4)
    with open("db.txt", "wt") as f:
        json.dump((db.version, json_db_version, database), f, encoding="ascii", sort_keys=True, indent=4)
        #json.dump(database,f,encoding = "ascii", sort_keys=True, indent=4)
    return database


def load(path="db.txt"):
    version = 22
    dbversion = 1
    with open(path, "r") as f:
        database = json.load(f, encoding="ascii")
    try:
        database[0]
        version = database[0]
        dbversion = database[1]
        database = database[2]
        print("Database version " + str(dbversion))

    except:
        print("Database version 1")
    for tile in database:
        color, b = database[tile]
        colorlib.data[db.ntiles[tile]] = color
        if b == True:
            if db.ntiles[tile] in colorlib.bad:
                colorlib.bad.remove(b)
        elif b == False:
            if db.ntiles[tile] not in colorlib.bad:
                colorlib.bad.append(db.ntiles[tile])
    return version, dbversion, database


# options = loadoptions()
if __name__ == "__main__":
    d = dump()
    #print ("i" == u"i")

    e = load()
    #print e
    #print
    #print d
