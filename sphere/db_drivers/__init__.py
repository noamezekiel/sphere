"""How to add a new database Driver?
To add a new databese Driver, named mydriver, add a file in this package named mydriver_driver.py
In that file implement a class named `Driver` that supply the following methods:

__init__(self, host, port):
    Constructor method.

    :param host: The database host address
    :type host: str
    :param port: The database port number
    :type port: int

def save(self, topic, data):
    Saves data of that topic.

    :param topic: The topic of the data
    :type topic: str
    :param data: The data
    :type data: :class:`object`

def get_users(self, user_id=None):
    Returns a list of all supported users. If user_id is mentioned, returns the specified user's details
    
    :param user_id: The id of the requested user, defaults to None
    :type user_id: int, optional
    :return: List of dictionaries that describes the user, or a single dictionary.
    :rtype: list, dictionary

def get_snapshots(self, user_id, snapshot_id=None):
    Returns the list of the specified user's snapshot. If snapshot_id is mentioned, returns the specified snapshot's.
    
    :param user_id: The id of the requested user
    :type user_id: int
    :param snapshot_id: The id of the requested snapshot
    :type snapshot_id: int, optional
    :return: List of dictionaries that describes the snapshots, or a single dictionary.
    :rtype: list, dictionary
"""
import os
import pathlib
import sys
from sphere.utils import load_drivers

root = pathlib.Path(os.path.dirname(__file__))
drivers = load_drivers(root)
sys.modules[__name__] = drivers