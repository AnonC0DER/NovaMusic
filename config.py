from os import getenv
from dotenv import load_dotenv
load_dotenv()

API_ID = int(getenv('API_ID'))
API_HASH = getenv('API_HASH')
BOT_TOKEN = getenv('BOT_TOKEN')
SUDO = getenv('SUDO')
BOT_USERNAME = getenv('BOT_USERNAME')
DB_HOST = getenv('DB_HOST')
DB_DATABASE = getenv('DB_DATABASE')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')