import logging
from json import loads

from codexbot.lib.server import http_response
from codexbot.services.slack.bot.Bot import Bot
from codexbot.services.slack.methods.handler import Handler


class Slack:

    __name__ = "Slack"

    def __init__(self):

        self.routes = [
            ('GET', '/slack/oauth', self.slack_oauth),
            ('POST', '/callbacks/slack', self.slack_callback),
        ]

        self.slackBot = Bot()

        logging.debug("Slack module initiated.")

    def run(self, broker):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.broker = broker

    @http_response
    async def slack_callback(self, get_params, post_params):
        """
        This route listens for incoming events from Slack and uses the event
        handler helper function to route events to our Bot.
        """
        slack_event = loads(post_params)
        if 'challenge' in slack_event:
            return slack_event['challenge']
        else:
            Handler(self.slackBot, slack_event)

    @http_response
    async def slack_oauth(self, get_params, post_params):

        if 'code' in get_params:
            self.slackBot.auth(get_params['code'])

        return 'OK'




