import firebase_admin
from firebase_admin import db
import json

class firebase_db:

    def __init__(self, credentials_path, database_url):
        ## Loading Database
        self.__credentials = firebase_admin.credentials.Certificate(credentials_path)
        self.__app = firebase_admin.initialize_app(self.__credentials, {'databaseURL': database_url})
        print(self.__app.name + ": initialized database correctly...")
        self.__ref = db.reference("/")
        self.data = self.get_data()

    def printer(self):
        print(json.dumps(self.get_data(), indent=4))

    def set_ref(self, path="/"):
        self.__ref = db.reference(path)
        self.data = self.get_data()

    def get_data(self):
        return self.__ref.get()

    def keys(self):
        return self.get_data().keys()
