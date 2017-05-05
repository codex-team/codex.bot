import logging
from urllib.parse import urlencode

import requests

from codexbot.globalcfg import URL
from codexbot.lib.server import http_response
from .config import BOT_NAME, API_TOKEN, API_URL, CALLBACK_ROUTE


class Telegram:

    __name__ = "Telegram"
    routes = [
        ('POST', self.config.callback_route(), self.telegram_callback)
    ]

    def __init__(self):
        self.__token = API_TOKEN
        self.__api_url = API_URL + API_TOKEN + '/'
        self.__callback_url = URL + CALLBACK_ROUTE
        self.__callback_route = CALLBACK_ROUTE

        self.__bot_name = BOT_NAME

        logging.debug("Telegram module initiated.")

    @http_response
    def telegram_callback(self, text, post, json):
        """
        Process messages from telegram bot
        :return:
        """
        logging.info("Got telegram callback {} {} {}".format(text, post, json))
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

    def message(self, text, chat_id):

        data = {
            'chat_id': chat_id,
            'text': text
        }
        url = self.__api_url + 'sendMessage'

        response = requests.post(url, json=data)
        if response.status_code != 200:
            logging.debug("Error while sending message to Telegram: {}".format(response.content))

        return response

    def image(self, filename, caption, chat_id):

        data = {
            'caption': caption,
            'chat_id': chat_id,
        }

        files = {
            'photo': open(filename, 'rb')
        }

        url = self.__api_url + 'sendPhoto'

        response = requests.post(url, data, files=files)
        if response.status_code != 200:
            logging.debug("Error while sending photo to Telegram: {}".format(response.content))

        return response
