#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests
from io import BytesIO

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
# options.brightness= 60

matrix = RGBMatrix(options = options)

mask = Image.open('mask.png').convert('L')
url = "https://venmopics.appspot.com/u/v1/m/732a8c89-05be-46e3-bdbe-6153a30e95b4"
name = "@baby-yezzus"
response = requests.get(url)
image = Image.open(BytesIO(response.content))

image  = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
image.putalpha(mask)

image.thumbnail((matrix.width/2, matrix.height/2), Image.ANTIALIAS)

image_width, image_height = image.size

text_image = Image.new('RGB',(32, 32))

draw = ImageDraw.Draw(text_image)
font = ImageFont.truetype("FreeSans.ttf", 10)
text_width, text_height = draw.textsize(name)
draw.text((0,0), name,(255,0,0),font=font, align="center")

# text_image.thumbnail((matrix.width/2, matrix.height/2), Image.ANTIALIAS)

img = Image.new('RGB',(matrix.width, matrix.height))

img.paste(image,((matrix.width - image_width)/2,0))
img.paste(text_image, (0, ((matrix.height + image_height) - text_height)/2))


# Make image fit our screen.
img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(img.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
