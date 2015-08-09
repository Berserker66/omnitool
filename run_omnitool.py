#! python3
# coding=utf-8

import runpy
import multiprocessing
if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")  # Prevents X11 crash on Linux - properly separates pygame internals
    text = """ ██████╗ ███╗   ███╗███╗   ██╗██╗████████╗ ██████╗  ██████╗ ██╗     
██╔═══██╗████╗ ████║████╗  ██║██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██║   ██║██╔████╔██║██╔██╗ ██║██║   ██║   ██║   ██║██║   ██║██║     
██║   ██║██║╚██╔╝██║██║╚██╗██║██║   ██║   ██║   ██║██║   ██║██║     
╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║   ██║   ╚██████╔╝╚██████╔╝███████╗
 ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝"""
    
    print(text)


    runpy.run_module('omnitool')
