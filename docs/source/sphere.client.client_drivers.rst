sphere.client.client\_drivers package
=====================================
How to add a new client Driver?
To add a new client Driver, named ``mydriver``, add a file in this package named ``mydriver_driver.py``
In that file implement a class named ``Driver`` that supply the following methods:

.. method:: __init__(self, path):
    Constructor method.
    
    :param path: The path to the sample
    :type path: str

.. method::get_user(self):
    Returns the user of the sample.
    
    :return: The user of the sample
    :rtype: :class:`sphere.protocol.User` object

.. method:: snapshots(self):
    An iterator that iterates over the snapshots.
    
    Each yield is a object of type :class:`sphere.protocol.Snapshot` object 

Submodules
----------

sphere.client.client\_drivers.protobuf\_driver module
-----------------------------------------------------

A protobuf Driver.