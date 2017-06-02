import random
import string
import gettext


class AppManager:

    def __init__(self, broker):

        gettext.translation('appmanager', 'i18n', ['ru']).install()

        self.core = broker.core
        self.broker = broker
        self.api = broker.api
        self.db = broker.core.db

        self.commands = {
            'newapp': self.add_app,
            'myapps': self.show_apps
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
