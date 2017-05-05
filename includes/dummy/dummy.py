import logging


class Dummy:

    __name__ = "Dummy"

    def __init__(self):
        logging.debug("Dummy module initiated.")

    def run(self, api):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        pass

    def get_routes(self):
        routes = []
        return routes
