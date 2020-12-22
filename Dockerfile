# todo: python:7-slim -> ERROR: Failed building wheel for multidict
# todo: python:3.5.3-slim -> SyntaxError: invalid syntax
#   File "/usr/local/lib/python3.7/site-packages/aiohttp/helpers.py", line 29
#       ensure_future = asyncio.async

FROM python:3.6.9

WORKDIR /home/bot
COPY requirements.txt .
RUN pip install -r requirements.txt