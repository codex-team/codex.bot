import logging

from codexbot.components.useful import grouped
from codexbot.services.telegram.types.markups import InlineKeyboard
from codexbot.systemapps.botmanager.base import ManagerBase


class AppManager(ManagerBase):

    def show_apps(self, chat_hash, command_payload):
        """
        Get all registered apps by owner field

        :param chat_hash: hash of app`s owner chat
        :param command_payload: empty
        :return:
        """
        apps = self.db.find(self.api.APPS_COLLECTION_NAME, {'owner': chat_hash})
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        if apps.count():
            message = 'Your apps: \n\n'
            for app in apps:
                message += '{}\nToken: {}\nHost: {}\nQueue: {}\n---------\n'.format(app['name'], app['token'], app['host'], app['queue'])
        else:
            message = 'There are no registered apps. Add new app using command /newapp {name} {host}.'

        messenger_service.send(
            chat['id'],
            {'text': message}
        )

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
        messenger_service = self.core.services[chat['service']]

        if len(app_data) < 2:
            message = "{} {}".format(
                'You should pass name and host of your app in format /newapp {name} {host}.',
                'Name and host should not contain spaces.'
            )
        elif len(app_data) > 2:
            message = "{} {}".format(
                'You should pass only name and host of your app in format /newapp {name} {host}.',
                'Name and host should not contain spaces.'
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
                message = 'Your app was successfully registered. Your token - {}'.format(app['token'])

        messenger_service.send(
            chat['id'],
            {'text': message}
        )
