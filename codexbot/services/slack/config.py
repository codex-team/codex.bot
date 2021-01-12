import logging
import os

from yaml import safe_load as safe_load_yaml

BOT_SLACK_CONFIG_FILE_PATH = os.environ.get(
    'BOT_SLACK_CONFIG_FILE_PATH',
    './cfg/bot/slack/config.yml'
)

BOT_NAME = ''
CLIENT_ID = ''
CLIENT_SECRET = ''
VERIFICATION = ''


def load_slack_yaml_config(yaml_cfg: dict) -> "None":
    global BOT_NAME, CLIENT_ID, CLIENT_SECRET, VERIFICATION

    BOT_NAME = yaml_cfg.get('BOT_NAME', '')
    CLIENT_ID = yaml_cfg.get('CLIENT_ID', '')
    CLIENT_SECRET = yaml_cfg.get('CLIENT_SECRET', '')
    VERIFICATION = yaml_cfg.get('VERIFICATION', '')


if BOT_SLACK_CONFIG_FILE_PATH is None:
    logging.warning('BOT_SLACK_CONFIG_FILE_PATH not set')
elif not os.path.exists(BOT_SLACK_CONFIG_FILE_PATH):
    logging.warning('BOT_SLACK_CONFIG_FILE_PATH not exists')
else:
    with open(BOT_SLACK_CONFIG_FILE_PATH) as cfg:
        yaml = safe_load_yaml(cfg)
        load_slack_yaml_config(yaml)
