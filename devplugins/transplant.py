config = {
    "name": "Area Transplant",
    "type": "transplant",
    "description": ["transfers tiles"]
}


class Transplant():
    def __init__(self):
        self.area = 190, 127
        self.source = 1875, 512
        self.dest = 4483, 429
        self.dist = self.dest[0] - self.source[0], self.dest[1] - self.source[1]
        self.i = 0

    def rec_header(self, header):
        if self.i == 0:
            self.header = header

    def rec_tiles(self, tiles):
        if self.i == 0:
            self.tiles = tiles
        else:
            x = 0
            for column in tiles:
                y = 0

                for tile in column:
                    # print (self.source[0]+self.area[0], x,self.source[0],y)
                    if self.source[0] + self.area[0] >= x >= self.source[0]:
                        if self.source[1] + self.area[1] >= y >= self.source[1]:
                            #print (tile)
                            self.tiles[x + self.dist[0]][y + self.dist[1]] = tile
                    y += 1
                x += 1
            return False

    def rec_chests(self, chests):
        if self.i == 0:
            self.chests = chests

    def rec_signs(self, signs):
        if self.i == 0:
            self.signs = signs

    def rec_npcs(self, npcs, names):
        if self.i == 0:
            self.npcs = npcs
            self.names = names
            # self.i = 1

    def run(self):
        self.i = 1
    
