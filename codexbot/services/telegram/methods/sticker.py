from .base import Base, message


class Sticker(Base):

    __name__ = "Sticker"

    method = 'sendSticker'

    @message
    def send(self, sticker, **kwargs):

        if not sticker:
            raise Exception('Path to sticker or sticker id is required')


        payload = {
            'sticker': sticker,
        }

        return {
            'payload': payload,
            'method': self.method
        }