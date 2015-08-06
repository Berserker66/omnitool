import pygame
import pygame.gfxdraw


class Bar():
    def __init__(self, size = (500,20), caption = "Loading:", bg = pygame.Color("black"), fg = pygame.Color("grey"),
                 abortable = True):

        pygame.display.init()#
        self.abortable = abortable
        self.size = size
        pygame.display.set_caption(caption)
        self.basecaption = caption
        self.surface = pygame.display.set_mode(size)
        self.rect = pygame.Rect((0,0), (0, self.size[1]))
        self.fg = fg
        self.bg = bg
        self.scale = self.size[0]/100
        self.set_progress(0)

    def set_progress(self, percent, caption = ""):
        for event in pygame.event.get():
            if event.type == 12 and self.abortable:
                pygame.quit()
                import sys
                sys.exit()
        if caption:
            pygame.display.set_caption(caption)
        self.progress = percent
        self.surface.fill(self.bg)
        self.rect.width = self.progress*self.scale
        pygame.gfxdraw.box(self.surface, self.rect, self.fg)
        pygame.display.update(self.rect)
