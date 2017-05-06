from .base import Base, message


class Photo(Base):

    __name__ = "Photo"

    method = 'sendPhoto'

    @message
    def send(self, photo, caption=None, **kwargs):

        if not photo:
            raise Exception('Photo is required')

        payload = {}

        files = {
            'photo': open(photo, 'rb'),
        }

        if caption:
            payload['caption'] = caption

        return {
            'payload': payload,
            'files': files,
            'method': self.method
        }