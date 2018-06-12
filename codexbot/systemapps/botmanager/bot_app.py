import logging

from codexbot.components.useful import grouped
from codexbot.services.telegram.types.markups import InlineKeyboard
from codexbot.systemapps.botmanager.apps import AppManager


class BotAppLink(AppManager):

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

    def link_bot(self, chat_hash, bot_name):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        apps = self.db.find('apps', {})
        linked_apps = self.db.find(self.api.BOT_APP_LINKS_COLLECTION_NAME, {'bot_name': bot_name})

        my_apps = [app['app_name'] for app in linked_apps]
        other_apps = []
        for app in apps:
            if app['name'] not in my_apps:
                other_apps.append(InlineKeyboard.button(app['name'], callback_data='core_applylink ' + bot_name + ' ' + app['name']))

        message = 'Your bot\'s applications: ' + ', '.join(my_apps) if len(my_apps) else 'No apps linked yet'
        message += '\n\nYou can unlink app from bot: /unlink <BOTNAME> <APPNAME>\n'

        messenger_service.send(chat['id'], {
            'text': message
        })

        if len(other_apps):
            messenger_service.send(chat['id'], {
                'text': 'Choose applications that can be included into your bot.',
                'markup': {
                    'inline_keyboard': InlineKeyboard(*grouped(other_apps, 2)).get()
                }
            })

    def apply_link(self, chat_hash, data):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        try:
            bot_name, app_name = data.split(" ")

            bot = self.db.find_one(self.api.BOTS_COLLECTION_NAME, {'name': bot_name, 'owner': chat_hash})
            app = self.db.find_one(self.api.APPS_COLLECTION_NAME, {'name': app_name})
            if not bot:
                messenger_service.send(chat['id'], {'text': 'Bot {} is undefined.'.format(bot_name)})
                return
            if not app:
                messenger_service.send(chat['id'], {'text': 'Application is undefined.'.format(app_name)})
                return

            lnk = {
                'app_name': app_name,
                'bot_name': bot_name,
                'owner': chat_hash
            }

            if not self.db.find_one(self.api.BOT_APP_LINKS_COLLECTION_NAME, lnk):
                if self.db.insert(self.api.BOT_APP_LINKS_COLLECTION_NAME, lnk):
                    self.api.load_bots()
                    messenger_service.send(chat['id'], {'text': '{} is successfully linked to {}.'.format(bot_name, app_name)})
                else:
                    messenger_service.send(chat['id'], {'text': 'Failed to link {} to {}.'.format(bot_name, app_name)})
            else:
                messenger_service.send(chat['id'], {'text': '{} is already linked to {}.'.format(bot_name, app_name)})

        except Exception as e:
            logging.error("Exception during apply link: {}".format(e))

    def unapply_link(self, chat_hash, data):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        try:
            bot_name, app_name = data.split(" ")

            bot = self.db.find_one(self.api.BOTS_COLLECTION_NAME, {'name': bot_name, 'owner': chat_hash})
            app = self.db.find_one(self.api.APPS_COLLECTION_NAME, {'name': app_name})
            if not bot:
                messenger_service.send(chat['id'], {'text': 'Bot {} is undefined.'.format(bot_name)})
                return
            if not app:
                messenger_service.send(chat['id'], {'text': 'Application is undefined.'.format(app_name)})
                return

            if self.db.remove(self.api.BOT_APP_LINKS_COLLECTION_NAME, {
                'app_name': app_name,
                'bot_name': bot_name,
                'owner': chat_hash
            }):
                self.api.load_bots()
                messenger_service.send(chat['id'], {'text': '{} is successfully unlinked from {}.'.format(app_name, bot_name)})
            else:
                messenger_service.send(chat['id'], {'text': 'Error. Maybe it is already unlinked.'})

        except Exception as e:
            logging.error("Exception during unapply link: {}".format(e))