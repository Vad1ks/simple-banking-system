# Write your code here
import random
import sys
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("create table if not exists \
card(id INTEGER,\
number TEXT,\
pin TEXT,\
balance INTEGER DEFAULT 0);")
conn.commit()


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


def luhn_check(num15):
    num15 = list(map(int, list(num15)))
    nums = []
    for i in range(len(num15)):
        if i % 2 == 0:
            if (num15[i] * 2) > 9:
                nums.append(num15[i] * 2 - 9)
            else:
                nums.append(num15[i] * 2)
        else:
            nums.append(num15[i])
    if sum(nums) % 10:
        return 10 - (sum(nums) % 10)
    else:
        return 0


def luhn_is_exists_check(num16):
    num16 = list(map(int, list(num16)))
    nums = []
    for i in range(len(num16)-1):
        if i % 2 == 0:
            if (num16[i] * 2) > 9:
                nums.append(num16[i] * 2 - 9)
            else:
                nums.append(num16[i] * 2)
        else:
            nums.append(num16[i])
    if sum(nums) % 10:
        checkSum = 10 - (sum(nums) % 10)
    else:
        checkSum = 0
    return checkSum == num16[-1]


def is_Exists(number):
    cur.execute("Select count(*) from card where number = '%s'" % number)
    checker = cur.fetchall()
    return checker[0][0]


def end():
    print("\nBye!")
    sys.exit(0)


class Card:
    #arr = []
    id = 1

    def __init__(self, number=None, pin=None):
        if number is None:
            self.number = ''
            self.number += '400000' + str(random_with_N_digits(9))
            last_digit = luhn_check(self.number)
            self.number += str(last_digit)
            self.pin = random.randint(1000, 9999)
        else:
            self.number = number
            self.pin = pin
        self.balance = 0
        #Card.arr.append(self)
        cur.execute("insert into card(id,number,pin) values(%d, '%s', '%s')" % (Card.id, self.number, self.pin))
        conn.commit()
        Card.id += 1

    def check(self):
        cur.execute("Select * from card where number = '%s' and pin = '%s'" % (self.number, self.pin))
        checker = cur.fetchall()
        if checker:
            checker = checker[0]
            balance = checker[3]
            temp = Card()
            temp.number = self.number
            temp.pin = self.pin
            temp.balance = balance
            return temp
        else:
            return None

    def show_balance(self):
        cur.execute("Select balance from card where number = '%s'" % self.number)
        bal = cur.fetchall()[0][0]
        self.balance = bal
        print("\nBalance: %d\n" % self.balance)

    def show_card_info(self):
        print("Your card number:\n%s" % self.number)
        print("Your card PIN:\n%s\n" % self.pin)

    def set_income(self, funds):
        cur.execute("Update card set balance = '%d' where number = '%s'" % (self.balance + funds, self.number))
        self.balance += income
        conn.commit()

    def transfer(self, cardnum, value):
        cur.execute("Update card set balance = balance - '%d' where number = '%s'" % (value, self.number))
        cur.execute("Update card set balance = balance + '%d' where number = '%s'" % (value, cardnum))
        conn.commit()

    def close_account(self):
        cur.execute("Delete from card where number = '%s'" % self.number)
        conn.commit()


while True:
    choice = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    if choice == 1:
        temp = Card()
        print("\nYour card has been created")
        temp.show_card_info()
    elif choice == 2:
        input_num = input("\nEnter your card number:\n")
        input_pin = int(input("Enter your PIN:\n"))
        obj = Card()
        obj.number = input_num
        obj.pin = input_pin
        obj = obj.check()
        if obj:
            print("\nYou have successfully logged in!\n")
            while True:
                choice = int(input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"))
                if choice == 1:
                    obj.show_balance()
                elif choice == 2:
                    income = int(input("\nEnter income:\n"))
                    obj.set_income(income)
                    print("Income was added!\n")
                elif choice == 3:
                    print("\nTransfer")
                    cardnum = input("Enter card number:\n")
                    if luhn_is_exists_check(cardnum):
                        if is_Exists(cardnum):
                            value = int(input("Enter how much money you want to transfer:\n"))
                            if obj.balance >= value:
                                obj.transfer(cardnum, value)
                                print("Success!\n")
                            else:
                                print("Not enough money!\n")
                        else:
                            print("Such a card does not exist.\n")
                    else:
                        print("Probably you made a mistake in the card number. Please try again!\n")
                elif choice == 4:
                    obj.close_account()
                    print("\nThe account has been closed!\n")
                elif choice == 5:
                    print("\nYou have successfully logged out!\n")
                    break
                elif choice == 0:
                    end()
        else:
            print("\nWrong card number or PIN!\n")
    elif choice == 0:
        end()
