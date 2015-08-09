__author__ = 'Fabian'

from .header import imgheader

import zipfile
import pygame

RGBA = 0
RGB = 1
formats = ["RGBA", "RGB"]

class ResourceManager():
    def __init__(self, ressourcefile, format = zipfile.ZIP_LZMA):
        self.zip = zipfile.ZipFile(ressourcefile, "r", format)

    def __getitem__(self,path):
        return self.zip.read(path)

    def get_image_data(self, path):
        data = self.zip.read(path)
        version, width, height = imgheader.unpack(data)
        imgdata = data[imgheader.size:]
        return ((width, height), imgdata)

    def get_pygame_image(self, path):
        data = self.zip.read(path)
        version, width, height = imgheader.unpack(data[:imgheader.size])
        imgdata = data[imgheader.size:]
        return pygame.image.fromstring(imgdata, (width, height), formats[version])


