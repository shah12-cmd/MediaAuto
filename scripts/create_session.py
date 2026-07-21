#!/usr/bin/env python3
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from src.config import settings

SESSION_FILE = 'data/session'

if __name__ == '__main__':
    client = TelegramClient(SESSION_FILE, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    client.start(phone=settings.TELEGRAM_PHONE)
    print('Session created at', SESSION_FILE)
