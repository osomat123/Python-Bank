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

def check_details(number, pin):
    query = f'SELECT * FROM card WHERE number = "{number}" AND pin = "{pin}"'
    cur.execute(query)
    records = cur.fetchall()
    conn.commit()

    if len(records) == 1:
        return [records[0][1], records[0][2], records[0][3]]

    return None


def account_page(account):
    print("\n1. Balance")
    print("2. Log out")
    print("0. Exit")

    choice = int(input())
    print()

    if choice == 1:
        print("Balance:", account[2])
        return account

    elif choice == 2:
        print("You have successfully logged out!")
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
