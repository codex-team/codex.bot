import logging
from urllib.parse import urlencode

import requests

from codexbot.globalcfg import URL
from codexbot.lib.server import http_response
from .config import CALLBACK_ROUTE, BOT_NAME, TOKEN, CLIENT_SECRET, CLIENT_ID

from slackclient import SlackClient


class Slack:

    __name__ = "Slack"

    def __init__(self):
        self.__callback_route = CALLBACK_ROUTE
        self.__callback_url = URL + CALLBACK_ROUTE
        self.__client_id = CLIENT_ID
        self.__client_secret = CLIENT_SECRET
        self.__bot_name = BOT_NAME
        self.__token = TOKEN
        self.routes = [
            ('GET', self.__callback_route, self.slack_callback)
        ]
        logging.debug("Slack module initiated.")

    def run(self, broker):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.broker = broker

        # Initialize Slack Client
        self.slack_client = SlackClient(self.__token)

        # test API
        self.slack_client.api_call("api.test")

        # Auth test
        self.slack_client.api_call("auth.test")


    @http_response
    def slack_callback(self, text, post, json):
        """
        Process messages from telegram bot
        :return:
        """
        logging.info("Got slack callback {} {} {}".format(text, post, json))

    def channels_list(self):
        channels_list = self.slack_client.api_call("channels.list")
        if channels_list.get('ok'):
            return channels_list['channels']
        return None

    def send_message(self, channel_id, message, username):
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            username=self.__bot_name
        )