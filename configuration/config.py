from .settings import SERVER, RABBITMQ, URL


class Config:

    __name__ = "Global config"

    def __init__(self):
        self.__server = SERVER
        self.__rabbitmq = RABBITMQ
        self.__url = URL

    def server(self):
        return self.__server['host'], self.__server['port']

    def rabbitmq(self):
        return self.__rabbitmq

    def url(self):
        return self.__url