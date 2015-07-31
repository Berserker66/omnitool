import sys

def run_flat():
    launch_plugin(('flatworld', 'Flatworld', 'generator'))


def run_plat():
    launch_plugin(('planetoids', 'Planetoids', 'generator'))


def run_arena():
    launch_plugin(('arena', 'Dungeon Arena', 'generator'))


def run_world():
    launch_plugin(('worldify', 'Worldify', 'generator'))


from omnitool import launch_plugin as base


def launch_plugin(*args, **kwargs):
    base(*args, **kwargs)


if sys.platform == "linux":
    def launch_plugin(*args, **kwargs):
        print("Relay")
        if sys.platform == "linux":
            import ctypes
            x11 = ctypes.cdll.LoadLibrary("libX11.so")
            retcode = x11.XInitThreads()
            assert (retcode != 0)
        base(*args, **kwargs)
