class Base:

    __name__ = "Keyboards interface"
    keyboard = []

    def row(self, *args):
        self.keyboard.append(list(args))
        return list(args)


class ReplyKeyboard(Base):

    __name__ = "Reply Keyboard Markup"

    @staticmethod
    def button(text, request_contact=False, request_location=False):

        return {
            'text': text,
            'request_contact': request_contact,
            'request_location': request_location
        }

    def get(self, resize_keyboard=True, one_time_keyboard=False, selective=False):

        if len(self.keyboard) == 0:
            return None

        return {
            'keyboard': self.keyboard,
            'resize_keyboard': resize_keyboard,
            'one_time_keyboard': one_time_keyboard,
            'selective': selective
        }

    def remove(self, selective=False):
        return {
            'remove_keyboard': True,
            'selective': selective
        }


class InlineKeyboard(Base):

    __name__ = "Inline Keyboard Markup"

    @staticmethod
    def button(text, callback_data=None, url=None, switch_inline_query=None, switch_inline_query_current_chat=None):

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

        if len(self.keyboard) == 0:
            return None

        return self.keyboard


class ForceReply:

    __name__ = "Force Reply"

    @staticmethod
    def get(selective=False):
        return {
            'force_reply': True,
            'selective': selective
        }