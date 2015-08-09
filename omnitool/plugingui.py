import os

import pygame

from pgu import gui
from .tlib import get_name
from .tinterface import get_worlds


def exit_prog(p):
    pygame.quit()
    import sys

    sys.exit()


def run(worlds, Plugin, ptype):
    # pygame.quit()
    from .shared import lang, theme


    class Quitbutton(gui.Button):
        def __init__(self, value=lang.pl_start):
            gui.Button.__init__(self, value, width=250, height=40)
            try:
                self.connect(gui.CLICK, app.quit, None)
            except AttributeError:
                self.connect(gui.CLICK, app.close, None)

    pygame.display.init()
    pygame.display.set_caption("Plugin World Selector")

    app = gui.Desktop(theme=theme)
    trans = False
    colspan = 1
    if ptype == "rec":
        tlabel = gui.Label(lang.pl_rec)
    elif ptype == "mod":
        tlabel = gui.Label(lang.pl_mod)
    else:
        trans = True
        tlabel = gui.Label(lang.pl_trans)
        colspan = 2
    main = gui.Table()
    app.connect(gui.QUIT, exit_prog, None)
    main.td(gui.Label(Plugin.config["name"], cls="h1"), colspan=colspan)
    for line in Plugin.config["description"]:
        main.tr()
        main.td(gui.Label(line), colspan=colspan)
    main.tr()
    main.td(gui.Spacer(12, 12))
    main.tr()
    main.td(tlabel, colspan=colspan)
    main.tr()
    main.td(gui.Spacer(12, 12))
    main.tr()
    if trans:
        main.td(gui.Label(lang.pl_trans_source))
        main.td(gui.Label(lang.pl_trans_target))
        main.tr()
        data = []
        liste2 = gui.List(250, 250)
        for w in worlds:
            with w.open("rb") as f:
                name = get_name(f)
            liste2.add(name, value=w)
        main.td(liste2)
    data = []
    liste = gui.List(250, 250)
    for w in worlds:
        with w.open("rb") as f:
            name = get_name(f)
        liste.add(name, value=w)
    main.td(liste)
    main.tr()
    main.td(gui.Spacer(12, 12))
    main.tr()
    main.td(Quitbutton(), colspan=colspan)
    app.run(main)
    pygame.display.quit()
    if trans:
        return liste.value, liste2.value
    return liste.value


if __name__ == "__main__":
    p, ws = get_worlds()
    run_rec(p, ws, None)
