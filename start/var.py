import os
import json 
import hashlib
import getpass
import random

MAX_TRIES = 2
FILENAME = "bank.json"
def load_users():
    if not os.path.exists(FILENAME):
        return{}
    with open( FILENAME,"r") as f:
        return json.load(f)
def save_users(users):
    with open(FILENAME,"w") as f:
        try:
            json.dump(users ,f,indent=2)
        except (TypeError,ValueError) as e:
            print(f" Couldnt save customers {e}")
def registration(users):
    tries = 0
    print("="*50)
    print("WELCOME TO THE BANK CLI")
    print("="*50)
    while tries < MAX_TRIES:
        user_data = {
            "id_number": input("Whats your id number?:"),
            "kra_pin" : input("Whats your KRA pin?: "),
            "first_name": input("Whats your first name ?:"),
            "last_name": input("Whats your last name?: ")
        }

        for field , value  in user_data.items():
            if not value:
                print(f" You left the {field}")
                continue
        
         
        



    