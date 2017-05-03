import requests
from aiohttp import web

class SlackCallbacks:

    def __init__(self):
        pass

    def send_message(self):
        pass

    async def open_ifmo(self):
        r = requests.get('http://ifmo.su')
        return web.Response(text=r.text)


    def say_hello(self):
        print("hello")

    def say_bye(self):
        print("bye")