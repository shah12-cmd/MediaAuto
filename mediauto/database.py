"""Database management for MediaAuto"""

import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, List

logger = logging.getLogger(__name__)

Base = declarative_base()


class SourceChannel(Base):
    """Source channel model"""
    __tablename__ = "source_channels"
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(String, unique=True, nullable=False)
    channel_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MessageHistory(Base):
    """Message history model"""
    __tablename__ = "message_history"
    
    id = Column(Integer, primary_key=True)
    source_channel_id = Column(String)
    source_message_id = Column(String)
    destination_message_id = Column(String, unique=True)
    content_hash = Column(String, unique=True)
    is_processed = Column(Boolean, default=False)
    sent_at = Column(DateTime, default=datetime.utcnow)


class BotLog(Base):
    """Bot log model"""
    __tablename__ = "bot_logs"
    
    id = Column(Integer, primary_key=True)
    level = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSession(Base):
    """User session model"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    authenticated = Column(Boolean, default=False)
    last_activity = Column(DateTime, default=datetime.utcnow)


class Settings(Base):
    """Settings model"""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, database_url: str = "sqlite:///./data/mediauto.db"):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self.init_db()
    
    def init_db(self) -> None:
        """Initialize database"""
        try:
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False} if "sqlite" in self.database_url else {}
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def add_source_channel(self, channel_id: str, channel_name: str) -> bool:
        """Add source channel"""
        try:
            session = self.get_session()
            existing = session.query(SourceChannel).filter_by(channel_id=channel_id).first()
            if existing:
                logger.warning(f"Channel {channel_id} already exists")
                session.close()
                return False
            
            channel = SourceChannel(channel_id=channel_id, channel_name=channel_name)
            session.add(channel)
            session.commit()
            session.close()
            logger.info(f"Added source channel: {channel_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding source channel: {e}")
            return False
    
    def get_source_channels(self) -> List[SourceChannel]:
        """Get all active source channels"""
        try:
            session = self.get_session()
            channels = session.query(SourceChannel).filter_by(is_active=True).all()
            session.close()
            return channels
        except Exception as e:
            logger.error(f"Error getting source channels: {e}")
            return []
    
    def remove_source_channel(self, channel_id: str) -> bool:
        """Remove source channel"""
        try:
            session = self.get_session()
            channel = session.query(SourceChannel).filter_by(channel_id=channel_id).first()
            if channel:
                session.delete(channel)
                session.commit()
                session.close()
                logger.info(f"Removed source channel: {channel_id}")
                return True
            session.close()
            return False
        except Exception as e:
            logger.error(f"Error removing source channel: {e}")
            return False
    
    def check_message_exists(self, content_hash: str) -> bool:
        """Check if message already processed"""
        try:
            session = self.get_session()
            exists = session.query(MessageHistory).filter_by(content_hash=content_hash).first()
            session.close()
            return exists is not None
        except Exception as e:
            logger.error(f"Error checking message: {e}")
            return False
    
    def add_message_to_history(self, source_channel_id: str, source_message_id: str,
                               destination_message_id: str, content_hash: str) -> bool:
        """Add message to history"""
        try:
            session = self.get_session()
            message = MessageHistory(
                source_channel_id=source_channel_id,
                source_message_id=source_message_id,
                destination_message_id=destination_message_id,
                content_hash=content_hash,
                is_processed=True
            )
            session.add(message)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error adding message to history: {e}")
            return False
    
    def add_log(self, level: str, message: str) -> bool:
        """Add log entry"""
        try:
            session = self.get_session()
            log = BotLog(level=level, message=message)
            session.add(log)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error adding log: {e}")
            return False
    
    def get_logs(self, limit: int = 100) -> List[BotLog]:
        """Get recent logs"""
        try:
            session = self.get_session()
            logs = session.query(BotLog).order_by(BotLog.created_at.desc()).limit(limit).all()
            session.close()
            return logs
        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return []
    
    def set_setting(self, key: str, value: str) -> bool:
        """Set a setting"""
        try:
            session = self.get_session()
            setting = session.query(Settings).filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = Settings(key=key, value=value)
                session.add(setting)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error setting configuration: {e}")
            return False
    
    def get_setting(self, key: str, default: str = None) -> Optional[str]:
        """Get a setting"""
        try:
            session = self.get_session()
            setting = session.query(Settings).filter_by(key=key).first()
            session.close()
            return setting.value if setting else default
        except Exception as e:
            logger.error(f"Error getting setting: {e}")
            return default
    
    def get_statistics(self) -> dict:
        """Get bot statistics"""
        try:
            session = self.get_session()
            total_messages = session.query(MessageHistory).count()
            total_channels = session.query(SourceChannel).count()
            active_channels = session.query(SourceChannel).filter_by(is_active=True).count()
            session.close()
            
            return {
                "total_messages": total_messages,
                "total_channels": total_channels,
                "active_channels": active_channels
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}


# Global database manager
db_manager = None


def init_database(database_url: str = "sqlite:///./data/mediauto.db") -> DatabaseManager:
    """Initialize global database manager"""
    global db_manager
    db_manager = DatabaseManager(database_url)
    return db_manager


def get_db() -> DatabaseManager:
    """Get global database manager"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager
