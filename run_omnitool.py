#! python3
# coding=utf-8

import runpy
from multiprocessing import freeze_support, set_start_method
if __name__ == "__main__":
    freeze_support()
    set_start_method("forkserver")  # Prevents X11 crash on Linux - properly separates pygame internals

    text = """ ██████╗ ███╗   ███╗███╗   ██╗██╗████████╗ ██████╗  ██████╗ ██╗     
██╔═══██╗████╗ ████║████╗  ██║██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██║   ██║██╔████╔██║██╔██╗ ██║██║   ██║   ██║   ██║██║   ██║██║     
██║   ██║██║╚██╔╝██║██║╚██╗██║██║   ██║   ██║   ██║██║   ██║██║     
╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║   ██║   ╚██████╔╝╚██████╔╝███████╗
 ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝"""
    
    print(text)

    runpy.run_module('omnitool', run_name="__main__")

if False:
    import omnitool  # freeze hook

print("Done - exiting")
import sys

print(sys.argv, __name__)
