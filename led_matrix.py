import os

import load_env_variables

build_device = os.getenv("BUILD_DEVICE")

if build_device == "target":
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

elif build_device == 'simulator':
    print("sim")
    import cv2
    import numpy as np

else:
   raise Exception(" `{}` is not a vaild build device type.".format(build_device))  


class led_matrix:
    def __init__(self):
        # Configuration for the matrix
        self.__options = RGBMatrixOptions()
        self.__options.rows = 32
        self.__options.chain_length = 1
        self.__options.parallel = 1
        self.__options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
        self.__options.brightness= 100

        self.matrix = RGBMatrix(options = self.__options)
        self.size = (self.matrix.width, self.matrix.height)

    def display(self, image):
        self.matrix.SetImage(image.convert('RGB'))        

    def set_settings(self):
        pass # TODO: Don't know how to update LED matrix setting on the fly yet

class mock_matrix:
    def __init__(self):
        self.size = (32,32)

    def display(self, image): 
        __image = np.array(image.convert('RGB'))
        cv2.imshow('image', cv2.resize(__image, (300, 300)))
        cv2.waitKey(1)

def Matrix_Factory():
    _instance = None

    if build_device == "target":
        _instance = led_matrix()

    elif build_device == 'simulator':
        _instance = mock_matrix()

    return _instance


