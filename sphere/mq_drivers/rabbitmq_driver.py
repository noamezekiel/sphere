import logging
import pika

logging.getLogger('pika').setLevel(logging.ERROR)

def produce(host, port, message, sector, sector_type, topic=None):
    """
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
    """
    params = pika.ConnectionParameters(host=host,
                                       port=port,
                                       heartbeat=600,
                                       blocked_connection_timeout=300)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=sector, exchange_type=sector_type)
    channel.basic_publish(
        exchange=sector,
        routing_key=topic or '',
        body=message)
    connection.close()

def consume(host, port, on_message, sector, sector_type, topics):
    """
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
    """
    params = pika.ConnectionParameters(host=host,
                                       port=port,
                                       heartbeat=600,
                                       blocked_connection_timeout=300)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=sector, exchange_type=sector_type)
    # binding early to prevent late-binding 
    def create_callback(topic):
        def callback(ch, method, properties, body):
            on_message(topic, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        return callback
    # a queue for each topic
    for topic in topics:
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=sector,
                           queue=queue_name,
                           routing_key=topic)
        channel.basic_consume(
            queue=queue_name, 
            on_message_callback=create_callback(topic))
    channel.start_consuming()
    connection.close()
