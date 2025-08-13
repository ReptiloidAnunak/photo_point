
import os
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

BASE_DIR = Path(__file__).parent


DATABASE_DIR = BASE_DIR / "database"
DATABASE = DATABASE_DIR / "app.db"
DATABASE_URL = 'sqlite:///database/app.db'


if not os.path.exists(DATABASE):
    with open(DATABASE, 'w'):
        pass


TEMPLATES_DIR = BASE_DIR / "templates"

PROVIDERS_LIST = ['sms', 'email', 'telegram']

TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE")
TWILIO_SID = os.getenv("TWILIO_SID")


TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")