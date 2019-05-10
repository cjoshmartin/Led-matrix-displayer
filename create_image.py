from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests
from io import BytesIO
import emoji

class display:
    def __init__(self, matrix_size, name,data):
        self.__font = ImageFont.truetype("FreeSans.ttf", 10)
        self.__font_color = (255, 0, 0)
        self.__width, self.__height = matrix_size
        self.__username = self.set_username(name)
        self.__data = data
    
    def __get_user_img(self):
        mask = Image.open('mask.png').convert('L')

        response = requests.get(self.__data["profile_picture"])
        image = Image.open(BytesIO(response.content))

        image  = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        image.putalpha(mask)

        image.thumbnail((self.__width/2,self.__height/2), Image.ANTIALIAS)

        image_width, image_height = image.size

        return image_width, image_height, image
    
    def __output(self, to_paste=None):
        img = Image.new('RGB',(self.__width,self.__height))
        
        if to_paste is not None:
            for paste in to_paste:
                img.paste(paste[0], paste[1])
        else:
            print("Nothing to paste on image")

        # Make image fit our screen.
        img.thumbnail((self.__width,self.__height), Image.ANTIALIAS)

        return img
        
    def user(self):

        image_width, image_height, image = self.__get_user_img()

        text_image = Image.new('RGB',(32, 32))

        draw = ImageDraw.Draw(text_image)
        font = self.__font
        text_width, text_height = draw.textsize(self.__username)
        draw.text(
                (0,0),
                self.__username,
                self.__font_color,
                font=self.__font, 
                align="center"
                )

        concat_images = [
                    (image,((self.__width - image_width)/2,0)),
                    (text_image, (0, ((self.__height + image_height) - text_height)/2))
                    ]

        return self.__output(concat_images)

    def message(self):
        text_image = Image.new('RGB',(32, 32))

        draw = ImageDraw.Draw(text_image)
        font = self.__font
        _payments_dict = self.__data["payments"]
        _a_payment = '"' +emoji.demojize(_payments_dict[_payments_dict.keys()[0]]["message"]) + '"'
        print(_a_payment)
        text_width, text_height = draw.textsize(_a_payment)

        draw.text(
                (0,0),
                _a_payment,
                self.__font_color,
                font=self.__font, 
                align="center"
                )

        concat_images = [
               (text_image, (0,0)) 
                ]
        return self.__output(concat_images)

    def set_font(self, size=10):
        self.__font = ImageFont.truetype(font, size)

    def set_font_color(self, color):
        self.__font_color = color

    def set_username(self, name):
        _username ="@" + name
        return _username

    def set_data(self, name, data):
        self.__username = self.set_username(name)
        self.__data = data
