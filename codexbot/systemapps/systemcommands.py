class SystemCommand:
    """
    Codex Bot system commands
    """

    def __init__(self, api):

        self.commands = {
            'apps': self.apps,
            'start': self.help,
            'help': self.help,
            'bots': self.bots
        }
        self.api = api

    async def help(self, chat, cmd_payload):

        text = "Codex Bot is a platform for services integration into messengers\n\n" \
               "To see available applications use /apps\n\n" \
               "To register new application use /newapp\n" \
               "To see your applications use /myapps\n\n" \
               "More information on ifmo.su/bot\n" \
               "CodeX Team"

        message_payload = {
            'chat_hash': chat,
            'text': text
        }

        await self.api.send_to_service('system', message_payload)

    async def apps(self, chat, cmd_payload):

        text = "Available applications:\n\n"

        available_apps = []

        for app in self.api.apps:

            command = self.api.apps[app]['name']
            description, app_token = self.api.commands.get(command, (None, None))
            if not description:
                continue

            text += "/{} — {}\n".format(command, description)
            available_apps.append(command)

        if not len(available_apps):
            text = "There are no available applications"

        message_payload = {
            'chat_hash': chat,
            'text': text
        }

        await self.api.send_to_service('system', message_payload)

    async def bots(self, chat, cmd_payload):
        text = "Controlled bots"

        message_payload = {
            'chat_hash': chat,
            'text': text
        }

        await self.api.send_to_service('system', message_payload)