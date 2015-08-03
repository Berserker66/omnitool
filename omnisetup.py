import shutil
import os

import cx_Freeze
import sys
import sysconfig
is_64bits = sys.maxsize > 2**32

folder = "exe.{platform}-{version}".format(platform = sysconfig.get_platform(),
                                                           version = sysconfig.get_python_version())
buildfolder = os.path.join("build", folder)
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
        os.remove(os.path.join(buildfolder, f))
    except FileNotFoundError:
        print("Warning: {} already doesn't exist, cannot remove.".format(f))

def installfile(name):
    dst = buildfolder
    print('copying', name, '->', dst)
    if os.path.isdir(name):
        dst = os.path.join(dst, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
    else:
        print('Warning, %s not found' % name)


extra_data = ["themes", "plugins", "tImages.zip"]
for data in extra_data:
    installfile(data)

if sys.platform == "win32" and os.path.isfile("upx.exe"):
    targets = os.listdir(buildfolder)
    targets = filter(lambda x:x.endswith((".pyd", ".exe")), targets)
    targets = " ".join((os.path.join(buildfolder, target) for target in targets))
    command = "upx.exe "+targets
    print(command)
    os.system(command)
