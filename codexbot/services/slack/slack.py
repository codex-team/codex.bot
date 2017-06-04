import logging

from json import loads
from codexbot.lib.server import http_response

from .Bot import Bot

pyBot = Bot()

class Slack:

    __name__ = "Slack"

    def __init__(self):

        self.routes = [
            ('GET', '/slack/oauth', self.slack_oauth),
            ('POST', '/callbacks/slack', self.slack_callback),
        ]

        logging.debug("Slack module initiated.")

    def run(self, broker):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.broker = broker

    @http_response
    async def slack_callback(self, text, post, json):
        """
        This route listens for incoming events from Slack and uses the event
        handler helper function to route events to our Bot.
        """
        slack_event = loads(text)
        print(slack_event)

    @http_response
    async def slack_oauth(self, text, post, json):

        print(text)
