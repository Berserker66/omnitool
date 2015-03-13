import os

import pygame


colors = {}
for p in os.listdir(os.getcwd()):
    if p[-3:] == "png":
        if p[:5] == "Tiles":
            colorsum = [0, 0, 0]
            image = pygame.image.load(p)
            size = image.get_size()
            i = 0
            for x in range(size[0]):
                for y in range(size[1]):
                    c = image.get_at((x, y))
                    if c[3]:
                        if c[0] == 247 and c[1] == 119 and c[2] == 249:
                            pass
                        elif c[0] == 223 and c[1] == 119 and c[2] == 249:
                            pass
                        else:
                            colorsum = [colorsum[0] + c[0], colorsum[1] + c[1], colorsum[2] + c[2]]
                            i += 1
            color = (int(colorsum[0] / float(i)),
                     int(colorsum[1] / float(i)),
                     int(colorsum[2] / float(i)))
            print(p[6:].strip(".png"), color)
            colors[int(p[6:].strip(".png"))] = color
rcolors = []
for i in range(len(colors)):
    rcolors.append(colors[i])
# print rcolors
print(colors)
colors = {}
for p in os.listdir(os.getcwd()):
    if p[-3:] == "png":
        if p[:4] == "Wall":
            colorsum = [0, 0, 0]
            image = pygame.image.load(p)
            size = image.get_size()
            i = 0
            for x in range(size[0]):
                for y in range(size[1]):
                    c = image.get_at((x, y))
                    if c[3]:
                        if c[0] == 247 and c[1] == 119 and c[2] == 249:
                            pass
                        elif c[0] == 223 and c[1] == 119 and c[2] == 249:
                            pass
                        else:
                            colorsum = [colorsum[0] + c[0], colorsum[1] + c[1], colorsum[2] + c[2]]
                            i += 1
            color = (int(colorsum[0] / float(i)),
                     int(colorsum[1] / float(i)),
                     int(colorsum[2] / float(i)))
            print(p[5:].strip(".png"), color)
            colors[int(p[5:].strip(".png"))] = color
rcolors = []
for i in range(1, len(colors)):
    rcolors.append(colors[i])
print(colors)
