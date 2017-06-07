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
    async def slack_callback(self, params):
        """
        This route listens for incoming events from Slack and uses the event
        handler helper function to route events to our Bot.
        """
        income_params = params['json']

        if 'challenge' in income_params:
            return income_params['challenge']
        else:
            Handler(income_params)
            return {
                'text' : 'OK',
                'status' : 200
            }

    @http_response
    async def slack_oauth(self, params):

        query = params['query']
        if 'code' in query:
            oauth = self.slackBot.auth(query['code'])
        else:
            result = {
                'text' : 'Ошибка',
                'status' : 404
            }

        print(oauth)
        pass
        # Pass commands from message data to broker
        await self.broker.service_to_app({
            'chat': {
                'id': oauth["team_id"],
                'type': ''
            },
            'user': {
                'id': update.message.user.id,
                'username': username,
                'lang': update.message.user.language_code
            },
            'service': self.__name__,
            'commands': update.get_commands(),
            'text': update.message.text
        })

        return result




