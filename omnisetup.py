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

if sys.platform == "linux":
    ext = "so"
else:
    ext = "pyd"
not_needed = (x + ext for x in ("pygame.movie.", "pygame.mixer_music.", "pygame.mixer.",
                                "pygame.overlay."))


for f in not_needed:
    try:
        os.remove(os.path.join("build", folder, f))
    except FileNotFoundError:
        print("Warning: {} already doesn't exist, cannot remove.".format(f))


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


extra_data = ["themes", "plugins", "tImages.zip"]
for data in extra_data:
    installfile(data)
