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
from create_image import create_image

## Loading Env variables
folder_path = os.path.dirname(os.path.abspath(__file__)) 
env_path =  folder_path + '/.env'
print "Loading env: " + env_path 
load_dotenv(dotenv_path=env_path, verbose=True)


DB = matrix_db(folder_path +  "/" + ".service-account-file.json", os.getenv('DB_URL'))
DB.printer()

matrix = led_matrix()

img = create_image(
        name=DB.keys()[1],
        url=DB.data[DB.keys()[1]]["profile_picture"], 
        matrix_size= matrix.size
        )


matrix.display(img)

try:
    print("Press CTRL-C to stop.")
    i = 5
    while i > 0:
        time.sleep(1)
        i-= 1
        print(i)
except KeyboardInterrupt:
    sys.exit(0)

print("Exiting...")
