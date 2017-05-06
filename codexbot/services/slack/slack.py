import logging
from urllib.parse import urlencode

import requests

from codexbot.globalcfg import URL
from codexbot.lib.server import http_response

from .config import CALLBACK_ROUTE, BOT_NAME, BOT_TOKEN, CLIENT_SECRET, CLIENT_ID
from .methods import send_message, get_bot_id, channels_list

from slackclient import SlackClient


class Slack:

    __name__ = "Slack"

    def __init__(self):
        """
        Initialize Slack module. 
        Get secrets and callback route from config
        """
        self.__callback_route = CALLBACK_ROUTE
        self.__callback_url = URL + CALLBACK_ROUTE
        self.__client_id = CLIENT_ID
        self.__client_secret = CLIENT_SECRET
        self.__bot_name = BOT_NAME
        self.__token = BOT_TOKEN

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
        api = self.slack_client.api_call("api.test")
        if api.get('ok'):
            logging.debug("Slack API - OK...")

        # Auth test
        auth = self.slack_client.api_call("auth.test")
        if auth.get('ok'):
            logging.debug("Slack Auth - OK...")

    @http_response
    def slack_callback(self, text, post, json):
        """
        Process messages from telegram bot
        :return:
        """
        logging.info("Got slack callback {} {} {}".format(text, post, json))