from os import getenv
from dotenv import load_dotenv
load_dotenv()

API_ID = int(getenv('API_ID'))
API_HASH = getenv('API_HASH')
BOT_TOKEN = getenv('BOT_TOKEN')
SUDO = getenv('SUDO')
BOT_USERNAME = getenv('BOT_USERNAME')
REDIES_SERVER = getenv('REDIES_SERVER')
REDIES_PASSWORD = getenv('REDIES_PASSWORD')
REDIES_PORT = getenv('REDIES_PORT')