from json import loads
from .message import Message
from .callbackquery import CallbackQuery


class Update:

    # https://core.telegram.org/bots/api#update
    __name__ = "Telegram Update"

    def __init__(self, data):

        self.message = None
        self.callback_query = None

        if type(data) is str:
            data = loads(data)

        self.id = data['update_id']

        if 'message' in data:
            self.message = Message(data['message'])
        if 'edited_message' in data:
            self.message = Message(data['edited_message'])
        if 'channel_post' in data:
            self.message = Message(data['channel_post'])
        if 'edited_channel_post' in data:
            self.message = Message(data['edited_channel_post'])
        if 'callback_query' in data:
            self.callback_query = CallbackQuery(data['callback_query'])

    def get_commands(self):

        if not self.message:
            return []

        commands = []

        for i in range(0, len(self.message.entities)):

            if self.message.entities[i].type != 'bot_command':
                continue

            command_start = self.message.entities[i].offset + 1
            command_end = self.message.entities[i].offset + self.message.entities[i].length

            payload_start = command_end + 1

            if i < len(self.message.entities) - 1:
                payload_end = self.message.entities[i+1].offset - 1
            else:
                payload_end = None

            commands.append({
                'command': self.message.text[command_start : command_end],
                'payload': self.message.text[payload_start : payload_end]
            })

        return commands

