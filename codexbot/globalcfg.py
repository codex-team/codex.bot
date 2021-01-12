import logging
import os

from yaml import safe_load as safe_load_yaml

BOT_CONFIG_FILE_PATH = os.environ.get(
    'BOT_CONFIG_FILE_PATH',
    './cfg/bot/global.yml'
)

##
# Main URL for services callbacks
# Should use https protocol
##
URL = ''

# HTTP server settings
SERVER = {
    'host': '127.0.0.1',
    'port': 1337
}

# RabbitMQ server settings
RABBITMQ = {
    'host': '127.0.0.1',
}

# DB settings
DB = {
    'name': 'default',
    'host': '127.0.0.1',
    'port': 27017
}

# i18n dir location
I18N_LOCATION = 'i18n'


def load_global_yaml_config(yaml_cfg: dict) -> "None":
    global URL, I18N_LOCATION, SERVER, RABBITMQ, DB

    URL = yaml_cfg.get('URL', '')

    I18N_LOCATION = yaml_cfg.get('I18N_LOCATION', 'i18n')

    RABBITMQ = yaml_cfg.get('RABBITMQ', {
        'host': '127.0.0.1',
    })

    DB = yaml_cfg.get('DB', {
        'name': 'default',
        'host': '127.0.0.1',
        'port': 27017
    }
                      )
    SERVER = yaml_cfg.get('SERVER', {
        'host': '127.0.0.1',
        'port': 1337
    })


if BOT_CONFIG_FILE_PATH is None:
    logging.warning('BOT_CONFIG_FILE_PATH not set')
elif not os.path.exists(BOT_CONFIG_FILE_PATH):
    logging.warning('BOT_CONFIG_FILE_PATH not exists')
else:
    with open(BOT_CONFIG_FILE_PATH) as cfg:
        yaml = safe_load_yaml(cfg)
        load_global_yaml_config(yaml)
