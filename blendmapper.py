import numpy

from blend import *
from blend_detail import *


blend = {1: 0,
         # 2 : 0,
         6: 0,
         7: 0,
         8: 0,
         9: 0,
         22: 0,
         #23 : 0,
         25: 0,
         30: 0,
         38: 0,
         37: 0,
         38: 0,
         39: 0,
         40: 0,
         41: 0,
         43: 0,
         44: 0,
         45: 0,
         46: 0,
         47: 0,

         53: 0,
         56: 0,
         58: 57,
         #59 : 123, no idea what mud blends into
         #60 : 59,
         63: 0,
         64: 0,
         65: 0,
         66: 0,
         67: 0,
         68: 0,
         #70 : 59,
         #75:59,
         76: 57,
         107: 0,
         108: 0,
         111: 0,
         112: 0,
         116: 0,
         117: 0,
         118: 0,
         119: 0,
         120: 0,
         121: 0,
         122: 0,
         123: 0,
         130: 0,
         131: 0,
         140: 0,

         }
blendto = {}
for x in range(65537):
    blendto[x] = [x]
for key in blend:
    blendto[blend[key]].append(key)
grass = {2: 0,
         23: 0,
         60: 59,
         70: 59,
         109: 0,

         }
grassto = {}
for x in range(255):
    grassto[x] = [x]
for key in grass:
    grassto[grass[key]].append(key)
    blendto[grass[key]].append(key)
# blendto[0].append(1)#dirt blends to stone
#fail = []
def calc(header, tiles, rmap):
    blendmap = numpy.zeros((header["width"], header["height"], 2), dtype=numpy.uint16)
    wblendmap = numpy.zeros((header["width"], header["height"], 2), dtype=numpy.uint16)
    for x in range(1, header["width"] - 1):
        for y in range(1, header["height"] - 1):
            wid = tiles[x][y][1]
            wblendmap[x][y] = wmix[(wid == tiles[x - 1][y][1], wid == tiles[x + 1][y][1],
                                    wid == tiles[x][y - 1][1], wid == tiles[x][y + 1][1])][rmap[x, y]]

            tid = tiles[x][y][0]
            blendmap[x][y] = mix[(tid == tiles[x - 1][y][0], tid == tiles[x + 1][y][0],
                                  tid == tiles[x][y - 1][0], tid == tiles[x][y + 1][0])][rmap[x, y]]
    return blendmap, wblendmap


def get(tiles, blendmap, wblendmap, rmap, x, y):
    wid = tiles[x][y][1]
    wblendmap[x][y] = wmix[(wid == tiles[x - 1][y][1], wid == tiles[x + 1][y][1],
                            wid == tiles[x][y - 1][1], wid == tiles[x][y + 1][1])][rmap[x, y]]

    tid = tiles[x][y][0]
    blendmap[x][y] = mix[(tid == tiles[x - 1][y][0], tid == tiles[x + 1][y][0],
                          tid == tiles[x][y - 1][0], tid == tiles[x][y + 1][0])][rmap[x, y]]


def get_tile(tiles, blendmap, rmap, x, y):
    tid = tiles[x][y][0]
    blendmap[x][y] = mix[(tid == tiles[x - 1][y][0], tid == tiles[x + 1][y][0],
                          tid == tiles[x][y - 1][0], tid == tiles[x][y + 1][0])][rmap[x, y]]


def get_wall(tiles, wblendmap, rmap, x, y):
    wid = tiles[x][y][1]
    wblendmap[x][y] = wmix[(wid == tiles[x - 1][y][1], wid == tiles[x + 1][y][1],
                            wid == tiles[x][y - 1][1], wid == tiles[x][y + 1][1])][rmap[x, y]]


def get_tile_detail(tiles, blendmap, rmap, x, y):
    tid = tiles[x][y][0]
    if tid in grass:
        bid = grass[tid]
        if tid == tiles[x - 1][y][0]:
            o = 1
        elif bid == tiles[x - 1][y][0]:
            o = 2
        else:
            o = 0
        if tid == tiles[x + 1][y][0]:
            p = 1
        elif bid == tiles[x + 1][y][0]:
            p = 2
        else:
            p = 0
        if tid == tiles[x][y - 1][0]:
            z = 1
        elif bid == tiles[x][y - 1][0]:
            z = 2
        else:
            z = 0
        if tid == tiles[x][y + 1][0]:
            w = 1
        elif bid == tiles[x][y + 1][0]:
            w = 2
        else:
            w = 0
        blendmap[x][y] = grass_detail[(o, p, z, w)][rmap[x, y]]
    elif tid in blend:
        bid = blend[tid]

        if tid == tiles[x - 1][y][0]:
            o = 1
        elif bid == tiles[x - 1][y][0]:
            o = 2
        else:
            o = 0
        if tid == tiles[x + 1][y][0]:
            p = 1
        elif bid == tiles[x + 1][y][0]:
            p = 2
        else:
            p = 0
        if tid == tiles[x][y - 1][0]:
            z = 1
        elif bid == tiles[x][y - 1][0]:
            z = 2
        else:
            z = 0
        if tid == tiles[x][y + 1][0]:
            w = 1
        elif bid == tiles[x][y + 1][0]:
            w = 2
        else:
            w = 0
        blendmap[x][y] = mix_detail[(o, p, z, w)][rmap[x, y]]

    else:
        accept = blendto[tid]
        blendmap[x][y] = mix[(tiles[x - 1][y][0] in accept, tiles[x + 1][y][0] in accept,
                              tiles[x][y - 1][0] in accept, tiles[x][y + 1][0] in accept)][rmap[x, y]]

