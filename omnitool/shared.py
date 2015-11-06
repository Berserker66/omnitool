import sys
import os
from pathlib import Path

from appdirs import user_config_dir

from .version import Version

__all__ = ("__version__", "appdata", "cachepath", "cache", "lang", "theme")

__version__ = Version(180301)
appdata = user_config_dir('omnitool', "", roaming = True)
cachepath = os.path.join(appdata, "cache.dill")
#filled in by omnitool.py:
cache = None
lang = None
theme = None
exit_prog = None

if getattr(sys, 'frozen', False):
	datadir = Path(sys.executable).parent
else:
	datadir = Path(__file__).parent

if False:
    from .Language import english as lang #IDE hook
