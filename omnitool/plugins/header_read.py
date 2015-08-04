config = {
    "name": "Header reader",  # plugin name
    "type": "receiver",  #plugin type
    "description": ["prints headerdata to console"]  #description
}


class Receiver():  # required class to be called by plugin manager
    def __init__(self):  #do any initialization stuff
        pass  # we dont need any, so we pass

    def rec_header(self, header):  #this is called by plugin manager when the header is read
        print()
        print("Header data for world %s" % header["name"])
        del (header["name"])
        for key in header:
            print("%-25s%40s" % (key, header[key]))
        return False
