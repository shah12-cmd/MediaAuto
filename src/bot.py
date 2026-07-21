from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from src.config import settings
from src.logger import logger
from src.db import get_session
from src.models import Source, MediaItem
import hashlib
import os

SESSION_FILE = 'data/session'

def make_client():
    if settings.TELEGRAM_BOT_TOKEN:
        client = TelegramClient(SESSION_FILE, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH).start(bot_token=settings.TELEGRAM_BOT_TOKEN)
    else:
        client = TelegramClient(SESSION_FILE, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    return client

async def ensure_logged_in(client: TelegramClient):
    if not await client.is_user_authorized() and not settings.TELEGRAM_BOT_TOKEN:
        await client.start(phone=settings.TELEGRAM_PHONE)

async def fetch_and_store(client: TelegramClient, peer: str):
    # Fetch newest messages and store media
    try:
        msgs = await client.get_messages(peer, limit=10)
        session = get_session()
        for m in msgs:
            if not m.media:
                continue
            key = f"{peer}:{m.id}"
            h = hashlib.sha256(key.encode()).hexdigest()
            exists = session.query(MediaItem).filter(MediaItem.hash==h).first()
            if exists:
                continue
            # Download media to file
            fpath = None
            try:
                fpath = await client.download_media(m, file=os.path.join('data','media'))
            except Exception:
                logger.exception('telethon download failed')
            item = MediaItem(source_id=None, message_id=m.id, file_path=fpath, caption=m.message or '', hash=h)
            session.add(item)
            session.commit()
            logger.info(f"Stored media {fpath}")
    except Exception:
        logger.exception('fetch_and_store failed')

async def run_fetcher():
    client = make_client()
    await ensure_logged_in(client)
    await client.connect()
    session = get_session()
    sources = session.query(Source).filter(Source.enabled==True).all()
    for s in sources:
        await fetch_and_store(client, s.peer)
    await client.disconnect()
