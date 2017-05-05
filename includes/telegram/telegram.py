import logging
import requests
import json
from urllib.parse import urlencode

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

    def run(self, server, api):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.server = server
        self.api = api
        routes = [
            ('POST', self.config.callback_route(), self.telegram_callback)
        ]
        self.server.set_routes(routes)
        self.set_webhook()

    def set_webhook(self):
        query = self.config.api_url() + 'setWebhook?' + urlencode({
            'url': self.config.callback_url()
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
        url = self.config.api_url() + 'sendMessage'

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

        url = self.config.api_url() + 'sendPhoto'

        response = requests.post(url, data, files=files)
        if response.status_code != 200:
            logging.debug("Error while sending photo to Telegram: {}".format(response.content))

        return response
