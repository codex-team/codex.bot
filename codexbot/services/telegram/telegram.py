import logging
from urllib.parse import urlencode

import requests

from codexbot.globalcfg import URL
from codexbot.lib.server import http_response
from .config import BOT_NAME, API_TOKEN, API_URL, CALLBACK_ROUTE
from .methods.message import Message
from .methods.photo import Photo
from .methods.sticker import Sticker
from .methods.video import Video

from .types.update import Update


class Telegram:

    __name__ = "Telegram"
    routes = []

    def __init__(self):
        self.__token = API_TOKEN
        self.__api_url = API_URL + API_TOKEN + '/'
        self.__callback_url = URL + CALLBACK_ROUTE
        self.__callback_route = CALLBACK_ROUTE
        self.__bot_name = BOT_NAME

        self.routes = [
            ('POST', CALLBACK_ROUTE, self.telegram_callback)
        ]

        self.message = Message(self.__api_url)
        self.photo = Photo(self.__api_url)
        self.sticker = Sticker(self.__api_url)
        self.video = Video(self.__api_url)

        logging.debug("Telegram module initiated.")

    @http_response
    def telegram_callback(self, text, post, json):
        """
        Process messages from telegram bot
        :return:
        """
        logging.info("Got telegram callback {} {} {}".format(text, post, json))

        update = Update(json)

        return True

    def run(self, broker):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.broker = broker
        self.set_webhook()

    def set_webhook(self):
        query = self.__api_url + 'setWebhook?' + urlencode({
            'url': self.__callback_url
        })

        try:
            result = requests.get(query)
        except Exception as e:
            logging.debug(e)
        else:
            logging.debug(result.content)

