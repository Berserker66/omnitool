config = {
    "name": "Header Modifier",  # plugin name
    "type": "modifier",  #plugin type
    "description": ["A GUI to change your world header!"]  #description
}

import pygame

from pgu import gui


class Modifier():
    def __init__(self):
        print("Header Modifier starting...")

    def rec_header(self, header):
        self.header = header
        print("Modifying the header for world: %s" % header["name"])

    def rec_tiles(self, tiles):
        self.tiles = tiles

    def rec_chests(self, chests):
        self.chests = chests

    def rec_signs(self, signs):
        self.signs = signs

    def rec_npcs(self, npcs, names):
        self.npcs = npcs
        self.names = names

    def run(self):
        self.genGui()
        return self.header

    def genGui(self):
        from omnitool import themename, Theme, lang, exit_prog

        theme = Theme(themename)

        class Quitbutton(gui.Button):
            def __init__(self, value="Finish"):
                gui.Button.__init__(self, value, width=60, height=40)
                try:
                    self.connect(gui.CLICK, app.quit, None)
                except AttributeError:
                    self.connect(gui.CLICK, app.close, None)


        pygame.display.init()

        pygame.display.set_caption("Header Modifier")

        app = gui.Desktop(theme=theme)

        main = gui.Table(width=300)

        app.connect(gui.QUIT, exit_prog, None)

        main.td(gui.Label("Spawn Point: "))
        X = gui.Input(value=self.header["spawn"][0], size=5)
        Y = gui.Input(value=self.header["spawn"][1], size=4)
        main.td(X)
        main.td(Y)
        main.tr()

        main.td(gui.Label("Hardmode: "))
        hardmode = gui.Switch(self.header["hardmode"])
        main.td(hardmode)

        main.td(gui.Label("Day: "))
        daytime = gui.Switch(self.header["is_day"])
        main.td(daytime)
        main.tr()

        main.td(gui.Label("Eye of Cthulhu killed: "))
        eoc = gui.Switch(self.header["bosses_slain"][0])
        main.td(eoc)

        main.td(gui.Label("Eater of Worlds killed: "))
        eow = gui.Switch(self.header["bosses_slain"][1])
        main.td(eow)
        main.tr()

        main.td(gui.Label("Skeletron killed: "))
        skelly = gui.Switch(self.header["bosses_slain"][2])
        main.td(skelly)

        main.td(gui.Label("Saved Goblin Tinkerer: "))
        tinkerbell = gui.Switch(self.header["npcs_saved"][0])
        main.td(tinkerbell)
        main.tr()

        main.td(gui.Label("Saved Mechanic: "))
        mech = gui.Switch(self.header["npcs_saved"][1])
        main.td(mech)

        main.td(gui.Label("Saved Wizard: "))
        wizziewizz = gui.Switch(self.header["npcs_saved"][2])
        main.td(wizziewizz)
        main.tr()

        main.td(gui.Label("Bloodmoon: "))
        bloodz = gui.Switch(self.header["is_bloodmoon"])
        main.td(bloodz)

        main.td(gui.Label("World Name: "))
        worldName = gui.Input(value=self.header["name"], size=8)
        main.td(worldName)
        main.tr()

        main.td(gui.Label("Invasion Type: "))
        # invasion = gui.Select()
        #invasion.add("None",0)
        #invasion.add("Goblin Invasion",1)
        #invasion.add("Frost Legion",2)
        invType = gui.List(110, 50)
        invType.add("None", value=0)
        invType.add("Goblin Invasion", value=1)
        invType.add("Frost Legion", value=2)

        if invType.value == None:
            invType.value = 0

        #main.td(invasion)
        main.td(invType)

        main.td(gui.Label("Invasion Amount (0-1000): "))
        invSize = (gui.Input(value=self.header["gob_inv_size"], size=8))
        main.td(invSize)
        main.tr()

        main.tr()

        main.td(Quitbutton(), colspan=4)

        app.run(main)

        pygame.display.quit()

        bosses = (int(eoc.value), int(eow.value), int(skelly.value))
        npcSaved = (int(tinkerbell.value), int(mech.value), int(wizziewizz.value))

        self.header["spawn"] = (int(X.value), int(Y.value))
        self.header["hardmode"] = int(hardmode.value)
        self.header["is_day"] = int(daytime.value)
        self.header["bosses_slain"] = bosses
        self.header["is_bloodmoon"] = int(bloodz.value)
        self.header["name"] = worldName.value
        self.header["gob_inv_size"] = int(invSize.value)
        self.header["gob_inv_type"] = int(invType.value)
        self.header["npcs_saved"] = npcSaved
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    