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
    _name= DB.keys()[index]
    _display = display(matrix.size)
    print(_name)
    return _display.user(
        name=_name,
        url=DB.data[_name]["profile_picture"], 
        )
try:
    print("Press CTRL-C to stop.")

    j = 0
    while True:
        img = image_creater_hack(j)
        matrix.display(img)

        time.sleep(5)

        if j < (DB.size() - 1 ):
            j += 1
        else:
            j = 0

except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)

print("Exiting...")
