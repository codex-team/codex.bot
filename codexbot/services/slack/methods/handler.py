from .message import Message


class Handler():
    def __init__(self, slack_client, slack_event):
        self.slack_client = slack_client
        self.slack_event  = slack_event

        self.handle(self.slack_event)

    def handle(self, slack_event):

        event = slack_event.get('event')
        print(event)
        if event.get('type') == 'message':
            message = Message()
            message.getMessage(event)

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