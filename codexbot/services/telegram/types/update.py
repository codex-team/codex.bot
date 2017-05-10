from json import loads
from .message import Message
from .callbackquery import CallbackQuery


class Update():

    message = None
    edited_message = None
    channel_post = None
    edited_channel_post = None
    callback_query = None

    def __init__(self, data):

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