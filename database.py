import firebase_admin
from firebase_admin import db ## https://github.com/firebase/firebase-admin-python/blob/18c2395df35977a6444fd95b8f66a29fda3b04a9/tests/test_db.py
import json
import urllib

## TODO: Add Caching

def internet_on():
    try: 
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.error.URLError as err:
        return False

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
        self.data =self.__ref.get()
        return self.data

    def keys(self):
        return self.get_data().keys()
    
    def put(self, data):
        self.__ref.set(data)
        print("Added data successfully")

    def size(self):
        return len(self.data)



class matrix_db(firebase_db): 
    def __init__(self, credentials_path, database_url):
        firebase_db.__init__(self, credentials_path, database_url)

    def get_name(self, index):
        return self.get_keys()[index]
    
    def get_user_timestamp(self, username):
        return self.get_data()["users"][username]["usage"][0]


    def get_user(self, index):
        _data = self.get_data()
        _user_dict =_data["users"] 
        _username_list = list(_user_dict.keys())
        return _username_list[index]
    
    def get_profile_photo(self, username):
        return self.get_user_list()[username]["profile_picture"]

    def get_message_list(self):
        return self.get_data()["payments"]

    def get_user_list(self):
        return self.get_data()["users"]

    def size(self):
        if "users" not in self.get_data():
            return 0;

        return len(self.get_user_list())
    

    def delete_message(self, timestamp):
        del self.data["payments"][timestamp]

        self.put(self.data)

    def update_transactions(self, username):
        if len(self.get_message_list()[username]["usage"]) < 2:
            del self.data["users"][username]
        else:
            del self.data["users"][username]["usage"][0]

        self.put(self.data)

    def update_past_payments(self, timestamp):
        if "past-payments" in  self.data:
            if not timestamp in  self.data['past-payments']:
                self.data['past-payments'].append(timestamp)
        else:
            self.data['past-payments'] = [timestamp]

        self.put(self.data)


