import os

from dotenv import load_dotenv

## Loading Env variables
folder_path = os.path.dirname(os.path.abspath(__file__)) 
env_path =  folder_path + '/.env'
print("Loading env: " + env_path)
load_dotenv(dotenv_path=env_path, verbose=True)
