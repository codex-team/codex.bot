from .message import Message
from codexbot.services.slack.bot.Bot import Bot


class Handler():
    def __init__(self, slack_event):
        self.slack_event  = slack_event
        self.slackBot = Bot()

        self.handle(self.slack_event)

    def handle(self, slack_event):

        event = slack_event.get('event')

        if event.get('type') == 'message':
            message = Message()
            message.getMessage(event)
            channel_id = event.get('channel')

            # this is bot message
            # do not listen
            if not event.get('bot_id') and not event.get('bot_message'):
                attachment = {
                            "title":"App hangs on reboot",
                            "title_link": "http://domain.com/ticket/123456",
                            "text": "If I restart my computer without quitting your app, it stops the reboot sequence.\nhttp://domain.com/ticket/123456",
                        }
                self.slackBot.client.api_call(
                    "chat.postMessage",
                    channel=channel_id,
                    text='Would you like to play a game?',
                    attachments=[attachment]
                )

        if event.get('type') == 'reaction_removed':
            print('reaction removed')
        elif event.get('type') == 'reaction_added':
            print('reaction_added')

    def get_bot_id(self, bot_name):
        members = self.slack_client.api_call("users.list")
        if members.get('ok'):
            users = members.get('members')
            for user in users:
                if 'name' in user and user.get('name') == bot_name:
                    print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
            else:
                print("could not find bot user with the name " + bot_name)

    def channels_list(self):
        channels_list = self.slack_client.api_call("channels.list")
        if channels_list.get('ok'):
            return channels_list['channels']
        return None

    def send_message(self, channel_id, message, emoji):
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            icon_emoji=':' + emoji,
            as_user=True
        )

    def channels_info(self, channel_id):
        channel_info = self.slack_client.api_call("channels.info", channel=channel_id)
        if channel_info:
            return channel_info
        return None