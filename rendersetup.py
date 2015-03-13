# from cx_Freeze import setup, Executable
import shutil
import os

import cx_Freeze


EXE = cx_Freeze.Executable(
    script="render.py",
    icon="Icon128.ico",
    compress=True,
)
cx_Freeze.setup(
    name="Omnitool",
    version="1",
    description="Omnitool",
    executables=[EXE],
    options={"build_exe": {"excludes": ["OpenGL", "tkinter", "tcl"]}
             }
)
not_needed = ()

for f in not_needed:
    os.remove(os.path.join("build", "exe.win32-3.2", f))


def installfile(name):
    dst = os.path.join('build', 'exe.win32-3.2')
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


extra_data = ["tImages"]
for data in extra_data:
    installfile(data)
