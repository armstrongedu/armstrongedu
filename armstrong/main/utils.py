from PIL import Image, ImageDraw, ImageFont
from django.conf import settings


def gen_cert(course, student):
    im = Image.open(r'C:\Users\Rahul sinha\Desktop\Python Learning Jupyter\new.jpg')
    d = ImageDraw.Draw(im)
    location = (100, 398)
    text_color = (0, 137, 209)
    font = ImageFont.truetype("arial.ttf", 120)
    d.text(location, i, fill = text_color, font = font)
    im.save("certificate_" + i + ".pdf")

def localize(template_name):
    name, extention = template_name.split('.')
    return f'{name}{"_ar" if settings.AS_LANG == "ar" else ""}.{extention}'
