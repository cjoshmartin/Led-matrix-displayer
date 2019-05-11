#!/usr/bin/env python

# System
import time
import sys
import os

# pip installs
from dotenv import load_dotenv

# Local 
from database import matrix_db
from led_matrix import led_matrix
from create_image import display

## Loading Env variables
folder_path = os.path.dirname(os.path.abspath(__file__)) 
env_path =  folder_path + '/.env'
print "Loading env: " + env_path 
load_dotenv(dotenv_path=env_path, verbose=True)


DB = matrix_db(folder_path +  "/" + ".service-account-file.json", os.getenv('DB_URL'))
DB.printer()

matrix = led_matrix()

# TODO: Get current day
# TODO: only grab venmo transactions from day of graduation and Sort by date/time in database
# TODO: Create a system to see which transactions have been already viewed and do no show them again
# DONE: Fix how user name are showed
# TODO: Instruction on how to use the venmo hat
# TODO: If transaction is less then $1, then send it back!
 
def image_creater_hack(index):
    from random import randrange

    _color = (randrange(265),randrange(265),randrange(265))
    _name= DB.data["users"].keys()[index]
    _data = DB.data["users"][_name]
    _display = display(matrix.size, _name, DB, _color)
    print(_name)
    return _display
try:
    print("Press CTRL-C to stop.")

    j = 0
    while True:
        img = image_creater_hack(j)
        scrolling_username_img = img.user()
        
        for i,username_img in enumerate(scrolling_username_img):
            if i == 0:
                time.sleep(0.08)
            matrix.display(username_img)
            time.sleep(0.05)


        scrolling_message_imgs = img.message()

        for i,message_img in enumerate(scrolling_message_imgs):
            if i == 0:
                time.sleep(0.05)
            matrix.display(message_img)
            time.sleep(0.06)

        time.sleep(2)

        if j < (DB.size() - 1 ):
            j += 1
        else:
            j = 0

except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)

print("Exiting...")
