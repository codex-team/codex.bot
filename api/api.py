import json
import logging

import asyncio


class Api:

    def __init__(self, core):
        logging.info("Api started.")
        self.core = core

    @asyncio.coroutine
    def callback(self, channel, body, envelope, properties):
        print(" [x] Received %r" % body)
        try:
            message = json.loads(body)
            command = message['cmd']
            payload = message['payload']
            version = message['api']
            incoming_queue = message['queue']

            if not version == "v1":
                logging.debug("Try to send")
                yield from self.core.send("{'result': 'Version invalid'}", incoming_queue)

            # TODO: Parse message
            """
            1. Register module
            2. Register commands from messengers
            """

        except Exception as e:
            logging.error(e)


