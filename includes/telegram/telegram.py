import logging

from lib.server import http_response


class Telegram:

    __name__ = "Telegram"

    def __init__(self):
        logging.debug("Telegram module initiated.")

    @http_response
    def telegram_callback(self, text, post, json):
        """
        Process messages from telegram bot
        :return:
        """
        logging.info("Got telegram callback {} {} {}".format(text, post, json))
        return True

    def run(self, server, api):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.server = server
        self.api = api
        routes = [
            ('POST', '/telegram/callback', self.telegram_callback)
        ]
        self.server.set_routes(routes)
