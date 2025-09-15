import random
import getpass

class ATM:
    def __init__(self):
        self.accounts = {
            '1234567890': {'pin': '1234', 'balance': 5000.0, 'name': 'John Doe'},
            '9876543210': {'pin': '4321', 'balance': 2500.0, 'name': 'Jane Smith'}
        }
        self.current_account = None

    def validate_pin(self, account_number, pin):
        if account_number in self.accounts and self.accounts[account_number]['pin'] == pin:
            self.current_account = account_number
            return True
        return False

    def check_balance(self):
        if self.current_account:
            return self.accounts[self.current_account]['balance']
        return 0.0

    def deposit(self, amount):
        if self.current_account and amount > 0:
            self.accounts[self.current_account]['balance'] += amount
            return True
        return False

    def withdraw(self, amount):
        if self.current_account and 0 < amount <= self.check_balance():
            self.accounts[self.current_account]['balance'] -= amount
            return True
        return False

def main():
    atm = ATM()
    
    print("\n=== Welcome to Python ATM Simulator ===")
    
    # Login
    while True:
        account_number = input("\nEnter your account number: ")
        pin = getpass.getpass("Enter your PIN: ")
        
        if atm.validate_pin(account_number, pin):
            print(f"\nWelcome, {atm.accounts[account_number]['name']}!")
            break
        else:
            print("\nInvalid account number or PIN. Please try again.")
    
    # Main menu
    while True:
        print("\n=== Main Menu ===")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            print(f"\nYour current balance is: ${atm.check_balance():.2f}")
            
        elif choice == '2':
            try:
                amount = float(input("\nEnter amount to deposit: $"))
                if amount > 0:
                    if atm.deposit(amount):
                        print(f"\n${amount:.2f} has been deposited successfully!")
                        print(f"New balance: ${atm.check_balance():.2f}")
                    else:
                        print("\nInvalid amount!")
                else:
                    print("\nAmount must be greater than zero!")
            except ValueError:
                print("\nPlease enter a valid amount!")
                
        elif choice == '3':
            try:
                amount = float(input("\nEnter amount to withdraw: $"))
                if amount > 0:
                    if atm.withdraw(amount):
                        print(f"\n${amount:.2f} has been withdrawn successfully!")
                        print(f"Remaining balance: ${atm.check_balance():.2f}")
                    else:
                        print("\nInsufficient funds or invalid amount!")
                else:
                    print("\nAmount must be greater than zero!")
            except ValueError:
                print("\nPlease enter a valid amount!")
                
        elif choice == '4':
            print("\nThank you for using Python ATM. Have a nice day!")
            break
            
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()
