#!/usr/bin/env python3
"""
Helper script to create a Telethon session in a headless environment.
This script ensures the repository root is on sys.path so `import src` works
when the script is executed from the scripts/ directory.
"""
from pathlib import Path
import sys

# Ensure repo root is on sys.path so `import src.*` works when running this script
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Now imports should resolve
from telethon import TelegramClient
from src.config import settings

SESSION_FILE = str(REPO_ROOT / 'data' / 'session')

def main():
    # ensure data dir exists
    (REPO_ROOT / 'data').mkdir(parents=True, exist_ok=True)

    print('Using repository root:', REPO_ROOT)
    print('Session file:', SESSION_FILE)
    print('Starting Telethon interactive login...')

    client = TelegramClient(SESSION_FILE, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    client.start(phone=settings.TELEGRAM_PHONE)
    print('Session created at', SESSION_FILE)

if __name__ == '__main__':
    main()
