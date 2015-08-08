import runpy
import multiprocessing
if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")  # Prevents X11 crash on Linux - properly separates pygame internals

    runpy.run_module('omnitool')
