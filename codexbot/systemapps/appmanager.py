import random
import string
import gettext
import logging

from codexbot.systemapps.botmanager.apps import AppManager
from codexbot.systemapps.botmanager.bot_app import BotAppLink
from codexbot.systemapps.botmanager.bots import BotManager


class Manager:

    def __init__(self, broker):

        gettext.translation('appmanager', 'i18n', ['ru']).install()

        self.core = broker.core
        self.broker = broker
        self.api = broker.api
        self.db = broker.core.db

        self.app_manager = AppManager(broker)
        self.bot_manager = BotManager(broker)
        self.bot_app_manager = BotAppLink(broker)

        self.commands = {
            'myapps': self.app_manager.show_apps,
            'newapp': self.app_manager.add_app,
            'manager': self.bot_manager.help,
            'bots': self.bot_manager.show_bots,
            'addbot': self.bot_manager.add_bot,
            'delbot': self.bot_manager.del_bot,
            'linkbot': self.bot_app_manager.link_bot,
            'botmenu': self.bot_manager.bot_menu,
            'applylink': self.bot_app_manager.apply_link,
            'unlink': self.bot_app_manager.unapply_link
        }

    def process(self, chat_hash, command_data):
        if command_data['command'] in self.commands:
            self.commands[command_data['command']](chat_hash, command_data['payload'])
        else:
            logging.error("Command not found: ", command_data)

