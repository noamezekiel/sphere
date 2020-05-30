sphere.mq\_drivers package
==========================
How to add a new message queue Driver?
To add a new message queue Driver, named ``mydriver``, add a file in this package named ``mydriver_driver.py``.
In that file implement the following methods:

.. method:: produce(host, port, message, sector, sector_type, topic=None):
    Produces a message to queue, on the specified sector.
    If the sector type is `fanout` all subscribers of that sector will receive the message.
    If the sector type is `direct` only subscribers of that specified topic will receive the message.
    
    Note: If the sector type is `fanout` no topic is expected.

    :param host: The message queue host address
    :type host: str
    :param port: The message queue port number
    :type port: int
    :param message: The message to produce
    :type message: str
    :param sector: The sector of the message
    :type sector: str
    :param sector_type: The type of the sector, can be `fanout` or `direct`
    :type sector_type: str
    :param topic: The topic of the message, defaults to None
    :type topic: str

.. method:: consume(host, port, on_message, sector, sector_type, topics):
    Subscribe to the specifies sector and preform a `on_message` on the messages.
    If the sector type is `fanout` the consumer will receive the message regardless of the topic.
    If the sector type is `direct` the consumer will receive the message only if the topic match.

    Note: The on_message function expects input of the form (topic, message).

    :param host: The message queue host address
    :type host: str
    :param port: The message queue port number
    :type port: int
    :param on_message: The function to preform on the message
    :type message: function
    :param sector: The sector of the message
    :type sector: str
    :param sector_type: The type of the sector, can be `fanout` or `direct`
    :type sector_type: str
    :param topics: The topics that will be consumed
    :type topic: list

Submodules
----------

sphere.mq\_drivers.rabbitmq\_driver module
------------------------------------------

A rabbitmq Driver.
