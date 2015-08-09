import os


def split(path, byteposes):
    i = 0
    nposes = []
    for x in range(len(byteposes)):
        if x:
            nposes.append(byteposes[x] - byteposes[x - 1])
        else:
            nposes.append(byteposes[x])
    for x in nposes:
        i += x
    i = 0
    with open(path, "rb") as f:
        for x in range(len(byteposes)):
            with open(str(i) + ".part", "wb") as d:
                d.write(f.read(nposes[x]))
            i += 1
        with open(str(i) + ".part", "wb") as d:
            d.write(f.read())


def join(name, delete=False, path=None):
    with open(name, "wb") as f:
        for x in range(6):
            if path:
                n = os.path.join(path, str(x) + ".part")
            else:
                n = str(x) + ".part"
            with open(n, "rb") as d:
                f.write(d.read())
            if delete:
                try:
                    os.remove(n)
                except:
                    pass


def cleanup():
    for x in range(6):
        try:
            os.remove(str(x) + ".part")
        except:
            pass


if __name__ == "__main__":
    from tinterface import World

    world = World("world2.wld")

    # world.make_split()
    from tlib import *

    with open("0.part", "rb") as f:
        h = get_header(f)
    with open("other.part", "wb") as f:
        set_header(f, h)
    with open("other.part", "rb") as f:
        print(f.read())
    join("world6.wld", False)
    print(world.header["name"] + " done")
