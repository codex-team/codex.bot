class Message():

    def __init__(self):
        pass

    def getMessage(self, event):
        if 'user' in event and 'text' in event:
            print('got message {}', format(event))

        elif 'previous_message' in event:
            print('got deleted message {}', format(event.get('previous_message')))
