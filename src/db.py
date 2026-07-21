from sqlmodel import create_engine, Session
from sqlmodel import SQLModel
from pathlib import Path

DB_FILE = Path(__file__).resolve().parents[1] / 'data' / 'mediaauto.db'
DB_FILE.parent.mkdir(parents=True, exist_ok=True)
ENGINE = create_engine(f"sqlite:///{DB_FILE}", echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(ENGINE)

def get_session():
    return Session(ENGINE)
