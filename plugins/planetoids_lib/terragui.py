import pygame

from pgu import gui


def run(main=None):
    from omnitool.shared import lang, theme, exit_prog, __version__
    from omnitool.pgu_override import Quitbutton


    pygame.display.init()
    pygame.display.set_caption("Planetoids & Terra Generator")
    if main == None:
        app = gui.Desktop(theme=theme)
        main = gui.Table()
        app.connect(gui.QUIT, exit_prog, None)
    else:
        main = gui.Table()
        app = gui.Dialog(gui.Label("Planetoids and Terra Generator"), main)

    main.td(gui.Label(lang.pt_name), align=-1)
    nameinput = gui.Input("Planetoids OT-V" + str(__version__), width=237)
    main.td(nameinput, colspan=2)
    main.tr()

    main.td(gui.Label(lang.pt_mode), align=-1)
    method = gui.Select(width=250)
    method.add(lang.pt_small, (1, 0))
    method.add(lang.pt_medium, (2, 0))
    method.add(lang.pt_large, (3, 0))
    method.add(lang.pt_square, (4, 0))
    method.add(lang.pt_both, (3, 1))
    method.add(lang.pt_square_terra, (4, 2))
    method.value = (3, 0)
    main.td(method, colspan=2)
    main.tr()

    main.td(gui.Label(lang.pt_start_sel), align=-1)
    time = gui.Select(width=250)

    time.add(lang.pt_morning, 2)
    time.add(lang.pt_day, 1)
    time.add(lang.pt_night, 3)
    time.add(lang.pt_bloodmoon, 4)
    time.value = 1
    main.td(time, colspan=2)
    main.tr()
    main.td(gui.Spacer(1, 24))
    main.tr()
    main.td(gui.Label(lang.pt_extras), align=-1, colspan=3)
    main.tr()
    main.td(gui.Label(lang.pt_sun), align=-1)
    darkness = gui.Switch()
    darkness.value = True
    main.td(darkness, colspan=2)
    main.tr()

    main.td(gui.Label(lang.pt_atlantis), align=-1)
    atlantis = gui.Switch()
    atlantis.value = False
    main.td(atlantis, colspan=2)
    main.tr()

    main.td(gui.Label(lang.pt_merchant), align=-1)
    merch = gui.Switch()
    merch.value = True
    main.td(merch, colspan=2)
    main.tr()
    main.td(gui.Label(lang.pt_lloot), align=-1)
    loot = gui.Switch()
    loot.value = False
    main.td(loot, colspan=2)
    main.tr()

    main.td(gui.Label("Hardmode:"), align=-1)
    hard = gui.Switch()
    hard.value = False
    main.td(hard, colspan=2)
    main.tr()
    main.td(gui.Label(lang.pt_mirror), align=-1)
    mirror = gui.Switch()
    mirror.value = False
    main.td(mirror, colspan=2)
    main.tr()
    # main.td(gui.Label(lang.pt_pre), align = -1)
    pre = gui.Switch()
    pre.value = False
    #main.td(pre, colspan = 2)

    #main.tr()
    main.td(gui.Spacer(1, 12))
    main.tr()
    main.td(Quitbutton(app, lang.pt_start), colspan=3)
    main.tr()
    main.td(gui.Spacer(1, 12))

    if app.__class__.__name__ == "Desktop":
        app.run(main)
        pygame.display.quit()
        return (nameinput.value, method.value, time.value, darkness.value, atlantis.value,
                merch.value, loot.value, hard.value, mirror.value, pre.value)
    else:
        app.open()


if __name__ == "__main__":
    run()
