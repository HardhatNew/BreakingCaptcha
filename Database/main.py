from dotenv import load_dotenv , find_dotenv
import os
import pprint
from pymongo import MongoClient
import certifi
#import datetime
ca = certifi.where()
load_dotenv(find_dotenv())

# Mongodb cluster connection code
password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://BreakingCaptcha:{password}@cluster0.zqad6gr.mongodb.net/?retryWrites=true&w=majority"    

client = MongoClient(connection_string, tlsCAFile=ca)

dbs = client.list_database_names()
BreakingCaptcha_db = client.BreakingCaptcha
collections = BreakingCaptcha_db.list_collection_names()
print(collections)

# defining a function to insert a user 
def insert_user_doc():
    collection = BreakingCaptcha_db.User
    User_document = {
        "ID":"xxxyyyzzz",
        "FName":"Nikhil",
        "LName":"Ranjan",
        "Email":"nik250795@gmail.com",
        "Username":"xyz",
        "Password":"****",
        "Date": "10/04/2023",
        "Data":"Multemedia_Data_ID"
    }

    inserted_id = collection.insert_one(User_document).inserted_id
    print(inserted_id)


insert_user_doc()