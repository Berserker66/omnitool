import time

import english
import german
import portuguese
import czech
import french
import spanish
import danish


for item in dir(english):
    langs = english, german, portuguese, czech, french, spanish, danish
    for lang in langs:
        if item not in dir(lang):
            print(lang.__name__ + ".py", "misses", item)

time.sleep(3)
