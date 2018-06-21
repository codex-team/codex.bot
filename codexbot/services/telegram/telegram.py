import json
import logging
from urllib.parse import urlencode

import requests

from codexbot.globalcfg import URL
from codexbot.lib.server import http_response
from .config import BOT_NAME, API_TOKEN, API_URL, CALLBACK_ROUTE
from .methods.message import Message
from .types.message import Message as MessageType
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
            ('POST', CALLBACK_ROUTE + '/{bot:.*}', self.telegram_callback),
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
        update = Update(params)

        if update.message:
            await self.send_message_to_app(update)
        elif update.callback_query:
            await self.send_callback_query_to_app(update)

        return {
            'text': 'ok',
            'status': 200
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
            'text': update.message.text,
            'bot': update.bot_id
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
            'data': update.callback_query.data,
            'bot': update.bot_id
        })

    def run(self, broker):
        """
        Make all stuff. For example, initialize process. Or just nothing.
        :return:
        """
        self.broker = broker
        self.set_webhook()
        #TODO: Maybe to reset webhooks for hijacked bots

    def set_webhook(self, api_token=None, callback_url=None):
        if not api_token:
            api_token = API_TOKEN

        if not callback_url:
            callback_url = CALLBACK_ROUTE

        query = API_URL + api_token + '/setWebhook?' + urlencode({
            'url': URL + callback_url
        })

        try:
            result = requests.get(query)
        except Exception as e:
            logging.debug(e)
        else:
            result_content = result.content
            logging.debug(result_content)
            return result_content

    def del_webhook(self, api_token):
        try:
            result = requests.get(API_URL + api_token + '/deleteWebhook')
        except Exception as e:
            logging.debug(e)
        else:
            logging.debug(result)

    async def send(self, chat_id, message_payload, app=None):
        """
        Send message to chat
        
         :param message_payload:
            - chat_hash     - chat hash
            - text          - message text
            – update_id     – message id for update. None if add new.
            – want_response – if you want to get response from service to app queue. default = False.
            - parse_mode    - message parse mode type
            - disable_web_page_preview - if it is needed to disable link preview
            - photo         - photo to send (you shouldn't pass text param if you want to send photo)
            - caption       - caption for photo
            For markups see https://core.telegram.org/bots/api#replykeyboardmarkup
            - markup:
                - keyboard
                - inline_keyboard
                - remove_keyboard
                - force_reply
        
        :param chat_id:
        :param app_data: dict
            'token':        application token,
            'name':         application name,
            'queue':        queue name,
            'host':         application host address,
            'port':         application port,
            'description':  application description
        :return: 
        """
        bot = message_payload.get('bot', None)
        if bot:
            bot = self.broker.api.bots.get(int(bot), None)
            if not bot:
                logging.debug("Bot not found!", message_payload)
                return
            bot_token = bot['data']['api_token']
        else:
            bot_token = None

        update_id = message_payload.get('update_id', None)

        if 'text' in message_payload:
            message = message_payload['text']

            parse_mode = message_payload.get('parse_mode', None)
            disable_web_page_preview = message_payload.get('disable_web_page_preview', False)

            if 'markup' in message_payload:
                markup = message_payload['markup']
                self.message.set_reply_markup(markup.get('keyboard', None),
                                              markup.get('inline_keyboard', None),
                                              markup.get('remove_keyboard', None),
                                              markup.get('force_reply', None))

            result = self.message.send(chat_id, message, parse_mode, disable_web_page_preview, bot_token=bot_token, update_id=update_id)
            want_response = message_payload.get('want_response', False)
            if app and want_response and result:
                message = json.dumps({
                    'command': 'callback query',
                    'payload': result['result'],
                    'want_response': want_response
                })
                await self.broker.add_to_app_queue(message, app['queue'], app['host'])
            return

        if 'photo' in message_payload:
            photo = message_payload['photo']
            caption = None
            if 'caption' in message_payload:
                caption = message_payload['caption']
            self.photo.send(chat_id, photo, caption, bot_token=bot_token, update_id=update_id)
            return

    def getMe(self, api_token=None):
        if not api_token:
            api_token = self.__token

        try:
            result = requests.get(API_URL + api_token + "/getMe")
            data = json.loads(result.text)
            return data

        except Exception as e:
            logging.debug(e)
