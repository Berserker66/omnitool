import time

import english
import german
import portuguese
import czech
import french
import spanish
import danish
import norwegian
import hungarian
import russian
import italian


for item in dir(english):
    langs = english, german, portuguese, czech, french, spanish, danish, norwegian, hungarian, russian, italian

    for lang in langs:
        if item not in dir(lang):
            print(lang.__name__ + ".py", "misses", item)

time.sleep(3)
