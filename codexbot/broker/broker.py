import asyncio
import logging

from codexbot.lib.rabbitmq import add_message_to_queue, init_receiver
from .api import API


class Broker:

    OK = 200
    WRONG = 400
    ERROR = 500

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
        try:
            logging.debug(" [x] Received %r" % body)
            yield from self.api.process(body.decode("utf-8"))
        except Exception as e:
            logging.error("Broker callback error")
            logging.error(e)

    def send(self, message, queue_name, host='localhost'):
        """
        Send message to queue on the host
        :param message: message string
        :param queue_name: name of destination queue
        :param host: destination host address
        :return:
        """
        yield from add_message_to_queue(message, queue_name, host=host)

    def start(self):
        """
        Receive all messages from 'core' queue to self.callback
        :return:
        """
        self.event_loop.run_until_complete(init_receiver(self.callback, "core"))
