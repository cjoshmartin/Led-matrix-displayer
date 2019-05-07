from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests
from io import BytesIO

def create_image(name, url, matrix_size):

    mask = Image.open('mask.png').convert('L')
    username = "@" + name
    _width,_height = matrix_size

    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    image  = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    image.putalpha(mask)

    image.thumbnail((_width/2, _height/2), Image.ANTIALIAS)

    image_width, image_height = image.size

    text_image = Image.new('RGB',(32, 32))

    draw = ImageDraw.Draw(text_image)
    font = ImageFont.truetype("FreeSans.ttf", 10)
    text_width, text_height = draw.textsize(name)
    draw.text((0,0),username,(255,0,0),font=font, align="center")

    img = Image.new('RGB',(_width, _height))

    img.paste(image,((_width - image_width)/2,0))
    img.paste(text_image, (0, ((_height + image_height) - text_height)/2))

    # Make image fit our screen.
    img.thumbnail((_width, _height), Image.ANTIALIAS)

    return img
