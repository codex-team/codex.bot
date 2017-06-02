from .base import Base, message


class Photo(Base):

    __name__ = "Photo"

    method = 'sendPhoto'

    @message
    def send(self, photo, caption=None, **kwargs):
        """
        Send photo to chat
        Use @message decorator
        
        :param photo: url to image
        :param caption: 
        :param kwargs: 
        :return: 
        """

        if not photo:
            raise Exception('Photo is required')

        payload = {
            'photo': photo
        }

        if caption:
            payload['caption'] = caption

        return {
            'payload': payload,
            'method': self.method
        }