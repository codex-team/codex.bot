from json import loads
from .message import Message
from .callbackquery import CallbackQuery


class Update:

    # https://core.telegram.org/bots/api#update
    __name__ = "Telegram Update"

    def __init__(self, data):

        self.message = None
        self.edited_message = None
        self.channel_post = None
        self.edited_channel_post = None
        self.callback_query = None

        if type(data) is str:
            data = loads(data)

        self.id = data['update_id']

        if 'message' in data:
            self.message = Message(data['message'])
        if 'edited_message' in data:
            self.edited_message = Message(data['edited_message'])
        if 'channel_post' in data:
            self.channel_post = Message(data['channel_post'])
        if 'edited_channel_post' in data:
            self.edited_channel_post = Message(data['edited_channel_post'])
        if 'callback_query' in data:
            self.callback_query = CallbackQuery(data['callback_query'])

    def get_commands(self):

        message = None

        if self.message:
            message = self.message
        if self.edited_message:
            message = self.edited_message
        if self.channel_post:
            message = self.channel_post
        if self.edited_channel_post:
            message = self.edited_channel_post

        if not message:
            return []

        commands = []

        for i in range(0, len(message.entities)):

            if message.entities[i].type != 'bot_command':
                continue

            command_start = message.entities[i].offset
            command_end = message.entities[i].offset + message.entities[i].length

            payload_start = command_end + 1

            if i < len(message.entities) - 1:
                payload_end = message.entities[i+1].offset - 1
            else:
                payload_end = None

            commands.append({
                'command': message.text[command_start : command_end],
                'payload': message.text[payload_start : payload_end]
            })

        return commands

