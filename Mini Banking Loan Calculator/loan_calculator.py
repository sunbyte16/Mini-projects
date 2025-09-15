import math
import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str
    annual_income: float
    credit_score: int
    existing_loans: List[dict] = None
    
    def __post_init__(self):
        if self.existing_loans is None:
            self.existing_loans = []
    
    def to_dict(self) -> dict:
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'annual_income': self.annual_income,
            'credit_score': self.credit_score,
            'existing_loans': self.existing_loans
        }
    
    def get_monthly_obligation(self) -> float:
        return sum(loan['monthly_payment'] 
                 for loan in self.existing_loans 
                 if loan['status'] == 'active')
    
    def is_eligible(self, requested_emi: float) -> Tuple[bool, str]:
        monthly_income = self.annual_income / 12
        dti_ratio = ((self.get_monthly_obligation() + requested_emi) / monthly_income) * 100
        
        if self.credit_score < 600:
            return False, "Credit score too low (min 600 required)"
        if dti_ratio > 40:
            return False, f"Debt-to-income ratio too high ({dti_ratio:.1f}% > 40%)"
        return True, "Eligible"

class LoanCalculator:
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.loan_products = {
            'personal': {'min': 1000, 'max': 50000, 'max_years': 5, 'rate': 10.5},
            'home': {'min': 50000, 'max': 2000000, 'max_years': 30, 'rate': 8.5},
            'car': {'min': 10000, 'max': 500000, 'max_years': 7, 'rate': 7.5},
            'education': {'min': 5000, 'max': 200000, 'max_years': 10, 'rate': 6.5}
        }
        self.load_data()
    
    def load_data(self):
        if os.path.exists('customers.json'):
            try:
                with open('customers.json', 'r') as f:
                    data = json.load(f)
                    self.customers = {k: Customer(**v) for k, v in data.items()}
            except (json.JSONDecodeError, FileNotFoundError):
                self.customers = {}
    
    def save_data(self):
        with open('customers.json', 'w') as f:
            json.dump({c.customer_id: c.to_dict() for c in self.customers.values()}, f, indent=2)
    
    def add_customer(self, name: str, email: str, phone: str, income: float, score: int) -> str:
        cid = f"C{len(self.customers)+1:04d}"
        self.customers[cid] = Customer(cid, name, email, phone, income, score)
        self.save_data()
        return cid
    
    def calculate_emi(self, principal: float, rate: float, years: int) -> float:
        if principal <= 0 or rate <= 0 or years <= 0:
            return 0.0
        monthly_rate = (rate / 100) / 12
        months = years * 12
        if monthly_rate == 0:
            return principal / months
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
        return round(emi, 2)
    
    def check_eligibility(self, cid: str, ltype: str, amount: float, years: int) -> dict:
        if ltype not in self.loan_products:
            return {'eligible': False, 'reason': 'Invalid loan type'}
        
        product = self.loan_products[ltype]
        if not (product['min'] <= amount <= product['max']):
            return {'eligible': False, 'reason': f'Amount must be ${product["min"]:,.2f}-${product["max"]:,.2f}'}
        
        if years < 1 or years > product['max_years']:
            return {'eligible': False, 'reason': f'Term must be 1-{product["max_years"]} years'}
        
        customer = self.customers.get(cid)
        if not customer:
            return {'eligible': False, 'reason': 'Customer not found'}
        
        rate = self._get_interest_rate(product['rate'], customer.credit_score)
        emi = self.calculate_emi(amount, rate, years)
        
        eligible, reason = customer.is_eligible(emi)
        if not eligible:
            return {'eligible': False, 'reason': reason}
        
        total_interest = (emi * years * 12) - amount
        return {
            'eligible': True,
            'loan_type': ltype,
            'amount': amount,
            'interest_rate': round(rate, 2),
            'term_years': years,
            'monthly_payment': emi,
            'total_interest': round(total_interest, 2),
            'total_payment': round(amount + total_interest, 2)
        }
    
    def _get_interest_rate(self, base_rate: float, credit_score: int) -> float:
        if credit_score >= 800:
            return base_rate - 2.0
        elif credit_score >= 700:
            return base_rate - 1.0
        elif credit_score >= 600:
            return base_rate
        return base_rate + 5.0

def display_menu():
    print("\n=== Loan Calculator ===")
    print("1. New Customer")
    print("2. Check Loan Eligibility")
    print("3. Calculate EMI")
    print("4. View Loan Products")
    print("5. Exit")

def main():
    calc = LoanCalculator()
    
    while True:
        display_menu()
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            print("\n=== New Customer ===")
            name = input("Full Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            income = float(input("Annual Income: $"))
            score = int(input("Credit Score (300-850): "))
            
            cid = calc.add_customer(name, email, phone, income, score)
            print(f"\n✅ Customer created! ID: {cid}")
        
        elif choice == '2':
            print("\n=== Check Loan Eligibility ===")
            cid = input("Customer ID: ").strip()
            print("\nLoan Types: personal, home, car, education")
            ltype = input("Loan Type: ").strip().lower()
            amount = float(input("Loan Amount: $"))
            years = int(input("Term (years): "))
            
            result = calc.check_eligibility(cid, ltype, amount, years)
            print("\n=== Result ===")
            if result['eligible']:
                print("✅ Approved!")
                print(f"Monthly Payment: ${result['monthly_payment']:,.2f}")
                print(f"Interest Rate: {result['interest_rate']}%")
                print(f"Total Interest: ${result['total_interest']:,.2f}")
                print(f"Total Payment: ${result['total_payment']:,.2f}")
            else:
                print(f"❌ Not Eligible: {result['reason']}")
        
        elif choice == '3':
            print("\n=== EMI Calculator ===")
            amount = float(input("Loan Amount: $"))
            rate = float(input("Interest Rate (%): "))
            years = int(input("Term (years): "))
            
            emi = calc.calculate_emi(amount, rate, years)
            total = emi * years * 12
            interest = total - amount
            
            print("\n=== Results ===")
            print(f"Monthly Payment: ${emi:,.2f}")
            print(f"Total Interest: ${interest:,.2f}")
            print(f"Total Payment: ${total:,.2f}")
        
        elif choice == '4':
            print("\n=== Loan Products ===")
            for name, details in calc.loan_products.items():
                print(f"\n{name.upper()} Loan")
                print(f"Amount: ${details['min']:,.2f} - ${details['max']:,.2f}")
                print(f"Term: Up to {details['max_years']} years")
                print(f"Base Rate: {details['rate']}%")
        
        elif choice == '5':
            print("\nThank you for using the Loan Calculator!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
