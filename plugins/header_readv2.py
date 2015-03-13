config = {
    "name": "Ijwu's Header Reader",  # plugin name
    "type": "receiver",  #plugin type
    "description": ["Prints the World Header into console."]  #description
}


class Receiver():  # required class to be called by plugin manager
    def __init__(self):  #do any initialization stuff
        pass  # we dont need any, so we pass

    def rec_header(self, header):  #this is called by plugin manager when the header is read
        print()
        print("Header data for world %s" % header["name"])
        print()
        if header["is_day"]:
            print("It is currently night on this world.")
        else:
            print("It is currently day on this world.")
        print()

        print("Your spawn point is located at:", header["spawn"])
        print()
        print("The world's rock layer starts at %4.1f" % header["rocklevel"])
        print()
        print("The world's surface level begins at %i" % int(header["groundlevel"]))
        # "groundlevel" is a float. Conversion recommended.
        print()
        print("You currently have %i Demon Altars broken on your world." % header["altars_broken"])
        if header["hardmode"]:
            if header["altars_broken"] % 3 == 0:
                print("The next ore to spawn after an altar is broken will be Cobalt.")
            elif header["altars_broken"] % 3 == 1:
                print("The next ore to spawn after an altar is broken will be Mythril.")
            elif header["altars_broken"] % 3 == 2:
                print("The next ore to spawn after an altar is broken will be Adamantite.")

        print()
        print("You currently have %i out of 3 Shadow Orbs broken on your world." % int(header["shadow_orbs_broken"]))
        # "shadow_orbs_broken" is a float by default. It dumps about 7 decimal places in after the 0. int conversion recommended.
        print()
        if (header["spawn"][0] - header["dungeon_xy"][0]) > 0:
            print("The dungeon is exactly %i tiles to the right of the spawn." % (
            header["spawn"][0] - header["dungeon_xy"][0]))
        else:
            print("The dungeon is exactly %i tiles to the left of the spawn." % abs(
                (header["spawn"][0] - header["dungeon_xy"][0])))

        print()

        if header["bosses_slain"].count(1) > 1:
            print("%i different bosses have been slain!" % header["bosses_slain"].count(1))
            print()

        if header["is_bloodmoon"]:
            print("A bloodmoon is currently active on this world, careful!")
            print()

            #if  header["gob_inv_size"] > 1:
            #   print("There are goblins incoming.")
            #   print("The goblins are %i tiles away from the spawn!" % int((header["spawn"] [0]- header["gob_inv_x"])))

        if header["hardmode"]:
            print("Hardmode is on! Be careful!")
        else:
            print("Hardmode is currently off.")

        print()

        if header["is_meteor_spawned"]:
            print("There's a meteor on the ground! Go mine it!")
        else:
            print("A meteor is ready to fall on your world. There are none on the ground.")

        del (header["name"])

        print()

        print("Raw header data:")
        for key in header:
            print("%-25s%40s" % (key, header[key]))

        print()
        print("^^^ Scroll up for important world information in sentence form! ^^^")

        return False
