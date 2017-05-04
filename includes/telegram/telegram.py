import logging

from lib.server import http_response
from .config import TelegramConfig

class Telegram:

    __name__ = "Telegram"

    def __init__(self):
        self.config = TelegramConfig()
        logging.debug("Telegram module initiated.")

    @http_response
    def telegram_callback(self, text, post, json):
        """
        Process messages from telegram bot
        :return:
        """
        logging.info("Got telegram callback {} {} {}".format(text, post, json))
        return True

    def get_routes(self):
        return [
            ('GET', '/telegram/callbacks/', self.telegram_callback)
        ]

    def run(self):
        pass
