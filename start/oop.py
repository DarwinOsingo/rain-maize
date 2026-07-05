class Account():
    def __init__(self,account_number,name,id_number,balance  ):
        self.name = name
        self.account_number = account_number
        self.id_number = id_number
        self.__balance= balance


    def deposit_money(self,amount):

        if amount <= 0:
            print("The amount must be more than 0")
            return
        total = self.__balance + amount
        self.__balance = total
        print(f"Successfully deposited {amount},account balance is now {total}")
        return total
    def check_balance (self):
        return self.__balance
    def withdraw(self,amount):
        if amount > self.__balance:
            print(f"You dont have that money fam your balance is {self.__balance}")
            return
        total = self.__balance - amount 
        self.balance = total
        return total



        