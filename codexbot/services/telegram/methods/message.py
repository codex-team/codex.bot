from .base import Base, message


class Message(Base):

    __name__ = "Message"

    methods = {
        'send': 'sendMessage',
        'edit': 'editMessageText',
        'forward': 'forwardMessage'
    }

    @message
    def send(self, text, parse_mode=None, disable_web_page_preview=False, update_id=None, **kwargs):
        """
        Send message to chat
        Use @message decorator
        
        :param text: 
        :param parse_mode: Markdown or HTML
        :param disable_web_page_preview: if True, disable links preview
        :param kwargs: 
        :return: message payload
        """

        if not text:
            raise Exception('Message text is required')

        payload = {
            'text': text
        }

        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_web_page_preview:
            payload['disable_web_page_preview'] = disable_web_page_preview
        if update_id:
            payload['message_id'] = int(update_id)

        return {
            'payload': payload,
            'method': self.methods['send'] if not update_id else self.methods['edit']
        }

    @message
    def forward(self, from_chat_id, message_id, **kwargs):
        """
        Forward message
        Use @message decorator
        
        :param from_chat_id: chat to forward from
        :param message_id: message to forward
        :param kwargs: 
        :return:
        """

        if not from_chat_id:
            raise Exception('Chat id to forward from is required')

        if not message_id:
            raise Exception('Message id is required')

        payload = {
            'from_chat_id': from_chat_id,
            'message_id': message_id
        }

        return {
            'payload': payload,
            'method': self.methods['forward']
        }
