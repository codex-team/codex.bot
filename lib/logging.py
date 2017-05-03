import logging

class Logging:

    def __init__(self):
        logger = logging.getLogger('asyncio')

        logger.setLevel(logging.DEBUG)
        format_str = "%(filename)-20s:%(lineno)-4s %(funcName)20s() \t %(message)s "

        logging.basicConfig(level=logging.DEBUG, format=format_str)
        logging.debug("Logging initiated.")
