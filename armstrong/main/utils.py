from pathlib import Path
import os

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings


def gen_cert(course, std):
    BASE_DIR = Path(__file__).resolve().parent.parent
    im = Image.open(os.path.join(BASE_DIR, 'main_static') + '/cert.jpg')
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype('main/cert.ttf', 100)
    d.text((300, 270,), std.name, fill=0, font=font)
    im.save(f'uploads/{course.id}-{std.id}.pdf')

def localize(template_name):
    name, extention = template_name.split('.')
    return f'{name}{"_ar" if settings.AS_LANG == "ar" else ""}.{extention}'
