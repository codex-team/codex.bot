class Message():

    def __init__(self):
        """
        https://api.slack.com/docs/message-formatting
        
        Send formated message messages 
        """
        pass

    def getMessage(self, event):
        """
        get message payloads and use special templates to respond
        :param event: 
        :return: 
        """
        if 'user' in event and 'text' in event:
            print('got message {}', format(event))

        elif 'previous_message' in event:
            print('got deleted message {}', format(event.get('previous_message')))
