from .base import Base, message


class Sticker(Base):

    __name__ = "Sticker"

    method = 'sendSticker'

    @message
    def send(self, sticker, **kwargs):
        """
        Sends sticker to chat
        Use @message decorator
        
        :param sticker: sticker id or url to .webp file
        :param kwargs: 
        :return: 
        """

        if not sticker:
            raise Exception('Path to sticker or sticker id is required')

        payload = {
            'sticker': sticker,
        }

        return {
            'payload': payload,
            'method': self.method
        }