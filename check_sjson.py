import json

with open("json.txt") as f:
    with open("jsonout.txt", "w") as g:
        json.dump(json.load(f), g, indent=4)
