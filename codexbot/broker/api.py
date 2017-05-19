import json
import random
import string

from ..lib.logging import Logging
import logging


class API:

    APPS_COLLECTION_NAME = 'apps'
    COMMANDS_COLLECTION_NAME = 'commands'

    def __init__(self, broker):

        self.logging = Logging()
        self.db = broker.core.db
        self.broker = broker

        # Methods list (command => processor)
        self.methods = {
            'initialize app': self.initialize_app,
            'register commands': self.register_commands,
            'send to service': self.send_to_service
        }
        # List of registered commands
        self.commands = {
            # Key is command name, value is tuple(description, application name)
            '/help': ('Show help', 'core')
        }
        # Generate list of applications (self.apps)
        self.apps = {}
        self.load_apps()

    def load_apps(self):
        """
        Load applications dictionary from DB into self.apps as dict('hash' => JSON))
        :return:
        """
        apps_list = self.db.find(API.APPS_COLLECTION_NAME, {})
        for app in apps_list:
            self.load_app(app)
        logging.debug(self.apps)

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

    @staticmethod
    def generate_app_token(size=8, chars=string.ascii_uppercase + string.digits):
        """
        Generate unique string
        Application will use this token for authentication
        :param size: size in symbols
        :param chars: letters used
        :return: string token
        """
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    def send_message(self, code, message, app_data):
        """
        Pack message with result code into JSON string and send to add_to_app_queue
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


    #--# Callbacks #--#

    async def initialize_app(self, app_name, app_data):
        """
        Initialize application.
        Responds with app_token if application was successfully registered.
        Responds with error (code and message) if application has been already registered.
        :param app_name:
        :param app_data: dict
            'name':         application name,
            'queue':        queue name,
            'host':         application host address,
            'port':         application port,
            'description':  application description in messenger
        :return:
        """
        try:
            app = self.db.find_one(API.APPS_COLLECTION_NAME, {'name': app_data['name'], 'host': app_data['host']})
            if app:
                await self.send_message(
                    self.broker.WRONG,
                    'Application {} is already registered'.format(app_name),
                    app_data
                )
            else:
                app_data['token'] = API.generate_app_token()
                self.db.insert(API.APPS_COLLECTION_NAME, app_data)
                self.load_app(app_data)
                await self.send_message(
                    self.broker.OK,
                    'Application {} has been successfully registered'.format(app_name),
                    app_data
                )
                await self.send_command('set token', {
                        'token': app_data['token']
                    }, app_data
                )

        except Exception as e:
            await self.send_message(self.broker.ERROR, 'Error', app_data)
            logging.error(e)
        else:
            logging.debug("Application {} initialized".format(app_name))

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
                   }
                ):
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

        chat = self.db.find_one('chats', {hash: chat_hash})

        if not chat:
            await self.send_message(self.broker.WRONG, 'Error', self.apps[app_token])
            return

        self.broker.core.services[chat['service']].add_to_app_queue(chat['id'], message_payload)