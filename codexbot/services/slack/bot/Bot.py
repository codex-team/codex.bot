import logging

from slackclient import SlackClient
from codexbot.services.slack.config.config import BOT_NAME, CLIENT_ID, CLIENT_SECRET, VERIFICATION

authed_teams = {}


class Bot():

    def __init__(self):

        self.name = BOT_NAME
        self.oauth = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "bot"
        }

        self.verification = VERIFICATION
        self.client = SlackClient("xoxb-191736210752-S5taEvseHbty11UZWPwj5R4T")

    def auth(self, code):

        auth_response = self.client.api_call(
            "oauth.access",
            client_id=self.oauth["client_id"],
            client_secret=self.oauth["client_secret"],
            code=code
        )

        team_id = auth_response["team_id"]
        authed_teams[team_id] = {
            "bot_token" : auth_response["bot"]["bot_access_token"]
        }

        self.__token = authed_teams[team_id]["bot_token"]

        self.client = SlackClient(self.__token)

        # Auth test
        auth = self.client.api_call("auth.test")
        if auth.get('ok'):
            logging.debug("Slack Auth - OK...")

        # test API
        api = self.client.api_call("api.test")
        if api.get('ok'):
            logging.debug("Slack API - OK...")
