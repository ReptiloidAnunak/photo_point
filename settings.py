
import os
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"

TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE")
TWILIO_SID = os.getenv("TWILIO_SID")


TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_BOT_CHAT = os.getenv("TG_BOT_CHAT")