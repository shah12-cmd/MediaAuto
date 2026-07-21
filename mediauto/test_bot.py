"""Test suite for MediaAuto bot"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from mediauto.config import BotConfig, ConfigManager
from mediauto.database import DatabaseManager, SourceChannel
from mediauto.content_processor import ContentProcessor
import tempfile
import os


class TestBotConfig(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.json")
    
    def test_config_initialization(self):
        """Test config initialization with defaults"""
        config = BotConfig()
        self.assertEqual(config.telegram_token, "")
        self.assertEqual(config.api_id, 0)
        self.assertFalse(config.ai_enabled)
    
    def test_config_manager_save_load(self):
        """Test saving and loading configuration"""
        manager = ConfigManager(self.config_path)
        manager.config.telegram_token = "test_token"
        manager.config.api_id = 12345
        manager.save_config()
        
        # Load in new manager
        new_manager = ConfigManager(self.config_path)
        self.assertEqual(new_manager.config.telegram_token, "test_token")
        self.assertEqual(new_manager.config.api_id, 12345)
    
    def test_config_validation(self):
        """Test configuration validation"""
        config_mgr = ConfigManager()
        is_valid, errors = config_mgr.validate_config()
        self.assertFalse(is_valid)
        self.assertTrue(len(errors) > 0)


class TestDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        self.db = DatabaseManager("sqlite:///:memory:")
    
    def test_add_source_channel(self):
        """Test adding source channel"""
        result = self.db.add_source_channel("@testchannel", "Test Channel")
        self.assertTrue(result)
        
        # Try adding duplicate
        result = self.db.add_source_channel("@testchannel", "Test Channel")
        self.assertFalse(result)
    
    def test_get_source_channels(self):
        """Test getting source channels"""
        self.db.add_source_channel("@channel1", "Channel 1")
        self.db.add_source_channel("@channel2", "Channel 2")
        
        channels = self.db.get_source_channels()
        self.assertEqual(len(channels), 2)
    
    def test_remove_source_channel(self):
        """Test removing source channel"""
        self.db.add_source_channel("@channel1", "Channel 1")
        result = self.db.remove_source_channel("@channel1")
        self.assertTrue(result)
        
        channels = self.db.get_source_channels()
        self.assertEqual(len(channels), 0)
    
    def test_message_history(self):
        """Test message history tracking"""
        hash1 = "abc123"
        exists = self.db.check_message_exists(hash1)
        self.assertFalse(exists)
        
        self.db.add_message_to_history("@channel", "123", "456", hash1)
        exists = self.db.check_message_exists(hash1)
        self.assertTrue(exists)
    
    def test_statistics(self):
        """Test getting statistics"""
        self.db.add_source_channel("@channel1", "Channel 1")
        self.db.add_message_to_history("@channel1", "123", "456", "hash1")
        
        stats = self.db.get_statistics()
        self.assertEqual(stats.get("total_messages"), 1)
        self.assertEqual(stats.get("total_channels"), 1)
        self.assertEqual(stats.get("active_channels"), 1)


class TestContentProcessor(unittest.TestCase):
    """Test content processing"""
    
    def setUp(self):
        self.config = {
            "remove_channel_links": True,
            "remove_channel_ids": False,
            "remove_ads": True,
            "remove_extra_hashtags": True,
            "ad_text": "Check our channel!",
            "destination_channel": "@mychannel",
        }
        self.processor = ContentProcessor(self.config)
    
    def test_remove_channel_links(self):
        """Test removing channel links"""
        text = "Check out @channel1 and @channel2 for more"
        result = self.processor.remove_channel_links(text)
        self.assertNotIn("@channel1", result)
        self.assertNotIn("@channel2", result)
    
    def test_remove_urls(self):
        """Test removing URLs"""
        text = "Visit https://example.com or http://test.org"
        result = self.processor.remove_urls(text)
        self.assertNotIn("https://", result)
        self.assertNotIn("http://", result)
    
    def test_process_caption(self):
        """Test full caption processing"""
        text = "Check @channel1 at https://example.com #hashtag"
        result = self.processor.process_caption(text)
        self.assertNotIn("@channel1", result)
        self.assertNotIn("https://example.com", result)
        self.assertIn("Check our channel!", result)  # ad_text added
    
    def test_shorten_text(self):
        """Test text shortening"""
        long_text = "a" * 600
        result = self.processor.shorten_text(long_text, max_length=500)
        self.assertEqual(len(result), 503)  # 500 - 3 for '...'
    
    def test_make_text_attractive(self):
        """Test adding emojis"""
        text = "This is a video about music"
        result = self.processor.make_text_attractive(text)
        # Check if emojis were added
        self.assertTrue(len(result) > len(text))


class TestContentHash(unittest.TestCase):
    """Test content hashing"""
    
    def test_calculate_hash(self):
        """Test hash calculation"""
        from mediauto.content_processor import calculate_media_hash
        
        content = b"test content"
        hash1 = calculate_media_hash(content)
        hash2 = calculate_media_hash(content)
        
        # Same content should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Different content should produce different hash
        hash3 = calculate_media_hash(b"different content")
        self.assertNotEqual(hash1, hash3)


if __name__ == "__main__":
    unittest.main()
