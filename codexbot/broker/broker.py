import asyncio
import json
import logging

from codexbot.lib.rabbitmq import send_message_v3, init_receiver_v3


class Broker:

    def __init__(self, core, event_loop):
        logging.info("Broker started ;)")
        self.core = core
        self.event_loop = event_loop

    @asyncio.coroutine
    def callback(self, channel, body, envelope, properties):
        print(" [x] Received %r" % body)
        try:
            message = json.loads(body)
            command = message['cmd']
            payload = message['payload']
            version = message['broker']
            incoming_queue = message['queue']

            if not version == "v1.1":
                logging.debug("Try to send")
                yield from self.send("{'result': 'Version invalid'}", incoming_queue)

            # TODO: Parse message
            """
            1. Register module
            2. Register commands from messengers
            """

        except Exception as e:
            logging.error(e)

    def send(self, message, queue_name, host='localhost'):
        yield from send_message_v3(message, queue_name)

    def start(self):
        self.event_loop.run_until_complete(init_receiver_v3(self.callback, "core"))

    # def add_queue(self, queue_name):
    #     self.event_loop.run_until_complete(init_receiver_v3(self.callback, queue_name))
    #     logging.debug("New queue {} added ".format(queue_name))
