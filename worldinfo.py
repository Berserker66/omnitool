from tinterface import get_header
from sys import argv


def make_info(path):
    with  open(path, "rb") as f:
        header = get_header(f)[0]
    for key in header:
        print(key + ": " + str(header[key]))


if __name__ == "__main__":
    if len(argv) > 1:
        make_info(argv[1])
    else:
        make_info("world1.wld")
