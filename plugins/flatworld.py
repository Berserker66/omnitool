config = {
    "name": "Flatworld",  # plugin name
    "type": "generator",  #plugin type
    "description": ["generates a flat world"]  #description
}
import pygame

import database as db  # import terraria database
from pgu import gui


class Generator():  # required class to be called by plugin manager
    def __init__(self):  #do any initialization stuff
        self.gen_gui()  #start the gui

    def run(self):  #executed after gui
        sizetype = self.size
        size = [(4200, 1200), (6300, 1800), (8400, 2400), (2400, 2400), (2100, 600)][sizetype]
        spawn = [(2100, 300), (3150, 300), (4200, 300), (1200, 300), (1050, 200)][sizetype]
        ground = [385.0, 385.0, 385.0, 385.0, 225.0][sizetype]
        rock = [703.0, 703.0, 703.0, 703.0, 353.0][sizetype]
        self.header = {'spawn': spawn, 'groundlevel': ground, 'is_bloodmoon': 0,
                       'dungeon_xy': spawn, 'worldrect': (0, size[0] * 16, 0, size[1] * 16),
                       'is_meteor_spawned': 0, 'gob_inv_time': 0, 'rocklevel': rock,
                       'gob_inv_x': 0.0, 'is_day': 1, 'shadow_orbs_broken': 0,
                       'width': size[0], 'version': db.version, 'gob_inv_type': 0,
                       'bosses_slain': (0, 0, 0), "npcs_saved": (0, 0, 0), "special_slain": (0, 0, 0),
                       'gob_inv_size': 0, 'height': size[1],
                       'ID': 1394000079, 'moonphase': 0, 'name': "Flatworld", "hardmode": 0,
                       "altars_broken": 0,
                       'is_a_shadow_orb_broken': 0, 'time': 13000.0}
        self.npcs = []
        self.names = db.names
        self.signs = [None] * 1000
        self.chests = [None] * 1000
        sur = spawn[1]
        #self.tiles = []
        if self.wall == 0:
            self.wall = None
        #for x in range(size[0]):#for each column
        col = [(None, None, 0, None, 0)] * (sur)
        col.append((self.surface, None, 0, None, 0))
        col.extend([(self.tile, self.wall, 0, None, 0)] * (-len(col) + self.header["height"]))
        #self.tiles.append(col)
        self.tiles = [col] * self.header["width"]

    def gen_gui(self):
        #get theme, language and end process function from omnitool API
        from omnitool import themename, Theme, lang, exit_prog, Quitbutton
        #load the theme
        theme = Theme(themename)
        #initilize pygame renderer
        pygame.display.init()
        #set window title to Flatworld, from language file
        pygame.display.set_caption(lang.flat)
        #application interface
        app = gui.Desktop(theme=theme)
        #main container, table
        main = gui.Table(width=800)
        #connect the QUIT event with Omnitool API exit_prog
        app.connect(gui.QUIT, exit_prog, None)
        #add label size to table
        main.td(gui.Label(lang.fw_size))
        #size drop down selection
        size = gui.Select(width=300)
        size.add(lang.fw_tiny, 4)
        size.add(lang.fw_small, 0)
        size.add(lang.fw_medium, 1)
        size.add(lang.fw_large, 2)
        size.add(lang.fw_square, 3)
        size.value = 0
        #add it to the table
        main.td(size)
        #surface label
        main.td(gui.Label(lang.fw_surf))

        surf = ["Grass Block", "Corrupt Grass Block", "Jungle Grass Block",
                "Mushroom Grass Block", "Hallowed Grass Block"]
        #surface drop down menu
        sur = gui.Select(width=300)
        sur.add("None", None)
        for grass in surf:
            sur.add(grass, db.tiles.index(grass))
        sur.value = None
        #add surface selection to table
        main.td(sur)

        #go to next line in table
        main.tr()
        #add tile label to table
        main.td(gui.Label(lang.fw_tile))
        #create tile list
        tiles = gui.List(300, 150)
        for tile in db.tiles:
            if db.tiles.index(tile) not in db.multitiles:
                tiles.add(gui.Label(tile), value=db.tiles.index(tile))
        #add tile list to table
        main.td(tiles)
        #add wall label to table
        main.td(gui.Label(lang.fw_wall))
        #create wall list
        walls = gui.List(300, 150)
        for wall in db.walls:
            walls.add(gui.Label(wall), value=db.walls.index(wall))
        #add wall list to table
        main.td(walls)
        #next row
        main.tr()
        #Generate! button
        main.td(Quitbutton(app), colspan=4)
        #run the application and open the window
        app.run(main)
        #when it's done, instruct pygame to clean up
        pygame.display.quit()
        #attach data to plugin, to be used in run()
        self.surface = sur.value
        self.wall = walls.value
        self.tile = tiles.value
        self.size = size.value
        if self.wall == 0:
            self.wall = None


if __name__ == "__main__":
    g = Generator()
    
