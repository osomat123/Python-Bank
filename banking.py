# Write your code here
import random

accounts = []

class Card:
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    IIN = '400000'

    def __init__(self):
        self.card_number = self.IIN + ''.join(random.choices(self.digits, k=9))
        self.check_sum = self.generate_check_sum()
        self.card_number = self.card_number + self.check_sum
        self.check_number()

        self.pin = ''.join(random.choices(self.digits, k=4))
        self.balance = 0

    def check_number(self):
        for account in accounts:
            if account.card_number == self.card_number:
                self.__init__()
                break

    def generate_check_sum(self):
        digits = [int(digit) for digit in list(self.card_number)]
        for i in range(0,15,2):
            digit = digits[i] * 2
            if digit > 9:
                digit -= 9;
            digits[i] = digit

        check_sum = (10 - (sum(digits) % 10)) % 10
        return str(check_sum)

def check_details(number, pin):
    for account in accounts:
        if (number == account.card_number) and (account.pin == pin):
            return account

    return None


def account_page(account):
    print("\n1. Balance")
    print("2. Log out")
    print("0. Exit")

    choice = int(input())
    print()

    if choice == 1:
        print("Balance:", account.balance)
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

        accounts.append(card)
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
