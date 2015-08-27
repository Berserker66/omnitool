config ={
    "name" : "Ijwu's MazeWorld Generator", #plugin name
    "type" : "generator", #plugin type
    "description" : ["Generates a maze world."] #description
     }
    
import omnitool.colorlib as clib
import omnitool.database as db
from pgu import gui
import pygame
from random import randint, choice, random
import time
    
class Generator():
    def __init__(self):
        self.orbLimit = 5
        self.lightMeUp = (4,None,0,(0,0),0)
        self.itemlist = {'Swiftness Potion': 30,
                     'Ice Rod': 1,
                     'Lesser Mana Potion': 20,
                     'Diving Gear': 1,
                     'Poisoned Knife': 250,
                     'Diving Helmet': 1,
                     'Adamantite Helmet': 1,
                     'Summer Hat': 1,
                     'Goldfish': 99,
                     "Plumber's Hat": 1,
                     'Explosives': 250,
                     'Staff of Regrowth': 1,
                     'Flower of Fire': 1,
                     "Neptune's Shell": 1,
                     'Anklet of the Wind': 1,
                     'Ninja Shirt': 1,
                     'Silver Axe': 1,
                     'Demon Bow': 1,
                     'Familiar Pants': 1,
                     'Adamantite Sword': 1,
                     'Meteor Hamaxe': 1,
                     'Glowing Mushroom': 99,
                     'Wooden Boomerang': 1,
                     'Adamantite Breastplate': 1,
                     'Iron Greaves': 1,
                     'Robe': 1,
                     "Hero's Hat": 1,
                     'Molten Fury': 1,
                     'Gold Broadsword': 1,
                     'Water Walking Potion': 30,
                     'Red Torch': 99,
                     'Slime Crown': 20,
                     'Whoopie Cushion': 1,
                     'Aqua Scepter': 1,
                     'Molten Pickaxe': 1,
                     'Adamantite Leggings': 1,
                     'Warrior Emblem': 1,
                     'Restoration Potion': 20,
                     'Fairy Bell': 1,
                     'Gold Bow': 1,
                     'Unholy Water': 250,
                     'Snow Globe': 1,
                     'Mining Shirt': 1,
                     'Seed': 250,
                     'Iron Pickaxe': 1,
                     'Laser Rifle': 1,
                     'Green Present': 1,
                     'Necro Helmet': 1,
                     'Copper Helmet': 1,
                     'Sticky Bomb': 50,
                     'Mana Flower': 1,
                     'Cobalt Drill': 1,
                     'Gold Shortsword': 1,
                     'Compass': 1,
                     'Enchanted Boomerang': 1,
                     'Copper Watch': 1,
                     'Hallowed Greaves': 1,
                     'Blue Present': 1,
                     "Philosopher's Stone": 1,
                     'Thorn Chakram': 1,
                     'Iron Hammer': 1,
                     'Shadow Greaves': 1,
                     'Goblin Battle Standard': 1,
                     'Necro Breastplate': 1,
                     'Gold Chainmail': 1,
                     'Titan Glove': 1,
                     'Yellow Phaseblade': 1,
                     'Molten Greaves': 1,
                     'Mythril Drill': 1,
                     'Hallowed Mask': 1,
                     'Jungle Hat': 1,
                     'Ninja Hood': 1,
                     'Aglet': 1,
                     'Invisibility Potion': 30,
                     'Silver Greaves': 1,
                     'Tuxedo Pants': 1,
                     'Silver Watch': 1,
                     'Ale': 30,
                     'Suspicious Looking Eye': 20,
                     "Nature's Gift": 1,
                     'Clockwork Assault Rifle': 1,
                     'Night Owl Potion': 30,
                     'Jungle Shirt': 1,
                     'Shadow Scalemail': 1,
                     'Red Phaseblade': 1,
                     'Silver Bow': 1,
                     'Copper Hammer': 1,
                     'Adamantite Mask': 1,
                     'Flaming Arrow': 250,
                     'Santa Shirt': 1,
                     'Wooden Sword': 1,
                     'Ruler': 1,
                     "Plumber's Pants": 1,
                     'Sticky Glowstick': 99,
                     'Familiar Wig': 1,
                     'White Phasesaber': 1,
                     'Fiery Greatsword': 1,
                     'Hamdrax': 1,
                     'Depth Meter': 1,
                     'Jungle Pants': 1,
                     'Hermes Boots': 1,
                     'Hallowed Headgear': 1,
                     'Rocket Boots': 1,
                     'Purple Phasesaber': 1,
                     'Cobalt Shield': 1,
                     'Jungle Rose': 1,
                     "The Doctor's Shirt": 1,
                     'Obsidian Shield': 1,
                     'Mana Crystal': 99,
                     'Crystal Storm': 1,
                     'Shiny Red Balloon': 1,
                     'Toolbelt': 1,
                     'Dynamite': 5,
                     'Silver Helmet': 1,
                     'Spectre Boots': 1,
                     'Thorns Potion': 30,
                     'Gold Watch': 1,
                     'Cobalt Repeater': 1,
                     'Adamantite Chainsaw': 1,
                     'Iron Bow': 1,
                     'Iron Shortsword': 1,
                     'Cloud in a Balloon': 1,
                     "Archaeologist's Jacket": 1,
                     'Demon Wings': 1,
                     'Flipper': 1,
                     'Dark Lance': 1,
                     'Phoenix Blaster': 1,
                     'Unholy Arrow': 250,
                     'Santa Hat': 1,
                     'Spear': 1,
                     'Gold Axe': 1,
                     'Worm Food': 20,
                     'Red Hat': 1,
                     'Gold Pickaxe': 1,
                     'Breaker Blade': 1,
                     'Mechanical Eye': 20,
                     'Grappling Hook': 1,
                     'Excalibur': 1,
                     'Lesser Restoration Potion': 20,
                     'Ranger Emblem': 1,
                     'Silver Broadsword': 1,
                     'Robot Hat': 1,
                     'Mythril Hood': 1,
                     'Minishark': 1,
                     'Clown Shirt': 1,
                     'Gills Potion': 30,
                     'Sorcerer Emblem': 1,
                     'Bunny Hood': 1,
                     'Ninja Pants': 1,
                     'Adamantite Glaive': 1,
                     'Gungnir': 1,
                     'Star Cannon': 1,
                     'Green Phaseblade': 1,
                     'Featherfall Potion': 30,
                     'Holy Arrow': 250,
                     'Yellow Present': 1,
                     'Silver Pickaxe': 1,
                     'Adamantite Repeater': 1,
                     'Iron Helmet': 1,
                     'Red Phasesaber': 1,
                     'Starfury': 1,
                     'Yellow Phasesaber': 1,
                     'Mushroom': 99,
                     'Purification Powder': 99,
                     'Glowstick': 99,
                     'Gold Hammer': 1,
                     'Rainbow Rod': 1,
                     'Purple Phaseblade': 1,
                     'Mana Potion': 50,
                     'Bone': 99,
                     'Cobalt Naginata': 1,
                     'Meteor Helmet': 1,
                     "Night's Edge": 1,
                     'Hallowed Repeater': 1,
                     'Nightmare Pickaxe': 1,
                     "Ball O' Hurt": 1,
                     'Familiar Shirt': 1,
                     'Mining Helmet': 1,
                     'Blue Phasesaber': 1,
                     'Gold Crown': 1,
                     'Lesser Healing Potion': 30,
                     'Ironskin Potion': 30,
                     'Iron Chainmail': 1,
                     'Hallowed Helmet': 1,
                     'GPS': 1,
                     'Copper Bow': 1,
                     'Mythril Greaves': 1,
                     'Cobalt Sword': 1,
                     'Clown Hat': 1,
                     'Wooden Arrow': 250,
                     'Band of Regeneration': 1,
                     'Adamantite Headgear': 1,
                     'Meteor Leggings': 1,
                     'White Phaseblade': 1,
                     'Magical Harp': 1,
                     'Gold Greaves': 1,
                     'Star Cloak': 1,
                     'Copper Greaves': 1,
                     'Necro Greaves': 1,
                     'Silver Shortsword': 1,
                     'Mechanical Worm': 20,
                     'Cursed Bullet': 250,
                     'Spelunker Potion': 30,
                     "Archaeologist's Hat": 1,
                     'Cloud in a Bottle': 1,
                     'The Breaker': 1,
                     'Molten Breastplate': 1,
                     'Cobalt Helmet': 1,
                     'War Axe of the Night': 1,
                     'Megashark': 1,
                     'Obsidian Horseshoe': 1,
                     'Silver Bullet': 250,
                     'Crystal Bullet': 250,
                     'Cross Necklace': 1,
                     "The Doctor's Pants": 1,
                     'Archery Potion': 30,
                     'Mechanical Skull': 20,
                     'Switch': 250,
                     'Wizard Hat': 1,
                     'Copper Chainmail': 1,
                     "Jester's Arrow": 250,
                     'Iron Axe': 1,
                     'Molten Hamaxe': 1,
                     'Sunfury': 1,
                     'Regeneration Potion': 30,
                     'Copper Shortsword': 1,
                     'Sunglasses': 1,
                     'Musket': 1,
                     'Adamantite Drill': 1,
                     "Hero's Pants": 1,
                     'Gravitation Potion': 30,
                     'Band of Starpower': 1,
                     'Copper Pickaxe': 1,
                     'Shotgun': 1,
                     'Silver Chainmail': 1,
                     'Magic Mirror': 1,
                     'Battle Potion': 30,
                     'Flamelash': 1,
                     'Harpoon': 1,
                     'Magic Dagger': 1,
                     'Mining Pants': 1,
                     'Magic Power Potion': 30,
                     'Inactive Stone Block': 250,
                     'Vile Powder': 99,
                     'Tuxedo Shirt': 1,
                     'Vilethorn': 1,
                     'Molten Helmet': 1,
                     'Life Crystal': 99,
                     'Hellfire Arrow': 250,
                     'Shadow Orb': 1,
                     'Trident': 1,
                     'Wooden Hammer': 1,
                     'Handgun': 1,
                     'Cobalt Breastplate': 1,
                     'Mana Regeneration Potion': 30,
                     'Flintlock Pistol': 1,
                     'Fish Bowl': 1,
                     'Bomb': 50,
                     'Mythril Sword': 1,
                     'Shuriken': 250,
                     'Clown Pants': 1,
                     'Cursed Arrow': 250,
                     "Light's Bane": 1,
                     'Mythril Repeater': 1,
                     'Throwing Knife': 250,
                     'Silver Hammer': 1,
                     'Cobalt Leggings': 1,
                     'Sandgun': 1,
                     "Hero's Shirt": 1,
                     'Top Hat': 1,
                     'Water Bolt': 1,
                     'Mythril Halberd': 1,
                     'Ivy Whip': 1,
                     'Cobalt Hat': 1,
                     'Angel Wings': 1,
                     'Greater Mana Potion': 99,
                     'Flamarang': 1,
                     'Blade of Grass': 1,
                     'Breathing Reed': 1,
                     'Cobalt Chainsaw': 1,
                     'Meteor Shot': 250,
                     'Holy Water': 250,
                     'Dirt Rod': 1,
                     'Goggles': 1,
                     'Iron Broadsword': 1,
                     'Spiky Ball': 250,
                     'Lucky Horseshoe': 1,
                     'Obsidian Skull': 1,
                     'Green Phasesaber': 1,
                     'Meteor Suit': 1,
                     'Mythril Chainsaw': 1,
                     'Greater Healing Potion': 30,
                     'Lens': 99,
                     "Archaeologist's Pants": 1,
                     'Bowl of Soup': 30,
                     'Gold Helmet': 1,
                     'Mythril Helmet': 1,
                     'Shadow Helmet': 1,
                     'Dual Hook': 1,
                     'Light Disc': 5,
                     'Moon Charm': 1,
                     'Hallowed Plate Mail': 1,
                     'Grenade': 250,
                     'Flamethrower': 1,
                     'Magic Missile': 1,
                     'Muramasa': 1,
                     'Santa Pants': 1,
                     'Bottled Water': 30,
                     'Blue Phaseblade': 1,
                     'Dao of Pow': 1,
                     'Wooden Bow': 1,
                     'Cobalt Mask': 1,
                     'Shackle': 1,
                     'Blowpipe': 1,
                     'Space Gun': 1,
                     'Copper Broadsword': 1,
                     'Mythril Chainmail': 1,
                     'Fallen Star': 250,
                     'Demon Scythe': 1,
                     'Healing Potion': 30,
                     'Blue Moon': 1,
                     'Mythril Hat': 1,
                     'Feral Claws': 1,
                     'Copper Axe': 1,
                     'Hunter Potion': 30,
                     'Pwnhammer': 1,
                     'Obsidian Skin Potion': 30,
                     'Shine Potion': 30}
        self.keys = []
        for key in self.itemlist.keys():
            self.keys.append(key) 
    
    def makeChestTiles(self):
        for chest in self.chests:
            if chest is not None:  
                self.tiles[chest[0][0]][chest[0][1]] = (21,None,0,(0,0),0)
                self.tiles[chest[0][0]+1][chest[0][1]] = (21,None,0,(18,0),0)
                self.tiles[chest[0][0]][chest[0][1]+1] = (21,None,0,(0,18),0)
                self.tiles[chest[0][0]+1][chest[0][1]+1] = (21,None,0,(18,18),0)
            if self.tiles[chest[0][0]][chest[0][1]+2] == (None, self.mapWall, 0, None, 0) or self.tiles[chest[0][0]+1][chest[0][1]+2] == (None, self.mapWall, 0, None, 0):
                self.tiles[chest[0][0]][chest[0][1]+2] = (1,None,0,None,0)
                self.tiles[chest[0][0]+1][chest[0][1]+2] = (1,None,0,None,0)
                self.tiles[chest[0][0]-1][chest[0][1]+2] = (4,self.mapWall,0,(44,0),0)
                self.tiles[chest[0][0]+2][chest[0][1]+2] = (4,self.mapWall,0,(22,0),0)
        print('Chest tiles made.')
        for x in range(1000-len(self.chests)):
            self.chests.append(None)
                
    def run(self):
        m = Maze()
        m.innerWorkings()
        sizeType = m.returnSize()
        size = [(4200,1200), (6300, 1800),(8400,2400),(1280,960)][sizeType]
        self.size = size
        spawn = (size[0]//2,size[1]//2)
        self.chestLimit = [100, 150, 250, 50][sizeType]
        self.header =  {'spawn': spawn, 'groundlevel': 300, 'is_bloodmoon': 0,
              'dungeon_xy': spawn, 'worldrect': (0, size[0]*16, 0, size[1]*16),
              'is_meteor_spawned': 0, 'gob_inv_time': 0, 'rocklevel': (size[1]//2),
              'gob_inv_x': 0.0, 'is_day': 1, 'shadow_orbs_broken': 0,
              'width': size[0], 'version': db.version, 'gob_inv_type': 0,
              'bosses_slain': (0, 0, 1), "npcs_saved" : (0,0,0), "special_slain": (0,0,0),
              'gob_inv_size': 0, 'height': size[1],
              'ID': 1337731060, 'moonphase': 0, 'name': "MazeWorld", "hardmode" : 0,
              "altars_broken" : 0,
              'is_a_shadow_orb_broken': 0, 'time': 13000.0}
        self.npcs = []
        self.names = db.names
        self.signs = [None]*1000
        self.chests = [((spawn[0],spawn[1]),[(1,"Dual Hook",0),(99,"Torch",0),(99,"Red Torch",0),(99,"Blue Torch",0),(1, "Nightmare Pickaxe",0),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None)])]
        self.tiles = self.convertList(m.createTileList())
        self.populateChestAreas(self.chooseChestAreas())
        self.makeChestTiles()
        self.placeShadowOrb(self.testShadowOrb())
        
    def chooseChestAreas(self):
        chestCount = 0
        chestAreas = []
        chosen = 0
        notch = 0
        while chestCount < self.chestLimit:
            testArea = (randint(0, self.size[0]-6),randint(0, self.size[1]-6))
            if self.tiles[testArea[0]][testArea[1]] == (None, self.mapWall, 0, None, 0) and self.tiles[testArea[0]+1][testArea[1]] == (None, self.mapWall, 0, None, 0) and self.tiles[testArea[0]][testArea[1]+1] == (None, self.mapWall, 0, None, 0) and self.tiles[testArea[0]+1][testArea[1]+1] == (None, self.mapWall, 0, None, 0) and self.tiles[testArea[0]+1][testArea[1]+2] == (self.mapTile, None, 0, None, 0) and self.tiles[testArea[0]][testArea[1]+2] == (self.mapTile, None, 0, None, 0):
                chestAreas.append((testArea))
                chosen += 1
#                print('Areas Chosen: ' + str(chosen))
                chestCount += 1
                
            else:
                notch += 1
#                print('Areas NOT Chosen: ' + str(notch))
        print('Chest Areas Chosen.')
        return chestAreas
    
    
            
    def testShadowOrb(self):
        orbAreas = []
        while len(orbAreas) < self.orbLimit: 
            testArea = (randint(0, self.size[0]),randint(0, self.size[1]))
            if self.tiles[(testArea[0])][(testArea[1])] == (None, self.mapWall, 0, None, 0) and self.tiles[(testArea[0])+1][(testArea[1])] == (None, self.mapWall, 0, None, 0) and self.tiles[(testArea[0])][(testArea[1]+1)] == (None, self.mapWall, 0, None, 0) and self.tiles[(testArea[0]+1)][(testArea[1]+1)] == (None, self.mapWall, 0, None, 0):
                orbAreas.append(testArea)
#                print('Shadow Orb area chosen.')
#            else:
#                print('Shadow orb area NOT chosen.')
#                print(testArea)
        return orbAreas
    
    def placeShadowOrb(self, orbAreas):
        for orb in orbAreas:
            self.tiles[orb[0]][orb[1]] = (31,None,0,(0,0),0)
            self.tiles[orb[0]+1][orb[1]] = (31,None,0,(18,0),0)
            self.tiles[orb[0]][orb[1]+1] = (31,None,0,(0,18),0)
            self.tiles[orb[0]+1][orb[1]+1] = (31,None,0,(18,18),0)
#            print('One orb placed.')
        print('Shadow Orbs placed.')
        
    def chooseContents(self):
        contents = []
        amount = randint(2,5)
        while len(contents) < amount:
            item = choice(self.keys)
            itemAmount = randint(1,self.itemlist[item])
            I = (itemAmount,item)
            contents.append(I)
            emptyChance = random()
            if emptyChance <= .03:
                contents = []
                break
        while len(contents) < 20:
#            print(len(contents))
            contents.append((0,None)) 
#        print(contents)
#        print(len(contents))
        return contents

            
        
    def populateChestAreas(self, chestAreas):
        for chest in chestAreas:
            self.chests.append((((chest[0],chest[1]),self.chooseContents())))
#            print(self.chests)
        print('Chest contents placed.')
        
    def gen_gui(self):
        from omnitool.shared import theme, lang, exit_prog
        from omnitool.pgu_override import Quitbutton
        pygame.display.init()
        pygame.display.set_caption("Maze World Generator")
        app = gui.Desktop(theme = theme)
        main = gui.Table(width = 800)
        app.connect(gui.QUIT,exit_prog,None)
        
        main.td(gui.Label("Maze Blocks: "))
        tileFrom = gui.List(300, 150)
        for tile in db.tiles:
            if db.tiles.index(tile) not in db.multitiles and db.tiles.index(tile) in clib.data:
                tileFrom.add(gui.Label(tile), value = db.tiles.index(tile))
        main.td(tileFrom)
        
#        main.td(gui.Label("Light up maze?"))
#        polkaDotButton = (gui.Switch(False))
#        main.td(polkaDotButton)
        
        main.tr()
        
        main.td(gui.Label("Maze BackWalls: "))
        tileInto = gui.List(300, 150)
        for wall in db.walls:
            if db.walls.index(wall) in clib.walldata:
                tileInto.add(gui.Label(wall), value = db.walls.index(wall))
        main.td(tileInto)
        
#        main.td(gui.Label("View generation?"))
        viewGenButton = (gui.Switch(False))
#        main.td(viewGenButton)
        
        main.tr()
        
        main.td(gui.Label("World Size: "))
        size = gui.List(110, 50)
        size.add("Tiny", value = 3)
        size.add("Small", value = 0)
        size.add("Medium", value = 1)
        size.add("Large", value = 2)
        main.td(size)
        
        
        
        main.td(gui.Label("Complexity: "))
        scale = gui.List(110,50)
        scale.add("Insane", value = 3)
        scale.add("Medium", value = 6)
        scale.add("Easy", value = 9)
        main.td(scale)
        
        main.tr()
        main.td(Quitbutton(app, lang.pt_start),colspan = 4)
        
        app.run(main)
        pygame.display.quit()
        
        self.tileFrom = clib.data[tileFrom.value]
        self.tileInto = clib.walldata[tileInto.value]
        self.size2 = size.value
        self.scale2 = scale.value
        self.viewGen = viewGenButton.value
#        self.polkaDotButt = polkaDotButton.value
        
    
    def convertList(self, tilelist):
        tileColorDict = dict([(v,k) for (k,v) in clib.data.items()])
        wallColorDict = dict([(v,k) for (k,v) in clib.walldata.items()])
        tiles = []
        for col in tilelist:
            column = []
            for tile in col:
                tile = (tile[0],tile[1],tile[2])
                if tile in tileColorDict:
                    if db.ntiles[db.tiles[tileColorDict[tile]]] == 130:
                        column.append((1, None, 0, None, 0))
                        self.mapTile = 1
                    else:
                        column.append(((db.ntiles[db.tiles[tileColorDict[tile]]]), None, 0, None, 0))
                        self.mapTile = (db.ntiles[db.tiles[tileColorDict[tile]]])
                else:
                    column.append((None, (db.nwalls[db.walls[wallColorDict[tile]]]), 0, None, 0))
                    self.mapWall = (db.nwalls[db.walls[wallColorDict[tile]]])
            tiles.append(column)
        return tiles
        
        
class Maze():
    def __init__(self):
        Generator.gen_gui(self)
        pygame.quit()
#        self.polkaDot = self.polkaDotButt
#        self.polkaColor = (4,None,0,(0,0),0)
        self.sizeType = self.size2
        self.scaling = (3*self.scale2)
        self.color = self.tileFrom
        self.wallColor = self.tileInto
        self.size = [(4200,1200), (6300, 1800),(8400,2400),(640,480)][self.sizeType]
        self.boundaryRect = pygame.Rect(1,1,self.size[0]//self.scaling+10, self.size[1]//self.scaling+10)
        self.totalSize = [5040000,11340000,20160000,307200][self.sizeType]
        self.currentCell = (randint(0,self.size[0]//self.scaling),randint(0,self.size[1]//self.scaling))
        while self.boundaryRect.collidepoint(self.currentCell) == False:
            self.currentCell = (randint(0,self.size[0]//self.scaling),randint(0,self.size[1]//self.scaling))
        self.visitedCells = 1
        self.cellLocation = []
        self.visitedLocation = []
        self.cellLocation.append(self.currentCell)
        if self.viewGen:
            pygame.init()
            self.mazeScreen = pygame.display.set_mode(self.size)
            pygame.display.set_caption("Spaghetti")
        else:
            self.mazeScreen = pygame.Surface(self.size)
        self.fpsClock = pygame.time.Clock()
        self.neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
        self.visited = pygame.mask.Mask(self.size)#MASK
        
    def get_smallest_rect(self, points):
        min_X = min((p[0] for p in points))
        min_Y = min((p[1] for p in points))
        max_X = max((p[0] for p in points))
        max_Y = max((p[1] for p in points))
        return (min_X-(self.scaling//2), min_Y-(self.scaling//2), max_X-min_X+(self.scaling), max_Y-min_Y+(self.scaling))
    
    def innerWorkings(self):
        """Maze Generation and the backbone of the recursive backtracking"""
        self.mazeScreen.fill(self.color)
        startTime = time.time()
        if self.viewGen:
            pygame.display.update()
        while 1:
            if self.viewGen:
                pygame.event.pump()
            self.checkNeighbors()
            if self.neighborsFree:
                self.move()
                p1 = (self.currentCell[0]*self.scaling,self.currentCell[1]*self.scaling)
                p2 = (self.cellLocation[-1][0]*self.scaling,self.cellLocation[-1][1]*self.scaling)
                pygame.draw.line(self.mazeScreen,self.wallColor,p1,p2,(self.scaling-4))
                self.currentCell = self.cellLocation[-1]
                if self.viewGen:
                    pygame.display.update(self.get_smallest_rect((p1,p2)))
                    #pygame.display.update()
                self.visitedCells += 1
            else:
                self.cellLocation.pop()
                if len(self.cellLocation):
                    self.currentCell = self.cellLocation[-1]
                else:
                    print('done')
                    print('Maze layout generation only took ' + str((startTime-time.time())*-1) + ' seconds!')
                    pygame.quit()
                    return True

    def checkNeighbors(self):
        """Check if any neighbors have been moved to"""
        self.neighborsFree = []
        for pos in self.neighbors:
            npos = (self.currentCell[0]+pos[0],self.currentCell[1]+pos[1])
            if not self.visited.get_at(npos) and self.boundaryRect.collidepoint(npos):#MASK
                self.neighborsFree.append(pos)

        
    def move(self):
        """ Picking a direction to move in - Must always be called after checkNeighbors()"""
        direction = choice(self.neighborsFree)
        new = (self.currentCell[0] + direction[0],self.currentCell[1] + direction[1])
        self.cellLocation.append(new)
        self.visited.set_at(new, 1)#MASK
        
    def returnSize(self):
        return self.sizeType
        
    def createTileList(self):
        tilelist = []
        counter = 0
        while counter < self.size[0]:
            counter2 = 0
            col = []
            while counter2 < self.size[1]:
                pixel = self.mazeScreen.get_at((counter,counter2))
                if str(pixel) in clib.data or clib.walldata:
                    counter2 += 1 
                    col.append(pixel)
            counter += 1
            tilelist.append(col)
        return tilelist
        