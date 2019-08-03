#!/usr/bin/env python

# System
import time
import sys
import os

# pip installs
from dotenv import load_dotenv

# Local 
from database import matrix_db, internet_on
from led_matrix import led_matrix
from create_image import display
import time
from random import randrange

## Loading Env variables
folder_path = os.path.dirname(os.path.abspath(__file__)) 
env_path =  folder_path + '/.env'
print "Loading env: " + env_path 
load_dotenv(dotenv_path=env_path, verbose=True)
matrix = led_matrix()

# TODO: Get current day
# TODO: only grab venmo transactions from day of graduation and Sort by date/time in database
# TODO: Create a system to see which transactions have been already viewed and do no show them again
# DONE: Fix how user name are showed
# DONE: Instruction on how to use the venmo hat
# TODO: If transaction is less then $1, then send it back!
 
def is_connected(db = None):
    if internet_on() and db is None:
        db = matrix_db(folder_path +  "/" + ".service-account-file.json", os.getenv('DB_URL'))
        db.printer()
        return db, db.size()
    else:
        return db, 0

def show_image_buffer(image_buffer, first_iter_sleep, iter_sleep):
    for i, frame in enumerate(image_buffer):
        if i == 0:
            time.sleep(first_iter_sleep)
        matrix.display(username_img)
        time.sleep(iter_sleep)

def create_image_from_user_data(index, DB):
    _color = (265,265,265)
    _name= DB.get_user(index)
    _display = display(matrix.size, _name, DB, _color)
    print(_name)
    
    return _display

def display_user_info(img):
    scrolling_username_buffer = img.user()
    show_image_buffer(scrolling_username_buffer, 0.1, 0.06)

def display_user_message(img):
    scrolling_message_buffer = img.message()
    show_image_buffer(scrolling_message_buffer, 0.05, 0.06)

def display_user(index, DB):
    if DB is not None and DB.get_data() is not None and "payments" in DB.get_data():
        img = create_image_from_user_data(index, DB)

        display_user_info(img)

        display_user_message(img)

        time.sleep(2)

    else:
        pass # Todo 

def display_instructions ():
    _="NOOP"
    _color = (randrange(265),randrange(265),randrange(265))
    instructions_message_buffer = display(matrix.size, _, _, _color).instructions()
    show_image_buffer(instructions_message_buffer, 0.05, 0.06)

#----------------------------------------------------------
def main():
    try:
        print("Press CTRL-C to stop.")
        DB, db_size = is_connected()

        while True:
            for j in range(db_size - 1):
                DB, _ = is_connected(DB)
                    
                display_user(j, DB)

                display_instructions()


    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)

    print("Exiting...")

if __name__ == "__main__":
    main()
