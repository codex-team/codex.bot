import json
import logging
from .callbacks import SlackCallbacks

class Slack:

    __name__ = "Slack"

    def __init__(self):
        logging.debug("Slack running")

    def register_api_command(self):
        return []

    def get_routes(self):
        return [
                   ('GET', '/slack/say_hello', SlackCallbacks.say_hello),
                   ('POST', '/slack/say_bye', SlackCallbacks.say_bye),
                   ('GET', '/slack/open_ifmo', SlackCallbacks.open_ifmo)
        ]

    def run(self):
        pass
