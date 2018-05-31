import random
import string
import gettext

import logging


class AppManager:

    def __init__(self, broker):

        gettext.translation('appmanager', 'i18n', ['ru']).install()

        self.core = broker.core
        self.broker = broker
        self.api = broker.api
        self.db = broker.core.db

        self.commands = {
            'newapp': self.add_app,
            'myapps': self.show_apps,
            'bots': self.show_bots,
            'addbot': self.add_bot,
            'delbot': self.del_bot
        }

    def add_app(self, chat_hash, app_data):
        """
        Register new app by command /newapp {app_name} {app_host}
        app_name - name of new app.
        app_host - url or ip of app`s host
        Name and host shouldn't contain spaces

        :param chat_hash: chat_hash from broker
        :param app_data: [app_name, app_host]
        :return:
        """
        chat = self.db.find_one('chats', {'hash': chat_hash})
        app_data = app_data.split(' ')

        if len(app_data) < 2:
            message = "{} {}".format(
                _('You should pass name and host of your app in format /newapp {name} {host}.'),
                _('Name and host should not contain spaces.')
            )
        elif len(app_data) > 2:
            message = "{} {}".format(
                _('You should pass only name and host of your app in format /newapp {name} {host}.'),
                _('Name and host should not contain spaces.')
            )
        else:
            app_name = app_data[0]
            app_host = app_data[1]

            app = self.db.find_one(self.api.APPS_COLLECTION_NAME, {'name': app_name})
            if app:
                message = _('App {} already exists.').format(app_name)
            else:

                app = {
                    'token': self.generate_app_token(),
                    'name': app_name,
                    'queue': app_name,
                    'host': app_host,
                    'port': 80,
                    'owner': chat_hash
                }
                self.generate_app_token()
                self.db.insert(self.api.APPS_COLLECTION_NAME, app)
                self.api.load_app(app)
                message = _('Your app was successfully registered. Your token - {}').format(app['token'])

        self.core.services[chat['service']].send(
            chat['id'],
            {'text': message}
        )

    def show_apps(self, chat_hash, command_payload):
        """
        Get all registered apps by owner field

        :param chat_hash: hash of app`s owner chat
        :param command_payload: empty
        :return:
        """
        apps = self.db.find(self.api.APPS_COLLECTION_NAME, {'owner': chat_hash})
        chat = self.db.find_one('chats', {'hash': chat_hash})

        if apps.count():
            message = _('Your apps: \n\n')
            for app in apps:
                message += _('{}\nToken: {}\nHost: {}\nQueue: {}\n---------\n').format(app['name'], app['token'], app['host'], app['queue'])
        else:
            message = _('There are no registered apps. Add new app using command /newapp {name} {host}.')

        self.core.services[chat['service']].send(
            chat['id'],
            {'text': message}
        )

    def show_bots(self, chat_hash, command_payload):
        bots = self.db.find(self.api.BOTS_COLLECTION_NAME, {'owner': chat_hash})
        chat = self.db.find_one('chats', {'hash': chat_hash})

        if bots.count():
            message = _('Your bots: \n\n')
            for bot in bots:
                message += _('{}\n'.format(bot['name']))
        else:
            message = _('There are no hijacked bots. Add new bot using command /addbot {api_token}')

        self.core.services[chat['service']].send(
            chat['id'],
            {'text': message}
        )

    def add_bot(self, chat_hash, bot_data):
        import re

        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]  # Only Telegram for now

        if not bot_data:
            messenger_service.send(chat['id'], {'text': _('You should pass API Token in format /addbot {api_token}.')})
            return

        if not re.match("\d+:[a-zA-Z0-9\+\/]+", bot_data):
            messenger_service.send(chat['id'], {
                'text': _('Looks like your API Token is invalid. You should provide API Token as /addbot {api_token}.')
            })
            return

        api_token = bot_data
        bot = self.db.find_one(self.api.BOTS_COLLECTION_NAME, {'api_token': api_token})
        if bot:
            messenger_service.send(chat['id'], {'text': _('Bot {} is already hijacked.').format(bot['name'])})
            return

        data = messenger_service.getMe(api_token)
        if not data['ok']:
            messenger_service.send(chat['id'], {
                'text': _('Error with code {}. {}'.format(data['error_code'], data['description']))
            })
            return

        bot = {
            'owner': chat_hash,
            'api_token': api_token,
            'name': data['result']['username'],
            'bot_id': data['result']['id']
        }

        logging.debug("/addbot with params", bot)

        messenger_service.set_webhook(api_token, "/telegram/callback/{}".format(bot['bot_id']))

        self.db.insert(self.api.BOTS_COLLECTION_NAME, bot)
        self.api.load_bot(bot)

        messenger_service.send(chat['id'], {'text': _('Your bot «{}» was successfully hijacked.').format(bot['name'])})

    def del_bot(self, chat_hash, bot_name):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        if not bot_name:
            messenger_service.send(chat['id'], {
                'text': _('Input bot name: /delbot {bot_name}.\nTo show your bots input /bots')
            })
            return

        bot = self.db.find_one(self.api.BOTS_COLLECTION_NAME, {'name': bot_name, 'owner': chat_hash})
        if not bot:
            messenger_service.send(chat['id'], {
                'text': _('Bot with name «{}» not found\nTo show your bots input /bots'.format(bot_name))
            })
            return

        api_token = bot['api_token']
        del self.api.bots[bot['bot_id']]
        self.db.remove(self.api.BOTS_COLLECTION_NAME, bot)
        messenger_service.del_webhook(api_token)
        messenger_service.send(chat['id'], {
            'text': _('Bot «{}» successfully delete. Webhook has been unset'.format(bot['name']))
        })

    def process(self, chat_hash, command_data):
        self.commands[command_data['command']](chat_hash, command_data['payload'])

    @staticmethod
    def generate_app_token(size=8, chars=string.ascii_uppercase + string.digits):
        """
        Generate unique string
        Application will use this token for authentication
        :param size: size in symbols
        :param chars: letters used
        :return: string token
        """
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
