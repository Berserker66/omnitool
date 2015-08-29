config = {
    "name": "Tombstone counter",  # plugin name
    "type": "receiver",  #plugin type
    "description": ["counts tombstones in a world"]  #description
}

from omnitool.database import tiles


class Receiver():  # required class to be called by plugin manager
    def __init__(self):  #do any initialization stuff
        self.tile_id = tiles.index("Grave Marker")  #we grab the ID of tombstone from database

    def rec_header(self, header):  #this is called by plugin manager when the header is read
        print("Counting Tombstones for %s" % header["name"].decode())  #so we print the name from header

    def rec_tiles(self, tiles):  #called when tiles are ready
        x = 0  #our counter variable
        for column in tiles:  # tiles come as 2D list
            for tile in column:  #so we need to get tiles like this
                if tile[0] == self.tile_id:  #tile[0] is the tile_id
                    x += 1  #increment counter for each found tombstone tile
        print("Found %d Tombstones" % (x // 4))  #divide counter by 4, because each tombstone consists of 4 "sub tiles"
        return False  #signal plugin manager we are done and dont need any further data
    
    
