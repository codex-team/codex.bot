import json
import random
import string

from ..lib.logging import Logging
import logging


class API:

    def __init__(self, broker):

        self.logging = Logging()
        self.db = broker.core.db
        self.broker = broker

        # Methods list (command => processor)
        self.methods = {
            'initialize plugin': self.initialize_plugin,
            'register commands': self.register_commands
        }
        # List of registered commands
        self.commands = {
            # Key is command name, value is tuple(description, module name)
            '/help': ('Show help', 'core')
        }
        # Generate list of modules (self.modules)
        self.modules = {}
        self.modules_token = {}
        self.load_modules()

    def load_modules(self):
        """
        Load modules dictionary from DB into self.modules as dict('hash' => JSON))
        :return:
        """
        modules_list = self.db.find('plugins', {})
        for module in modules_list:
            self.modules[module['plugin']] = module
            self.modules_token[module['token']] = module

    @staticmethod
    def generate_token(size=8, chars=string.ascii_uppercase + string.digits):
        """
        Generate unique string
        :param size: size in symbols
        :param chars: letters used
        :return: string token
        """
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    def send_message(self, code, message, plugin_data):
        """
        Pack message with result code into json string and send to brocker.send
        :param code: status code
        :param message: message
        :param plugin_data: dictionary with 'queue' and 'host' parameters of the destination queue
        :return:
        """
        message = json.dumps({
            'code': code,
            'message': message
        })
        return self.broker.send(message, plugin_data['queue'], host=plugin_data['host'])

    def process(self, data):
        """
        Process message with corresponding proccessor from self.methods by key in 'command' field
        :param data: dictionary with 'command', 'plugin' and 'payload' keys
        :return:
        """
        data = json.loads(data)
        yield from self.methods[data['command']](data['plugin'], data['payload'])


    #--# Callbacks #--#

    def initialize_plugin(self, plugin_name, plugin_data):
        """
        Initialize module.
        Return unique hashcode ID if the module in registered successfully.
        Return error code and message if module has already been registered.
        :param plugin_name:
        :param plugin_data: dict
            'plugin':       plugin name,
            'queue':        queue name,
            'host':         plugin host address,
            'port':         plugin port,
            'description':  plugin description in messenger
        :return:
        """
        try:
            plugin = self.db.find_one('plugins', {'plugin': plugin_data['plugin'], 'host': plugin_data['host']})
            if plugin:
                yield from self.send_message(500, 'Plugin {} is already registered'.format(plugin_name), plugin_data)
            else:
                plugin_data['token'] = API.generate_token()
                self.db.insert('plugins', plugin_data)
                yield from self.send_message(200, 'Plugin {} has been successfully registered'.format(plugin_name), plugin_data)

        except Exception as e:
            yield from self.send_message(308, 'Error', plugin_data)
            logging.error(e)
        else:
            logging.debug("Plugin {} initialized".format(plugin_name))

    def register_commands(self, plugin_name, plugin_data):
        """
        Register list of commands as belongings to the module with plugin_name
        :param plugin_name: module name string
        :param plugin_data: list of commands
            [
                'description':      command description for messenger
                'name':             command name
            ]
        :return:
        """
        try:
            commands_len = len(plugin_data)
            deny = []
            for command in plugin_data:
                name, description = command
                if not name in self.commands.keys():
                    self.commands[name] = (description, plugin_name)
                    self.db.insert('commands', {
                        'name': name,
                        'description': description,
                        'module': plugin_name,
                        'token': self.modules[plugin_name]['token']
                    })
                else:
                    deny.append(name)

        except Exception as e:
            yield from self.send_message(308, 'Error', plugin_data)
            logging.error(e)
        else:
            logging.debug("Plugin {} registered {} commands".format(plugin_name, commands_len - len(deny)))