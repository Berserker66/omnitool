import os

from pgu.gui import Desktop, basic, container
from pgu.gui.const import *
from pygame.locals import *


class MyApp(Desktop):
    def __init__(self, **params):
        Desktop.__init__(self, **params)
        self.zoomed = False
        self.first = True

    def event(self, ev):  # override
        self.set_global_app()

        if (self.appArea and hasattr(ev, "pos")):
            # Translate into subsurface coordinates
            pos = (ev.pos[0] - self.appArea.x,
                   ev.pos[1] - self.appArea.y)
            args = {"pos": pos}
            # Copy over other misc mouse parameters
            for name in ("buttons", "rel", "button"):
                if (hasattr(ev, name)):
                    args[name] = getattr(ev, name)

            ev = pygame.event.Event(ev.type, args)

        #NOTE: might want to deal with ACTIVEEVENT in the future.
        self.send(ev.type, ev)
        container.Container.event(self, ev)
        if ev.type == MOUSEBUTTONUP:
            if ev.button not in (4, 5):  # Ignores the mouse wheel
                # Also issue a "CLICK" event
                sub = pygame.event.Event(CLICK, {
                    'button': ev.button,
                    'pos': ev.pos})
                self.send(sub.type, sub)
                container.Container.event(self, sub)

        elif ev.type == 16:  #videoresize
            try:
                del (os.environ["SDL_VIDEO_WINDOW_POS"])
            except KeyError:
                pass
            self.on_resize(self, ev)
            self.repaint()


def change_image(self, value):
    self.value = value
    self.style.width, self.style.height = value.get_width(), value.get_height()


basic.Image.change_image = change_image
