#!/usr/bin/env python3
"""
Student Record Manager - A simple CRUD system for managing student records
Supports both CSV and JSON file formats with full CRUD operations
"""

import csv
import json
import os
import sys
from typing import List, Dict, Optional, Union
from datetime import datetime


class StudentRecordManager:
    """Main class for managing student records with CSV and JSON support"""
    
    def __init__(self, data_file: str = "students.json", file_format: str = "json"):
        """
        Initialize the Student Record Manager
        
        Args:
            data_file: Name of the data file
            file_format: Format of the data file ('json' or 'csv')
        """
        self.data_file = data_file
        self.file_format = file_format.lower()
        self.students = []
        self.load_data()
    
    def load_data(self) -> None:
        """Load student data from file"""
        try:
            if os.path.exists(self.data_file):
                if self.file_format == "json":
                    with open(self.data_file, 'r', encoding='utf-8') as file:
                        self.students = json.load(file)
                elif self.file_format == "csv":
                    with open(self.data_file, 'r', newline='', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        self.students = list(reader)
                        # Convert age to int for CSV data
                        for student in self.students:
                            student['age'] = int(student['age'])
                print(f"✓ Loaded {len(self.students)} student records from {self.data_file}")
            else:
                print(f"ℹ No existing data file found. Starting with empty database.")
                self.students = []
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.students = []
    
    def save_data(self) -> None:
        """Save student data to file"""
        try:
            if self.file_format == "json":
                with open(self.data_file, 'w', encoding='utf-8') as file:
                    json.dump(self.students, file, indent=2, ensure_ascii=False)
            elif self.file_format == "csv":
                with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                    if self.students:
                        fieldnames = ['student_id', 'name', 'age', 'grade', 'email']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.students)
            print(f"✓ Data saved to {self.data_file}")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def add_student(self, student_id: str, name: str, age: int, grade: str, email: str) -> bool:
        """
        Add a new student record
        
        Args:
            student_id: Unique student identifier
            name: Student's full name
            age: Student's age
            grade: Student's grade/class
            email: Student's email address
            
        Returns:
            bool: True if successful, False if student ID already exists
        """
        # Check for duplicate student ID
        if any(student['student_id'] == student_id for student in self.students):
            print(f"❌ Error: Student ID '{student_id}' already exists!")
            return False
        
        # Validate email format
        if '@' not in email or '.' not in email.split('@')[1]:
            print("❌ Error: Invalid email format!")
            return False
        
        # Validate age
        if not isinstance(age, int) or age < 1 or age > 150:
            print("❌ Error: Age must be a positive integer between 1 and 150!")
            return False
        
        new_student = {
            'student_id': student_id,
            'name': name,
            'age': age,
            'grade': grade,
            'email': email
        }
        
        self.students.append(new_student)
        self.save_data()
        print(f"✓ Student '{name}' added successfully!")
        return True
    
    def view_all_students(self) -> None:
        """Display all student records"""
        if not self.students:
            print("📝 No student records found.")
            return
        
        print(f"\n📚 Student Records ({len(self.students)} total):")
        print("=" * 80)
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Grade':<10} {'Email':<25}")
        print("-" * 80)
        
        for student in self.students:
            print(f"{student['student_id']:<10} {student['name']:<20} {student['age']:<5} {student['grade']:<10} {student['email']:<25}")
        print("=" * 80)
    
    def search_student(self, search_term: str) -> List[Dict]:
        """
        Search for students by ID or name
        
        Args:
            search_term: Student ID or name to search for
            
        Returns:
            List of matching student records
        """
        matches = []
        search_term_lower = search_term.lower()
        
        for student in self.students:
            if (search_term_lower in student['student_id'].lower() or 
                search_term_lower in student['name'].lower()):
                matches.append(student)
        
        return matches
    
    def display_search_results(self, matches: List[Dict], search_term: str) -> None:
        """Display search results in a formatted table"""
        if not matches:
            print(f"🔍 No students found matching '{search_term}'")
            return
        
        print(f"\n🔍 Search Results for '{search_term}' ({len(matches)} found):")
        print("=" * 80)
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Grade':<10} {'Email':<25}")
        print("-" * 80)
        
        for student in matches:
            print(f"{student['student_id']:<10} {student['name']:<20} {student['age']:<5} {student['grade']:<10} {student['email']:<25}")
        print("=" * 80)
    
    def update_student(self, student_id: str) -> bool:
        """
        Update an existing student's details
        
        Args:
            student_id: ID of the student to update
            
        Returns:
            bool: True if successful, False if student not found
        """
        student = next((s for s in self.students if s['student_id'] == student_id), None)
        
        if not student:
            print(f"❌ Student with ID '{student_id}' not found!")
            return False
        
        print(f"\n📝 Updating student: {student['name']} (ID: {student_id})")
        print("Press Enter to keep current value, or type new value:")
        
        # Update name
        new_name = input(f"Name [{student['name']}]: ").strip()
        if new_name:
            student['name'] = new_name
        
        # Update age
        while True:
            age_input = input(f"Age [{student['age']}]: ").strip()
            if not age_input:
                break
            try:
                new_age = int(age_input)
                if 1 <= new_age <= 150:
                    student['age'] = new_age
                    break
                else:
                    print("❌ Age must be between 1 and 150!")
            except ValueError:
                print("❌ Please enter a valid number for age!")
        
        # Update grade
        new_grade = input(f"Grade [{student['grade']}]: ").strip()
        if new_grade:
            student['grade'] = new_grade
        
        # Update email
        while True:
            email_input = input(f"Email [{student['email']}]: ").strip()
            if not email_input:
                break
            if '@' in email_input and '.' in email_input.split('@')[1]:
                student['email'] = email_input
                break
            else:
                print("❌ Invalid email format!")
        
        self.save_data()
        print(f"✓ Student '{student['name']}' updated successfully!")
        return True
    
    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student record
        
        Args:
            student_id: ID of the student to delete
            
        Returns:
            bool: True if successful, False if student not found
        """
        student = next((s for s in self.students if s['student_id'] == student_id), None)
        
        if not student:
            print(f"❌ Student with ID '{student_id}' not found!")
            return False
        
        print(f"\n⚠️  Are you sure you want to delete student '{student['name']}' (ID: {student_id})?")
        confirm = input("Type 'yes' to confirm deletion: ").strip().lower()
        
        if confirm == 'yes':
            self.students = [s for s in self.students if s['student_id'] != student_id]
            self.save_data()
            print(f"✓ Student '{student['name']}' deleted successfully!")
            return True
        else:
            print("❌ Deletion cancelled.")
            return False
    
    def sort_students(self, sort_by: str) -> None:
        """
        Sort students by specified field
        
        Args:
            sort_by: Field to sort by ('name', 'age', or 'grade')
        """
        if not self.students:
            print("📝 No student records to sort.")
            return
        
        if sort_by == 'name':
            self.students.sort(key=lambda x: x['name'].lower())
            print("✓ Students sorted by name")
        elif sort_by == 'age':
            self.students.sort(key=lambda x: x['age'])
            print("✓ Students sorted by age")
        elif sort_by == 'grade':
            self.students.sort(key=lambda x: x['grade'])
            print("✓ Students sorted by grade")
        else:
            print("❌ Invalid sort field. Use 'name', 'age', or 'grade'")
            return
        
        self.save_data()
        self.view_all_students()
    
    def export_to_format(self, target_format: str, filename: str = None) -> bool:
        """
        Export data to different format
        
        Args:
            target_format: Target format ('csv' or 'json')
            filename: Optional custom filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not filename:
            base_name = self.data_file.rsplit('.', 1)[0]
            filename = f"{base_name}_export.{target_format}"
        
        try:
            if target_format == "json":
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(self.students, file, indent=2, ensure_ascii=False)
            elif target_format == "csv":
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    if self.students:
                        fieldnames = ['student_id', 'name', 'age', 'grade', 'email']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.students)
            else:
                print("❌ Invalid format. Use 'csv' or 'json'")
                return False
            
            print(f"✓ Data exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return False
    
    def import_from_file(self, filename: str) -> bool:
        """
        Import data from file
        
        Args:
            filename: Path to the file to import
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(filename):
            print(f"❌ File '{filename}' not found!")
            return False
        
        try:
            imported_students = []
            file_ext = filename.lower().split('.')[-1]
            
            if file_ext == 'json':
                with open(filename, 'r', encoding='utf-8') as file:
                    imported_students = json.load(file)
            elif file_ext == 'csv':
                with open(filename, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    imported_students = list(reader)
                    # Convert age to int for CSV data
                    for student in imported_students:
                        student['age'] = int(student['age'])
            else:
                print("❌ Unsupported file format. Use .json or .csv files")
                return False
            
            # Check for duplicate IDs
            existing_ids = {s['student_id'] for s in self.students}
            duplicates = [s for s in imported_students if s['student_id'] in existing_ids]
            
            if duplicates:
                print(f"⚠️  Found {len(duplicates)} duplicate student IDs. Skipping duplicates.")
                imported_students = [s for s in imported_students if s['student_id'] not in existing_ids]
            
            self.students.extend(imported_students)
            self.save_data()
            print(f"✓ Imported {len(imported_students)} student records from {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing data: {e}")
            return False


def display_menu() -> None:
    """Display the main menu"""
    print("\n" + "="*60)
    print("🎓 STUDENT RECORD MANAGER")
    print("="*60)
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Sort Students")
    print("7. Export Data")
    print("8. Import Data")
    print("9. Change File Format")
    print("0. Exit")
    print("="*60)


def get_user_choice() -> str:
    """Get user menu choice"""
    return input("\nEnter your choice (0-9): ").strip()


def get_student_input() -> tuple:
    """Get student information from user"""
    print("\n📝 Add New Student")
    print("-" * 30)
    
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("❌ Student ID cannot be empty!")
        return None
    
    name = input("Full Name: ").strip()
    if not name:
        print("❌ Name cannot be empty!")
        return None
    
    while True:
        try:
            age = int(input("Age: ").strip())
            if 1 <= age <= 150:
                break
            else:
                print("❌ Age must be between 1 and 150!")
        except ValueError:
            print("❌ Please enter a valid number for age!")
    
    grade = input("Grade/Class: ").strip()
    if not grade:
        print("❌ Grade cannot be empty!")
        return None
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email cannot be empty!")
        return None
    
    return student_id, name, age, grade, email


def main():
    """Main program function"""
    print("🎓 Welcome to Student Record Manager!")
    print("Choose your preferred file format:")
    print("1. JSON (recommended)")
    print("2. CSV")
    
    format_choice = input("Enter choice (1-2): ").strip()
    file_format = "json" if format_choice == "1" else "csv"
    data_file = f"students.{file_format}"
    
    manager = StudentRecordManager(data_file, file_format)
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == "0":
            print("\n👋 Thank you for using Student Record Manager!")
            break
        
        elif choice == "1":  # Add New Student
            student_data = get_student_input()
            if student_data:
                manager.add_student(*student_data)
        
        elif choice == "2":  # View All Students
            manager.view_all_students()
        
        elif choice == "3":  # Search Student
            search_term = input("\n🔍 Enter Student ID or Name to search: ").strip()
            if search_term:
                matches = manager.search_student(search_term)
                manager.display_search_results(matches, search_term)
            else:
                print("❌ Please enter a search term!")
        
        elif choice == "4":  # Update Student
            student_id = input("\n📝 Enter Student ID to update: ").strip()
            if student_id:
                manager.update_student(student_id)
            else:
                print("❌ Please enter a Student ID!")
        
        elif choice == "5":  # Delete Student
            student_id = input("\n🗑️  Enter Student ID to delete: ").strip()
            if student_id:
                manager.delete_student(student_id)
            else:
                print("❌ Please enter a Student ID!")
        
        elif choice == "6":  # Sort Students
            print("\n📊 Sort Students by:")
            print("1. Name")
            print("2. Age")
            print("3. Grade")
            sort_choice = input("Enter choice (1-3): ").strip()
            
            sort_fields = {"1": "name", "2": "age", "3": "grade"}
            if sort_choice in sort_fields:
                manager.sort_students(sort_fields[sort_choice])
            else:
                print("❌ Invalid choice!")
        
        elif choice == "7":  # Export Data
            print("\n📤 Export Data to:")
            print("1. JSON")
            print("2. CSV")
            export_choice = input("Enter choice (1-2): ").strip()
            
            if export_choice == "1":
                manager.export_to_format("json")
            elif export_choice == "2":
                manager.export_to_format("csv")
            else:
                print("❌ Invalid choice!")
        
        elif choice == "8":  # Import Data
            filename = input("\n📥 Enter filename to import: ").strip()
            if filename:
                manager.import_from_file(filename)
            else:
                print("❌ Please enter a filename!")
        
        elif choice == "9":  # Change File Format
            print("\n🔄 Change File Format:")
            print("1. JSON")
            print("2. CSV")
            format_choice = input("Enter choice (1-2): ").strip()
            
            new_format = "json" if format_choice == "1" else "csv"
            new_file = f"students.{new_format}"
            
            # Export current data to new format
            if manager.export_to_format(new_format, new_file):
                print(f"✓ Switched to {new_format.upper()} format. New file: {new_file}")
                manager = StudentRecordManager(new_file, new_format)
            else:
                print("❌ Failed to change file format!")
        
        else:
            print("❌ Invalid choice! Please enter a number between 0-9.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)
