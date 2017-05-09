import requests
import logging


def message(function):

    def decorator(self, chat_id, *args, **kwargs):

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

        if len(files.keys()):
            result = requests.post(self.api_url + data['method'], data=data['payload'], files=files)
        else:
            result = requests.post(self.api_url + data['method'], json=data['payload'])

        if result.status_code != 200:
            logging.debug('Error while sending Telegram message: {}'.format(result.content))
            return False

        return True

    return decorator

class Base:

    __name__ = "Telegram object interface"

    def __init__(self, api_url):
        self.api_url = api_url

    reply_markup = {}

    def set_reply_markup(self, keyboard=None, inline_keyboard=None, remove_keyboard=None, force_reply=None):
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