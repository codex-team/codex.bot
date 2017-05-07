from .base import Base, message


class Video(Base):

    __name__ = "Video"

    method = 'sendVideo'

    @message
    def send(self, video, caption=None, duration=None, width=None, height=None, **kwargs):
        """
        Sends video to chat
        Use @message decorator
        
        :param video: path to file
        :param caption: 
        :param duration: 
        :param width: 
        :param height: 
        :param kwargs: 
        :return: 
        """
        if not video:
            raise Exception('Video is required')

        payload = {}

        files = {
            'video': open(video, 'rb'),
        }

        if caption:
            payload['caption'] = caption
        if duration:
            payload['duration'] = duration
        if height:
            payload['height'] = height
        if width:
            payload['width'] = width

        return {
            'payload': payload,
            'files': files,
            'method': self.method
        }