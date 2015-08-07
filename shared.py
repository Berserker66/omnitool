from version import Version
import appdirs
import os

__all__ = ("__version__", "appdata", "cachepath", "cache", "lang", "theme")

__version__ = Version(180102)
appdata = appdirs.user_config_dir('omnitool', "", roaming = True)
cachepath = os.path.join(appdata, "cache.dill")
#filled in by omnitool.py:
cache = None
lang = None
theme = None
exit_prog = None



if False:
    import Language.english as lang #IDE hook