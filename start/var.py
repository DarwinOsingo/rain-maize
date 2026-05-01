import os
import json 
import hashlib
import getpass
import random
import datetime 

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
    
    print("="*50)
    print("WELCOME TO THE BANK CLI")
    print("="*50)
    while True:
        user_data = {
            "id_number": input("Whats your id number?:"),
            "kra_pin" : input("Whats your KRA pin?: "),
            "first_name": input("Whats your first name ?:"),
            "last_name": input("Whats your last name?: ")
        }

        for field , value  in user_data.items():
            if not value:
                print(f" You left the {field}")
                break
        while True:
            print("Please pick a secure pin ")
            
            pin = getpass.getpass("Please set your PIN for the account?: ")
            if not pin:
                print("Please pick a solid 4 digit PIN")
            
                
            confirm = input("Please confirm your PIN number")
            if pin != confirm:
                print("PIN numbers do not match!!")
                continue

            if len(pin) < 4:
                print("Please pick a better password ")
                continue 
            
            account_number = "".join([str(random.randint(0, 9)) for n in range(12)])
            hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
            time = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            users[account_number]= {
                **user_data,
                "account_number": account_number,
                "pin": hashed_pin,
                "created_at": time,
                "balance": 0.0
            }
            save_users(users)
            print(f"Successful registration your account number is {account_number}")
            break
            
        
def login(users):
    tries =0
    while tries < MAX_TRIES:
        account_number = input("Whats your account  number?: ?: ")
        if not account_number:
            print("Account number cant be empty")
            continue 
        if account_number not in users:
            print("No such account friend")
            tries +1
            continue

        while True:
            pin = getpass.getpass("Your PIN password?: ")
            if not pin :
                print("This field cant be empty")
                continue

            break
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        name = users[account_number]["first_name"]
        time = datetime.datetime.now().strftime("%d %m %y %H:%M")
        if  hashed_pin == users[account_number]["pin"]:
            print(f"You succesfully logged in welcome {name} youve loged in at {time} ")
        else:
            tries+=1
            print(f"Wrong PIN chances remaining : {MAX_TRIES-tries}")
            continue
        print("="*50)
        print("Weloome to the Your account")
        print("="*50)
        print("Please pick an option \n 1. Deposit money \n 2. Withdraw money  \n 3. Check balance \n 4. Exit login "  )
        def deposit_money():
            add = int(input("How much will you depositing?: "))
            total = users[account_number]["balance"] + add
            print(f"The moneys been successfully added your balance is now {total :.2f}")
            users[account_number]["balance"]= total
            save_users(users)
            return
        def withdraw_money():
            sub = int(input("Please input the number youd like to withdraw? "))
            if sub > users[account_number]["balance"]:
                print("Insufficient funds for withdrawal")
            total = users[account_number]["balance"] - sub
            
            print(f"Completed widthdraw the money left in the account is {total :.2f}")
            users[account_number]["balance"]= total
            save_users(users)
            return
        def check_balance():
            total = users[account_number]["balance"]
            print(f"Your current standing is {total :.2f}")
            return
        def exit_login():
            print("Goodbye")
            return 
        while True:
            choice = input("Whats your choice ?: ")
            if choice == "1":
                deposit_money()
            elif choice == "2":
                withdraw_money()
            elif choice == "3":
                check_balance()
            elif choice == "4":
                exit_login
            else:
                print("Invalid option!!")
                
                

def exit_script():
    print("Goodbye have a lovely rest of your day")
    return

def main():

    users= load_users()
    while True:
        print("="*50)
        print("Welocme to the banking CLI")
        print("="*50)
        final_choice = int(input("Please pick an option between \n 1. Login \n 2. Rgistration \n 3. Exit \n:"))
        choice = final_choice 


        if choice == 1:
            login(users)
        elif choice == 2:
            registration(users)
        elif choice == 3:
            exit_script()
        else:
            print("Invalid try again lease")
if __name__ == "__main__":
    main()


        
            







            



            
        



    