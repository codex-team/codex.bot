from .base import Base, message


class Message(Base):

    __name__ = "Message"

    methods = {
        'send': 'sendMessage',
        'forward': 'forwardMessage'
    }

    @message
    def send(self, text, parse_mode=None, disable_web_page_preview=True, **kwargs):

        if not text:
            raise Exception('Message text is required')

        payload = {
            'text': text
        }

        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_web_page_preview:
            payload['disable_web_page_preview'] = disable_web_page_preview

        return {
            'payload': payload,
            'method': self.methods['send']
        }

    @message
    def forward(self, from_chat_id, message_id, **kwargs):

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
