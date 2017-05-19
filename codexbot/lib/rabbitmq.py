import aioamqp

# This file will be copied to every module by bash script during initial setup.

async def init_receiver(callback, queue_name, host='localhost'):
    transport, protocol = await aioamqp.connect()
    channel = await protocol.channel()
    await channel.queue_declare(queue_name=queue_name, passive=False, auto_delete=True)
    await channel.basic_consume(callback, queue_name=queue_name)


async def add_message_to_queue(data, queue_name, host='localhost'):
    transport, protocol = await aioamqp.connect()
    channel = await protocol.channel()

    await channel.queue_declare(queue_name=queue_name, passive=False, auto_delete=True)

    await channel.basic_publish(
        payload=data,
        exchange_name='',
        routing_key=queue_name
    )

    await protocol.close()
    transport.close()