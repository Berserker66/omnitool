__author__ = 'Fabian Dill <fabian.dill@web.de>'
__copyright__ = 'Copyright (C) 2010 Fabian Dill'
"""
You are allowed to modify, distribute and use this file however you may see fit,
except you may not claim this work as yours.

If you use this I would like to get credit, but that is not mandatory.
"""
from os import environ

from pygame import display, image, init, NOFRAME

from PIL import ImageGrab


init()


def splash(size, name, path="splash.png"):
    environ['SDL_VIDEO_WINDOW_POS'] = "center"
    display.set_caption(name)
    wininfo = display.Info()
    screensize = (wininfo.current_w, wininfo.current_h)
    desktop = ImageGrab.grab()
    screen = display.set_mode(size, NOFRAME, 32)
    background = image.load(path).convert_alpha()
    w, h = size
    w //= 2
    h //= 2
    desktop = desktop.crop((screensize[0] // 2 - w, screensize[1] // 2 - h,
                            screensize[0] // 2 + w, screensize[1] // 2 + h))
    string = desktop.tostring()
    desktop = image.fromstring(string, size, desktop.mode)
    desktop.blit(background, (0, 0))
    screen.blit(desktop, (0, 0))
    display.update()


if __name__ == "__main__":
    splash((512, 512), "Test", "splash.png")
    import time

    time.sleep(5)
