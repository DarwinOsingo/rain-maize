import getpass
import os 
import hashlib
import json
MAX_TRIES = 3
FILENAME = "reg.json"
def load_users():
    if not os.path.exists(FILENAME):
        return{}
    try :
        with open(FILENAME, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
def save_users(users):
    with open(FILENAME,"w") as f:
        json.dump(users,f,indent = 4)
def hash_passwords(password):
    return hashlib.sha256(password.encode()).hexdigest()
def registration(users):
    while True:
        username = input("Please type in your desired username?:  ")
        if not username:
            print("username feild cant  be empty ")
            continue
        if username in users:
            print("sorry that username is already in use please pick another one")
            continue
        break
    while True:
        password = input("Please type in your refferred password?: ")  
        if len(password) < 8:
            print("Passowrd length must exceed 8 charcters")
            continue 
        confirm = input("Please confirm your password")
        if confirm != password:
            print ("The password must match in both fields ")
            continue
        users[username] = {
            "password":hash_passwords(password)
        } 
        save_users(users)  
        print(f"Registration successfull,welcome {username}")
        break       
def login(users):
    tries = 0
    while tries < MAX_TRIES:
        username = input("Whats your username?:")
        password = getpass.getpass (" whats your password ?:" )

        if not username:
            print("Username field cant be empty!!")
        if not password:
            
            print("Password field cant be empty")
            continue
        hashed_password = hash_passwords(password)
        if username in users and hashed_password == users[username]["password"]:
            print(f"welcome {username} youve successfully logged in !")
            return True
        else:
            tries +=1 
            print(f"unsuccesfull login remianing attempts {MAX_TRIES-tries}")
            continue
def exit_script():
    print("Goodbye estimmed users")
    return None

def main():
    users =load_users()
    while True:
        choice = input("Please pick an option between: \n 1.Login \n 2.Registration \n 3.Exit \n :")
        if choice =="1":
            login(users)
        elif choice == "2":
            registration(users)
        elif choice == "3":
            exit_script()
        else:
            print("Invalid option")

    

if __name__ == "__main__":
    main()
    
