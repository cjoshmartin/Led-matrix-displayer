from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests
from io import BytesIO
import emoji
from random import randrange
import os

folder_path = os.path.dirname(os.path.abspath(__file__)) 

class display:
    def __init__(self, matrix_size, name, db, color):
        self.__font = ImageFont.truetype("FreeSans.ttf", 11)
        self.__font_color = color
        self.__width, self.__height = matrix_size
        self.__username = name
        self.__db  = db
    
    def __get_user_img(self):
        mask = Image.open('mask.png').convert('L')

        response = requests.get(self.__db.get_data()["users"][self.__username]["profile_picture"])
        image = Image.open(BytesIO(response.content))

        image  = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        image.putalpha(mask)

        image.thumbnail((self.__width/2,self.__height/2), Image.ANTIALIAS)

        image_width, image_height = image.size

        return image_width, image_height, image
    
    def __output(self, to_paste=None,background_color=(0,0,0)):
        img = Image.new('RGB',(self.__width,self.__height), background_color)
        
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
        _text ="The following message is from "+ self.set_username(self.__username) + "..." 
        text_image = Image.new('RGB',(len(_text)*32, 15))

        draw = ImageDraw.Draw(text_image)
        font = self.__font
        text_width, text_height = draw.textsize(_text)
        draw.text(
                (0,0),
                _text,
                self.__font_color,
                font=self.__font, 
                )

        output_imgs = []
        xpos = 0
        
        while xpos < text_width:

            concat_images = [
                        (image,(15,15)),
                        (text_image, (-xpos, 0))
                        ]

            output_imgs.append(self.__output(concat_images))
            xpos += 1

        return output_imgs

    def message(self):

        _payments_dict = self.__db.get_data()["payments"]
        _timestamp = self.__db.get_data()["users"][self.__username]["usage"][0]
        _a_payment = '"' +emoji.demojize(_payments_dict[_timestamp]["message"]).encode('ascii', 'ignore') + '"'

        text_image = Image.new('RGB',(32 * len(_a_payment) , 32))

        draw = ImageDraw.Draw(text_image)
        font = self.set_font(15)
        print(_a_payment)
        text_width, text_height = draw.textsize(_a_payment)

        draw.text(
                (0,0),
                _a_payment,
                self.__font_color,
                font=font, 
                align="center"
                )

        output_imgs = []
        xpos = 0
        
        while xpos < (text_width * 1.2):

            concat_images = [
                        (text_image, (-xpos, 0))
                        ]

            output_imgs.append(self.__output(concat_images))
            xpos += 1
        
        # del self.__db.data["payments"][_timestamp]

        # if len(self.__db.data["users"][self.__username]["usage"]) < 2:
            # del self.__db.data["users"][self.__username]
        # else:
            # del self.__db.data["users"][self.__username]["usage"][0]

        # if "past-payments" in  self.__db.data:
            # if not _timestamp in  self.__db.data['past-payments']:
                # self.__db.data['past-payments'].append(_timestamp)
        # else:
            # self.__db.data['past-payments'] = [_timestamp]

        # self.__db.put(self.__db.data)

        return output_imgs

    def instructions(self):
        background_color =(256,256,256)
        _text = "Thanks Mom For Helping Me Get Here!"
        
        text_image = Image.new('RGB',(32 * len(_text) , 15) )

        draw = ImageDraw.Draw(text_image)
        font = self.set_font(15)
        text_width, text_height = draw.textsize(_text)

        draw.text(
                (0,0),
                _text,
                self.__font_color,
                font=font, 
                align="center"
                )

        output_imgs = []
        xpos = 0
        
        while xpos < (text_width * 1.2):

            concat_images = [
                        (text_image, (-xpos, 0))
                        ]

            _color = (randrange(265),randrange(265),randrange(265))
            output_imgs.append(self.__output(concat_images, _color))
            xpos += 1

        return output_imgs

#   helper functions

    def set_font(self, size=10):
        return ImageFont.truetype("FreeSans.ttf", size)

    def set_font_color(self, color):
        self.__font_color = color

    def set_username(self, name):
        _username ="@" + name
        return _username

    def set_data(self, name, data):
        self.__username = self.set_username(name)
        self.__data = data
