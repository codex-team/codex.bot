import asyncio
import importlib
import logging
import os

from api.api import Api
from lib.rabbitmq import init_receiver_v3, send_message_v3
from lib.server import Server


class Core:

    def __init__(self):
        self.modules = {}

        self.init_logging()
        self.event_loop = asyncio.get_event_loop()
        self.init_api()
        self.init_server()
        self.init_queue()
        self.init_modules()
        self.server.start()

    def init_logging(self):
        logging.getLogger('asyncio').setLevel(logging.DEBUG)
        format_str = "[%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=format_str)
        logging.debug("Logging initiated.")

    def init_queue(self):
        logging.debug("Initiate queue and loop.")
        self.api.start()

    def init_server(self):
        self.server = Server(self.event_loop)

    def init_api(self):
        self.api = Api(self, self.event_loop)

    def init_modules(self):
        """
        Collects core modules from subdirectories
        :return:
        """
        for module in filter(lambda x: not x.startswith('__'), os.listdir('includes')):
            try:
                current_module = importlib.import_module("includes.{}".format(module))

                name = current_module.module_obj.__name__
                if name in self.modules:
                    raise Exception("Module {} is already registered.".format(name))

                self.modules[name] = current_module.module_obj
                current_module.module_obj.run(self.server, self.api)

            except Exception as e:
                logging.error(e)

        logging.debug("{} modules loaded.".format(len(self.modules)))


# TODO1: static methods
# TODO2: logging setup

core = Core()
