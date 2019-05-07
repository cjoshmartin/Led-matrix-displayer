from rgbmatrix import RGBMatrix, RGBMatrixOptions

class led_matrix:
    def __init__(self):
        # Configuration for the matrix
        self.__options = RGBMatrixOptions()
        self.__options.rows = 32
        self.__options.chain_length = 1
        self.__options.parallel = 1
        self.__options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
        # self.__options.brightness= 60

        self.matrix = RGBMatrix(options = self.__options)
        self.width = self.matrix.width
        self.height = self.matrix.height

    def display(self, image):
        self.matrix.SetImage(image.convert('RGB'))        

    def set_settings(self):
        pass # TODO: Don't know how to update LED matrix setting on the fly yet

