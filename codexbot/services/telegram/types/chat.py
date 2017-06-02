from json import loads


class Chat:

    # https://core.telegram.org/bots/api#chat
    __name__ = "Telegram Chat"

    def __init__(self, data):

        self.title = None
        self.username = None
        self.first_name = None
        self.last_name = None
        self.all_members_are_administrators = None

        if type(data) == str:
            data = loads(data)

        self.id = data['id']
        self.type = data['type']

        if 'title' in data:
            self.first_name = data['title']
        if 'username' in data:
            self.first_name = data['username']
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'all_members_are_administrators' in data:
            self.all_members_are_administrators = data['all_members_are_administrators']
