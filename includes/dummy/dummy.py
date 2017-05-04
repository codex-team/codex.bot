import logging


class Dummy:

    __name__ = "Dummy"

    def __init__(self):
        logging.debug("Dummy module initiated.")

    def run(self, server, api):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        pass
