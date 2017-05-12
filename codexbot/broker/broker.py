import asyncio
import json
import logging

from codexbot.lib.rabbitmq import send_message_v3, init_receiver_v3
from .api import API

class Broker:

    def __init__(self, core, event_loop):
        logging.info("Broker started ;)")
        self.core = core
        self.event_loop = event_loop
        self.api = API(self)

    @asyncio.coroutine
    def callback(self, channel, body, envelope, properties):
        print(" [x] Received %r" % body)
        yield from self.api.process(body.decode("utf-8"))

    def send(self, message, queue_name, host='localhost'):
        yield from send_message_v3(message, queue_name, host=host)

    def start(self):
        self.event_loop.run_until_complete(init_receiver_v3(self.callback, "core"))
