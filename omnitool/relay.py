"""Moves functions out of __main__.py for frozen multiprocessing to work"""

import webbrowser


def run_flat():
    launch_plugin(('flatworld', 'Flatworld', 'generator'))


def run_plat():
    launch_plugin(('planetoids', 'Planetoids', 'generator'))


def run_arena():
    launch_plugin(('arena', 'Dungeon Arena', 'generator'))


def run_world():
    launch_plugin(('worldify', 'Worldify', 'generator'))


from omnitool import launch_plugin as base
from omnitool import gen_slices


def launch_plugin(*args, **kwargs):
    base(*args, **kwargs)

def launch_gen_slices(*args, **kwargs):#freezing relay
    gen_slices(*args, **kwargs)


def run_with_browser(func, filepath, *args):
    """
    Run func with *args, then open filepath in browser
    :param func: function, that accepts *args
    :param filepath: filepath to open in browser
    :param args: arguments to func
    :return:
    """
    func(*args)
    webbrowser.open(str(filepath))