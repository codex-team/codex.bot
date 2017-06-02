from json import loads
from .user import User


class MessageEntity:

    # https://core.telegram.org/bots/api#messageentity
    __name__ = "Telegram Message Entity"

    def __init__(self, data):

        self.url = None
        self.user = None

        if type(data) is str:
            data = loads(data)

        self.type = data['type']
        self.offset = data['offset']
        self.length = data['length']

        if 'url' in data:
            self.url = data['url']
        if 'user' in data:
            self.user = User(data['user'])
