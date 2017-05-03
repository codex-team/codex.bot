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

    def get_routes(self):
        return [
            ('GET', '/telegram/callbacks/', self.telegram_callback)
        ]

    def run(self):
        pass
