from json import loads
from .message import Message
from .callbackquery import CallbackQuery
from ..telegram_settings import BOT_NAME


class Update:

    # https://core.telegram.org/bots/api#update
    __name__ = "Telegram Update"

    def __init__(self, request_params):

        self.message = None
        self.callback_query = None

        data = request_params['json']

        if type(data) is str:
            data = loads(data)

        self.id = data['update_id']
        self.bot_id = request_params['params'].get('bot', None)

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
        command_entities = []
        for entity in self.message.entities:
            if entity.type == 'bot_command':
                command_entities.append(entity)

        for i in range(0, len(command_entities)):

            if command_entities[i].type != 'bot_command':
                continue

            command_start = command_entities[i].offset + 1
            command_end = command_entities[i].offset + command_entities[i].length

            payload_start = command_end + 1

            if i < len(command_entities) - 1:
                payload_end = command_entities[i+1].offset - 1
            else:
                payload_end = None

            command = self.message.text[command_start : command_end]

            if BOT_NAME in command:
                command, botname = command.split('@', 1)

            commands.append({
                'command': command,
                'payload': self.message.text[payload_start : payload_end]
            })

        return commands

