"""Low level interface to Terraria data"""
from struct import unpack, pack, Struct
import sys

from .database import items, rev_items, multitiles


is_exe = hasattr(sys, "frozen")
### Parser for .wld data types ###
def decode7bit(bytes):
    lbytes = list(bytes)
    value = 0
    shift = 0
    while True:
        byteval = lbytes.pop(0)
        if (byteval & 128) == 0: break
        value |= ((byteval & 0x7F) << shift)
        shift += 7
    return (value | (byteval << shift))


def encode7bit(value):
    temp = value
    bytes = ""
    while temp >= 128:
        bytes += chr(0x000000FF & (temp | 0x80))
        temp >>= 7
    bytes += chr(temp)
    return bytes


def get_long_string(f):
    namelen = decode7bit(f.read(2))  # int(unpack("<B", f.read(1))[0])
    if namelen < 127:
        f.seek(-1, 1)
    name = unpack("<" + str(namelen) + "s", f.read(namelen))[0].decode()
    return name


formats = (  # ("word" , "<H", 2),
             ("byte", "<B", 1),
             ("short", "<h", 2),
             ("ushort", "<H", 2),
             ("int", "<I", 4),
             ("uint", "<i", 4),
             ("long", "<Q", 8),
             ("double", "<d", 8),
             ("float", "<f", 4),
             )


def get_short(f, num=1):
    if num == 1:
        return unpack("<h", f.read(2))[0]
    return unpack("<" + "h" * num, f.read(2 * num))


def get_ushort(f, num=1):
    if num == 1:
        return unpack("<H", f.read(2))[0]
    return unpack("<" + "H" * num, f.read(2 * num))


def get_uint(f, num=1):
    if num == 1:
        return unpack("<I", f.read(4))[0]
    return unpack("<" + "I" * num, f.read(num * 4))


def get_int(f, num=1):
    if num == 1:
        return unpack("<i", f.read(4))[0]
    return unpack("<" + "i" * num, f.read(num * 4))


def get_long(f, num=1):
    if num == 1:
        return unpack("<Q", f.read(8))[0]
    return unpack("<" + "Q" * num, f.read(num * 8))


def get_byte(f, num=1):
    if num == 1:
        return unpack("<B", f.read(1))[0]
    return unpack("<" + "B" * num, f.read(num))


def get_double(f, num=1):
    if num == 1:
        return unpack("<d", f.read(8))[0]
    return unpack("<" + "d" * num, f.read(num * 8))


def get_float(f, num=1):
    if num == 1:
        return unpack("<f", f.read(4))[0]
    return unpack("<" + "f" * num, f.read(num * 4))


def set_uint(data):
    return pack("<I", data)


def set_int(data):
    return pack("<i", data)


def set_ushort(data):
    return pack("<H", data)


#def set_word(data):
#    return pack("<H", data)
def set_byte(data):
    return pack("<B", data)


def get_string(f):
    namelen = int(unpack("<B", f.read(1))[0])
    return unpack("<" + str(namelen) + "s", f.read(namelen))[0]  #.decode()


def set_string(data):
    if len(data) > 126:
        return encode7bit(len(data)) + pack("<" + str(len(data)) + "s", str.encode(data))
        #return encode7bit(len(data))+pack("<"+len(data)*"s",*data)
    else:
        return pack("<B", len(data)) + pack("<" + str(len(data)) + "s", str.encode(data))
        #return pack("<B", len(data))+pack("<"+len(data)*"s",*data)


def set_double(data):
    return pack("<d", data)


def set_float(data):
    return pack("<f", data)


for name, form, l in formats:
    s = Struct(form)

    def make_local(s, l):
        def generic(f):
            return s.unpack(f.read(l))[0]

        return generic

    globals()["get_g%s" % name] = make_local(s, l)

### Parser end ###


### content parser for .wld structures ###

def get_item(f):
    amount = get_gbyte(f)
    if amount:
        return amount, items[get_int(f)], get_gbyte(f)
    else:
        return 0, None


def set_items(f, items):
    for item in items:
        f.write(set_byte(item[0]))  #amount
        if item[0]:
            f.write(set_int(rev_items[item[1]]))  #itemid
            if len(item) > 2:
                f.write(set_byte(item[2]))  #prefix
            else:
                f.write(zero)


def set_items_id(f, items):
    for item in items:
        f.write(set_byte(item[0]))  #amount
        if item[0]:
            f.write(set_uint(item[1]))  #itemid
            if len(item) > 2:
                f.write(set_byte(item[2]))  #prefix
            else:
                f.write(zero)


def set_items_uni(f, items):
    for item in items:
        f.write(set_byte(item[0]))
        if item[0]:
            f.write(set_string(str(item[1])))
            f.write(set_byte(item[2]))


def get_chest(f):
    if get_gbyte(f):  #if exists
        return get_uint(f, 2), [get_item(f) for x in range(20)]
        # return none if no chest exists
        # otherwise return (pos, [(amount, name), (amount, name) ....]


def set_chests(f, chests):
    for chest in chests:
        if chest == None:
            f.write(zero)
        else:
            f.write(one)
            f.write(set_uint(chest[0][0]) + set_uint(chest[0][1]))
            set_items(f, chest[1])


def get_npc_names(f):
    return [get_string(f) for x in range(10)]


def set_npc_names(f, names):
    [f.write(set_string(name)) for name in names]


def set_chests_uni(f, chests):
    for chest in chests:
        if chest == None:
            f.write(zero)
        else:
            f.write(one)
            f.write(set_uint(chest[0][0]) + set_uint(chest[0][1]))
            set_items_uni(f, chest[1])


def get_sign(f):
    if get_gbyte(f):
        return get_long_string(f), get_uint(f, 2)


def set_sign(f, sign):
    if sign != None:
        f.write(one + set_string(sign[0]) + set_uint(sign[1][0]) + set_uint(sign[1][1]))
    else:
        f.write(zero)


def set_signs(f, signs):
    [set_sign(f, sign) for sign in signs]


def get_npc(f):
    #get_byte(f)
    if get_gbyte(f):
        return get_string(f), get_float(f, 2), get_gbyte(f), get_uint(f, 2)
        #return none if no npc exists
        #otherwise return (name, (current_x, current_y), homeless, (home_X, home_Y))


def get_trail(f):
    return (get_gbyte(f), get_string(f), get_gint(f))  #(1,name,ID)


def set_trail(f, trail):
    f.write(set_byte(trail[0]) + set_string(trail[1]) + set_uint(trail[2]))


def set_npc(f, npc):
    if npc != None:
        f.write(
            one + set_string(str(npc[0])) + set_float(npc[1][0]) + set_float(npc[1][1]) + set_byte(npc[2]) + set_uint(
                npc[3][0]) + set_uint(npc[3][1]))
    else:
        f.write(zero)


def get_name(f):
    get_gint(f)
    return get_string(f)


def get_header(f):
    """ returns a dict of header data"""
    version = get_gint(f)
    if version >= 100:
        if version > 140:
            get_long(f)
            rev = get_uint(f)
            get_long(f)


        #get sections
        sectiondata = {"sections" : get_uint(f, get_gshort(f)),
                       "tiletypes" : get_gshort(f)}
        multitiles_ = set()
        mask = 0x80
        for x in range(sectiondata["tiletypes"]):
            if mask == 0x80:
                flags = get_gbyte(f)
                mask = 0x01
            else: mask <<=1
            if flags & mask == mask:
                multitiles_.add(x)

    else:
        multitiles_ = multitiles

    if version <= 36:
        d = {"name": get_string(f),
             "ID": get_gint(f),
             "worldrect": get_uint(f, 4),
             "height": get_gint(f),
             "width": get_gint(f),
             "spawn": get_uint(f, 2),
             "groundlevel": get_gdouble(f),
             "rocklevel": get_gdouble(f),
             "time": get_gdouble(f),
             "is_day": get_gbyte(f),
             "moonphase": get_gint(f),
             "is_bloodmoon": get_gbyte(f),
             "dungeon_xy": get_uint(f, 2),
             "bosses_slain": get_byte(f, 3),
             "npcs_saved": get_byte(f, 3),
             "special_slain": get_byte(f, 2),
             "is_a_shadow_orb_broken": get_gbyte(f),
             "is_meteor_spawned": get_gbyte(f),
             "shadow_orbs_broken": get_gbyte(f),
             "altars_broken": get_gint(f),
             "hardmode": get_gbyte(f),
             "gob_inv_time": get_gint(f),
             "gob_inv_size": get_gint(f),
             "gob_inv_type": get_gint(f),
             "gob_inv_x": get_gdouble(f)}
    elif version < 68:
        d = {"name": get_string(f),
             "ID": get_gint(f),
             "worldrect": get_uint(f, 4),
             "height": get_gint(f),
             "width": get_gint(f),
             "spawn": get_uint(f, 2),
             "groundlevel": get_gdouble(f),
             "rocklevel": get_gdouble(f),
             "time": get_gdouble(f),
             "is_day": get_gbyte(f),
             "moonphase": get_gint(f),
             "is_bloodmoon": get_gbyte(f),
             "dungeon_xy": get_uint(f, 2),
             "bosses_slain": get_byte(f, 3),
             "npcs_saved": get_byte(f, 3),
             "special_slain": get_byte(f, 3),
             "is_a_shadow_orb_broken": get_gbyte(f),
             "is_meteor_spawned": get_gbyte(f),
             "shadow_orbs_broken": get_gbyte(f),
             "altars_broken": get_gint(f),
             "hardmode": get_gbyte(f),
             "gob_inv_time": get_gint(f),
             "gob_inv_size": get_gint(f),
             "gob_inv_type": get_gint(f),
             "gob_inv_x": get_gdouble(f)}
    elif version < 71:
        d = {"name": get_string(f),
             "ID": get_gint(f),
             "worldrect": get_uint(f, 4),
             "height": get_gint(f),
             "width": get_gint(f),
             "moontype": get_byte(f),
             "treedata": get_uint(f, 7),
             "cavedata": get_uint(f, 10),
             "spawn": get_uint(f, 2),
             "groundlevel": get_gdouble(f),
             "rocklevel": get_gdouble(f),
             "time": get_gdouble(f),
             "is_day": get_gbyte(f),
             "moonphase": get_gint(f),
             "is_bloodmoon": get_gbyte(f),
             "dungeon_xy": get_uint(f, 2),
             "is_crimson": get_gbyte(f),
             "bosses_slain": get_byte(f, 10),
             "npcs_saved": get_byte(f, 3),
             "special_slain": get_byte(f, 4),
             "is_a_shadow_orb_broken": get_gbyte(f),
             "is_meteor_spawned": get_gbyte(f),
             "shadow_orbs_broken": get_gbyte(f),
             "altars_broken": get_gint(f),
             "hardmode": get_gbyte(f),
             "gob_inv_time": get_gint(f),
             "gob_inv_size": get_gint(f),
             "gob_inv_type": get_gint(f),
             "gob_inv_x": get_gdouble(f),
             "raining": get_gbyte(f),
             "raintime": get_gint(f),
             "maxrain": get_float(f),
             "oretiers": get_int(f, 3),
             "background_styles": get_byte(f, 8),
             "clouds": get_uint(f),
             "cloudcount": get_gushort(f),
             "windspeed": get_float(f),


             }
    elif version < 80:
        d = {"name": get_string(f),
             "ID": get_gint(f),
             "worldrect": get_uint(f, 4),
             "height": get_gint(f),
             "width": get_gint(f),
             "moontype": get_byte(f),
             "treedata": get_uint(f, 7),
             "cavedata": get_uint(f, 10),
             "spawn": get_uint(f, 2),
             "groundlevel": get_gdouble(f),
             "rocklevel": get_gdouble(f),
             "time": get_gdouble(f),
             "is_day": get_gbyte(f),
             "moonphase": get_gint(f),
             "is_bloodmoon": get_gbyte(f),
             "is_eclipse": get_gbyte(f),
             "dungeon_xy": get_uint(f, 2),
             "is_crimson": get_gbyte(f),
             "bosses_slain": get_byte(f, 10),
             "npcs_saved": get_byte(f, 3),
             "special_slain": get_byte(f, 4),
             "is_a_shadow_orb_broken": get_gbyte(f),
             "is_meteor_spawned": get_gbyte(f),
             "shadow_orbs_broken": get_gbyte(f),
             "altars_broken": get_gint(f),
             "hardmode": get_gbyte(f),
             "gob_inv_time": get_gint(f),
             "gob_inv_size": get_gint(f),
             "gob_inv_type": get_gint(f),
             "gob_inv_x": get_gdouble(f),
             "raining": get_gbyte(f),
             "raintime": get_gint(f),
             "maxrain": get_float(f),
             "oretiers": get_int(f, 3),
             "background_styles": get_byte(f, 8),
             "clouds": get_uint(f),
             "cloudcount": get_gushort(f),
             "windspeed": get_float(f),
             }
    elif version < 103:# version 102+
        d = {"name": get_string(f),
             "ID": get_gint(f),
             "worldrect": get_uint(f, 4),
             "height": get_gint(f),
             "width": get_gint(f),
             "moontype": get_byte(f),
             "treedata": get_uint(f, 7),
             "cavedata": get_uint(f, 10),
             "spawn": get_uint(f, 2),
             "groundlevel": get_gdouble(f),
             "rocklevel": get_gdouble(f),
             "time": get_gdouble(f),
             "is_day": get_gbyte(f),
             "moonphase": get_gint(f),
             "is_bloodmoon": get_gbyte(f),
             "is_eclipse": get_gbyte(f),
             "dungeon_xy": get_uint(f, 2),
             "is_crimson": get_gbyte(f),
             "bosses_slain": get_byte(f, 10),
             "npcs_saved": get_byte(f, 3),
             "special_slain": get_byte(f, 4),
             "is_a_shadow_orb_broken": get_gbyte(f),
             "is_meteor_spawned": get_gbyte(f),
             "shadow_orbs_broken": get_gbyte(f),
             "altars_broken": get_gint(f),
             "hardmode": get_gbyte(f),
             "gob_inv_time": get_gint(f),
             "gob_inv_size": get_gint(f),
             "gob_inv_type": get_gint(f),
             "gob_inv_x": get_gdouble(f),
             "raining": get_gbyte(f),
             "raintime": get_gint(f),
             "maxrain": get_float(f),
             "oretiers": get_int(f, 3),
             "background_styles": get_byte(f, 8),
             "clouds": get_uint(f),
             "cloudcount": get_gushort(f),
             "windspeed": get_float(f),
             "anglerstrings" : [get_string(f) for _ in range(get_gint(f))],
             "angler_saved" : get_gbyte(f),
             "angler_quest" : get_gint(f)

             }
    else:#version 147
        d = {"name": get_string(f),
             "ID": get_gint(f),
             "worldrect": get_uint(f, 4),
             "height": get_gint(f),
             "width": get_gint(f),
             "expert" : get_gbyte(f),
             "creationtime" : get_glong(f),
             "moontype": get_gbyte(f),
             "treedata": get_uint(f, 7),
             "cavedata": get_uint(f, 10),
             "spawn": get_uint(f, 2),
             "groundlevel": get_gdouble(f),
             "rocklevel": get_gdouble(f),
             "time": get_gdouble(f),
             "is_day": get_gbyte(f),
             "moonphase": get_gint(f),
             "is_bloodmoon": get_gbyte(f),
             "is_eclipse": get_gbyte(f),
             "dungeon_xy": get_uint(f, 2),
             "is_crimson": get_gbyte(f),
             "bosses_slain": get_byte(f, 11),
             "npcs_saved": get_byte(f, 3),
             "special_slain": get_byte(f, 4),
             "is_a_shadow_orb_broken": get_gbyte(f),
             "is_meteor_spawned": get_gbyte(f),
             "shadow_orbs_broken": get_gbyte(f),
             "altars_broken": get_gint(f),
             "hardmode": get_gbyte(f),
             "gob_inv_time": get_gint(f),
             "gob_inv_size": get_gint(f),
             "gob_inv_type": get_gint(f),
             "gob_inv_x": get_gdouble(f),
             "slime_rain_time" : get_gdouble(f),
             "sundial_cooldown" : get_gbyte(f),
             "raining": get_gbyte(f),
             "raintime": get_gint(f),
             "maxrain": get_float(f),
             "oretiers": get_int(f, 3),
             "background_styles": get_byte(f, 8),
             "clouds": get_uint(f),
             "cloudcount": get_gushort(f),
             "windspeed": get_float(f),
             "anglerstrings" : [get_string(f) for _ in range(get_gint(f))],
             "angler_saved" : get_gbyte(f),
             "angler_quest" : get_gint(f),
             "saved_stylist" : get_gbyte(f),
             "saved_collector" : get_gbyte(f),
             "invasionsize" : get_gint(f),
             "cultist_delay" : get_gint(f),
             "mobkills" : get_uint(f, get_ushort(f)),
             "fastforward" : get_gbyte(f),
             "extra_flags" : get_byte(f, 18)
             }
    d["version"] = version

    return d, multitiles_

def set_header(f, h):
    f.write(set_uint(h["version"]))
    f.write(set_string(h["name"]))
    f.write(set_uint(h["ID"]))
    f.write(set_uint(h["worldrect"][0]))
    f.write(set_uint(h["worldrect"][1]))
    f.write(set_uint(h["worldrect"][2]))
    f.write(set_uint(h["worldrect"][3]))
    f.write(set_uint(h["height"]))
    f.write(set_uint(h["width"]))
    f.write(set_uint(h["spawn"][0]))
    f.write(set_uint(h["spawn"][1]))
    f.write(set_double(h["groundlevel"]))
    f.write(set_double(h["rocklevel"]))
    f.write(set_double(h["time"]))
    f.write(set_byte(h["is_day"]))
    f.write(set_uint(h["moonphase"]))
    f.write(set_byte(h["is_bloodmoon"]))
    f.write(set_uint(h["dungeon_xy"][0]))
    f.write(set_uint(h["dungeon_xy"][1]))
    f.write(set_byte(h["bosses_slain"][0]) + set_byte(h["bosses_slain"][1]) + set_byte(h["bosses_slain"][2]))
    f.write(set_byte(h["npcs_saved"][0]) + set_byte(h["npcs_saved"][1]) + set_byte(h["npcs_saved"][2]))
    f.write(set_byte(h["special_slain"][0]) + set_byte(h["special_slain"][1]) + set_byte(h["special_slain"][2]))
    f.write(set_byte(h["is_a_shadow_orb_broken"]))
    f.write(set_byte(h["is_meteor_spawned"]))
    f.write(set_byte(h["shadow_orbs_broken"]))
    f.write(set_uint(h["altars_broken"]))
    f.write(set_byte(h["hardmode"]))
    f.write(set_uint(h["gob_inv_time"]))
    f.write(set_uint(h["gob_inv_size"]))
    f.write(set_uint(h["gob_inv_type"]))
    f.write(set_double(h["gob_inv_x"]))


def set_tile_detail(f, tile, amount):
    """
    takes an openend world file as argument
    header needs to be skipped or read first
    returns a tuple containing tile data
    return (tile_id, wall_id, liquid)
    """
    if tile[0] != None:
        f.write(one)
        f.write(set_byte(tile[0]))
        if tile[0] in multitiles:
            f.write(set_ushort(tile[3][0]) + set_ushort(tile[3][1]))
    else:
        f.write(zero)
    #f.write(one)
    if tile[1] != None:
        f.write(one)
        f.write(set_byte(tile[1]))
    else:
        f.write(zero)
    if tile[2] != 0:
        f.write(one)
        if tile[2] > 0:
            f.write(set_byte(tile[2]))
            f.write(zero)
        else:
            f.write(set_byte(-tile[2]))
            f.write(one)
    else:
        f.write(zero)
    f.write(set_byte(tile[4]))
    f.write(set_ushort(amount))


def set_tiles(f, tiles, header, report=True, callback = None):
    total = header["width"] * header["height"]
    for x in range(header["width"]):
        y = 0
        while y < header["height"]:
            tile = tiles[x][y]
            amount = 0
            while y < header["height"] - 1 - amount and tile == tiles[x][y + 1 + amount]:
                amount += 1

            if amount:
                y += amount
                set_tile_detail(f, tile, amount - 1)
            else:
                y += 1
                set_tile_detail(f, tile, 0)
        if report:
            if x % 100 == 0:
                progress = ((x * header["height"] + y)) * 100.0 / total
                st = "%6.2f%% done writing tiles" % (progress)
                if callback:callback.set_progress(50+progress/2)
                print(st)


def set_tile(f, tile):
    """
    takes an openend world file as argument
    header needs to be skipped or read first
    returns a tuple containing tile data
    return (tile_id, wall_id, liquid)
    """
    if tile[0] != None:
        f.write(one)
        f.write(set_byte(tile[0]))
        if tile[0] in multitiles:
            f.write(set_ushort(tile[3][0]) + set_ushort(tile[3][1]))
    else:
        f.write(zero)
    if tile[1] != None:
        f.write(one)
        f.write(set_byte(tile[1]))
    else:
        f.write(zero)
    if tile[2] != 0:
        f.write(one)
        if tile[2] > 0:
            f.write(set_byte(tile[2]))
            f.write(zero)
        else:
            f.write(set_byte(-tile[2]))
            f.write(one)
    else:
        f.write(zero)
    f.write(zero)
    f.write(set_ushort(0))


def set_tile_no_amount(f, tile, mt_override = False):
    """
    takes an openend world file as argument
    header needs to be skipped or read first
    returns a tuple containing tile data
    return (tile_id, wall_id, liquid)
    """
    if tile[0] != None:
        f.write(one)
        f.write(set_byte(tile[0]))
        if tile[0] in multitiles and not mt_override:
            f.write(set_ushort(tile[3][0]) + set_ushort(tile[3][1]))
    else:
        f.write(zero)
    if tile[1] != None:
        f.write(one)
        f.write(set_byte(tile[1]))
    else:
        f.write(zero)
    if tile[2] != 0:
        f.write(one)
        if tile[2] > 0:
            f.write(set_byte(tile[2]))
            f.write(zero)
        else:
            f.write(set_byte(-tile[2]))
            f.write(one)
    else:
        f.write(zero)
    f.write(zero)

def get_tile_buffered(f):
    """
    takes an openend world file as argument
    header needs to be skipped or read first
    returns a tuple containing tile data
    return (tile_id, wall_id, liquid)
    """

    if get_byte(f):  #if exists
        ttype = get_byte(f)
        if ttype in multitiles:
            multi = get_ushort(f, 2)
        else:
            multi = None
    else:
        ttype = None
        multi = None
    walled = get_byte(f)
    if walled:
        wall = get_byte(f)
    else:
        wall = None
    liquid = get_byte(f)
    if liquid:
        liquidamount, lava = get_byte(f, 2)
        if lava:
            liquid = -liquidamount  #its lava
        else:
            liquid = liquidamount  # its water
    wire = get_byte(f)
    tile = (ttype, wall, liquid, multi, wire)

    return (tile, get_ushort(f)+1)


def get_tile_buffered_12_masked(f):  #Terraria 1.2 bitmask
    """
    takes an openend world file as argument
    header needs to be skipped or read first
    returns an iterator containing tile data
    return (tile_id, wall_id, liquid)
    """

    header1 = get_gbyte(f)
    header2 = get_gbyte(f) if header1 & 1 else 0
    header3 = get_gbyte(f) if header2 & 1 else 0

    if (header1 & 2):  #if exists
        if (header1 & 32) != 32:
            ttype = get_gbyte(f)
        else:
            ttype = get_gushort(f)
        if ttype in multitiles:
            multi = get_ushort(f, 2)
        else:
            multi = None
        if (header3 & 8):  #has a color
            get_gbyte(f)  #read in color and GC
    else:
        ttype = None
        multi = None
    if (header1 & 4):
        wall = get_gbyte(f)
        if (header3 & 16):  #has a color
            get_gbyte(f)  #read in color and GC
    else:
        wall = None
    liquid = (header1 & 24)>>3
    if liquid:
        liquid = (256*(liquid-1))+get_gbyte(f)
    if header2 > 1:
        wire = (header2 & 2), (header2 & 4), (header2 & 8)
    else:
        wire = 0,0,0

    rle = (header1 & 192) >> 6
    if rle == 0:pass
    elif rle == 1:
        rle = get_gbyte(f)
    elif rle == 2:
        rle = get_gshort(f)
    else:raise Exception("RLE compression error.")

    tile = (ttype, wall, liquid, multi, wire)

    return tile, rle+1


### content parser end ###



zero = set_byte(0)
one = set_byte(1)
