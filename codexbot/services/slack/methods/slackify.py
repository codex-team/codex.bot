from html.parser import HTMLParser
from html.entities import name2codepoint


class Slackify(HTMLParser):
    def __init__(self, html, *args, **kwargs):

        # call parent constructor __init__
        super().__init__(*args, **kwargs)

        # slackified string
        self.output = ''

        # send to HTMLParser feed function to parse HTML string
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        """
        Create slack markdown

        https://api.slack.com/docs/message-formatting

        :param tag: income tag, that will be switched into slack supported markdown 
        :param attrs: we need to recover attributes of anchor
        :return: 
        """

        if tag == 'b' or tag == 'strong':
            self.output += ' *'
        if tag == 'i' or tag == 'em':
            self.output += ' _'
        if tag == 'code':
            self.output += ' `'
        if tag == 'a':
            self.output += ' <'
            for attr in attrs:
                self.output += attr[1] + '|'

    def handle_endtag(self, tag):
        """
        https://api.slack.com/docs/message-formatting
        :param tag: endtag. Close tag via markdown 
        :return: 
        """
        if tag == 'b' or tag == 'strong':
            self.output += '* '
        if tag == 'i' or tag == 'em':
            self.output += '_ '
        if tag == 'a':
            self.output += '> '
        if tag == 'code':
            self.output += '` '

    def handle_data(self, data):
        """
        concatenate TEXT nodes into output
        :param data: 
        :return: 
        """
        self.output += data

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        pass

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))

    def handle_decl(self, data):
        pass

    def get_output(self):
        """
        substitute multiple whitespace with single whitespace

        link: https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
        :return: 
        """
        return ' '.join(self.output.split())