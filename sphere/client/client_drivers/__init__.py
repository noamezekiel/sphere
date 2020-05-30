""" How to add a new client Driver?
To add a new client Driver, named mydriver, add a file in this package named mydriver_driver.py
In that file implement a class named `Driver` that supply the following methods:

__init__(self, path):
    Constructor method.
    
    :param path: The path to the sample
    :type path: str

get_user(self):
    Returns the user of the sample.
    
    :return: The user of the sample
    :rtype: :class:`sphere.protocol.User` object

def snapshots(self):
    An iterator that iterates over the snapshots.
    
    Each yield is a object of type :class:`sphere.protocol.Snapshot` object 
"""
import os
import pathlib
import sys
from sphere.utils import load_drivers


root = pathlib.Path(os.path.dirname(__file__))
drivers = load_drivers(root)
sys.modules[__name__] = drivers