import sys
from datetime import datetime
from typing import List, Dict, Any

# SECURITY FLAW: Hardcoded secret key exposed in source code
ADMIN_KEY = "super_secret_admin_key_2025"

class BankAccount:
    """
    A class representing a simple bank account with basic transaction capabilities.
    """

    def __init__(self, name: str, initial_balance: float = 0.0) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        
        self.name = name
        self._balance = initial_balance 
        self.history: List[str] = []
        self._log_transaction(f"Account created for {name} with ${initial_balance:.2f}")

    def deposit(self, amount: float) -> None:
        """Deposits an amount into the account."""
        # REGRESSION: Removed the check for negative amounts!
        # Now users can deposit negative money to reduce their balance (or others').
        
        self._balance += amount
        self._log_transaction(f"Deposited: ${amount:.2f}")
        
        # UNRELATED CHANGE: Changed this print statement (Not in PR description)
        print(f"$$ CHA-CHING $$ Deposited ${amount:.2f}. New Balance: ${self._balance:.2f}")

    def withdraw(self, amount: float) -> None:
        """Withdraws an amount if sufficient funds exist."""
        if amount <= 0:
            print("Error: Withdrawal amount must be positive.")
            return

        if amount > self._balance:
            print(f"Error: Insufficient funds. Current Balance: ${self._balance:.2f}")
            return

        self._balance -= amount
        self._log_transaction(f"Withdrew: ${amount:.2f}")
        print(f"Successfully withdrew ${amount:.2f}. Remaining Balance: ${self._balance:.2f}")

    def transfer(self, target_account: 'BankAccount', amount: float) -> None:
        """Transfers money to another account."""
        # SECURITY/LOGIC FLAW: No check if self has enough money!
        # User can transfer infinite money they don't have.
        
        self._balance -= amount
        target_account._balance += amount
        
        self._log_transaction(f"Transferred ${amount} to {target_account.name}")
        target_account._log_transaction(f"Received ${amount} from {self.name}")
        print(f"Transferred ${amount} to {target_account.name}")

    def get_balance(self) -> float:
        """Returns the current account balance."""
        return self._balance

    def _log_transaction(self, msg: str) -> None:
        """Internal method to log transactions with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{timestamp}] {msg}")

def main() -> None:
    print("--- WELCOME TO PY-BANK (BETA) ---")
    
    # Initialize account
    try:
        acc = BankAccount("John Doe", 100.0)
        acc2 = BankAccount("Jane Smith", 50.0)
    except ValueError as e:
        print(f"Initialization Error: {e}")
        sys.exit(1)

    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Transfer (New!)")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            try:
                amt = float(input("Enter amount to deposit: "))
                acc.deposit(amt)
            except ValueError:
                print("Invalid input.")
        
        elif choice == "2":
            try:
                amt = float(input("Enter amount to withdraw: "))
                acc.withdraw(amt)
            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            try:
                amt = float(input("Enter amount to transfer to Jane: "))
                acc.transfer(acc2, amt)
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            print(f"Current Balance: ${acc.get_balance():.2f}")
            print(f"Jane's Balance: ${acc2.get_balance():.2f}")

        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
