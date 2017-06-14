class SystemCommand:
    """
    Codex Bot system commands
    """

    def __init__(self, api):

        self.commands = {
            'apps': self.apps,
            'start': self.help,
            'help': self.help
        }
        self.api = api

    async def help(self, chat, cmd_payload):

        # text = "Codex.Bot — платформа для интеграции различных сервисов в мессенджеры.\n\n" \
        #        "Для просмотра подключенных приложений используйте команду /apps\n\n" \
        #        "Для регистрации нового приложения введите /newapp\n" \
        #        "Для просмотра ваших приложений введите /myapps \n\n" \
        #        "Больши информации на bot.ifmo.su\n" \
        #        "Codex Team"

        text = "Codex Bot is a platform for services integration into messengers\n\n" \
               "To see available applications use /apps\n\n" \
               "To register new application use /newapp\n" \
               "To see your applications use /myapps\n\n" \
               "More information on bot.ifmo.su\n" \
               "Codex Team"

        message_payload = {
            'chat_hash': chat,
            'text': text
        }

        await self.api.send_to_service('system', message_payload)

    async def apps(self, chat, cmd_payload):

        # text = "Доступные приложения\n\n"
        text = "Available applications:\n\n"

        avaliable_apps = []

        for app in self.api.apps:

            command = self.api.apps[app]['name']
            print(self.api.commands)
            description, app_token = self.api.commands.get(command, (None, None))
            if not description:
                continue

            text += "/{} — {}\n".format(command, description)
            avaliable_apps.append(command)

        if not len(avaliable_apps):
            # text = 'Доступных приложений нет'
            text = "There are no available applications"

        message_payload = {
            'chat_hash': chat,
            'text': text
        }

        await self.api.send_to_service('system', message_payload)