from distutils.core import setup
import os
import shutil

import py2exe


origIsSystemDLL = py2exe.build_exe.isSystemDLL


def isSystemDLL(pathname):
    if os.path.basename(pathname).lower() in ["sdl_ttf.dll", "libogg-0.dll", "libfreetype-6.dll", "win32.dll",
                                              "libvorbisfile-3.dll"]:
        return 0
    return origIsSystemDLL(pathname)


py2exe.build_exe.isSystemDLL = isSystemDLL


def installfile(name):
    dst = os.path.join('dist', project_name)
    print
    'copying', name, '->', dst
    if os.path.isdir(name):
        dst = os.path.join(dst, name)
        # print dst+" folder"
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
        # print name+" file"
    else:
        print
        'Warning, %s not found' % name


setup(
    console=[
        {
            "script": "parse.py",
            # "icon_resources": [(1, "PRS.ico")]
            #"bundle_files": 3,
            #"compressed" : True,
            #"optimize" : 2
        }
    ],
    # cmdclass = {"py2exe" : Py2exe},
    #data_files = ["libvorbisfile-3.dll"],
    options={"py2exe": {"bundle_files": 1,
                        "compressed": True,
                        "optimize": 2,
                        "ascii": 1,
                        #"skip_archive":1,
                        #"packages" : ["logging", "ctypes", "_ctypes","weakref"],
                        "packages": ["encodings"],
                        "includes": ['distutils.util'],
                        "excludes": ["pygame", "OpenGL", "numpy", "PIL", "Tkinter", "pyreadline", "multiprocessing"]}},
    #"includes" : ["numpy", "ctypes", "logging", "OpenGL.platform.win32"],
    #"excludes" : ["Tkinter"]}},
    zipfile=None,
)

script = ""
project_name = os.path.splitext(os.path.split(script)[1])[0]
extra_data = ["database.txt"]
for data in extra_data:
    installfile(data)
print
"done"
