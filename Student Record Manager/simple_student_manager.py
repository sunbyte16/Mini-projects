#!/usr/bin/env python3
"""
Simple Student Record Manager - Interactive Input/Output Version
Takes user input and provides immediate output for each operation
"""

import json
import csv
import os
from typing import List, Dict


class SimpleStudentManager:
    """Simple student record manager with direct input/output"""
    
    def __init__(self):
        self.students = []
        self.load_data()
    
    def load_data(self):
        """Load existing data from JSON file"""
        try:
            if os.path.exists("students.json"):
                with open("students.json", 'r') as file:
                    self.students = json.load(file)
                print(f"✓ Loaded {len(self.students)} existing student records")
            else:
                print("ℹ Starting with empty database")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.students = []
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open("students.json", 'w') as file:
                json.dump(self.students, file, indent=2)
            print("✓ Data saved successfully")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def add_student(self):
        """Add a new student - takes input and shows output"""
        print("\n" + "="*50)
        print("📝 ADD NEW STUDENT")
        print("="*50)
        
        # Get input from user
        student_id = input("Enter Student ID: ").strip()
        if not student_id:
            print("❌ Student ID cannot be empty!")
            return
        
        # Check for duplicate
        if any(s['student_id'] == student_id for s in self.students):
            print(f"❌ Student ID '{student_id}' already exists!")
            return
        
        name = input("Enter Full Name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return
        
        try:
            age = int(input("Enter Age: ").strip())
            if age < 1 or age > 150:
                print("❌ Age must be between 1 and 150!")
                return
        except ValueError:
            print("❌ Please enter a valid number for age!")
            return
        
        grade = input("Enter Grade/Class: ").strip()
        if not grade:
            print("❌ Grade cannot be empty!")
            return
        
        email = input("Enter Email: ").strip()
        if not email or '@' not in email:
            print("❌ Invalid email format!")
            return
        
        # Add student
        new_student = {
            'student_id': student_id,
            'name': name,
            'age': age,
            'grade': grade,
            'email': email
        }
        
        self.students.append(new_student)
        self.save_data()
        
        # Show output
        print("\n✅ STUDENT ADDED SUCCESSFULLY!")
        print(f"Student ID: {student_id}")
        print(f"Name: {name}")
        print(f"Age: {age}")
        print(f"Grade: {grade}")
        print(f"Email: {email}")
        print(f"Total students in database: {len(self.students)}")
    
    def view_all_students(self):
        """View all students - shows formatted output"""
        print("\n" + "="*80)
        print("📚 ALL STUDENT RECORDS")
        print("="*80)
        
        if not self.students:
            print("📝 No student records found.")
            return
        
        print(f"Total Students: {len(self.students)}")
        print("-" * 80)
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Grade':<10} {'Email':<25}")
        print("-" * 80)
        
        for i, student in enumerate(self.students, 1):
            print(f"{student['student_id']:<10} {student['name']:<20} {student['age']:<5} {student['grade']:<10} {student['email']:<25}")
        
        print("="*80)
    
    def search_student(self):
        """Search for a student - takes input and shows output"""
        print("\n" + "="*50)
        print("🔍 SEARCH STUDENT")
        print("="*50)
        
        search_term = input("Enter Student ID or Name to search: ").strip()
        if not search_term:
            print("❌ Please enter a search term!")
            return
        
        # Search for matches
        matches = []
        search_lower = search_term.lower()
        
        for student in self.students:
            if (search_lower in student['student_id'].lower() or 
                search_lower in student['name'].lower()):
                matches.append(student)
        
        # Show output
        print(f"\n🔍 SEARCH RESULTS FOR '{search_term}':")
        print("="*60)
        
        if not matches:
            print("❌ No students found matching your search.")
            return
        
        print(f"Found {len(matches)} student(s):")
        print("-" * 60)
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Grade':<10} {'Email':<25}")
        print("-" * 60)
        
        for student in matches:
            print(f"{student['student_id']:<10} {student['name']:<20} {student['age']:<5} {student['grade']:<10} {student['email']:<25}")
        
        print("="*60)
    
    def update_student(self):
        """Update a student - takes input and shows output"""
        print("\n" + "="*50)
        print("✏️ UPDATE STUDENT")
        print("="*50)
        
        student_id = input("Enter Student ID to update: ").strip()
        if not student_id:
            print("❌ Please enter a Student ID!")
            return
        
        # Find student
        student = next((s for s in self.students if s['student_id'] == student_id), None)
        if not student:
            print(f"❌ Student with ID '{student_id}' not found!")
            return
        
        print(f"\n📝 Current details for {student['name']}:")
        print(f"Student ID: {student['student_id']}")
        print(f"Name: {student['name']}")
        print(f"Age: {student['age']}")
        print(f"Grade: {student['grade']}")
        print(f"Email: {student['email']}")
        
        print("\nEnter new values (press Enter to keep current value):")
        
        # Update name
        new_name = input(f"Name [{student['name']}]: ").strip()
        if new_name:
            student['name'] = new_name
        
        # Update age
        age_input = input(f"Age [{student['age']}]: ").strip()
        if age_input:
            try:
                new_age = int(age_input)
                if 1 <= new_age <= 150:
                    student['age'] = new_age
                else:
                    print("❌ Age must be between 1 and 150!")
            except ValueError:
                print("❌ Invalid age format!")
        
        # Update grade
        new_grade = input(f"Grade [{student['grade']}]: ").strip()
        if new_grade:
            student['grade'] = new_grade
        
        # Update email
        new_email = input(f"Email [{student['email']}]: ").strip()
        if new_email:
            if '@' in new_email:
                student['email'] = new_email
            else:
                print("❌ Invalid email format!")
        
        self.save_data()
        
        # Show output
        print("\n✅ STUDENT UPDATED SUCCESSFULLY!")
        print(f"Updated details for {student['name']}:")
        print(f"Student ID: {student['student_id']}")
        print(f"Name: {student['name']}")
        print(f"Age: {student['age']}")
        print(f"Grade: {student['grade']}")
        print(f"Email: {student['email']}")
    
    def delete_student(self):
        """Delete a student - takes input and shows output"""
        print("\n" + "="*50)
        print("🗑️ DELETE STUDENT")
        print("="*50)
        
        student_id = input("Enter Student ID to delete: ").strip()
        if not student_id:
            print("❌ Please enter a Student ID!")
            return
        
        # Find student
        student = next((s for s in self.students if s['student_id'] == student_id), None)
        if not student:
            print(f"❌ Student with ID '{student_id}' not found!")
            return
        
        print(f"\n⚠️ STUDENT TO DELETE:")
        print(f"Student ID: {student['student_id']}")
        print(f"Name: {student['name']}")
        print(f"Age: {student['age']}")
        print(f"Grade: {student['grade']}")
        print(f"Email: {student['email']}")
        
        confirm = input("\nAre you sure you want to delete this student? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            self.students = [s for s in self.students if s['student_id'] != student_id]
            self.save_data()
            print(f"\n✅ STUDENT '{student['name']}' DELETED SUCCESSFULLY!")
            print(f"Remaining students in database: {len(self.students)}")
        else:
            print("❌ Deletion cancelled.")
    
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🎓 STUDENT RECORD MANAGER")
        print("="*60)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("0. Exit")
        print("="*60)
    
    def run(self):
        """Main program loop"""
        print("🎓 Welcome to Student Record Manager!")
        print("This program takes your input and provides immediate output.")
        
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (0-5): ").strip()
            
            if choice == "0":
                print("\n👋 Thank you for using Student Record Manager!")
                break
            elif choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_all_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            else:
                print("❌ Invalid choice! Please enter a number between 0-5.")
            
            input("\nPress Enter to continue...")


def main():
    """Main function"""
    try:
        manager = SimpleStudentManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
