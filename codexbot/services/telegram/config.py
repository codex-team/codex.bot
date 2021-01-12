import logging
import os

from yaml import safe_load as safe_load_yaml

BOT_TELEGRAM_CONFIG_FILE_PATH = os.environ.get(
    'BOT_TELEGRAM_CONFIG_FILE_PATH',
    './cfg/bot/telegram/config.yml'
)

# Route for telegram callbacks. Should starts with /
CALLBACK_ROUTE = '/telegram/callback'

# Telegram bot name
BOT_NAME = '@yourbot'

# Telegram bot api token. You can get it from @BotFather
API_TOKEN = ''

CODEX_FATHER_BOT_API_TOKEN = ''

# URL to Telegram's bot API
API_URL = 'https://api.telegram.org/bot'


def load_telegram_yaml_config(yaml_cfg: dict) -> "None":
    global CALLBACK_ROUTE, BOT_NAME, API_TOKEN, CODEX_FATHER_BOT_API_TOKEN, API_URL

    CALLBACK_ROUTE = yaml_cfg.get('CALLBACK_ROUTE', '/telegram/callback')
    BOT_NAME = yaml_cfg.get('BOT_NAME', '@yourbot')
    API_TOKEN = yaml_cfg.get('API_TOKEN', '')
    CODEX_FATHER_BOT_API_TOKEN = yaml_cfg.get('CODEX_FATHER_BOT_API_TOKEN', '')
    API_URL = yaml_cfg.get('API_URL', 'https://api.telegram.org/bot')


if BOT_TELEGRAM_CONFIG_FILE_PATH is None:
    logging.warning('BOT_TELEGRAM_CONFIG_FILE_PATH not set')
elif not os.path.exists(BOT_TELEGRAM_CONFIG_FILE_PATH):
    logging.warning('BOT_TELEGRAM_CONFIG_FILE_PATH not exists')
else:
    with open(BOT_TELEGRAM_CONFIG_FILE_PATH) as cfg:
        yaml = safe_load_yaml(cfg)
        load_telegram_yaml_config(yaml)
