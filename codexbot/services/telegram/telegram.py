import logging
from urllib.parse import urlencode

import requests

from codexbot.globalcfg import URL
from codexbot.lib.server import http_response
from .config import BOT_NAME, API_TOKEN, API_URL, CALLBACK_ROUTE
from .methods.message import Message
from .methods.photo import Photo
from .methods.sticker import Sticker
from .methods.video import Video

from .types.update import Update


class Telegram:

    __name__ = "Telegram"
    routes = []

    def __init__(self):
        self.__token = API_TOKEN
        self.__api_url = API_URL + API_TOKEN + '/'
        self.__callback_url = URL + CALLBACK_ROUTE
        self.__callback_route = CALLBACK_ROUTE
        self.__bot_name = BOT_NAME

        self.routes = [
            ('POST', CALLBACK_ROUTE, self.telegram_callback)
        ]

        self.message = Message(self.__api_url)
        self.photo = Photo(self.__api_url)
        self.sticker = Sticker(self.__api_url)
        self.video = Video(self.__api_url)

        logging.debug("Telegram service initiated.")

    @http_response
    async def telegram_callback(self, params):
        """
        Process messages from telegram bot
        :return:
        """
        logging.info("Got telegram callback {}".format(params['json']))

        # Parse telegram message
        update = Update(params['json'])

        if update.message:
            await self.send_message_to_app(update)
        elif update.callback_query:
            await self.send_callback_query_to_app(update)

        return {
            'text' : 'ok',
            'status' : 200
        }

    async def send_message_to_app(self, update):
        if update.message.user.username:
            username = update.message.user.username
        else:
            username = update.message.user.first_name

        # Pass commands from message data to broker
        await self.broker.commands_to_app({
            'chat': {
                'id': update.message.chat.id,
                'type': update.message.chat.type
            },
            'user': {
                'id': update.message.user.id,
                'username': username,
                'lang': update.message.user.language_code
            },
            'service': self.__name__,
            'commands': update.get_commands(),
            'text': update.message.text
        })

    async def send_callback_query_to_app(self, update):
        if update.callback_query.user.username:
            username = update.callback_query.user.username
        else:
            username = update.callback_query.user.first_name

        await self.broker.callback_query_to_app({
            'chat': {
                'id': update.callback_query.message.chat.id,
                'type': update.callback_query.message.chat.type
            },
            'user': {
                'id': update.callback_query.user.id,
                'username': username,
                'lang': update.callback_query.user.language_code
            },
            'service': self.__name__,
            'data': update.callback_query.data
        })

    def run(self, broker):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.broker = broker
        self.set_webhook()

    def set_webhook(self):
        query = self.__api_url + 'setWebhook?' + urlencode({
            'url': self.__callback_url
        })

        try:
            result = requests.get(query)
        except Exception as e:
            logging.debug(e)
        else:
            logging.debug(result.content)

    def send(self, chat_id, message_payload):
        """
        Send message to chat
        
         :param message_payload:
            - chat_hash  - chat hash
            - text       - message text
            - parse_mode - message parse mode type
            - photo      - photo to send (you shouldn't pass text param if you want to send photo)
            - caption    - caption for photo
            For markups see https://core.telegram.org/bots/api#replykeyboardmarkup
            - markup:
                - keyboard
                - inline_keyboard
                - remove_keyboard
                - force_reply
        
        :param chat_id: 
        :return: 
        """
        if 'text' in message_payload:
            message = message_payload['text']

            parse_mode = message_payload.get('parse_mode', None)

            if 'markup' in message_payload:
                markup = message_payload['markup']
                self.message.set_reply_markup(markup.get('keyboard', None),
                                              markup.get('inline_keyboard', None),
                                              markup.get('remove_keyboard', None),
                                              markup.get('force_reply', None))

            self.message.send(chat_id, message, parse_mode)
            return

        if 'photo' in message_payload:
            photo = message_payload['photo']
            caption = None
            if 'caption' in message_payload:
                caption = message_payload['caption']
            self.photo.send(chat_id, photo, caption)
            return
