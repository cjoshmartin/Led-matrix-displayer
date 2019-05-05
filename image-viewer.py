#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image,ImageOps
import requests
from io import BytesIO

mask = Image.open('mask.png').convert('L')

url = "https://venmopics.appspot.com/u/v1/m/732a8c89-05be-46e3-bdbe-6153a30e95b4"
name = "Josh Martin"
response = requests.get(url)
image = Image.open(BytesIO(response.content))

image  = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
image.putalpha(mask)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
options.brightness= 60

matrix = RGBMatrix(options = options)

# Make image fit our screen.
image.thumbnail((matrix.width/2, matrix.height/2), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
