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
import japanese

from __init__ import check

langs = german, portuguese, czech, french, spanish, danish, norwegian, hungarian, russian, italian, japanese

complete = True
for lang in langs:
    missing = check(english, lang)
    for item in missing:
        print(lang.__name__ + ".py", "misses", item)
        complete = False

if not complete:
    import sys
    sys.exit(1)
