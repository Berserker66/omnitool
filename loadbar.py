import pygame
import pygame.gfxdraw


class Bar():
    def __init__(self, size = (500,20), caption = "Planetoids:", bg = pygame.Color("black"), fg = pygame.Color("grey")):

        pygame.display.init()#
        self.size = size
        pygame.display.set_caption(caption)
        self.basecaption = caption
        self.surface = pygame.display.set_mode(size)
        self.fg = fg
        self.bg = bg
        self.scale = self.size[0]/100
        self.set_progress(0)

    def set_progress(self, percent, caption = ""):
        for event in pygame.event.get():
            if event.type == 12:
                pygame.quit()
                import sys
                sys.exit()
        if caption:
            pygame.display.set_caption(caption)
        self.progress = percent
        self.surface.fill(self.bg)
        rect = ((0,0), (self.progress*self.scale, self.size[1]))
        pygame.gfxdraw.box(self.surface, rect, self.fg)
        pygame.display.update(rect)
