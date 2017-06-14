import logging

from codexbot.lib.server import http_response
from codexbot.services.slack.bot.Bot import Bot, authed_teams


class Slack:

    __name__ = "Slack"

    def __init__(self):

        self.routes = [
            ('GET', '/slack/oauth', self.slack_oauth),
            ('POST', '/slack/events', self.slack_events),
            ('POST', '/slack/commands', self.slack_commands)
        ]

        logging.debug("Slack module initiated.")

    def run(self, broker):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.broker = broker

    @http_response
    async def slack_commands(self, params):

        # get necessary params from request
        team_id = params['post']['team_id']
        channel_id = params['post']['channel_id']
        command = params['post']['command']
        text = params['post']['command']
        user_id = params['post']['user_id']
        user_name = params['post']['user_name']

        # getting command name without slash
        commands = {
            'command': command[1:],
            'payload': text
        }

        # Pass commands from message data to broker
        await self.broker.commands_to_app({
            'chat': {
                'id': team_id + '.' + channel_id,
                'type': 'private' if params['post']['channel_name'] == 'directmessage' else 'group'  # --- private or channel
            },
            'user': {
                'id': user_id,
                'username': user_name,
                'lang': None
            },
            'service': self.__name__,
            'commands': [commands],
            'text': text
        })

        # return empty response
        return {
            'text' : '',
            'status': 200
        }

    @http_response
    async def slack_oauth(self, params):

        query = params['query']

        slackBot = Bot("")

        if 'code' in query:
            oauth = slackBot.auth(query['code'], self.broker)
        else:
            return {
                'text': 'Ошибка',
                'status': 404
            }

        return oauth

    @http_response
    async def slack_events(self, params):
        """
        This route listens for incoming events from Slack and uses the event
        handler helper function to route events to our Bot.
        """
        income_params = params['json']

        # confirm event subscription
        if 'challenge' in income_params:
            return {
                'text' : income_params['challenge'],
                'status' : 200
            }
        else:

            return {
                'text' : '',
                'status' : 200
            }

    def send(self, chat_id, message_payload):

        team_id, channel_id = chat_id.split('.')

        query = self.broker.core.db.find_one('slack', {
            'team_id': team_id
        })

        if team_id in authed_teams and "bot_token" in authed_teams[team_id]:
            token = authed_teams[team_id]["bot_token"]
        else:
            token = query['token']

        # initialize slack client
        slackBot = Bot(token)

        # send post message request to channel
        slackBot.client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message_payload['text'],
        )




