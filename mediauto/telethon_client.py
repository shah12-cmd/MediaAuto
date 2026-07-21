"""Telethon client for Telegram interactions"""

import logging
import asyncio
from typing import Optional, List, Callable
from telethon import TelegramClient, events
from telethon.tl.types import Message

logger = logging.getLogger(__name__)


class TelethonBot:
    """Telethon-based Telegram client for automated interactions"""
    
    def __init__(self, api_id: int, api_hash: str, phone_number: str, session_name: str = "mediauto_session"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_name = session_name
        self.client = None
        self.message_handler: Optional[Callable] = None
    
    async def connect(self) -> bool:
        """Connect to Telegram"""
        try:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
            await self.client.connect()
            
            # Check if already authorized
            if not await self.client.is_user_authorized():
                await self.client.send_code_request(self.phone_number)
                code = input("Enter the code sent to Telegram: ")
                
                # Try to sign in
                try:
                    await self.client.sign_in(self.phone_number, code)
                except Exception as e:
                    # 2FA might be required
                    if "password" in str(e).lower():
                        password = input("Enter your 2FA password: ")
                        await self.client.sign_in(password=password)
                    else:
                        raise
            
            logger.info("Successfully connected to Telegram")
            return True
        
        except Exception as e:
            logger.error(f"Error connecting to Telegram: {e}")
            return False
    
    async def disconnect(self) -> None:
        """Disconnect from Telegram"""
        if self.client:
            await self.client.disconnect()
            logger.info("Disconnected from Telegram")
    
    async def get_messages(self, channel: str, limit: int = 100) -> List[Message]:
        """Get recent messages from a channel"""
        try:
            entity = await self.client.get_entity(channel)
            messages = await self.client.get_messages(entity, limit=limit)
            logger.info(f"Retrieved {len(messages)} messages from {channel}")
            return messages
        except Exception as e:
            logger.error(f"Error getting messages from {channel}: {e}")
            return []
    
    async def forward_message(self, message: Message, destination: str) -> Optional[Message]:
        """Forward a message to destination"""
        try:
            dest_entity = await self.client.get_entity(destination)
            forwarded = await self.client.forward_messages(dest_entity, message)
            logger.info(f"Forwarded message to {destination}")
            return forwarded
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")
            return None
    
    async def send_message(self, destination: str, message: str) -> Optional[Message]:
        """Send a text message"""
        try:
            dest_entity = await self.client.get_entity(destination)
            sent = await self.client.send_message(dest_entity, message)
            logger.info(f"Sent message to {destination}")
            return sent
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    async def send_photo(self, destination: str, photo_path: str, caption: str = None) -> Optional[Message]:
        """Send a photo"""
        try:
            dest_entity = await self.client.get_entity(destination)
            sent = await self.client.send_file(dest_entity, photo_path, caption=caption)
            logger.info(f"Sent photo to {destination}")
            return sent
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            return None
    
    async def send_video(self, destination: str, video_path: str, caption: str = None) -> Optional[Message]:
        """Send a video"""
        try:
            dest_entity = await self.client.get_entity(destination)
            sent = await self.client.send_file(dest_entity, video_path, caption=caption)
            logger.info(f"Sent video to {destination}")
            return sent
        except Exception as e:
            logger.error(f"Error sending video: {e}")
            return None
    
    async def send_file(self, destination: str, file_path: str, caption: str = None) -> Optional[Message]:
        """Send a file"""
        try:
            dest_entity = await self.client.get_entity(destination)
            sent = await self.client.send_file(dest_entity, file_path, caption=caption)
            logger.info(f"Sent file to {destination}")
            return sent
        except Exception as e:
            logger.error(f"Error sending file: {e}")
            return None
    
    async def download_media(self, message: Message, download_path: str) -> Optional[str]:
        """Download media from message"""
        try:
            if message.media:
                path = await self.client.download_media(message.media, download_path)
                logger.info(f"Downloaded media to {path}")
                return path
        except Exception as e:
            logger.error(f"Error downloading media: {e}")
        return None
    
    def register_message_handler(self, func: Callable) -> None:
        """Register a message handler"""
        self.message_handler = func
        
        # Set up event handler
        if self.client:
            @self.client.on(events.NewMessage)
            async def handler(event):
                await self.message_handler(event.message)
    
    async def listen(self) -> None:
        """Start listening for new messages"""
        if self.client:
            await self.client.run_until_disconnected()
    
    async def get_channel_info(self, channel: str) -> dict:
        """Get information about a channel"""
        try:
            entity = await self.client.get_entity(channel)
            return {
                "id": entity.id,
                "title": getattr(entity, "title", None),
                "username": getattr(entity, "username", None),
                "description": getattr(entity, "description", None),
                "members": getattr(entity, "participants_count", None),
            }
        except Exception as e:
            logger.error(f"Error getting channel info: {e}")
            return {}
