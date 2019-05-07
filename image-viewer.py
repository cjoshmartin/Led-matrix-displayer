#!/usr/bin/env python
import time
import sys

from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

from database import firebase_db
from led_matrix import led_matrix


## Loading Env variables
folder_path = os.path.dirname(os.path.abspath(__file__)) 
env_path =  folder_path + '/.env'
print "Loading env: " + env_path 
load_dotenv(dotenv_path=env_path, verbose=True)


DB = firebase_db(folder_path +  "/" + ".service-account-file.json", os.getenv('DB_URL'))
DB.printer()

matrix = led_matrix()

mask = Image.open('mask.png').convert('L')
name = DB.keys()[1]
url = DB.data[name]["profile_picture"]
username = "@" + name

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
draw.text((0,0),username,(255,0,0),font=font, align="center")

img = Image.new('RGB',(matrix.width, matrix.height))

img.paste(image,((matrix.width - image_width)/2,0))
img.paste(text_image, (0, ((matrix.height + image_height) - text_height)/2))


# Make image fit our screen.
img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.display(img)

try:
    print("Press CTRL-C to stop.")
    i = 5
    while i > 0:
        time.sleep(1)
        i-= 1
        print(i)
except KeyboardInterrupt:
    sys.exit(0)

print("Exiting...")
