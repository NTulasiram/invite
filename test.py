import sys
from datetime import datetime
from typing import List

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
        """Deposits a positive amount into the account."""
        if amount <= 0:
            print("Error: Deposit amount must be positive.")
            return

        self._balance += amount
        self._log_transaction(f"Deposited: ${amount:.2f}")
        print(f"Successfully deposited ${amount:.2f}. New Balance: ${self._balance:.2f}")

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
        """Transfers money to another account safely."""
        # 1. Input Validation
        if amount <= 0:
            print("Error: Transfer amount must be positive.")
            return
        
        # 2. Insufficient Funds Check
        if amount > self._balance:
            print(f"Error: Insufficient funds for transfer. Current Balance: ${self._balance:.2f}")
            return

        # 3. Execution
        self._balance -= amount
        target_account._balance += amount
        
        # 4. Logging
        self._log_transaction(f"Transferred ${amount:.2f} to {target_account.name}")
        target_account._log_transaction(f"Received ${amount:.2f} from {self.name}")
        print(f"Successfully transferred ${amount:.2f} to {target_account.name}")

    def get_balance(self) -> float:
        """Returns the current account balance."""
        return self._balance

    def _log_transaction(self, msg: str) -> None:
        """Internal method to log transactions with the updated readable format."""
        # Changed format slightly as per PR description (more readable date)
        timestamp = datetime.now().strftime("%b %d, %Y - %H:%M:%S")
        self.history.append(f"| {timestamp} | {msg}")

def main() -> None:
    print("--- WELCOME TO PY-BANK (SECURE) ---")
    
    # Initialize accounts safely
    try:
        acc = BankAccount("John Doe", 100.0)
        acc2 = BankAccount("Jane Smith", 50.0)
    except ValueError as e:
        print(f"Initialization Error: {e}")
        sys.exit(1)

    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            try:
                amt = float(input("Enter amount to deposit: "))
                acc.deposit(amt)
            except ValueError:
                print("Invalid input: Please enter a numeric value.")
        
        elif choice == "2":
            try:
                amt = float(input("Enter amount to withdraw: "))
                acc.withdraw(amt)
            except ValueError:
                print("Invalid input: Please enter a numeric value.")

        elif choice == "3":
            try:
                amt = float(input("Enter amount to transfer to Jane: "))
                acc.transfer(acc2, amt)
            except ValueError:
                print("Invalid input: Please enter a numeric value.")

        elif choice == "4":
            print(f"Current Balance ({acc.name}): ${acc.get_balance():.2f}")
            print(f"Current Balance ({acc2.name}): ${acc2.get_balance():.2f}")

        elif choice == "5":
            print("Thank you for banking with us. Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
