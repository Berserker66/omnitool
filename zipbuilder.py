from zipfile import *

import os

print("Zipping content files...", end="")

with ZipFile(os.path.join("build", "content.lzma"), "w", ZIP_LZMA) as Z:
    for file in os.listdir("tImages"):
        Z.write(os.path.join("tImages", file), arcname = file)

print("Done!")