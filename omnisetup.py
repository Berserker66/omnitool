import shutil
import os

import cx_Freeze
import sys
import sysconfig
is_64bits = sys.maxsize > 2**32

folder = "exe.{platform}-{version}".format(platform = sysconfig.get_platform(),
                                                           version = sysconfig.get_python_version())

print("Outputting to: "+folder)
EXE = cx_Freeze.Executable(
    script="omnitool.py",
    icon="Icon128.ico",
    compress=True,
)
cx_Freeze.setup(
    name="Omnitool",
    version="1",
    description="Omnitool",
    executables=[EXE],
    options={"build_exe": {"excludes": ["OpenGL", "tkinter", "tcl"],
                           "packages": ["multiprocessing"],
                           "includes" : ("loadbar","colorsys")}
             }
)
not_needed = ("pygame.movie.pyd", "pygame.mixer_music.pyd", "pygame.mixer.pyd",
              "pygame.overlay.pyd", "pygame.pixelarray.pyd")

for f in not_needed:
    os.remove(os.path.join("build", folder, f))


def installfile(name):
    dst = os.path.join('build', folder)
    print('copying', name, '->', dst)
    if os.path.isdir(name):
        dst = os.path.join(dst, name)
        #print dst+" folder"
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
        #print name+" file"
    else:
        print('Warning, %s not found' % name)


extra_data = ["themes", "Images", "steam_api.dll", "plugins", "build/content.lzma"]
for data in extra_data:
    installfile(data)
