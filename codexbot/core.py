import asyncio
import importlib
import logging
import os
import gettext

from codexbot.lib.db import Db
from codexbot.lib.logging import Logging
from codexbot.broker.broker import Broker
from codexbot.globalcfg import SERVER, DB, I18N_LOCATION
from codexbot.lib.server import Server


class Core:

    def __init__(self):
        self.services = {}
        self.logging = Logging()
        self.init_i18n()
        self.overload_settings()
        self.event_loop = asyncio.get_event_loop()
        self.init_db()
        self.init_broker()
        self.init_server()
        self.init_services()
        self.init_queue()
        self.server.start()

    def overload_settings(self):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', help="local port")
        parser.add_argument('--port', help="local port")
        args = parser.parse_args()
        if args.host:
            SERVER['host'] = args.host
        if args.port:
            SERVER['port'] = int(args.port)

    # TODO создать отдельный модуль для подключения словарей к модулям
    #      но это не точно
    def init_i18n(self):
        gettext.translation('main', I18N_LOCATION, ['ru']).install()
        logging.debug("Initiate i18n.")

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
        logging.debug("Initiate DB.")
        self.db = Db(DB['name'], DB['host'], DB['port'])

    def init_services(self):
        """
        Collects core modules from subdirectories
        :return:
        """
        for service in filter(lambda x: not x.startswith('.') and not x.startswith('__'), os.listdir('codexbot/services')):
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
