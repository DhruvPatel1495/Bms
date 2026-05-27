# Bms
app.py
from db import create_tables
from auth import register, login
from banking import *

# CREATE DATABASE TABLES
create_tables()

while True:

    print("\n===== BANKING MANAGEMENT SYSTEM =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter Choice: ")

    # REGISTER
    if choice == "1":
        register()

    # LOGIN
    elif choice == "2":

        success = login()

        if success:

            while True:

                print("\n===== BANK MENU =====")
                print("1. Create Account")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Check Balance")
                print("5. View All Accounts")
                print("6. Logout")

                ch = input("Enter Choice: ")

                if ch == "1":
                    create_account()

                elif ch == "2":
                    deposit()

                elif ch == "3":
                    withdraw()

                elif ch == "4":
                    check_balance()

                elif ch == "5":
                    view_accounts()

                elif ch == "6":
                    print("Logged Out Successfully!")
                    break

                else:
                    print("Invalid Choice")

    # EXIT
    elif choice == "3":
        print("Thank You!")
        break

    else:
        print("Invalid Choice")

db.py
import sqlite3

def connect_db():
    conn = sqlite3.connect("database.db")
    return conn


def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # ACCOUNTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        acc_no TEXT PRIMARY KEY,
        name TEXT,
        balance REAL
    )
    """)

    conn.commit()
    conn.close()
banking.py
from db import connect_db

# CREATE ACCOUNT
def create_account():

    conn = connect_db()
    cursor = conn.cursor()

    acc_no = input("Enter Account Number: ")
    name = input("Enter Name: ")
    balance = float(input("Enter Initial Balance: "))

    cursor.execute(
        "INSERT INTO accounts VALUES (?, ?, ?)",
        (acc_no, name, balance)
    )

    conn.commit()
    conn.close()

    print("Account Created Successfully!")


# DEPOSIT
def deposit():

    conn = connect_db()
    cursor = conn.cursor()

    acc_no = input("Enter Account Number: ")
    amount = float(input("Enter Deposit Amount: "))

    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE acc_no=?",
        (amount, acc_no)
    )

    conn.commit()
    conn.close()

    print("Money Deposited Successfully!")


# WITHDRAW
def withdraw():

    conn = connect_db()
    cursor = conn.cursor()

    acc_no = input("Enter Account Number: ")
    amount = float(input("Enter Withdrawal Amount: "))

    cursor.execute(
        "SELECT balance FROM accounts WHERE acc_no=?",
        (acc_no,)
    )

    result = cursor.fetchone()

    if result:

        balance = result[0]

        if balance >= amount:

            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE acc_no=?",
                (amount, acc_no)
            )

            conn.commit()
            print("Withdrawal Successful!")

        else:
            print("Insufficient Balance!")

    else:
        print("Account Not Found!")

    conn.close()


# CHECK BALANCE
def check_balance():

    conn = connect_db()
    cursor = conn.cursor()

    acc_no = input("Enter Account Number: ")

    cursor.execute(
        "SELECT * FROM accounts WHERE acc_no=?",
        (acc_no,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        print("\n===== ACCOUNT DETAILS =====")
        print("Account Number:", result[0])
        print("Name:", result[1])
        print("Balance:", result[2])

    else:
        print("Account Not Found!")


# VIEW ALL ACCOUNTS
def view_accounts():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts")

    accounts = cursor.fetchall()

    conn.close()

    print("\n===== ALL ACCOUNTS =====")

    for acc in accounts:

        print("----------------------")
        print("Account Number:", acc[0])
        print("Name:", acc[1])
        print("Balance:", acc[2])
auth.py
from db import connect_db

# REGISTER USER
def register():

    conn = connect_db()
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()

    print("Registration Successful!")


# LOGIN USER
def login():

    conn = connect_db()
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        print("Login Successful!")
        return True

    else:
        print("Invalid Username or Password")
        return False
