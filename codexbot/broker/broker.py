import json
import logging
import random
import string

from aio_pika import IncomingMessage

from codexbot.globalcfg import RABBITMQ
from codexbot.lib.rabbitmq import add_message_to_queue, init_receiver
from codexbot.systemapps.appmanager import Manager
from codexbot.systemapps.systemcommands import SystemCommand
from .api import API


class Broker:

    OK = 200
    WRONG = 400
    ERROR = 500

    system_commands = {}

    def __init__(self, core, event_loop):
        logging.info("Broker started ;)")
        self.core = core
        self.event_loop = event_loop
        self.api = API(self)
        self.app_manager = Manager(self)
        self.system_commands = SystemCommand(self.api, self.core)

    async def callback(self, message: IncomingMessage):
        """
        Process all messages from 'core' queue by self.API object
        :param channel:
        :param body:
        :param envelope:
        :param properties:
        :return:
        """
        with message.process():
            try:
                logging.debug(" [x] Received %r" % message.body)
                await self.api.process(message.body.decode("utf-8"))
                message.ack()
            except Exception as e:
                logging.error("Broker callback error")
                logging.error(e)

    async def commands_to_app(self, message_data):
        """
        Find application by command and send there message data.
        
        :param message_data: 
        :return: 
        """
        chat_hash = self.get_chat_hash(message_data)
        user_hash = self.get_user_hash(message_data)
        bot_id = message_data.get('bot', None)

        key = API.get_pending_app_key({'user': user_hash, 'chat': chat_hash})

        # If there are pending app for user in current chat, pass message to app
        if key in self.api.pending_apps:

            app = self.api.apps[self.api.pending_apps[key]['app']]

            payload = {
                'text': message_data['text'],
                'chat': chat_hash,
                'user': user_hash,
                'bot': bot_id
            }

            self.api.reset_pending(self.api.pending_apps[key])
            await self.api.send_command('user answer', payload, app)
            return

        bot_data = self.api.bots.get(int(bot_id), None) if bot_id else None

        for incoming_cmd in message_data['commands']:

            if bot_id is not None and bot_data is not None and bot_data['data']['name'] in incoming_cmd['command']:
                incoming_cmd['command'], _ = incoming_cmd['command'].split('@', 1)

            if incoming_cmd['command'] in self.app_manager.commands:
                if bot_id is None:
                    await self.app_manager.process(chat_hash, incoming_cmd)
                continue

            # Handle core-predefined command
            if incoming_cmd['command'] in self.system_commands.commands:
                return await self.system_commands.commands[incoming_cmd['command']](chat_hash, incoming_cmd['payload'], bot_id)

            command_data = self.api.commands.get(incoming_cmd['command'])

            if not command_data:
                continue

            app = self.api.apps[command_data[1]]

            if bot_id is not None:
                # check if bot is linked to the app
                if app['name'] not in self.api.bots[int(bot_id)]['apps']:
                    continue

            message = json.dumps({
                'command': 'service callback',
                'payload': {
                    'command': incoming_cmd['command'],
                    'params': incoming_cmd['payload'],
                    'chat': chat_hash,
                    'user': user_hash,
                    'bot': message_data.get('bot', None)
                },
            })

            await self.add_to_app_queue(message, app['queue'], app['host'])

    async def callback_query_to_app(self, query):
        (app_token, data) = query['data'].split(' ', 1)

        chat_hash = self.get_chat_hash(query)
        user_hash = self.get_user_hash(query)

        if app_token.startswith('core_'):
            await self.app_manager.process(chat_hash, {'command': app_token[5:], 'payload': data})
            return

        app = self.api.apps[app_token]

        payload = {
            'data': data,
            'chat': chat_hash,
            'user': user_hash,
            'bot': query.get('bot', None)
        }

        await self.api.send_command('callback query', payload, app)

    async def add_to_app_queue(self, message, queue_name, host):
        """
        Send message to app queue on the host 
        :param message: message string
        :param queue_name: name of destination queue
        :param host: destination host address
        :return:
        """
        logging.debug('Now i pass message {} to the {} queue'.format(message, queue_name))
        await add_message_to_queue(message, queue_name, host)

    def start(self):
        """
        Receive all messages from 'core' queue to self.callback
        :return:
        """
        self.event_loop.run_until_complete(init_receiver(self.callback, "core", RABBITMQ['host']))

    def get_chat_hash(self, message_data):
        """
        Search chat_hash in db. If chat_hash not found, generate new and insert it to db
        
        :param message_data: 
        :return: 
        """

        chat = self.core.db.find_one('chats', {'id': message_data['chat']['id']})

        if not chat:
            chat_hash = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

            self.core.db.insert(
                'chats',
                {
                    'id': message_data['chat']['id'],
                    'type': message_data['chat']['type'],
                    'hash': chat_hash,
                    'service': message_data['service']
                }
            )
        else:
            chat_hash = chat['hash']

        return chat_hash

    def get_user_hash(self, message_data):
        """
        Search user_hash in db. If hash not found, generate new and insert it to db

        :param message_data: 
        :return: 
        """

        user = self.core.db.find_one('users', {'id': message_data['user']['id']})

        if not user:
            user_hash = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

            self.core.db.insert(
                'users',
                {
                    'id': message_data['user']['id'],
                    'hash': user_hash,
                    'username': message_data['user']['username'],
                    'lang': message_data['user']['lang'],
                    'service': message_data['service']
                }
            )
        else:
            user_hash = user['hash']

        return user_hash