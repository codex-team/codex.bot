import json
import logging


class Telegram:

    __name__ = "Telegram"

    def __init__(self):
        logging.debug("Telegram module initiated.")

    def register_api_commands(self):
        """
        Register api commands to route.
        :return: list()
        """
        return []

    async def telegram_callback(self, request):
        """
        Process messages from telegram bot
        :return:
        """
        data = await request.text()
        update = json.loads(data)

    def run(self, server, api):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        server.router.add_post('/telegram/callback', self.telegram_callback)
