"""Content processing utilities for MediaAuto"""

import re
import logging
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import hashlib
import io

logger = logging.getLogger(__name__)


class ContentProcessor:
    """Process message content"""
    
    # Regex patterns
    CHANNEL_LINK_PATTERN = r'@[\w_]+'
    CHANNEL_ID_PATTERN = r'\b\d+\b'
    HASHTAG_PATTERN = r'#[\w]+'
    URL_PATTERN = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    def __init__(self, config):
        self.config = config
    
    def remove_channel_links(self, text: str) -> str:
        """Remove channel links like @channelname"""
        if not self.config.get("remove_channel_links", True):
            return text
        return re.sub(self.CHANNEL_LINK_PATTERN, '', text).strip()
    
    def remove_channel_ids(self, text: str) -> str:
        """Remove numeric IDs that might be channel references"""
        if not self.config.get("remove_channel_ids", True):
            return text
        # Be careful not to remove all numbers, just potential channel IDs
        return text
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text"""
        return re.sub(self.URL_PATTERN, '', text).strip()
    
    def remove_extra_hashtags(self, text: str) -> str:
        """Remove extra hashtags, keep only important ones"""
        if not self.config.get("remove_extra_hashtags", True):
            return text
        
        hashtags = re.findall(self.HASHTAG_PATTERN, text)
        if len(hashtags) > 5:
            # Remove hashtags, keep only text
            text = re.sub(self.HASHTAG_PATTERN, '', text).strip()
        
        return text
    
    def process_caption(self, caption: str) -> str:
        """Process caption with all enabled filters"""
        if not caption:
            return caption
        
        # Remove URLs first
        caption = self.remove_urls(caption)
        
        # Remove channel links
        caption = self.remove_channel_links(caption)
        
        # Remove extra hashtags
        caption = self.remove_extra_hashtags(caption)
        
        # Add advertisement text if configured
        if self.config.get("ad_text"):
            caption += f"\n\n{self.config.get('ad_text')}"
        
        # Add destination channel info
        if self.config.get("destination_channel"):
            dest_channel = self.config.get("destination_channel")
            channel_link = f"@{dest_channel}" if isinstance(dest_channel, str) else f"Channel {dest_channel}"
            caption += f"\n\n━━━━━━━━━━━━━\n📢 {channel_link}\n━━━━━━━━━━━━━"
        
        return caption
    
    def calculate_hash(self, content: bytes) -> str:
        """Calculate SHA256 hash of content"""
        return hashlib.sha256(content).hexdigest()
    
    def add_watermark(self, image_data: bytes, watermark_text: str = None,
                      watermark_image: str = None) -> Optional[bytes]:
        """Add watermark to image"""
        if not self.config.get("watermark_enabled", False):
            return image_data
        
        try:
            # Open image
            image = Image.open(io.BytesIO(image_data))
            
            # Use provided text or from config
            text = watermark_text or self.config.get("watermark_text", "MediaAuto")
            
            # Add text watermark
            if text:
                draw = ImageDraw.Draw(image)
                # Try to use a nice font, fallback to default
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
                except:
                    font = ImageFont.load_default()
                
                # Position in bottom right
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                position = (image.width - text_width - 10, image.height - text_height - 10)
                
                # Draw with semi-transparent background
                draw.text(position, text, font=font, fill=(255, 255, 255, 128))
            
            # Save to bytes
            output = io.BytesIO()
            image.save(output, format='PNG')
            return output.getvalue()
        
        except Exception as e:
            logger.error(f"Error adding watermark: {e}")
            return image_data
    
    def shorten_text(self, text: str, max_length: int = 500, suffix: str = "...") -> str:
        """Shorten text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    def make_text_attractive(self, text: str) -> str:
        """Add emojis and formatting to make text more attractive"""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Add emojis to common words
            if any(word in line.lower() for word in ['video', 'film', 'movie']):
                line = '🎬 ' + line if not line.startswith(('🎬', '📽️')) else line
            elif any(word in line.lower() for word in ['photo', 'image', 'picture']):
                line = '📸 ' + line if not line.startswith(('📸', '🖼️')) else line
            elif any(word in line.lower() for word in ['music', 'song', 'audio']):
                line = '🎵 ' + line if not line.startswith(('🎵', '🎶')) else line
            elif any(word in line.lower() for word in ['news', 'breaking']):
                line = '📰 ' + line if not line.startswith('📰') else line
            
            formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def translate_to_persian(self, text: str) -> str:
        """
        Translate text to Persian
        Note: This requires an external translation service
        For now, returning original text
        """
        # TODO: Implement actual translation using:
        # - Google Translate API
        # - Azure Translator
        # - or other service
        logger.warning("Translation service not yet implemented")
        return text


def calculate_media_hash(media_data: bytes) -> str:
    """Calculate hash for media content"""
    return hashlib.sha256(media_data).hexdigest()
