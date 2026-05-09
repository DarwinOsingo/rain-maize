import getpass
import datetime
MAX_TRIES = 3

users = {
    "Darwin":{
        "password":"bigdaddy",
        "role": "admin"
    }
}
def banner():
    print("="* 50)
    print("WELCOME TO THE CLI USER")
    print("="*50)
def login(users):
    tries = 0

    while tries < MAX_TRIES:
        username = input("Whats your username?:")
        if not username:
            print("Whats the issue fill the damn field !!😂😂")
            continue
        password = getpass.getpass("Your paswword?: ")
        time = datetime.datetime.now().strftime("%d %m %y ")
        if username in users and password == users["Darwin"]["password"]:

            print(f" Welcome {username},Youve logged in at {time}")
            break
            
        else:
            print(f"chances remaining {MAX_TRIES-tries} ")
            tries += 1
            



banner()
login(users)

