from codexbot.components.useful import grouped
from codexbot.services.telegram.types.markups import InlineKeyboard


class ManagerBase:

    def __init__(self, broker):
        self.core = broker.core
        self.broker = broker
        self.api = broker.api
        self.db = broker.core.db

    def help(self, chat_hash, command_payload):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        self.core.services[chat['service']].send(chat['id'], {
            'text': 'Available commands:\n' + \
            '1. /bots – list of your bots\n' + \
            '2. /addbot <API_TOKEN> – hijack your bot\n' + \
            '3. /delbot <NAME> – delete your bot'
        })

    def add_app_to_bot(self, chat_hash, params):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        apps = self.db.find('apps', {})
        buttons = grouped([InlineKeyboard.button(app['name'], callback_data='/addapp ' + app['token']) for app in apps], 2)

        messenger_service.send(chat['id'], {
            'text': 'Choose applications that can be included into your bot',
            'markup': {
                'inline_keyboard': InlineKeyboard(*buttons).get()
            }
        })
