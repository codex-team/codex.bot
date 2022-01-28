import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

URL = os.environ.get("URL")

SERVER_HOST = os.environ.get("SERVER_HOST")
SERVER_PORT = int(os.environ.get("SERVER_PORT"))

RABBITMQ = os.environ.get("RABBITMQ_URL")

DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = int(os.environ.get("DATABASE_PORT"))

