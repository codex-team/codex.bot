import json
import random
import string

from ..lib.logging import Logging
import logging


class API:
    APPS_COLLECTION_NAME = 'apps'
    BOTS_COLLECTION_NAME = 'bots'
    BOT_APP_LINKS_COLLECTION_NAME = 'bot_app_links'
    COMMANDS_COLLECTION_NAME = 'commands'
    PENDING_APPS_COLLECTION_NAME = 'pending_apps'

    def __init__(self, broker):

        self.logging = Logging()
        self.db = broker.core.db
        self.broker = broker

        # Methods list (command => processor)
        self.methods = {
            'register commands': self.register_commands,
            'send to service': self.send_to_service,
            'wait user answer': self.wait_user_answer
        }

        self.commands = {}

        # Generate list of applications (self.apps)
        self.apps = {}
        self.bots = {}
        self.load_apps()
        self.load_bots()

        self.pending_apps = {}
        self.load_pending_apps()

        self.load_commands()

    def load_commands(self):
        commands = self.db.find(API.COMMANDS_COLLECTION_NAME, {})
        for command in commands:
            self.commands[command['name']] = (command['description'], command['app_token'])

    def load_apps(self):
        """
        Load applications dictionary from DB into self.apps as dict('hash' => JSON))
        :return:
        """
        apps_list = self.db.find(API.APPS_COLLECTION_NAME, {})
        for app in apps_list:
            self.load_app(app)

    def load_bots(self):
        bots_list = self.db.find(API.BOTS_COLLECTION_NAME, {})
        for bot in bots_list:
            self.load_bot(bot)

    def load_bot(self, bot_data):
        bots_links = self.db.find(API.BOT_APP_LINKS_COLLECTION_NAME, {'bot_name': bot_data['name']})
        self.bots[bot_data['bot_id']] = {'data': bot_data, 'apps': set([link['app_name'] for link in bots_links])}

    def load_app(self, app_data):
        """
        Adds application to the local self.apps cache
        :param app_data: dict
            'token':        application token,
            'name':         application name,
            'queue':        queue name,
            'host':         application host address,
            'port':         application port,
            'description':  application description
        :return:
        """
        if not app_data['token'] in self.apps:
            self.apps[app_data['token']] = app_data

    def set_pending(self, app):
        """
        Add app to the local self.pending_apps cache
        
        :param pending_data:
            - user - user hash
            - chat - chat hash
            - app - app token
        :return: 
        """
        key = self.get_pending_app_key(app)
        self.pending_apps[key] = app

    def reset_pending(self, app):
        """
        Remove app from db and from cache
        :param app:
        :return: 
        """

        self.db.remove(API.PENDING_APPS_COLLECTION_NAME, app)

        key = self.get_pending_app_key(app)
        self.pending_apps.pop(key, None)

    def load_pending_apps(self):
        """
        Load stored pending_apps
        :return: 
        """

        apps = self.db.find(API.PENDING_APPS_COLLECTION_NAME, {})
        for app in apps:
            self.set_pending(app)

    def send_message(self, code, message, app_data):
        """
        Pack message with result code into JSON string and send to broker.add_to_app_queue
        :param code: status code
        :param message: message
        :param app_data: dictionary with 'queue' and 'host' parameters of the destination queue
        :return:
        """
        payload = {
            'code': code,
            'message': message
        }
        return self.send_command('show message', payload, app_data)

    def send_command(self, command, payload, app_data):
        message = json.dumps({
            'command': command,
            'payload': payload
        })
        logging.debug(" [+] Send {}".format(message))
        return self.broker.add_to_app_queue(message, app_data['queue'], host=app_data['host'])

    async def process(self, message_data):
        """
        Process message with corresponding proccessor from self.methods by key in 'command' field
        :param message_data: dictionary with 'command', (app) 'token' and 'payload' keys

        !!! Except 1 case:
        For processing 'initialize app' command, we send app-name as 'token'

        :return:
        """
        message_data = json.loads(message_data)
        app_token = message_data['token']
        await self.methods[message_data['command']](app_token, message_data['payload'])

    # --# Callbacks #--#



    async def register_commands(self, app_token, commands):
        """
        Register list of commands as belongings to the application with app_token
        :param app_token: application token string
        :param commands: list of commands
            [
                'description':      command description for messenger
                'name':             command name
            ]
        :return:
        """

        if app_token not in self.apps:
            logging.error('Cant register commands: application with token {} not loaded.'.format(app_token))
            return

        app_name = self.apps[app_token]['name']

        try:
            commands_len = len(commands)
            deny = []
            for command in commands:
                name, description = command
                if not name in self.commands.keys() and \
                   not self.db.find_one(API.COMMANDS_COLLECTION_NAME, {
                       'name': name
                   }):
                    self.commands[name] = (description, app_token)
                    self.db.insert(API.COMMANDS_COLLECTION_NAME, {
                        'name': name,
                        'description': description,
                        'app_name': app_name,
                        'app_token': app_token
                    })
                else:
                    deny.append(name)

        except Exception as e:
            await self.send_message(self.broker.ERROR, 'Error', self.apps[app_token])
            logging.error(e)
        else:
            logging.debug("Application {} registered {} commands".format(app_name, commands_len - len(deny)))
            await self.send_message(
                self.broker.OK,
                "Application {} registered {} commands".format(app_name, commands_len - len(deny)),
                self.apps[app_token]
            )

    async def send_to_service(self, app_token, message_payload):
        """
        Find service by chat_hash and pass there message_payload:
        :param message_payload:
            - chat_hash  - chat hash
            - text       - message text
            - parse_mode - message parse mode type
            - photo      - photo to send (you shouldn't pass text param if you want to send photo)
            - caption    - caption for photo
            For markups see https://core.telegram.org/bots/api#replykeyboardmarkup
            - markup:
                - keyboard
                - inline_keyboard
                - remove_keyboard
                - force_reply
        
        :param app_token: 
        :return: 
        """
        chat_hash = message_payload['chat_hash']

        chat = self.db.find_one('chats', {'hash': chat_hash})

        if not chat:
            await self.send_message(self.broker.WRONG, 'Error', self.apps[app_token])
            return

        self.broker.core.services[chat['service']].send(chat['id'], message_payload)

    async def wait_user_answer(self, app_token, payload):
        """
        Add pending state for payload['user'] in payload['chat']
        
        :param app_token: 
        :param payload:
        :return: 
        """

        if 'chat' not in payload or 'user' not in payload:
            await self.send_message(self.broker.WRONG, 'Error', self.apps[app_token])
            return

        self.db.update(API.PENDING_APPS_COLLECTION_NAME,
                       {
                           'chat': payload['chat'],
                           'user': payload['user']
                       },
                       {
                           'chat': payload['chat'],
                           'user': payload['user'],
                           'app': app_token
                       },
                       True  # upsert
                       )

        payload['app'] = app_token
        self.set_pending(payload)

        if len(payload['prompt']):
            chat = self.db.find_one('chats', {'hash': payload['chat']})
            self.broker.core.services[chat['service']].send(chat['id'], {'text': payload['prompt']})

        await self.send_message(self.broker.OK, 'Pending state for app registered', self.apps[app_token])

    @staticmethod
    def get_pending_app_key(app):
        return app['user'] + ':' + app['chat']
