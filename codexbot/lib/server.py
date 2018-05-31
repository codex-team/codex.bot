import aiohttp.web


def http_response(function):
    async def wrapper(self, request):
        text = await request.text()
        post = await request.post()
        headers = request.headers
        params = request.match_info
        query = request.query

        try:
            json = await request.json()
        except Exception as e:
            json = {}
        result = await function(self, {
            'text': text,
            'post': post,
            'json': json,
            'params': params,
            'headers': headers,
            'query': query
        })

        response_text = result.get('text', '')
        response_status = result.get('status', 200)

        if response_status != 404:
            return aiohttp.web.Response(text=response_text)
        else:
            return aiohttp.web.HTTPNotFound(text=response_text)
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
