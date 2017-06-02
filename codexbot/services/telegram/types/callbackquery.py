from json import loads
from .user import User
from .message import Message


class CallbackQuery:

    # https://core.telegram.org/bots/api#callbackquery
    __name__ = "Telegram Callback Query"

    def __init__(self, data):

        self.message = None
        self.inline_message_id = None
        self.data = None

        if type(data) is str:
            data = loads(data)

        self.id = data['id']
        self.user = User(data['from'])
        self.chat_instance = data['chat_instance']

        if 'message' in data:
            self.message = Message(data['message'])
        if 'inline_message_id' in data:
            self.inline_message_id = Message(data['inline_message_id'])
        if 'data' in data:
            self.data = data['data']