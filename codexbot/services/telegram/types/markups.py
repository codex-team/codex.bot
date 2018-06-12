class Base:
    """
    Interface for Telegram markup keyboard objects
    """

    __name__ = "Telegram keyboards interface"

    def __init__(self):
        self.keyboard = []

    def row(self, *args):
        """
        Append arguments to keyboard as new row
        
        :param args: Reply or Inline Keyboard objects 
        :return: 
        """

        self.keyboard.append(list(args))
        return list(args)


class ReplyKeyboard(Base):

    # https://core.telegram.org/bots/api#replykeyboardmarkup
    __name__ = "Telegram Reply Keyboard Markup"

    # https://core.telegram.org/bots/api#inlinekeyboardbutton
    @staticmethod
    def button(text, request_contact=False, request_location=False):
        """
        Returns ReplyKeyboardButton object
        
        :param text: button label
        :param request_contact: if True, button requests user's phone contact
        :param request_location: if True, button requests user's location request 
        :return: ReplyKeyboardButton object
        """

        return {
            'text': text,
            'request_contact': request_contact,
            'request_location': request_location
        }

    def get(self, resize_keyboard=True, one_time_keyboard=False, selective=False):
        """
        Returns ReplyKeyboard object
        Keyboard array is stored in self.keyboard
        
        :param resize_keyboard: if True, keyboard will be fit to buttons labels
        :param one_time_keyboard: if True, keyboard will be removed after pressing the button
        :param selective: if True, keyboard will be shown only for mentioned users or for user, whose message is under reply
        :return: InlineKeyboard object
        """

        if len(self.keyboard) == 0:
            return None

        return {
            'keyboard': self.keyboard,
            'resize_keyboard': resize_keyboard,
            'one_time_keyboard': one_time_keyboard,
            'selective': selective
        }

    # https://core.telegram.org/bots/api#replykeyboardremove
    def remove(self, selective=False):
        return {
            'remove_keyboard': True,
            'selective': selective
        }


class InlineKeyboard(Base):

    # https://core.telegram.org/bots/api#inlinekeyboardmarkup
    __name__ = "Telegram Inline Keyboard Markup"

    def __init__(self, *rows):
        super(InlineKeyboard, self).__init__()
        for row in rows:
            self.row(*row)

    # https://core.telegram.org/bots/api#keyboardbutton
    @staticmethod
    def button(text, callback_data=None, url=None, switch_inline_query=None, switch_inline_query_current_chat=None):
        """
        Returns InlineKeyboardButton object
        
        :param text: button label
        :param callback_data: data, which will be send as inline query if user press the button
        :param url: url to open when user press the button
        :param switch_inline_query: if set, requests user to select chat and fill input field with passed data 
        :param switch_inline_query_current_chat: if set, fill input field in current chat with passed data
        :return: InlineKeyboardButton object
        """

        button = {
            'text': str(text),
            'callback_data': str(text)
        }

        if callback_data:
            button['callback_data'] = callback_data
        if url:
            button['url'] = url
        if switch_inline_query:
            button['switch_inline_query'] = switch_inline_query
        if switch_inline_query_current_chat:
            button['switch_inline_query_current_chat'] = switch_inline_query_current_chat

        return button

    def get(self):
        """
        Returns InlineKeyboard object
        Keyboard array is stored in self.keyboard
        
        :return: InlineKeyboard object
        """

        if len(self.keyboard) == 0:
            return None

        return self.keyboard


class ForceReply:

    # https://core.telegram.org/bots/api#forcereply
    __name__ = "Telegram Force Reply"

    @staticmethod
    def get(selective=False):
        """
        Returns ReplyKeyboardRemove object
        
        :param selective: if True, remove keyboard only for mentioned users, or for user, whose message is under reply
        :return: ReplyKeyboardRemove object 
        """

        return {
            'force_reply': True,
            'selective': selective
        }