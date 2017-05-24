import asyncio
import importlib
import logging
import os

from codexbot.lib.db import Db
from codexbot.lib.logging import Logging
from codexbot.broker.broker import Broker
from codexbot.globalcfg import SERVER, DB
from codexbot.lib.server import Server


class Core:

    def __init__(self):
        self.services = {}

        self.logging = Logging()
        self.event_loop = asyncio.get_event_loop()
        self.init_db()
        self.init_broker()
        self.init_server()
        self.init_services()
        self.init_queue()
        self.server.start()

    def init_queue(self):
        logging.debug("Initiate queue and loop.")
        self.broker.start()

    def init_server(self):
        self.server = Server(self.event_loop, SERVER['host'], SERVER['port'])

    def init_broker(self):
        self.broker = Broker(self, self.event_loop)

    def init_db(self):
        """
        Initialize self.db object with 'default' database name
        :return:
        """
        logging.debug("Initiate DB")
        self.db = Db(DB['name'], DB['host'], DB['port'])

    def init_services(self):
        """
        Collects core modules from subdirectories
        :return:
        """
        for service in filter(lambda x: not x.startswith('__'), os.listdir('codexbot/services')):
            try:
                current_service = importlib.import_module("codexbot.services.{}".format(service))

                name = current_service.service_obj.__name__
                if name in self.services:
                    raise Exception("Service {} is already registered.".format(name))

                self.services[name] = current_service.service_obj

                current_service.service_obj.run(self.broker)

                # set routes for this service
                self.server.set_routes(current_service.service_obj.routes)

            except Exception as e:
                logging.error(e)

        logging.debug("{} services loaded.".format(len(self.services)))
