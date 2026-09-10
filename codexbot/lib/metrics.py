import aiohttp.web
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest


messages_sent = Counter(
    'codexbot_messages_sent_total',
    'Messages passed from an application to a messenger service',
    ['app', 'chat']
)

telegram_api_requests = Counter(
    'codexbot_telegram_api_requests_total',
    'Telegram API calls by method and response code',
    ['method', 'code']
)

telegram_rate_limited = Counter(
    'codexbot_telegram_rate_limited_total',
    'Telegram API calls rejected with 429 Too Many Requests',
    ['method']
)

last_send_success = Gauge(
    'codexbot_last_send_success_timestamp_seconds',
    'Unix time of the last successful Telegram API call'
)


async def metrics_handler(request):
    return aiohttp.web.Response(
        body=generate_latest(),
        headers={'Content-Type': CONTENT_TYPE_LATEST}
    )
