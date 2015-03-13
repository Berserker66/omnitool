from tinterface import World

world = World("world3.wld")
world.ready_chests()
z = 0
items = {}
for x in world.chests:
    if x != None:
        print
        x
world.ready_signs()
for x in world.signs:
    if x: print
    x
world.ready_npcs()
print
"NPCs"
for x in world.npcs:
    print
    x
print
world.header
with open("world2.wld", "rb") as f:
    f.seek(world.signs.endpos - 2)
    content = f.read(2)
for c in content:
    print
    c,
    

