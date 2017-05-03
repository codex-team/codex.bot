import asyncio
import importlib
import os
from aiohttp import web
import logging

from api.api import Api
from lib.rabbitmq import init_receiver_v3, send_message_v3
from lib.logging import Logging


class Core:

    def __init__(self):
        self.modules = {}

        self.logging = Logging()
        self.event_loop = asyncio.get_event_loop()
        self.api = Api(self)
        self.init_server()
        self.init_queue()
        self.init_modules()
        web.run_app(self.server, host='127.0.0.1', port=1337)

    def init_queue(self):
        logging.debug("Initiate event loop.")
        self.event_loop.run_until_complete(init_receiver_v3(self.api.callback, "core"))

    def init_server(self):
        self.server = web.Application(loop=self.event_loop)

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

    def send(self, message, queue_name, host='localhost'):
        yield from send_message_v3(message, queue_name)


# TODO1: static methods
# TODO2: logging setup

core = Core()
