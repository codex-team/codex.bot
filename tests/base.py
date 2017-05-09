import json


class BaseTest(object):
    """This object represents a Base test and its sets of functions."""

    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)

    @staticmethod
    def is_json(string):
        try:
            json.loads(string)
        except ValueError:
            return False

        return True
