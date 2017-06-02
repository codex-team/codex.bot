from json import loads


class User:

    # https://core.telegram.org/bots/api#user
    __name__ = "Telegram User"

    def __init__(self, data):

        self.last_name = None
        self.username = None
        self.language_code = None

        if type(data) == str:
            data = loads(data)

        self.id = data['id']
        self.first_name = data['first_name']

        if 'last_name' in data:
            self.last_name = data['last_name']

        if 'username' in data:
            self.username = data['username']

        if 'language_code' in data:
            self.language_code = data['language_code']
