import random
import string


class AppManager:

    def __init__(self, broker):

        self.core = broker.core
        self.broker = broker
        self.api = broker.api
        self.db = broker.core.db

        self.commands = {
            'newapp': self.add_app,
            'myapps': self.show_apps
        }

    def add_app(self, chat_hash, app_data):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        app_data = app_data.split(' ')

        if len(app_data) < 2:
            message = 'You should pass name and host of your app without spaces'
        elif len(app_data) > 2:
            message = 'You should pass only name and host of your app without spaces'
        else:
            app = self.db.find_one(self.api.APPS_COLLECTION_NAME, {'name': app_data[0]})
            if app:
                message = 'App {} already exists'.format(app_data[0])
            else:

                app = {
                    'token': self.generate_app_token(),
                    'name': app_data[0],
                    'queue': app_data[0],
                    'host': app_data[1],
                    'port': 80,
                    'owner': chat_hash
                }
                self.generate_app_token()
                self.db.insert(self.api.APPS_COLLECTION_NAME, app)
                self.api.load_app(app)
                message = 'Your app was successfully registered. Your token - {}'.format(app['token'])

        self.core.services[chat['service']].send(
            chat['id'],
            {'text': message}
        )

    def show_apps(self, chat_hash, command_payload):
        apps = self.db.find(self.api.APPS_COLLECTION_NAME, {'owner': chat_hash})
        chat = self.db.find_one('chats', {'hash': chat_hash})

        if apps.count():
            message = 'Your apps: \n\n'
            for app in apps:
                message += '{}\nToken: {}\nHost: {}\nQueue: {}\n---------\n'.format(app['name'], app['token'], app['host'], app['queue'])
        else:
            message = 'There are no registered apps. Add new app using command /newapp {name} {host}'

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
