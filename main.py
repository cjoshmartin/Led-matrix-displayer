#!/usr/bin/env python

# System
import time
import sys
import os

# Local 
from load_env_variables import folder_path
from database import matrix_db, internet_on
from led_matrix import Matrix_Factory
from create_image import display
import time
from random import randrange

matrix = Matrix_Factory()

# TODO: Get current day
# TODO: only grab venmo transactions from day of graduation and Sort by date/time in database
# TODO: Create a system to see which transactions have been already viewed and do no show them again
# DONE: Fix how user name are showed
# DONE: Instruction on how to use the venmo hat
# TODO: If transaction is less then $1, then send it back!
 
class Matrix_Service:
    def __init__(self):
         self.__db = None
         self.__image = None
         self.__user_index = 0

    def is_connected(self):
        if internet_on() and self.__db is None:
            self.__db = matrix_db(folder_path +  "/" + ".service-account-file.json", os.getenv('DB_URL'))
            self.__db.printer()
            return self.__db, self.__db.size()
        else:
            self.__db = None
            return self.__db, 1
        
    def __increment_user(self):
        _, _size = self.is_connected()
        self.__user_index = self.__user_index + 1 if self.__user_index < _size - 1 else 0 

    def show_image_buffer(self, image_buffer, first_iter_sleep, iter_sleep):

        for i, frame in enumerate(image_buffer):
            if i == 0:
                time.sleep(first_iter_sleep)
            matrix.display(frame)
            time.sleep(iter_sleep)

    def create_image_from_user_data(self):
        _color = (265,265,265)
        _name= self.__db.get_user(self.__user_index)
        _display = display(matrix.size, _name, self.__db, _color)
        print(_name)
        
        return _display

    def display_user_info(self):
        scrolling_username_buffer = self.__image.user()
        self.show_image_buffer(scrolling_username_buffer, 0.1, 0.06)

    def display_user_message(self):
        scrolling_message_buffer = self.__image.message()
        self.show_image_buffer(scrolling_message_buffer, 0.05, 0.06)

    def display_user(self):
        if self.__db is not None and self.__db.get_data() is not None and "payments" in self.__db.get_data():

            self.__image = self.create_image_from_user_data()

            self.self.display_user_info()

            self.display_user_message()

            time.sleep(2)


    def display_instructions (self):
        _="NOOP"
        _color = (randrange(265),randrange(265),randrange(265))
        instructions_message_buffer = display(matrix.size, _, _, _color).instructions()
        self.show_image_buffer(instructions_message_buffer, 0.05, 0.06)

    def play(self):
        try:
            print("Press CTRL-C to stop.")
            while True:
                    self.is_connected()
                    self.display_user()
                    self.display_instructions()
                    self.__increment_user()

        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


#----------------------------------------------------------
def main():
    service = Matrix_Service()
    service.play()

#----------------------------------------------------------

if __name__ == "__main__":
    main()
