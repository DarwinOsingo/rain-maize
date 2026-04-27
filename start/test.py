import os 
import getpass
import json
import bcrypt
import hashlib

MAX_TRIES = 3
DB_FILE = "users.json"
def password_hasher(password):
    return hashlib.sha256(password.encode()).hexdigest()
   

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE,"r") as f:
        return json.load(f)
def save_users(users):
    with open(DB_FILE,"w")as f:
        json.dump(users,f,indent = 2)
def register(users):
    while True:
        username = input("What do you want your username to be ?:").strip()
        if not username:
            print("Error:Username field cannot be empty!")
        else:
            if username in users:
                print("Username already exists,please pick another one")
                continue
            break
    while True:
        password = getpass.getpass("Please set a secure password ")
        confirm = getpass.getpass("Please confirm your password")
        if password != confirm:
            print("passwords do not match!")
            continue
        if len(password) < 8:
            print("The password cant be less than 8 charcters ")
            continue
        break
    
    users[username]= password_hasher(password)
    save_users(users)
    print(f"Account created.Welcome , {username}!\n")
def login():
    users = load_users()
    attempts = 0
    while attempts < MAX_TRIES:
        print("="*40 )
        print("Welcome to login !")
        print("="* 40)
        user_name = input("Whats your username ?:").strip()
        password = getpass.getpass("Your password fam?:")
        if user_name in users and password_hasher(password) == users[user_name]:
        
            print(f"signed in successfully into {user_name}")
            return user_name
        else:
            attempts += 1 
            print(f"Invalid username or password try again,chances remaining {MAX_TRIES-attempts}")
            continue
    print("Too many failed attempts retsrt the session")
    return None
def invalid_option():
    print("invalid option")
def exit():
    print("Goodbye")
    return None
def main():
    users = load_users()
    print("=== Auth System ===")
    print("1. Login")
    print("2. Register")
    print("3.Exit")
    choice = input("Choose an option (1/2)")
    if choice == "1":
        login()
    elif choice == "2":
        register(users)
    elif choice == "3":
        exit()


    else:
        print("Invalid input")



   
if __name__ == "__main__":
    main()



