import logging
import pika

logging.getLogger('pika').setLevel(logging.ERROR)

def produce(host, port, message, sector, sector_type, topic=None):
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
