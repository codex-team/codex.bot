import asyncio
import importlib
import logging
import os

from codexbot.lib.logging import Logging
from codexbot.broker.broker import Broker
from codexbot.globalcfg import SERVER, HANDSHAKE_URL
from codexbot.lib.server import Server, http_response


class Core:

    def __init__(self):
        self.modules = {}

        self.logging = Logging()
        self.event_loop = asyncio.get_event_loop()
        self.init_broker()
        self.init_server()
        self.set_system_routes()
        self.init_queue()
        self.init_modules()
        self.server.start()

    def init_queue(self):
        self.logging.log("Initiate queue and loop.")
        self.broker.start()

    def init_server(self):
        self.server = Server(self.event_loop, SERVER['host'], SERVER['port'])

    def set_system_routes(self):
        """
        Specifies required core-routes
        :return:
        """

        routes = [
            ('POST', HANDSHAKE_URL, self.handshake_callback)
        ]
        self.server.set_routes(routes)

    @http_response
    def handshake_callback(self, text, post, json):
        """
        External tools handshake
        Uses to specify unique queue name for tool
        :param text:
        :param post:
        :param json:
        :return: queue name
        """
        tool = post["tool"]
        self.logging.log("Handshake request received from {} tool ".format(tool))

        # TODO provide name uniqueness
        queue_name_delegated = tool

        # TODO register queue for tool
        # self.broker.add_queue(queue_name_delegated)

        return queue_name_delegated

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

                # set routes for this module
                self.server.set_routes(current_module.module_obj.routes)

            except Exception as e:
                logging.error(e)

        self.logging.log("{} modules loaded.".format(len(self.modules)))
