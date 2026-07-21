import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN','')
    TELEGRAM_API_ID: int = int(os.getenv('TELEGRAM_API_ID','0') or 0)
    TELEGRAM_API_HASH: str = os.getenv('TELEGRAM_API_HASH','')
    TELEGRAM_PHONE: str = os.getenv('TELEGRAM_PHONE','')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY','')
    MEDIA_DIR: str = os.getenv('MEDIA_DIR','data/media')
    PANEL_ADMIN_USER: str = os.getenv('PANEL_ADMIN_USER','admin')
    PANEL_ADMIN_PASS: str = os.getenv('PANEL_ADMIN_PASS','changeme')

settings = Settings()

# Ensure directories
os.makedirs(settings.MEDIA_DIR, exist_ok=True)
