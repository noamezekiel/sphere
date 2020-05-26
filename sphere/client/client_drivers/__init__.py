import os
import pathlib
import sys
from sphere.utils import load_drivers


root = pathlib.Path(os.path.dirname(__file__))
drivers = load_drivers(root)
sys.modules[__name__] = drivers