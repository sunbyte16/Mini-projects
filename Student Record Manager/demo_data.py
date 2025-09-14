#!/usr/bin/env python3
"""
Demo Data Generator for Student Record Manager
Creates sample student data for testing the application
"""

import json
import csv
import random
from typing import List, Dict

# Sample data for generating realistic student records
FIRST_NAMES = [
    "John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Jessica",
    "Robert", "Ashley", "William", "Amanda", "Richard", "Jennifer", "Charles",
    "Lisa", "Joseph", "Nancy", "Thomas", "Karen", "Christopher", "Betty",
    "Daniel", "Helen", "Matthew", "Sandra", "Anthony", "Donna", "Mark", "Carol"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson"
]

GRADES = ["A", "B", "C", "D", "F", "A+", "B+", "C+", "D+", "A-", "B-", "C-", "D-"]
CLASSES = ["Grade 9", "Grade 10", "Grade 11", "Grade 12", "Freshman", "Sophomore", "Junior", "Senior"]

EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "student.edu", "university.edu"]


def generate_student_id(index: int) -> str:
    """Generate a unique student ID"""
    return f"S{index:03d}"


def generate_name() -> str:
    """Generate a random full name"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"


def generate_age() -> int:
    """Generate a random age between 16 and 25"""
    return random.randint(16, 25)


def generate_grade() -> str:
    """Generate a random grade"""
    return random.choice(GRADES)


def generate_class() -> str:
    """Generate a random class/grade level"""
    return random.choice(CLASSES)


def generate_email(name: str) -> str:
    """Generate an email based on the student's name"""
    first_name, last_name = name.lower().split()
    domain = random.choice(EMAIL_DOMAINS)
    # Create variations of email formats
    formats = [
        f"{first_name}.{last_name}@{domain}",
        f"{first_name}{last_name}@{domain}",
        f"{first_name[0]}.{last_name}@{domain}",
        f"{first_name}{last_name[0]}@{domain}"
    ]
    return random.choice(formats)


def generate_student_records(count: int = 10) -> List[Dict]:
    """Generate a list of student records"""
    students = []
    
    for i in range(1, count + 1):
        name = generate_name()
        student = {
            "student_id": generate_student_id(i),
            "name": name,
            "age": generate_age(),
            "grade": generate_grade(),
            "email": generate_email(name)
        }
        students.append(student)
    
    return students


def save_demo_data_json(filename: str = "demo_students.json", count: int = 10) -> None:
    """Save demo data as JSON file"""
    students = generate_student_records(count)
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(students, file, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {count} demo student records in {filename}")


def save_demo_data_csv(filename: str = "demo_students.csv", count: int = 10) -> None:
    """Save demo data as CSV file"""
    students = generate_student_records(count)
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        if students:
            fieldnames = ['student_id', 'name', 'age', 'grade', 'email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
    
    print(f"✓ Generated {count} demo student records in {filename}")


def main():
    """Main function to generate demo data"""
    print("🎓 Student Record Manager - Demo Data Generator")
    print("=" * 50)
    
    try:
        count = int(input("Enter number of students to generate (default 10): ") or "10")
        if count < 1 or count > 100:
            print("❌ Please enter a number between 1 and 100")
            return
        
        print(f"\nGenerating {count} demo student records...")
        
        # Generate both JSON and CSV files
        save_demo_data_json("demo_students.json", count)
        save_demo_data_csv("demo_students.csv", count)
        
        print(f"\n✅ Demo data generation complete!")
        print("You can now:")
        print("1. Run 'python student_manager.py' to start the application")
        print("2. Use 'Import Data' option to load demo_students.json or demo_students.csv")
        print("3. Or copy the data to students.json/students.csv to start with demo data")
        
    except ValueError:
        print("❌ Please enter a valid number")
    except Exception as e:
        print(f"❌ Error generating demo data: {e}")


if __name__ == "__main__":
    main()
