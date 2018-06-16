import logging

from codexbot.components.useful import grouped
from codexbot.systemapps.botmanager.base import ManagerBase


class BotManager(ManagerBase):

    async def show_bots(self, chat_hash, command_payload):
        """
        Show all hijacked bots that you own (in the chat).

        :param chat_hash:
        :param command_payload:
        :return:
        """
        bots = list(self.db.find(self.api.BOTS_COLLECTION_NAME, {'owner': chat_hash}))
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        if len(bots):
            buttons = grouped([{
                "text": bot['name'],
                "callback_data": 'core_botmenu {}'.format(bot['bot_id'])
            } for bot in bots], 2)
            await messenger_service.send(chat['id'], {
                'text': 'Choose bot to modify settings',
                'markup': {
                    'inline_keyboard': buttons
                }
            })
        else:
            await messenger_service.send(chat['id'], {
                'text': 'There are no hijacked bots. Add new bot using command /addbot {api_token}'
            })

    async def add_bot(self, chat_hash, bot_data):
        import re

        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]  # Only Telegram for now

        if not bot_data:
            await messenger_service.send(chat['id'], {'text': 'You should pass API Token in format /addbot {api_token}.'})
            return

        if not re.match("\d+:[a-zA-Z0-9\+\/]+", bot_data):
            await messenger_service.send(chat['id'], {
                'text': 'Looks like your API Token is invalid. You should provide API Token as /addbot {api_token}.'
            })
            return

        api_token = bot_data
        bot = self.db.find_one(self.api.BOTS_COLLECTION_NAME, {'api_token': api_token})
        if bot:
            await messenger_service.send(chat['id'], {'text': 'Bot {} is already hijacked.'.format(bot['name'])})
            return

        data = messenger_service.getMe(api_token)
        if not data['ok']:
            await messenger_service.send(chat['id'], {
                'text': 'Error with code {}. {}'.format(data['error_code'], data['description'])
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

        await messenger_service.send(chat['id'], {'text': 'Your bot «{}» was successfully hijacked. Type /bots to show your bots.'.format(bot['name'])})

    async def del_bot(self, chat_hash, bot_name):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        if not bot_name:
            await messenger_service.send(chat['id'], {
                'text': 'Input bot name: /delbot {bot_name}.\nTo show your bots input /bots'
            })
            return

        bot = self.db.find_one(self.api.BOTS_COLLECTION_NAME, {'name': bot_name, 'owner': chat_hash})
        if not bot:
            await messenger_service.send(chat['id'], {
                'text': 'Bot with name «{}» not found\nTo show your bots input /bots'.format(bot_name)
            })
            return

        api_token = bot['api_token']
        del self.api.bots[bot['bot_id']]
        self.db.remove(self.api.BOTS_COLLECTION_NAME, bot)
        messenger_service.del_webhook(api_token)
        await messenger_service.send(chat['id'], {
            'text': 'Bot «{}» successfully delete. Webhook has been unset'.format(bot['name'])
        })

    async def bot_menu(self, chat_hash, bot_id):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        bot = self.db.find_one(self.api.BOTS_COLLECTION_NAME, {'bot_id': int(bot_id), 'owner': chat_hash})
        if not bot:
            await messenger_service.send(chat['id'], {
                'text': 'Bot is undefined. Error! Alarm! Code: {}'.format(bot_id)
            })
        else:
            await messenger_service.send(chat['id'], {
                'text': 'Your bot «{}» is just awesome\nYou can:\n'
                        '/delbot {} – delete it\n'
                        '/linkbot {} – configure available applications\n'
                        '/sethelp {} <HTML_TEXT> – set help message. It is HTML compatible\n'
                        .format(*[bot['name']] * 4)
            })

    async def set_help(self, chat_hash, data):
        chat = self.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        try:
            bot_name, help_text = data.split(' ', 1)
        except Exception as e:
            return await messenger_service.send(chat['id'], {
                'text': 'Usage error. Try /sethelp <BOT_NAME> <HTML_TEXT>'
            })

        bot = self.db.find_one(self.api.BOTS_COLLECTION_NAME, {'name': bot_name, 'owner': chat_hash})
        if not bot:
            await messenger_service.send(chat['id'], {
                'text': 'Bot {} is undefined'.format(bot_name)
            })
        else:
            bot['help'] = help_text
            self.db.update(self.api.BOTS_COLLECTION_NAME, {'name': bot_name, 'owner': chat_hash}, bot)
            await messenger_service.send(chat['id'], {
                'text': 'Done.'
            })
