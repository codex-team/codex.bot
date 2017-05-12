import json
from ..lib.logging import Logging
import logging


class API:

    def __init__(self):
        self.methods = {
            'initialize plugin': self.initialize_plugin
        }
        self.logging = Logging()

    def process(self, data):
        data = json.loads(data)
        self.methods[data['command']](data['plugin'], data['payload'])

    def initialize_plugin(self, plugin_name, plugin_data):
        logging.debug("Plugin {} initialized".format(plugin_name))