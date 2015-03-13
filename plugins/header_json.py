config = {
    "name": "Header to JSON",  # plugin name
    "type": "receiver",  #plugin type
    "description": ["prints headerdata json file"]  #description
}
import json


class Receiver():  # required class to be called by plugin manager
    def __init__(self):  #do any initialization stuff
        pass

    def rec_header(self, header):  #this is called by plugin manager when the header is read
        with open("json_header.txt", "wt") as f:
            json.dump(header, f, indent=4)
        return False
