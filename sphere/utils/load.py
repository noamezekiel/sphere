import importlib
import os
import sys


def load_drivers(root):
    drivers = {}
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if not path.name.endswith('_driver.py'):
            continue
        module = importlib.import_module(f'{root.name}.{path.stem}',package=root.name)
        drivers[path.name.rstrip('driver.py')[:-1]] = module
    return drivers

def load_parsers(root):
    parsers = {}
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if not path.name.startswith('parse_'):
            continue
        module = importlib.import_module(f'{root.name}.{path.stem}',package=root.name)
        if path.stem in module.__dict__:
            parsers[path.stem.lstrip('parse')[1:]] = module.__dict__[path.stem]
    return parsers