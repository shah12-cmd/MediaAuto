from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.db import init_db, get_session
from src.models import Source, User, Log
from src.logger import logger
from sqlmodel import select
from passlib.context import CryptContext
from src.config import settings

app = FastAPI(title='MediaAuto Panel')

templates = Jinja2Templates(directory='src/templates')
app.mount('/static', StaticFiles(directory='src/static'), name='static')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    return get_session()

@app.on_event('startup')
def startup():
    init_db()
    # ensure admin user
    db = get_session()
    user = db.exec(select(User).where(User.username==settings.PANEL_ADMIN_USER)).first()
    if not user:
        user = User(username=settings.PANEL_ADMIN_USER, hashed_password=pwd_context.hash(settings.PANEL_ADMIN_PASS), is_admin=True)
        db.add(user)
        db.commit()

@app.get('/', response_class=HTMLResponse)
def dashboard(request: Request):
    db = get_session()
    sources = db.exec(select(Source)).all()
    logs = db.exec(select(Log).order_by(Log.created_at.desc()).limit(50)).all()
    return templates.TemplateResponse('dashboard.html', {'request': request, 'sources': sources, 'logs': logs})

@app.post('/sources/add')
def add_source(name: str = Form(...), peer: str = Form(...)):
    db = get_session()
    s = Source(name=name, peer=peer)
    db.add(s)
    db.commit()
    return RedirectResponse(url='/', status_code=303)

@app.post('/sources/delete')
def del_source(id: int = Form(...)):
    db = get_session()
    s = db.get(Source, id)
    if s:
        db.delete(s)
        db.commit()
    return RedirectResponse(url='/', status_code=303)
