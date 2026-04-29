import getpass
import datetime
MAX_TRIES = 3

users = {
    "Darwin":{
        "password":"bigdaddy",
        "role": "admin"
    }
}
def login(users):
    tries = 0

    while tries < MAX_TRIES:
        username = input("Whats your username?:")
        if not username:
            print("Whats the issue fill the damn field !!😂😂")
            continue
        password = getpass.getpass("Your paswword?: ")
        if username in users and password == users["Darwin"]["password"]:
            print(f" Welcome {username}")
            
        else:
            print(f"chances remaining {MAX_TRIES-tries} ")
            tries += 1
            

if __name__ =="__main__":
    login(users)


