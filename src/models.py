from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Source(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    peer: str  # username or channel id
    enabled: bool = True
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class MediaItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: Optional[int]
    message_id: Optional[int]
    file_path: Optional[str]
    caption: Optional[str]
    sent_to: Optional[str]
    hash: Optional[str]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    is_admin: bool = False
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cron_expr: str
    enabled: bool = True

class Log(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level: str
    message: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
