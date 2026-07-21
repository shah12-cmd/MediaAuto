from sqlmodel import Session, select
from src.db import get_session
from src.models import MediaItem

def remove_duplicates():
    db = get_session()
    items = db.exec(select(MediaItem)).all()
    seen = set()
    for it in items:
        if it.hash in seen:
            db.delete(it)
        else:
            seen.add(it.hash)
    db.commit()
