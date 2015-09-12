import os
import sys
from importlib import import_module

def load_language(name : str):
    """Load a language module by name."""
    if os.path.isfile("custom.py"):
        sys.path.append(".")
        import custom as lang
        sys.path.remove(".")
    else:
        lang = import_module('.Language.' + name, package='omnitool')
    if name != "english":
        englang = import_module('.Language.english', package='omnitool')
        for entry in check(englang, lang):
            print("Warning:", lang.__name__, "misses", entry, ". Defaulting to english.")
            setattr(lang, entry, getattr(englang, entry))
    return lang

def check(base, checkee):
    """check the checkee language for any missing entries, using base as reference.
    Return names of all missing entries."""
    base = dir(base)
    base.remove("__author__")
    base = set(base)
    return base-set(dir(checkee))
