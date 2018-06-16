import logging


class SystemCommand:
    """
    Codex Bot system commands
    """

    def __init__(self, api, core):

        self.commands = {
            'start': self.help,
            'help': self.help,
            'apps': self.apps
        }
        self.api = api
        self.core = core

    async def help(self, chat_hash, cmd_payload, bot_id):

        chat = self.core.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        if bot_id:
            bot = self.api.db.find_one(self.api.BOTS_COLLECTION_NAME, {'bot_id': int(bot_id)})
            if bot:
                return await messenger_service.send(chat['id'], {
                    'text': bot.get('help', bot.get('help', 'Help message is not set')),
                    'bot': bot_id,
                    'parse_mode': 'HTML'
                })

        text = "Codex Bot is a platform for services integration into messengers\n\n" \
               "To see available applications use /apps\n\n" \
               "To register new application use /newapp\n" \
               "To see your applications use /myapps\n\n" \
               "More information on ifmo.su/bot\n" \
               "CodeX Team"

        message_payload = {
            'chat_hash': chat['hash'],
            'text': text
        }

        await self.api.send_to_service('system', message_payload)

    async def apps(self, chat_hash, cmd_payload, bot_id):

        chat = self.core.db.find_one('chats', {'hash': chat_hash})
        messenger_service = self.core.services[chat['service']]

        if bot_id is not None:
            bot_name = self.core.db.find_one(self.api.BOTS_COLLECTION_NAME, {'bot_id': int(bot_id)}).get('name', None)
            bot_apps = [link['app_name'] for link in self.core.db.find(self.api.BOT_APP_LINKS_COLLECTION_NAME, {'bot_name': bot_name})]
            available_apps = bot_apps
        else:
            available_apps = [app['name'] for app in self.api.apps.values()]

        text = "Available applications:\n\n" + \
               '\n\n'.join(["/{} – {}".format(app, self.api.commands.get(app, "")[0]) for app in available_apps if app in self.api.commands])

        if not len(available_apps):
            text = "There are no available applications"

        await messenger_service.send(chat['id'], {
            'text': text,
            'bot': bot_id
        })
