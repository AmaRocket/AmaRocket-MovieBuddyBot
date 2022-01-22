import os
from dotenv import load_dotenv

load_dotenv()

# bot token
TOKEN = os.getenv("TOKEN")

# api tmdb key
API_KEY = os.getenv('API_KEY')  # v3

# postgres
DB_URI = os.getenv('URI')
