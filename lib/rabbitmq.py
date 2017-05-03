import asyncio
import aioamqp
import logging
import pika

# This file will be copied to every module by bash script during initial setup.

def init_receiver(callback, queue_name, host='localhost'):
    """
    Initialize receiver for rabbitmq queue.

    :param callback: Callback for incoming message processing.
    :param queue_name: Name of queue.
    :param host: Rabbitmq host. Default='localhost'.
    :return: ! Blocking thread
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    logging.debug(' [*] Queue {} declared.'.format(queue_name))
    channel.start_consuming()


def send_message(data, queue_name, host='localhost'):
    """
    Send message to specific queue. Connection will be opened and then closed.
    :param data: Data to send.
    :param queue_name: Name of queue.
    :param host: Rabbitmq host. Default='localhost'.
    :return: None.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=data)
    logging.debug(" [x] Sent {} to {}".format(data, queue_name))
    connection.close()


@asyncio.coroutine
def init_receiver_v3(callback, queue_name, host='localhost'):
    transport, protocol = yield from aioamqp.connect()
    channel = yield from protocol.channel()
    yield from channel.queue_declare(queue_name=queue_name, passive=False, auto_delete=True)
    yield from channel.basic_consume(callback, queue_name=queue_name)


@asyncio.coroutine
def send_message_v3(data, queue_name, host='localhost'):
    transport, protocol = yield from aioamqp.connect()
    channel = yield from protocol.channel()

    yield from channel.queue_declare(queue_name=queue_name, passive=False, auto_delete=True)

    yield from channel.basic_publish(
        payload=data,
        exchange_name='',
        routing_key=queue_name
    )

    yield from protocol.close()
    transport.close()


@asyncio.coroutine
def delete_queue(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_delete(queue=queue_name)
    connection.close()
