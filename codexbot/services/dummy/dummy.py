import logging


class Dummy:

    __name__ = "Dummy"
    routes = []

    def __init__(self):
        self.get_routes()
        logging.debug("Dummy module initiated.")

    def run(self, broker):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        pass

    def get_routes(self):
        pass
