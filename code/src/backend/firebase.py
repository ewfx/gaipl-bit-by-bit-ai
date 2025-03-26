import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore 

import base64
import json


service_account_encoded_data={}

# Open and read the JSON file
with open("./data/auth_encoded.json", "r") as file:
    json_data = json.load(file)  # Converts JSON to a Python dictionary

# Store the data in a variable
service_account_encoded_data = json_data

cred_data ={}
for data in service_account_encoded_data:
    cred_data[data]= base64.b64decode(service_account_encoded_data[data]).decode("utf-8")
cred = credentials.Certificate(cred_data)
firebase_admin.initialize_app(cred)
print(cred)
db = firestore.client()

def get_env_keys():
    keys_ref = db.collection("Keys").stream()
    keys={}
    for key in keys_ref:
        keys=key.to_dict()
    return keys

