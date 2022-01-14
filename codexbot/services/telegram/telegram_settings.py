import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

BOT_NAME = os.environ.get("TELEGRAM_BOT_NAME")

CALLBACK_ROUTE = os.environ.get("TELEGRAM_CALLBACK_ROUTE")

API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

API_URL = os.environ.get("TELEGRAM_API_URL")
