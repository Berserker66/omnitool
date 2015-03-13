def run_flat():
    launch_plugin(('flatworld', 'Flatworld', 'generator'))


def run_plat():
    launch_plugin(('planetoids', 'Planetoids', 'generator'))


def run_arena():
    launch_plugin(('arena', 'Dungeon Arena', 'generator'))


def run_world():
    launch_plugin(('worldify', 'Worldify', 'generator'))


from omnitool import launch_plugin as base


def launch_plugin(*args, **kwargs): base(*args, **kwargs)
