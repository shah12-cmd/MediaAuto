import openai
from src.config import settings
from src.logger import logger

openai.api_key = settings.OPENAI_API_KEY

def rewrite_caption(text: str, mode: str='shorten') -> str:
    if not openai.api_key:
        return text
    prompt = ''
    if mode == 'shorten':
        prompt = f"Shorten and make this text catchy for a Telegram post (keep it Persian if input is Persian):\n\n{text}\n\nShort version:" 
    elif mode == 'emoji':
        prompt = f"Add relevant emojis and make this text more engaging:\n\n{text}\n\nResult:" 
    else:
        prompt = f"Rewrite the following text to be more engaging for social media:\n\n{text}\n\nRewritten:" 
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role":"user","content":prompt}],
            max_tokens=200
        )
        out = resp.choices[0].message.content.strip()
        return out
    except Exception:
        logger.exception('OpenAI rewrite failed')
        return text
