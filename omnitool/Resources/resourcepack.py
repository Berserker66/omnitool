__author__ = 'Fabian'
import os
import zipfile
import pygame
import array
pygame.init()
import threading
ziplock = threading.Lock()

RGBA_FORMAT = "RGBA"
RGB_FORMAT = "RGB"
BENCHMARK = True
formats = [RGBA_FORMAT, RGB_FORMAT]

from concurrent.futures import ThreadPoolExecutor
threadpool = ThreadPoolExecutor(10)

from header import imgheader
#Version, Width, Height



empty = array.array("B", (0).to_bytes(3, "little"))

relpath = os.path.join("tImages")

def handle_image(zip, path):
    base, _ = os.path.splitext(path)
    img = pygame.image.load(path)
    rel = os.path.relpath(base+".img", relpath)
    version = not img.get_alpha()
    form = formats[version]
    string = pygame.image.tostring(img, form)
    data = imgheader.pack(version, *img.get_size())+string
    with ziplock:
        zip.writestr(rel, data)
    print("Packed {:4}  ".format(form), rel)

def write(zip, path):
    rel = os.path.relpath(path, relpath)
    with ziplock:
        zip.write(path, rel)
    print("Stored", rel)

tasks = []

if BENCHMARK:
    import time
    start = time.clock()

with zipfile.ZipFile(os.path.join("tImages.zip"), "w", zipfile.ZIP_LZMA) as zip:
    for dirpath, _, filenames in os.walk(relpath):
        for file in filenames:
            path = os.path.join(dirpath, file)
            if file.endswith(".png"):
                tasks.append(threadpool.submit(handle_image, zip, path))
            elif file.endswith(".db"):
                pass
            else:
                tasks.append(threadpool.submit(write,zip, path))


    [task.result() for task in tasks]

if BENCHMARK:
    print("Took {} seconds".format(time.clock()-start))