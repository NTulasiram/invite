import os
import sys
import random  # Unused import
from datetime import datetime

# HARDCODED SECRET (Security Flaw)
ADMIN_PASSWORD = "secret_admin_123" 

class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        # LOGIC ERROR: Allows depositing negative numbers (stealing money)
        self.balance += amount
        self.log_transaction(f"Deposited: {amount}")
        print(f"Deposited ${amount}. New Balance: ${self.balance}")

    def withdraw(self, amount):
        # LOGIC ERROR: No check for insufficient funds (allows overdrafting to infinity)
        self.balance -= amount
        self.log_transaction(f"Withdrew: {amount}")
        print(f"Withdrew ${amount}. Remaining: ${self.balance}")

    def log_transaction(self, msg):
        # FORMATTING: Using a mutable default argument list is dangerous, 
        # but here we just have bad timestamp formatting
        timestamp = datetime.now().strftime("%Y/%d/%m") # Weird date format (Day in middle)
        self.history.append(f"[{timestamp}] {msg}")

    def get_user_data(self):
        # SECURITY FLAW: Returning sensitive data (memory address) or just bad practice
        return self.__dict__ 

def login():
    print("--- WELCOME TO PY-BANK ---")
    user_input = input("Enter admin password to start: ")
    
    # SECURITY: Plain text password comparison
    if user_input == ADMIN_PASSWORD:
        return True
    else:
        return False

def main():
    if login():
        # LOGIC: 'acc' is created but never really used safely
        acc = BankAccount("John Doe", 100)
        
        while True:
            print("\n1. Deposit")
            print("2. Withdraw")
            print("3. Exit")
            
            choice = input("Choose: ")
            
            if choice == "1":
                # BUG: potential ValueError if user enters text instead of number
                amt = float(input("Amount: ")) 
                acc.deposit(amt)
            elif choice == "2":
                amt = float(input("Amount: "))
                acc.withdraw(amt)
            elif choice == "3":
                break
            else:
                # Poor error handling
                print("Bad input")

if __name__ == "__main__":
    main()
