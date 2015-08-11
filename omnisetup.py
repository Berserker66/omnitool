import shutil
import os
import sys
from pathlib import Path

import cx_Freeze
import sysconfig
is_64bits = sys.maxsize > 2**32

folder = "exe.{platform}-{version}".format(platform = sysconfig.get_platform(),
                                           version = sysconfig.get_python_version())
buildfolder = Path("build", folder)
print("Outputting to: "+folder)
EXE = cx_Freeze.Executable(
    script="run_omnitool.py",
    targetName="Omnitool" if sys.platform == "linux" else "Omnitool.exe",
    icon="Icon128.ico",
    compress=True,
)
cx_Freeze.setup(
    name="Omnitool",
    version="1",
    description="Omnitool",
    executables=[EXE],
    options={
        "build_exe": {
            "excludes": ["OpenGL", "tkinter", "tcl"],
            "packages": ["omnitool"],
            "includes" : (),
        },
    },
)

if sys.platform == "linux":
    ext = "so"
else:
    ext = "pyd"
not_needed = (x + ext for x in ("pygame.movie.", "pygame.mixer_music.", "pygame.mixer.",
                                "pygame.overlay."))

for f in not_needed:
    try:
        os.remove(str(buildfolder / f))
    except FileNotFoundError:
        print("Warning: {} already doesn't exist, cannot remove.".format(f))

def installfile(path):
    dst = buildfolder

    print('copying', path, '->', dst)
    if path.is_dir():
        dst /= path.name
        if dst.is_dir():
            shutil.rmtree(str(dst))
        shutil.copytree(str(path), str(dst))
    elif path.is_file():
        shutil.copy(str(path), str(dst))
    else:
        print('Warning,', path, 'not found')


extra_data = ["omnitool/themes", "plugins", "tImages.zip"]
for data in extra_data:
    installfile(Path(data))

if sys.platform == "win32" and os.path.isfile("upx.exe"):
    strbuild = str(buildfolder)
    targets = os.listdir(strbuild)
    targets = filter(lambda x:x.endswith((".pyd", ".exe")), targets)
    targets = " ".join((os.path.join(strbuild, target) for target in targets))
    command = "upx.exe "+targets
    print(command)
    os.system(command)
