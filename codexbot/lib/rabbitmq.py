import aio_pika

async def init_receiver(callback, queue_name, host='localhost'):
    connection = await aio_pika.connect_robust(host=host)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.consume(callback)


async def add_message_to_queue(data, queue_name, host='localhost'):
    connection = await aio_pika.connect_robust(host=host)
    channel = await connection.channel()
    message = aio_pika.Message(data.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT)
    await channel.default_exchange.publish(message, routing_key=queue_name)
    await connection.close()
