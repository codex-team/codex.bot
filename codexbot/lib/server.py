import aiohttp.web


def http_response(function):
    async def wrapper(self, request):
        text = await request.text()
        post = await request.post()
        try:
            json = await request.json()
        except Exception as e:
            json = {}
        result = function(self, text, post, json)
        return aiohttp.web.Response(text="OK")
    return wrapper


class Server:

    def __init__(self, event_loop, host='localhost', port=1337):
        self.event_loop = event_loop
        self.host, self.port = host, port
        self.web_server = aiohttp.web.Application(loop=self.event_loop)

    def set_routes(self, routes):
        """
        TODO: Check if route is already defined.
        :param routes:
        :return:
        """
        for route in routes:
            self.web_server.router.add_route(*route)

    def start(self):
        aiohttp.web.run_app(self.web_server, host=self.host, port=self.port)
