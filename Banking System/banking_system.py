import json
import os
import uuid
from datetime import datetime
from getpass import getpass

class BankAccount:
    def __init__(self, account_number, name, pin, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = balance
        self.transactions = []
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._add_transaction("Deposit", amount)
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._add_transaction("Withdrawal", -amount)
            return True
        return False
    
    def transfer(self, amount, recipient_account):
        if self.withdraw(amount):
            recipient_account.deposit(amount)
            self._add_transaction(f"Transfer to {recipient_account.account_number}", -amount)
            recipient_account._add_transaction(f"Transfer from {self.account_number}", amount)
            return True
        return False
    
    def _add_transaction(self, transaction_type, amount):
        self.transactions.append({
            'type': transaction_type,
            'amount': abs(amount),
            'balance': self.balance,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def get_statement(self):
        return {
            'account_number': self.account_number,
            'name': self.name,
            'balance': self.balance,
            'created_at': self.created_at,
            'transactions': self.transactions
        }

class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()
    
    def load_accounts(self):
        if os.path.exists('accounts.json'):
            try:
                with open('accounts.json', 'r') as f:
                    data = json.load(f)
                    for acc_num, acc_data in data.items():
                        account = BankAccount(
                            acc_num,
                            acc_data['name'],
                            acc_data['pin'],
                            acc_data['balance']
                        )
                        account.transactions = acc_data.get('transactions', [])
                        account.created_at = acc_data.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        self.accounts[acc_num] = account
            except (json.JSONDecodeError, FileNotFoundError):
                self.accounts = {}
    
    def save_accounts(self):
        data = {}
        for acc_num, account in self.accounts.items():
            data[acc_num] = account.get_statement()
        with open('accounts.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def create_account(self, name, pin, initial_deposit=0.0):
        account_number = str(uuid.uuid4().int)[:10]
        self.accounts[account_number] = BankAccount(account_number, name, pin, initial_deposit)
        self.save_accounts()
        return account_number
    
    def authenticate(self, account_number, pin):
        account = self.accounts.get(account_number)
        if account and account.pin == pin:
            return account
        return None

def display_menu():
    print("\n=== Banking System ===")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

def display_user_menu():
    print("\n=== Account Menu ===")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. View Statement")
    print("6. Logout")

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def main():
    bank = BankingSystem()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':  # Create Account
            print("\n=== Create New Account ===")
            name = input("Enter your full name: ").strip()
            while True:
                pin = getpass("Create a 4-digit PIN: ")
                if pin.isdigit() and len(pin) == 4:
                    break
                print("PIN must be 4 digits.")
            
            initial_deposit = get_float_input("Initial deposit amount (or 0): ") or 0.0
            account_number = bank.create_account(name, pin, initial_deposit)
            print(f"\nAccount created successfully!")
            print(f"Your account number is: {account_number}")
            print("Please keep this number safe!")
        
        elif choice == '2':  # Login
            print("\n=== Login ===")
            account_number = input("Enter account number: ").strip()
            pin = getpass("Enter PIN: ")
            
            account = bank.authenticate(account_number, pin)
            if account:
                print(f"\nWelcome, {account.name}!")
                user_session(account, bank)
            else:
                print("\nInvalid account number or PIN.")
        
        elif choice == '3':  # Exit
            print("\nThank you for using our banking system!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

def user_session(account, bank):
    while True:
        display_user_menu()
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':  # Check Balance
            print(f"\nAccount Balance: ${account.balance:.2f}")
            
        elif choice == '2':  # Deposit
            amount = get_float_input("\nEnter amount to deposit: $")
            if account.deposit(amount):
                bank.save_accounts()
                print(f"\n${amount:.2f} deposited successfully!")
                print(f"New balance: ${account.balance:.2f}")
            else:
                print("\nInvalid amount!")
                
        elif choice == '3':  # Withdraw
            amount = get_float_input("\nEnter amount to withdraw: $")
            if account.withdraw(amount):
                bank.save_accounts()
                print(f"\n${amount:.2f} withdrawn successfully!")
                print(f"Remaining balance: ${account.balance:.2f}")
            else:
                print("\nInsufficient funds or invalid amount!")
                
        elif choice == '4':  # Transfer
            recipient_number = input("\nEnter recipient's account number: ").strip()
            recipient = bank.accounts.get(recipient_number)
            if not recipient:
                print("\nRecipient account not found!")
                continue
                
            if recipient.account_number == account.account_number:
                print("\nCannot transfer to the same account!")
                continue
                
            amount = get_float_input("Enter amount to transfer: $")
            if account.transfer(amount, recipient):
                bank.save_accounts()
                print(f"\n${amount:.2f} transferred successfully to {recipient.name}!")
                print(f"Your new balance: ${account.balance:.2f}")
            else:
                print("\nTransfer failed. Insufficient funds or invalid amount!")
                
        elif choice == '5':  # View Statement
            print(f"\n=== Account Statement ===")
            print(f"Account Number: {account.account_number}")
            print(f"Account Holder: {account.name}")
            print(f"Current Balance: ${account.balance:.2f}")
            print("\nTransaction History:")
            print("-" * 50)
            print("{:<20} {:<15} {:<15} {}".format("Date/Time", "Type", "Amount", "Balance"))
            print("-" * 50)
            
            for tx in account.transactions:
                print("{:<20} {:<15} ${:<14.2f} ${:.2f}".format(
                    tx['timestamp'],
                    tx['type'],
                    tx['amount'],
                    tx['balance']
                ))
                
        elif choice == '6':  # Logout
            print("\nLogging out...")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
