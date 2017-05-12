import asyncio
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
        """
        Process all messages from 'core' queue by self.API object
        :param channel:
        :param body:
        :param envelope:
        :param properties:
        :return:
        """
        logging.debug(" [x] Received %r" % body)
        yield from self.api.process(body.decode("utf-8"))

    def send(self, message, queue_name, host='localhost'):
        """
        Send message to queue on the host
        :param message: message string
        :param queue_name: name of destination queue
        :param host: destination host address
        :return:
        """
        yield from send_message_v3(message, queue_name, host=host)

    def start(self):
        """
        Receive all messages from 'core' queue to self.callback
        :return:
        """
        self.event_loop.run_until_complete(init_receiver_v3(self.callback, "core"))
