import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

@dataclass
class Employee:
    emp_id: str
    name: str
    position: str
    base_salary: float
    join_date: str
    department: str
    bank_account: str
    tax_id: str
    allowances: Dict[str, float] = None
    deductions: Dict[str, float] = None
    
    def __post_init__(self):
        if self.allowances is None:
            self.allowances = {}
        if self.deductions is None:
            self.deductions = {}
    
    def add_allowance(self, name: str, amount: float):
        self.allowances[name] = amount
    
    def add_deduction(self, name: str, amount: float):
        self.deductions[name] = amount
    
    def calculate_gross_salary(self) -> float:
        return self.base_salary + sum(self.allowances.values())
    
    def calculate_total_deductions(self) -> float:
        return sum(self.deductions.values())
    
    def calculate_net_salary(self) -> float:
        return self.calculate_gross_salary() - self.calculate_total_deductions()
    
    def to_dict(self) -> dict:
        return {
            'emp_id': self.emp_id,
            'name': self.name,
            'position': self.position,
            'base_salary': self.base_salary,
            'join_date': self.join_date,
            'department': self.department,
            'bank_account': self.bank_account,
            'tax_id': self.tax_id,
            'allowances': self.allowances,
            'deductions': self.deductions
        }

class PayrollSystem:
    def __init__(self):
        self.employees: Dict[str, Employee] = {}
        self.payroll_records: Dict[str, List[dict]] = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists('employees.json'):
            try:
                with open('employees.json', 'r') as f:
                    data = json.load(f)
                    for emp_id, emp_data in data.items():
                        self.employees[emp_id] = Employee(**emp_data)
            except (json.JSONDecodeError, FileNotFoundError):
                self.employees = {}
        
        if os.path.exists('payroll_records.json'):
            try:
                with open('payroll_records.json', 'r') as f:
                    self.payroll_records = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.payroll_records = {}
    
    def save_data(self):
        with open('employees.json', 'w') as f:
            json.dump({e.emp_id: e.to_dict() for e in self.employees.values()}, f, indent=4)
        
        with open('payroll_records.json', 'w') as f:
            json.dump(self.payroll_records, f, indent=4)
    
    def add_employee(self, **kwargs) -> str:
        emp_id = f"EMP{len(self.employees) + 1:04d}"
        employee = Employee(emp_id=emp_id, **kwargs)
        self.employees[emp_id] = employee
        self.payroll_records[emp_id] = []
        self.save_data()
        return emp_id
    
    def get_employee(self, emp_id: str) -> Optional[Employee]:
        return self.employees.get(emp_id)
    
    def process_payroll(self, emp_id: str, month: int, year: int) -> dict:
        if emp_id not in self.employees:
            return None
        
        employee = self.employees[emp_id]
        
        # Check if payroll already processed for this month
        payroll_id = f"{year:04d}{month:02d}"
        for record in self.payroll_records.get(emp_id, []):
            if record['payroll_id'].startswith(payroll_id):
                return None  # Already processed
        
        # Create payroll record
        payroll = {
            'payroll_id': f"{payroll_id}{len(self.payroll_records[emp_id]) + 1:03d}",
            'month': month,
            'year': year,
            'base_salary': employee.base_salary,
            'allowances': employee.allowances.copy(),
            'deductions': employee.deductions.copy(),
            'gross_salary': employee.calculate_gross_salary(),
            'total_deductions': employee.calculate_total_deductions(),
            'net_salary': employee.calculate_net_salary(),
            'payment_date': datetime.now().strftime("%Y-%m-%d"),
            'status': 'processed'
        }
        
        self.payroll_records[emp_id].append(payroll)
        self.save_data()
        return payroll
    
    def get_payroll_history(self, emp_id: str) -> List[dict]:
        return self.payroll_records.get(emp_id, [])

def display_menu():
    print("\n=== Employee Payroll System ===")
    print("1. Add New Employee")
    print("2. View Employee Details")
    print("3. Add Allowance")
    print("4. Add Deduction")
    print("5. Process Payroll")
    print("6. View Payroll History")
    print("7. List All Employees")
    print("8. Exit")

def get_float_input(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_int_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

def add_employee_ui(payroll_system: PayrollSystem):
    print("\n=== Add New Employee ===")
    name = input("Full Name: ").strip()
    position = input("Position: ").strip()
    base_salary = get_float_input("Base Salary: ")
    department = input("Department: ").strip()
    bank_account = input("Bank Account Number: ").strip()
    tax_id = input("Tax ID: ").strip()
    
    emp_id = payroll_system.add_employee(
        name=name,
        position=position,
        base_salary=base_salary,
        join_date=datetime.now().strftime("%Y-%m-%d"),
        department=department,
        bank_account=bank_account,
        tax_id=tax_id
    )
    
    print(f"\n✅ Employee added successfully! Employee ID: {emp_id}")

def view_employee_ui(payroll_system: PayrollSystem):
    emp_id = input("\nEnter Employee ID: ").strip().upper()
    employee = payroll_system.get_employee(emp_id)
    
    if not employee:
        print("Employee not found!")
        return
    
    print("\n=== Employee Details ===")
    print(f"ID:           {employee.emp_id}")
    print(f"Name:         {employee.name}")
    print(f"Position:     {employee.position}")
    print(f"Department:   {employee.department}")
    print(f"Join Date:    {employee.join_date}")
    print(f"Base Salary:  ${employee.base_salary:,.2f}")
    
    print("\n=== Allowances ===")
    if employee.allowances:
        for name, amount in employee.allowances.items():
            print(f"- {name}: ${amount:,.2f}")
    else:
        print("No allowances added.")
    
    print("\n=== Deductions ===")
    if employee.deductions:
        for name, amount in employee.deductions.items():
            print(f"- {name}: ${amount:,.2f}")
    else:
        print("No deductions added.")
    
    print("\n=== Salary Summary ===")
    print(f"Gross Salary:    ${employee.calculate_gross_salary():,.2f}")
    print(f"Total Deductions: ${employee.calculate_total_deductions():,.2f}")
    print(f"Net Salary:      ${employee.calculate_net_salary():,.2f}")

def add_allowance_ui(payroll_system: PayrollSystem):
    emp_id = input("\nEnter Employee ID: ").strip().upper()
    employee = payroll_system.get_employee(emp_id)
    
    if not employee:
        print("Employee not found!")
        return
    
    print(f"\nCurrent Allowances for {employee.name}:")
    for name, amount in employee.allowances.items():
        print(f"- {name}: ${amount:,.2f}")
    
    name = input("\nAllowance Name: ").strip()
    amount = get_float_input("Amount: $")
    
    employee.add_allowance(name, amount)
    payroll_system.save_data()
    print("\n✅ Allowance added successfully!")

def add_deduction_ui(payroll_system: PayrollSystem):
    emp_id = input("\nEnter Employee ID: ").strip().upper()
    employee = payroll_system.get_employee(emp_id)
    
    if not employee:
        print("Employee not found!")
        return
    
    print(f"\nCurrent Deductions for {employee.name}:")
    for name, amount in employee.deductions.items():
        print(f"- {name}: ${amount:,.2f}")
    
    name = input("\nDeduction Name: ").strip()
    amount = get_float_input("Amount: $")
    
    employee.add_deduction(name, amount)
    payroll_system.save_data()
    print("\n✅ Deduction added successfully!")

def process_payroll_ui(payroll_system: PayrollSystem):
    emp_id = input("\nEnter Employee ID: ").strip().upper()
    employee = payroll_system.get_employee(emp_id)
    
    if not employee:
        print("Employee not found!")
        return
    
    print("\n=== Process Payroll ===")
    print(f"Employee: {employee.name}")
    print(f"Position: {employee.position}")
    
    month = get_int_input("Enter month (1-12): ")
    if month < 1 or month > 12:
        print("Invalid month!")
        return
    
    year = get_int_input("Enter year (e.g., 2023): ")
    
    payroll = payroll_system.process_payroll(emp_id, month, year)
    
    if not payroll:
        print("\n❌ Payroll already processed for this month or employee not found!")
        return
    
    print("\n✅ Payroll Processed Successfully!")
    print("\n=== Payslip ===")
    print(f"Employee:    {employee.name}")
    print(f"Employee ID: {employee.emp_id}")
    print(f"Period:      {month:02d}/{year}")
    print(f"Pay Date:    {payroll['payment_date']}")
    print(f"Payroll ID:  {payroll['payroll_id']}")
    
    print("\n--- Earnings ---")
    print(f"Base Salary: ${payroll['base_salary']:,.2f}")
    
    if payroll['allowances']:
        print("\nAllowances:")
        for name, amount in payroll['allowances'].items():
            print(f"- {name}: ${amount:,.2f}")
    
    print("\n--- Deductions ---")
    if payroll['deductions']:
        for name, amount in payroll['deductions'].items():
            print(f"- {name}: ${amount:,.2f}")
    else:
        print("No deductions")
    
    print("\n--- Summary ---")
    print(f"Gross Salary:    ${payroll['gross_salary']:,.2f}")
    print(f"Total Deductions: ${payroll['total_deductions']:,.2f}")
    print(f"Net Salary:      ${payroll['net_salary']:,.2f}")
    print("\nThank you for using our payroll system!")

def view_payroll_history_ui(payroll_system: PayrollSystem):
    emp_id = input("\nEnter Employee ID: ").strip().upper()
    employee = payroll_system.get_employee(emp_id)
    
    if not employee:
        print("Employee not found!")
        return
    
    history = payroll_system.get_payroll_history(emp_id)
    
    if not history:
        print(f"\nNo payroll records found for {employee.name}")
        return
    
    print(f"\n=== Payroll History for {employee.name} ===")
    print("-" * 80)
    print("{:<12} {:<10} {:<15} {:<15} {:<15} {:<10}".format(
        "Payroll ID", "Period", "Base Salary", "Allowances", "Deductions", "Net Pay"))
    print("-" * 80)
    
    for record in sorted(history, key=lambda x: (x['year'], x['month']), reverse=True):
        period = f"{record['month']:02d}/{record['year']}"
        print("{:<12} {:<10} ${:<14,.2f} ${:<14,.2f} ${:<14,.2f} ${:<10,.2f}".format(
            record['payroll_id'],
            period,
            record['base_salary'],
            sum(record['allowances'].values()),
            sum(record['deductions'].values()),
            record['net_salary']
        ))

def list_employees_ui(payroll_system: PayrollSystem):
    if not payroll_system.employees:
        print("\nNo employees found!")
        return
    
    print("\n=== Employee List ===")
    print("-" * 100)
    print("{:<10} {:<25} {:<20} {:<15} {:<15} {:<15}".format(
        "ID", "Name", "Position", "Department", "Join Date", "Status"))
    print("-" * 100)
    
    for emp_id, employee in payroll_system.employees.items():
        print("{:<10} {:<25} {:<20} {:<15} {:<15} {:<15}".format(
            emp_id,
            employee.name[:24],
            employee.position[:19],
            employee.department[:14],
            employee.join_date,
            "Active"
        ))

def main():
    payroll_system = PayrollSystem()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            add_employee_ui(payroll_system)
        elif choice == '2':
            view_employee_ui(payroll_system)
        elif choice == '3':
            add_allowance_ui(payroll_system)
        elif choice == '4':
            add_deduction_ui(payroll_system)
        elif choice == '5':
            process_payroll_ui(payroll_system)
        elif choice == '6':
            view_payroll_history_ui(payroll_system)
        elif choice == '7':
            list_employees_ui(payroll_system)
        elif choice == '8':
            print("\nThank you for using the Employee Payroll System!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
