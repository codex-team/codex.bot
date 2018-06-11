import random
import string
import gettext
import logging

from codexbot.systemapps.botmanager.apps import AppManager
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

        self.commands = {
            'myapps': self.app_manager.show_apps,
            'newapp': self.app_manager.add_app,
            'manager': self.bot_manager.help,
            'bots': self.bot_manager.show_bots,
            'addbot': self.bot_manager.add_bot,
            'delbot': self.bot_manager.del_bot,
            'addapp': self.bot_manager.add_app_to_bot
        }

    def process(self, chat_hash, command_data):
        self.commands[command_data['command']](chat_hash, command_data['payload'])

    @staticmethod
    def generate_app_token(size=8, chars=string.ascii_uppercase + string.digits):
        """
        Generate unique string
        Application will use this token for authentication
        :param size: size in symbols
        :param chars: letters used
        :return: string token
        """
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
