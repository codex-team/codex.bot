import asyncio
import aioamqp
import logging
import pika

# This file will be copied to every module by bash script during initial setup.

@asyncio.coroutine
def init_receiver(callback, queue_name, host='localhost'):
    transport, protocol = yield from aioamqp.connect()
    channel = yield from protocol.channel()
    yield from channel.queue_declare(queue_name=queue_name, passive=False, auto_delete=True)
    yield from channel.basic_consume(callback, queue_name=queue_name)


@asyncio.coroutine
def add_message_to_queue(data, queue_name, host='localhost'):
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
