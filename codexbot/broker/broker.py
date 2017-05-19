import asyncio
import json
import logging
import random
import string

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

    def service_handler(self, message_data):

        chat = self.core.db.find_one('chats', {'id': message_data['chat']})

        if not chat:
            chat_hash = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
            self.core.db.insert('chats', {'id': message_data['chat'], 'hash': chat_hash, 'service': message_data['service']})
        else:
            chat_hash = chat['hash']

        for incoming_cmd in message_data['commands']:

            app_cmd = self.core.db.find_one(self.api.COMMANDS_COLLECTION_NAME, {
                'name': incoming_cmd['command']
            })

            if not app_cmd:
                return

            app = self.core.db.find_one(self.api.APPS_COLLECTION_NAME, {
                'name': app_cmd['app_name']
            })

            message = json.dumps({
                'command': 'service callback',
                'payload': {
                    'command': incoming_cmd['command'],
                    'params': incoming_cmd['payload'],
                    'chat': chat_hash
                }
            })

            self.send(message, app['queue'], app['host'])




    def send(self, message, queue_name, host='localhost'):
        """
        Send message to queue on the host
        :param message: message string
        :param queue_name: name of destination queue
        :param host: destination host address
        :return:
        """
        self.event_loop.run_until_complete(add_message_to_queue(message, queue_name, host=host))

    def start(self):
        """
        Receive all messages from 'core' queue to self.callback
        :return:
        """
        self.event_loop.run_until_complete(init_receiver(self.callback, "core"))
