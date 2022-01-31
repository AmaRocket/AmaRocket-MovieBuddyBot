import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# bot token
TOKEN = os.getenv("TOKEN")

# api tmdb key
API_KEY = os.getenv('API_KEY')  # v3



# Postgres
PGHOST = os.getenv('PGHOST')
PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('PG_PASS')
DB_NAME = os.getenv('DB_NAME')


# For the FUTURE
I18N_DOMAIN = 'MovieBuddyBot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
