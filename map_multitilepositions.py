import itertools
import pygame
import os
from collections import Counter

def get_written(distance, pinks):
    return len(tuple(filter(lambda p:p<distance, pinks)))

class MultiMap():
    def __init__(self, surface_or_data):
        if type(surface_or_data) == dict:
            self.entry = surface_or_data["entry"]
            self.stride = surface_or_data["stride"]
        else:
            size = surface_or_data.get_size()
            i = 0
            grid_x = Counter()
            grid_y = Counter()
            for x in range(size[0]):
                for y in range(size[1]):
                    c = surface_or_data.get_at((x, y))
                    if c[3]:
                        if c[0] == 247 and c[1] == 119 and c[2] == 249:
                            grid_x[x]+=1
                            grid_y[y]+=1
                        elif c[0] == 223 and c[1] == 119 and c[2] == 249:
                            grid_x[x]+=1
                            grid_y[y]+=1

            self.stride = 0
            highest = grid_x.most_common(1)[0][1]#highest hit rate
            cutoff = highest//2
            xpink = set()
            for k,i in grid_x.items():
                if i > cutoff:
                    xpink.add(k)
            entry_x = set()
            for i in xpink:
                if i+1 in xpink:pass
                else:entry_x.add(i+1)
            entry_x.remove(max(entry_x))
            if entry_x:
                stride = min(entry_x)
            entry_x.add(0)



            highest = grid_y.most_common(1)[0][1]#highest hit rate
            cutoff = highest//2
            ypink = set()
            for k,i in grid_y.items():
                if i > cutoff:
                    ypink.add(k)
            entry_y = set()
            for i in ypink:
                if i+1 in ypink:pass
                else:entry_y.add(i+1)
            entry_y.remove(max(entry_y))
            if entry_y:
                stride = min(entry_y)
            entry_y.add(0)

            self.entry = tuple(itertools.product(entry_x, entry_y))

        def get_data(self):
            return {"entry" : self.entry,
                    "stride" : self.stride}

def create_mappings(folder = "tImages"):
    import database
    multimaps = {}
    for i in database.multitiles:
        s = pygame.image.load(os.path.join(folder, "Tiles_"+str(i)+".png"))
        print("Determined multitile mapping for Tile "+str(i))
        try:
            multimaps[i] = MultiMap(s)
        except IndexError:
            print("Could not determine multitile mapping for Tile "+str(i))
        except Exception:
            import traceback
            traceback.print_exc()



if __name__ == "__main__":
    create_mappings()