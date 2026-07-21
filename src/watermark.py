from PIL import Image, ImageDraw, ImageFont
import subprocess
import os
from src.logger import logger

def watermark_image(input_path: str, output_path: str, text: str='@MediaAuto'):
    try:
        im = Image.open(input_path).convert('RGBA')
        txt = Image.new('RGBA', im.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt)
        font_size = max(12, im.size[0]//20)
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except Exception:
            font = ImageFont.load_default()
        margin = 10
        text_w, text_h = draw.textsize(text, font=font)
        x = im.size[0] - text_w - margin
        y = im.size[1] - text_h - margin
        draw.text((x,y), text, fill=(255,255,255,200), font=font)
        out = Image.alpha_composite(im, txt)
        out.convert('RGB').save(output_path, 'JPEG')
        return output_path
    except Exception:
        logger.exception('watermark image failed')
        return input_path

def watermark_video(input_path: str, output_path: str, text: str='@MediaAuto'):
    # Use ffmpeg drawtext filter (requires libfreetype)
    cmd = [
        'ffmpeg','-y','-i', input_path,
        '-vf', f"drawtext=text='{text}':fontcolor=white@0.8:fontsize=24:x=w-tw-10:y=h-th-10",
        '-codec:a','copy', output_path
    ]
    try:
        subprocess.check_call(cmd)
        return output_path
    except Exception:
        logger.exception('watermark video failed')
        return input_path
