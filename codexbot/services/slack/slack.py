import logging
import json

from codexbot.lib.server import http_response
from codexbot.services.slack.Bot import Bot, authed_teams


class Slack:

    __name__ = "Slack"

    def __init__(self):

        self.routes = [
            ('GET', '/slack/oauth', self.slack_oauth),
            ('POST', '/slack/events', self.slack_events),
            ('POST', '/slack/commands', self.slack_commands),
            ('POST', '/slack/buttons', self.slack_buttons),
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
        text = params['post']['text']
        user_id = params['post']['user_id']
        user_name = params['post']['user_name']

        # getting command name without slash
        commands = {
            'command': command[1:],
            'payload': text
        }

        # send event type to core handler
        type = 'private' if params['post']['channel_name'] == 'directmessage' else 'group'

        # Pass commands from message data to broker
        await self.broker.commands_to_app({
            'chat': {
                'id': team_id + '.' + channel_id,
                'type': type # --- private or channel
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
    async def slack_buttons(self, params):

        callback = params['post']

        if 'payload' in callback:
            payload = callback['payload']
            payload = json.loads(payload)

            # I don't know how, but I get such response from metrika module
            # Response looks:
            # { "actions": [{"name": "$name", "value":"$value", "type":"button"}], "channel":{"name":"$channelname", "id":"$hash"}}
            data = payload['actions'][0]['value']
            channel_id = payload['channel']['id']
            team_id = payload['team']['id']
            user_id = payload['user']['id']
            user_name = payload['user']['name']

            # send event type to core handler
            type = 'private' if payload['channel']['name'] == 'directmessage' else 'group'

            await self.broker.callback_query_to_app({
                'chat': {
                    'id': team_id + '.' + channel_id,
                    'type': type
                },
                'user': {
                    'id': user_id,
                    'username': user_name,
                    'lang': None
                },
                'service': self.__name__,
                'data': data
            })

        return {
            'text': '',
            'status': 200
        }

    @http_response
    async def slack_oauth(self, params):
        """
        After hand-filling command in api.slack.com/apps, we got verification request wth 'challenge' and 'token'. 
        To verify, pass back 'challenge' field.
        
        Api URL : https://api.slack.com/events/url_verification
        
        :param params: responds http_response decorator.  
        :return: 
        """
        query = params['query']

        # set bot instance
        slackBot = Bot()

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
        """
        Used by Codex bot core to send message to the required platform
        
        :param chat_id: 
        :param message_payload: 
        :return: 
        """
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

        if 'text' in message_payload:
            template = 'codexbot/services/slack/templates/text.json'

            # send post message request to channel
            slackBot.client.api_call(
                "chat.postMessage",
                channel=channel_id,
                text=message_payload['text'],
                mrkdwn=True
            )

        if 'photo' in message_payload:
            template = 'codexbot/services/slack/templates/image.json'

            with open(template) as data_file:
                data = json.load(data_file)

            # fill in empty template
            data[0]['title'] = 'CodeX'
            data[0]['text'] = message_payload['caption']
            data[0]['image_url'] = message_payload['photo']

            # send post message request to channel
            slackBot.client.api_call(
                "chat.postMessage",
                channel=channel_id,
                attachments=json.dumps(data),
                mrkdwn=True
            )

        if 'markup' in message_payload:
            template = 'codexbot/services/slack/templates/buttons.json'

            with open(template) as data_file:
                data = json.load(data_file)

            actions = []
            url = None

            # fill in template
            for row in message_payload['markup']['inline_keyboard']:
                for button in row:
                    if 'url' in button:
                        # add link if button has link
                        url = button['url']
                    else:
                        # add buttons to message attachments
                        actions.append({
                            'name': 'button',
                            'text': button['text'],
                            'value': button['callback_data'],
                            'type': 'button'
                        })

            if url is None:
                data[0]['actions'] = actions

                # send post message request to channel with link
                slackBot.client.api_call(
                    "chat.postMessage",
                    channel=channel_id,
                    attachments=json.dumps(data),
                    mrkdwn=True
                )
            else:
                data[0]['title'] = url
                data[0]['title_link'] = url

                # send post message request to channel with buttons
                slackBot.client.api_call(
                    "chat.postMessage",
                    channel=channel_id,
                    attachments=json.dumps(data),
                    mrkdwn=True
                )




