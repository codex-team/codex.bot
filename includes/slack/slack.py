import json
import logging
from .callbacks import SlackCallbacks

class Slack:

    __name__ = "Slack"

    def __init__(self):
        logging.debug("Slack running")

    def register_api_command(self):
        return []

    def run(self, server, api):
        server.router.add_get('/slack/say_hello', SlackCallbacks.say_hello)
        server.router.add_post('/slack/say_bye', SlackCallbacks.say_bye)
        server.router.add_get('/slack/open_ifmo', SlackCallbacks.open_ifmo)