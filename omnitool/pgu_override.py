import os

from pathlib import Path

from pgu.gui import Desktop, basic, container, surface, Theme, Button
from pgu.gui.const import *
from pygame.locals import *

from .shared import datadir


class MyApp(Desktop):
    def __init__(self, **params):
        Desktop.__init__(self, **params)
        self.queue = []
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
    #override
    def run(self, widget=None, screen=None, delay=10):
        """Run an application.

        Automatically calls App.init and then forever loops while
        calling App.event and App.update

        Keyword arguments:
            widget -- the top-level widget to use
            screen -- the pygame surface to render to
            delay -- the delay between updates (in milliseconds)
        """
        self.init(widget, screen)
        while not self._quit:
            todo = self.queue[:]
            [self.queue.remove(t) for t in todo]
            for row in todo:
                row[0](*row[1:])
            self.loop()
            pygame.time.wait(delay)

def change_image(self, value):
    self.value = value
    self.style.width, self.style.height = value.get_width(), value.get_height()

theme_path = datadir / 'themes'

class MyTheme(Theme):
    def __init__(self, name):
        try:
            Theme.__init__(self, str(theme_path / name))
        except:
            print("Warning: Unable to load selected theme", theme_path / name)
            for name in theme_path.iterdir():
                try:
                    Theme.__init__(self, str(theme_path / name))
                except:
                    pass
                else:
                    return
            raise

def myupdate(self, s):
    updates = []

    if self.myfocus: self.toupdate[self.myfocus] = self.myfocus

    for w in self.topaint:
        if w is self.mywindow:
            continue
        else:
            sub = surface.subsurface(s, w.rect)
            w.paint(sub)
            updates.append(pygame.rect.Rect(w.rect))
    while 1:
        try:
            for w in self.toupdate:
                if w is self.mywindow:
                    continue
                else:
                    us = w.update(surface.subsurface(s, w.rect))
                if us:
                    for u in us:
                        updates.append(pygame.rect.Rect(u.x + w.rect.x, u.y + w.rect.y, u.w, u.h))
            break
        except RuntimeError:
            pass
    for w in self.topaint:
        if w is self.mywindow:
            w.paint(self.top_surface(s, w))
            updates.append(pygame.rect.Rect(w.rect))
        else:
            continue

    for w in self.toupdate:
        if w is self.mywindow:
            us = w.update(self.top_surface(s, w))
        else:
            continue
        if us:
            for u in us:
                updates.append(pygame.rect.Rect(u.x + w.rect.x, u.y + w.rect.y, u.w, u.h))

    self.topaint = {}
    self.toupdate = {}

    return updates

class Quitbutton(Button):
    def __init__(self, app, text):
        Button.__init__(self, text, width=300, height=40)
        try:
            self.connect(CLICK, app.quit, None)
        except AttributeError:
            self.connect(CLICK, app.close, None)

container.Container.update = myupdate
basic.Image.change_image = change_image
