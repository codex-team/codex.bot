from configuration.config import Config
from .settings import BOT_NAME, API_TOKEN, API_URL, CALLBACK_ROUTE


class TelegramConfig(Config):

    __name__ = "Telegram config"

    def __init__(self):
        super().__init__()

        self.__token = API_TOKEN
        self.__api_url = API_URL + API_TOKEN + '/'
        self.__callback_url = self.url() + CALLBACK_ROUTE
        self.__callback_route = CALLBACK_ROUTE
        self.__bot_name = BOT_NAME

    def token(self):
        return self.__token

    def api_url(self):
        return self.__api_url

    def callback_url(self):
        return self.__callback_url

    def callback_route(self):
        return self.__callback_route

    def bot_name(self):
        return self.__bot_name