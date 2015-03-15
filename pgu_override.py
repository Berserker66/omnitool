import os

from pgu.gui import Desktop, basic, container, FileDialog
from pgu.gui.const import *
from pygame.locals import *


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

class MyFileDialog(FileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_dir.connect(ACTIVATE, self._button_okay_clicked_, None)

    def _button_okay_clicked_(self, arg):
        if self.input_dir.value != self.curdir:
            if os.path.isdir(self.input_dir.value):
                self.input_file.value = ""
                self.curdir = os.path.abspath(self.input_dir.value)
                self.list.clear()
                self._list_dir_()
            else:
                self.input_dir.value = self.curdir
        else:
            self.value = os.path.join(self.curdir, self.input_file.value)
            self.send(CHANGE)
            self.close()


basic.Image.change_image = change_image
