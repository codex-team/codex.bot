import requests
import logging
import json

from codexbot.services.telegram.config import API_URL


def message(function):
    """
    Decorator for telegram sending methods    
    :param function: 
    :return: 
    """

    def decorator(self, chat_id, *args, **kwargs):
        """
        Telegram methods wrapper.
        Gets required :param chat_id:
        Optional keyword arguments:
        :argument reply_to_message_id: message to reply
        :argument disable_notification: if True, sending message silently
        :argument reply_markup: Telegram reply_markup object. Could be set by set_reply_markup
        :argument bot: Telegram bot ID. None if it is the core bot.
        
        :param self: 
        :param chat_id: 
        :param args: 
        :param kwargs: 
        :return True|False: True if message was sent successfully, False otherwise 
        """
        if not chat_id:
            raise Exception('Chat id is required')

        data = function(self, *args, **kwargs)

        data['payload']['chat_id'] = chat_id

        if 'reply_to_message_id' in kwargs:
            data['payload']['reply_to_message_id'] = kwargs['reply_to_message_id']

        if 'disable_notification' in kwargs:
            data['payload']['disable_notification'] = kwargs['disable_notification']

        if 'reply_markup' in kwargs:
            data['payload']['reply_markup'] = kwargs['reply_markup']
        elif len(self.reply_markup.keys()):
            data['payload']['reply_markup'] = self.reply_markup

        files = {}
        if 'files' in data:
            files = data['files']

        api_url = self.api_url
        if 'bot_token' in kwargs and kwargs['bot_token']:
            api_url = API_URL + kwargs['bot_token'] + "/"

        if len(files.keys()):
            data['payload']['reply_markup'] = json.dumps(data['payload']['reply_markup'])
            result = requests.post(api_url + data['method'], data=data['payload'], files=files)
        else:
            result = requests.post(api_url + data['method'], json=data['payload'])

        self.clear_reply_markup()

        if result.status_code != 200:
            logging.debug('Error while sending Telegram message: {}'.format(result.content))
            return False

        return True

    return decorator


class Base:
    """
    Interface for Telegram objects
    """

    __name__ = "Telegram object interface"

    def __init__(self, api_url):
        self.api_url = api_url
        self.reply_markup = {}

    def set_reply_markup(self, keyboard=None, inline_keyboard=None, remove_keyboard=None, force_reply=None):
        """
        Fill self.reply_markup.
        Message decorator use self.reply_markup to send markup to chat
        
        :param keyboard: Reply Keyboard object. Could be got by ReplyKeyboard class
        :param inline_keyboard: Inline Keyboard object. Could be got by InlineKeyboard class
        :param remove_keyboard: Reply Keyboard Remove object. Could be got by ReplyKeyboard class
        :param force_reply: Force Reply object. Could be got by ForceReply class
        """

        if keyboard:
            self.reply_markup['keyboard'] = keyboard['keyboard']
            self.reply_markup['resize_keyboard'] = keyboard['resize_keyboard']
            self.reply_markup['one_time_keyboard'] = keyboard['one_time_keyboard']
            self.reply_markup['selective'] = keyboard['selective']
        if inline_keyboard:
            self.reply_markup['inline_keyboard'] = inline_keyboard
        if remove_keyboard:
            self.reply_markup['remove_keyboard'] = remove_keyboard['remove_keyboard']
            self.reply_markup['selective'] = remove_keyboard['selective']
        if force_reply:
            self.reply_markup['force_reply'] = force_reply['force_reply']
            self.reply_markup['selective'] = force_reply['selective']

    def clear_reply_markup(self):
        self.reply_markup = {}