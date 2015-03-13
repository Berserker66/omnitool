from OpenGL.GL import *


class Texture():
    def __init__(self, surface, hotspot=(0, 0), group=None, name=None):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        if hotspot == None:
            self.hotspot = self.width / 2, self.height / 2
        else:
            self.hotspot = hotspot
        self.group = group
        self.name = name


def render_tile(display, image, position, x, y):
    # print (area, area[0])
    if (not hasattr(image, "GLtexture")):
        display.load(image)
    glLoadIdentity()

    x0, y0 = position
    #x,y,w,h = area
    s0 = x / image.width
    s1 = s0 + 16 / image.width
    t0 = 1 - y / image.height
    t1 = 1 - y / image.height - 16 / image.height
    x1 = x0 + 16
    y1 = y0 + 16
    glBindTexture(GL_TEXTURE_2D, image.GLtexture.texture_id)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2d(s0, t0);
    glVertex2f(x0, y0)
    glTexCoord2d(s0, t1);
    glVertex2f(x0, y1)
    glTexCoord2d(s1, t1);
    glVertex2f(x1, y1)
    glTexCoord2d(s1, t0);
    glVertex2f(x1, y0)
    glEnd()

