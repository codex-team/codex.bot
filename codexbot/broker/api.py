import json
import random
import string

from ..lib.logging import Logging
import logging


class API:

    def __init__(self, broker):
        self.methods = {
            'initialize plugin': self.initialize_plugin
        }
        self.logging = Logging()
        self.broker = broker
        self.db = broker.core.db

    def generate_token(self, size=8, chars=string.ascii_uppercase + string.digits):
        """
        Generate unique string for using as GitHub callback URI (route)
        :param size: size in symbols
        :param chars: letters used
        :return: string token
        """
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    def send_message(self, code, message, plugin_data):
        message = json.dumps({
            'code': code,
            'message': message
        })
        return self.broker.send(message, plugin_data['queue'], host=plugin_data['host'])

    def process(self, data):
        data = json.loads(data)
        yield from self.methods[data['command']](data['plugin'], data['payload'])

    def initialize_plugin(self, plugin_name, plugin_data):
        """

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
                plugin_data['token'] = self.generate_token()
                self.db.insert('plugins', plugin_data)
                yield from self.send_message(200, 'Plugin {} has been successfully registered'.format(plugin_name), plugin_data)

        except Exception as e:
            yield from self.send_message(308, 'Error', plugin_data)
            logging.error(e)
        else:
            logging.debug("Plugin {} initialized".format(plugin_name))