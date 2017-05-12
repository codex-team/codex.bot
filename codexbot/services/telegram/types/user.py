from json import loads


class User:

    # https://core.telegram.org/bots/api#user
    __name__ = "Telegram User"

    last_name = None
    username = None

    def __init__(self, data):

        if type(data) == str:
            data = loads(data)

        self.id = data['id']
        self.first_name = data['first_name']

        if 'last_name' in data:
            self.last_name = data['last_name']

        if 'username' in data:
            self.username = data['username']
