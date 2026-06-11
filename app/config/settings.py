import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

LOSS_ALERT_THRESHOLD = 5

DATABASE_URL = "sqlite:///data/database.db"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
