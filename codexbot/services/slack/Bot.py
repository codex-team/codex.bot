import logging

from slackclient import SlackClient
from codexbot.services.slack.slack_settings import BOT_NAME, CLIENT_ID, CLIENT_SECRET

authed_teams = {}


class Bot():

    def __init__(self, token=None):

        """
        connect slack client with slack bot 
        
        :param token: 
        """
        self.name = BOT_NAME
        self.oauth = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "bot"
        }

        self.collection_name = 'slack'
        self.verification = VERIFICATION
        self.client = SlackClient(token)

    def auth(self, code, broker):

        """
        Authentificate bot: 
            1. send oauth.access api method with params below
            2. getting team and token
            3. Save team_id as key and token as value
        
        :param code:  this code will be send by Slack App. 
        :param broker: core method that allows us to do database queries
        :return: 
        """
        if not code:
            return {
                'text' : 'Code expected',
                'status': 404
            }

        auth_response = self.client.api_call(
            "oauth.access",
            client_id=self.oauth["client_id"],
            client_secret=self.oauth["client_secret"],
            code=code
        )

        if not auth_response.get('ok'):
            if auth_response.get('error') == 'code_already_used':
                return {
                    'text' : 'The application was connected with errors. Please, try to reinstall application',
                    'status' : 200
                }
            else:
                return {
                    'text' : 'Error occured in authentification proccess',
                    'status' : 200
                }
        else:
            team_id = auth_response["team_id"]
            authed_teams[team_id] = {
                "bot_token" : auth_response["bot"]["bot_access_token"]
            }

            token = authed_teams[team_id]["bot_token"]

            # insert or update team_id and token to further bot usage
            broker.core.db.update(self.collection_name,
                                  {
                                    'team_id': team_id
                                  },
                                  {
                                    'team_id': team_id,
                                    'token': token
                                  },
                                  upsert=True)

            self.client = SlackClient(token)

        test_auth = False
        test_api = False

        # Auth test
        auth = self.client.api_call("auth.test")
        if auth.get('ok'):
            test_auth = True
            logging.debug("Slack Auth - OK...")

        # test API
        api = self.client.api_call("api.test")
        if api.get('ok'):
            test_api = True
            logging.debug("Slack API - OK...")

        if test_auth and test_api:
            return {
                'result' : auth_response,
                'text' : 'Application was authorized successfully!',
                'status': 200
            }
        else:
            return {
                'text' : 'Error. Token is not correct or you are not allowed to use API',
                'status': 200
            }