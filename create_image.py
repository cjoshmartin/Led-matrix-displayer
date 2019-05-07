from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests
from io import BytesIO


class display:
    def __init__(self, matrix_size):
        self.__font = ImageFont.truetype("FreeSans.ttf", 10)
        self.__font_color = (255, 0, 0)
        self.__width, self.__height = matrix_size

    def user(self, name, url):
        mask = Image.open('mask.png').convert('L')
        username = "@" + name

        response = requests.get(url)
        image = Image.open(BytesIO(response.content))

        image  = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        image.putalpha(mask)

        image.thumbnail((self.__width/2,self.__height/2), Image.ANTIALIAS)

        image_width, image_height = image.size

        text_image = Image.new('RGB',(32, 32))

        draw = ImageDraw.Draw(text_image)
        font = self.__font
        text_width, text_height = draw.textsize(name)
        draw.text(
                (0,0),
                username,
                self.__font_color,
                font=self.__font, 
                align="center"
                )

        img = Image.new('RGB',(self.__width,self.__height))

        img.paste(image,((self.__width - image_width)/2,0))
        img.paste(text_image, (0, ((self.__height + image_height) - text_height)/2))

        # Make image fit our screen.
        img.thumbnail((self.__width,self.__height), Image.ANTIALIAS)

        return img

    def message(self):
        pass # TODO: Create how messages are displayed

    def set_font(self, size=10):
        self.__font = ImageFont.truetype(font, size)

    def set_font_color(self, color):
        self.__font_color = color
