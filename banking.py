# Write your code here
import random
import sqlite3

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()

try:
    query = 'CREATE TABLE card(id INTEGER PRIMARY KEY AUTOINCREMENT,number TEXT NOT NULL UNIQUE,pin TEXT NOT NULL,balance INTEGER DEFAULT 0);'
    cur.execute(query)
    conn.commit()
    #print(cur.execute('PRAGMA table_info(card);').fetchall())

except sqlite3.OperationalError:
    pass

class Card:
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    IIN = '400000'

    def __init__(self):
        self.card_number = self.IIN + ''.join(random.choices(self.digits, k=9))
        self.check_sum = self.generate_check_sum()

        self.card_number = self.card_number + self.check_sum
        self.pin = ''.join(random.choices(self.digits, k=4))
        self.balance = 0

        self.add_to_db()

    def add_to_db(self):
        query = f'INSERT INTO card(number,pin,balance) VALUES({self.card_number},{self.pin},{self.balance});'
        try:
            cur.execute(query)
            conn.commit()
        except sqlite3.IntegrityError:
            self.__init__()

    def generate_check_sum(self):
        digits = [int(digit) for digit in list(self.card_number)]
        for i in range(0, 15, 2):
            digit = digits[i] * 2
            if digit > 9:
                digit -= 9
            digits[i] = digit

        check_sum = (10 - (sum(digits) % 10)) % 10
        return str(check_sum)

class User:
    def __init__(self,number,pin):

        self.number = number
        self.pin = pin
        self.id, self.balance = self.get_info()

    def get_info(self):
        query = f'SELECT * FROM card WHERE number = "{self.number}" AND pin ="{self.pin}"'
        cur.execute(query)
        records = cur.fetchall()
        conn.commit()

        return (records[0][0],records[0][3])

    def add_income(self):
        print("\nEnter income: ")
        amount = int(input())
        self.balance += amount

        query = f'UPDATE card SET balance={self.balance} WHERE number="{self.number}"'
        cur.execute(query)
        conn.commit()

        print("Income was added!")

    def transfer_money(self,other_number,amount):
        if amount > self.balance:
            print("Not enough money!")
            return

        # Remove money from account
        self.balance -= amount
        query = f'UPDATE card SET balance = {self.balance} WHERE number="{self.number}"'
        cur.execute(query)
        conn.commit()

        # Add money to other account
        query = f'SELECT * from card WHERE number = "{other_number}"'
        cur.execute(query)
        record = cur.fetchall()
        previous_balance = record[0][3]
        amount += previous_balance
        query = f'UPDATE card SET balance = {amount} WHERE number = "{other_number}"'
        cur.execute(query)
        conn.commit()

        print("Success!")

    def delete_account(self):
        query = f'DELETE FROM card WHERE number = "{self.number}"'
        cur.execute(query)
        conn.commit()

        print("The account has been closed!")

def check_details(number, pin):
    query = f'SELECT * FROM card WHERE number = "{number}" AND pin = "{pin}"'
    cur.execute(query)
    records = cur.fetchall()
    conn.commit()

    if len(records) == 1:
        return User(number,pin)

    return None

def is_valid(card_number):
    if len(card_number) != 16:
        return False

    digits = [int(digit) for digit in list(card_number[:15])]
    for i in range(0, 15, 2):
        digit = digits[i] * 2
        if digit > 9:
            digit -= 9
        digits[i] = digit

    check_sum = (10 - (sum(digits) % 10)) % 10

    if check_sum != int(card_number[-1]):
        return False

    return True

def in_database(card_number):
    query = f'SELECT number FROM card WHERE number = "{card_number}"'
    cur.execute(query)
    records = cur.fetchall()
    conn.commit()

    if len(records) != 1:
        return False

    return True

def account_page(account):
    print("\n1. Balance")
    print("2. Add Income")
    print("3. Do Transfer")
    print("4. Close Account")
    print("5. Log out")
    print("0. Exit")

    choice = int(input())
    print()

    if choice == 1:
        print("Balance:", account.balance)
        return account

    elif choice == 5:
        print("You have successfully logged out!")
        return 1

    elif choice == 2:
        account.add_income()
        return account

    elif choice == 3:
        print("Transfer")
        print("Enter card number: ")
        other_card = input()

        if other_card == account.number:
            print("You can't transfer money to the same account!")

        elif not is_valid(other_card):
            print("Probably you made a mistake in the card number. Please try again!")

        elif not in_database(other_card):
            print("Such a card does not exist.")

        else:
            print("Enter how much money you want to transfer: ")
            amount = int(input())
            account.transfer_money(other_card,amount)
        return account

    elif choice == 4:
        account.delete_account()
        return 1

    else:
        return -1


def main_page():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    choice = int(input())
    print()

    if choice == 1:
        card = Card()
        print("Your card has been created")

        print("Your card number:")
        print(card.card_number)

        print("Your card PIN")
        print(card.pin)

        return 1

    elif choice == 2:
        print("Enter your card number:")
        number = input()

        print("Enter your PIN:")
        pin = input()

        print()

        account = check_details(number, pin)
        if account:
            print("You have successfully logged in!")
            return account

        else:
            print("Wrong card number or PIN!")
            return 1

    else:
        return -1


ret = 1
while True:

    if ret == 1:
        ret = main_page()

    elif ret == -1:
        print("Bye!")
        break

    else:
        ret = account_page(ret)

    print()
