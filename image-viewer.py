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

 
def image_creater_hack(index):
    _name= DB.data["users"].keys()[index]
    _data = DB.data["users"][_name]
    _display = display(matrix.size, _name, DB)
    print(_name)
    return _display
try:
    print("Press CTRL-C to stop.")

    j = 0
    while True:
        img = image_creater_hack(j)
        scrolling_username_img = img.user()

        for username_img in scrolling_username_img:
            matrix.display(username_img)
            time.sleep(0.05)

        matrix.display(img.message())

        time.sleep(2)

        if j < (DB.size() - 1 ):
            j += 1
        else:
            j = 0

except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)

print("Exiting...")
