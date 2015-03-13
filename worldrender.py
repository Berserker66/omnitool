from __future__ import with_statement

import pygame

from tlib import get_tile, get_chest
from tinterface import get_header
import colorlib


def mul(tupl, scale):
    return (tupl[0] * scale, tupl[1] * scale)


def get_map(path):
    # target = pygame.rect.Rect((943, 222),(3, 12))
    with open(path, "rb") as f:
        header = get_header(f)[0]  #read header with tlib.get_header and also reach tile data in f
        x, y = header["width"], header["height"]  #read world size from header cache
        s = pygame.surface.Surface((x, y))  #create a software surface to save tile colors in
        for xi in range(x):  # for each slice
            for yi in range(y):  # get the tiles
                #tiles start from the upper left corner, then go downwards
                # when a slice is complete its starts with the next slice

                tile, wall, liquid, multi = get_tile(f)  #tlib.get_tile
                #if target.collidepoint(xi,yi):
                #    print tile, multi
                if not liquid:  #liquid == 0 means no liquid
                    # there could be a liquid and a tile, like a chest and water,
                    #but I can only set one color to a pixel anyway, so I priotise the tile
                    if tile == None:
                        s.set_at((xi, yi), (255, 255, 255))  #if no tile present, set it white
                    elif tile in colorlib.data:
                        s.set_at((xi, yi), colorlib.data[tile])  #if colorlib has a color use it
                    else:
                        s.set_at((xi, yi), (tile * 2, tile * 2, tile * 2))  #otherwise multiply tile id to make a grey
                elif liquid > 0:  #0>x>256 is water, the higher x is the more water is there
                    s.set_at((xi, yi), (255 - liquid, 255 - liquid, 255))
                else:  #lava is -256>x>0
                    s.set_at((xi, yi), (255, 255 + liquid, 255 + liquid))

            if xi % 10 == 0:  # every ten slices print the progress
                import sys

                st = "loaded %5d of %d" % (xi, x)
                sys.stdout.write(st + "\b" * len(st))
                #pygame.image.save(s, path[:-3]+"png")
    print("Completed loading! ")
    return s, header


if __name__ == "__main__":
    pygame.init()
    image, header = get_map("world1.wld")
    # image = pygame.image.load("world1.png")
    res = (1024, 786)
    spawn = header["spawn"]
    clock = pygame.time.Clock()
    zoom = 3
    pos = -spawn[0] + res[0] // 2, -spawn[1] + res[1] // 2
    r = True
    size = image.get_size()
    contain = pygame.surface.Surface(res)
    pygame.display.set_caption("Terraria World Render")
    s = pygame.display.set_mode(res, pygame.RESIZABLE)

    while 1:

        events = pygame.event.get()
        for event in events:
            if event.type == 12:
                pygame.quit()
                import sys

                sys.exit()
            elif event.type == 4:
                if event.buttons[0]:
                    pos = pos[0] + event.rel[0], pos[1] + event.rel[1]
                    r = True
            elif event.type == 2:
                if event.key == "z":
                    zoom += 1
                    if zoom == 6:
                        zoom = 1
                    r = True
            elif event.type == 5:
                if event.button == 3:
                    spawn = +res[0] * (zoom - 1) * 0.5 / zoom - pos[0] + event.pos[0] / zoom, res[1] * (
                    zoom - 1) * 0.5 / zoom - pos[1] + event.pos[1] / zoom
            elif event.type == 6:
                if event.button == 4:
                    zoom += 1
                elif event.button == 5:
                    zoom -= 1
                zoom = min(5, max(1, zoom))
                r = True
            elif event.type == 16:
                res = event.size
                r = True
                s = pygame.display.set_mode(res, pygame.RESIZABLE)

        if r:
            buf = pygame.surface.Surface((res[0], res[1]))
            buf.blit(image, pos)
            center = (spawn[0] + pos[0], spawn[1] + pos[1])
            pygame.draw.line(buf, (255, 0, 0), (center[0] - 50 / zoom, center[1]),
                             (center[0] + 50 / zoom, center[1]))
            pygame.draw.line(buf, (255, 0, 0), (center[0], center[1] - 50 / zoom),
                             (center[0], center[1] + 50 / zoom))
            if zoom > 1:
                buf = pygame.transform.scale(buf, (res[0] * zoom, res[1] * zoom))
            s.blit(buf, (-res[0] * (zoom - 1) * 0.5, -res[1] * (zoom - 1) * 0.5))

        pygame.display.flip()
        r = False
        clock.tick(60)
        
