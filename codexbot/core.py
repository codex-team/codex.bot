import asyncio
import importlib
import logging
import os

from codexbot.lib.logging import Logging
from codexbot.broker.broker import Broker
from codexbot.globalcfg import SERVER
from codexbot.lib.server import Server


class Core:

    def __init__(self):
        self.modules = {}

        self.logging = Logging()
        self.event_loop = asyncio.get_event_loop()
        self.init_broker()
        self.init_server()
        self.init_queue()
        self.init_modules()
        self.server.start()

    def init_queue(self):
        logging.debug("Initiate queue and loop.")
        self.broker.start()

    def init_server(self):
        self.server = Server(self.event_loop, SERVER['host'], SERVER['port'])

    def init_broker(self):
        self.broker = Broker(self, self.event_loop)

    def init_modules(self):
        """
        Collects core modules from subdirectories
        :return:
        """
        for module in filter(lambda x: not x.startswith('__'), os.listdir('codexbot/services')):
            try:
                current_module = importlib.import_module("codexbot.services.{}".format(module))

                name = current_module.module_obj.__name__
                if name in self.modules:
                    raise Exception("Module {} is already registered.".format(name))

                self.modules[name] = current_module.module_obj

                current_module.module_obj.run(self.broker)

                # get routes for this module
                self.server.set_routes(current_module.module_obj.routes)

            except Exception as e:
                logging.error(e)

        logging.debug("{} modules loaded.".format(len(self.modules)))
