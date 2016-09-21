from omnitool.shared import __version__
import shutil

version = __version__.get_name()
print(version)
shutil.copy("README.md", "README.back")
with open("README.back") as inp:
    lines = inp.readlines()
    lines[0] = "Current version : {}, for Terraria 1.3.3.1 on Windows and Linux.\n".format(version)
with open("README.md", "w") as out:
    out.writelines(lines)

innos = {"setup.iss", "setup64.iss"}
for setup in innos:
    shutil.copy(setup, setup + ".back")
    with open(setup) as inp:
        lines = inp.readlines()
        lines[4] = '#define MyAppVersion "{}"\n'.format(version)
    with open(setup, "w") as out:
        out.writelines(lines)
