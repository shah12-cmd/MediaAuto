import os
import subprocess
from pathlib import Path
from typing import Optional
from src.logger import logger

YT_DLP = 'yt-dlp'

def download_media(url: str, out_dir: Optional[str]=None) -> Optional[str]:
    out_dir = out_dir or os.getenv('MEDIA_DIR','data/media')
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    # Build yt-dlp command
    out_template = str(Path(out_dir)/'%(id)s.%(ext)s')
    cmd = [YT_DLP, '--no-warnings', '--no-progress', '-o', out_template, url]
    try:
        logger.info(f"Downloading {url} -> {out_dir}")
        subprocess.check_call(cmd)
        # Find file (last modified)
        files = sorted(Path(out_dir).glob('*'), key=lambda p: p.stat().st_mtime, reverse=True)
        if files:
            return str(files[0])
    except subprocess.CalledProcessError as e:
        logger.exception('yt-dlp failed')
    return None
