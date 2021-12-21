import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)


BOT_NAME = os.environ.get("SLACK_BOT_NAME")

CLIENT_ID = os.environ.get("SLACK_CLIENT_ID")

CLIENT_SECRET = os.environ.get("SLACK_CLIENT_SECRET")